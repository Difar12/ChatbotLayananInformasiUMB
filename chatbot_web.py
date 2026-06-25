# chatbot_web.py
import logging
import re
import time
import secrets
from flask import Flask, request, jsonify, session, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import google.generativeai as genai
from google.api_core import exceptions as google_api_exceptions
from datetime import timedelta

# Impor dari file-file yang sudah dipisah
import config
from utils import log_activity, search_knowledge_base, get_follow_ups, parse_bot_response, gather_kb_context
from database_ID import AUTOCOMPLETE_TERMS_ID


def _strip_html(text):
    """Ubah jawaban ber-HTML menjadi teks bersih agar konteks ke Gemini mudah dibaca.
    Tautan <a href='url'>teks</a> dipertahankan sebagai 'teks (url)'."""
    text = str(text)
    text = re.sub(r"<a\s[^>]*href=['\"]?([^'\" >]+)[^>]*>(.*?)</a>", r"\2 (\1)", text,
                  flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)          # buang sisa tag HTML
    text = re.sub(r"\s+", " ", text)              # rapikan spasi berlebih
    return text.strip()


# --- Konfigurasi Google Gemini ---
if config.GOOGLE_API_KEY:
    genai.configure(api_key=config.GOOGLE_API_KEY)


def _build_gemini_model(with_search: bool):
    """Bangun GenerativeModel. Bila with_search=True, coba aktifkan Google Search
    grounding. Spesifikasi tool berbeda antar versi SDK/model, jadi dicoba beberapa
    bentuk; bila semua gagal, kembalikan model tanpa tool (degradasi mulus)."""
    base_kwargs = dict(
        model_name=config.GEMINI_MODEL,
        system_instruction=config.SYSTEM_PROMPT_ID,
    )
    if not with_search:
        return genai.GenerativeModel(**base_kwargs)

    # Urutan percobaan: tool 'google_search' (Gemini 2.x) lalu 'google_search_retrieval' (1.5).
    for tool_spec in ({"google_search": {}}, "google_search_retrieval"):
        try:
            return genai.GenerativeModel(**base_kwargs, tools=tool_spec)
        except Exception as e:  # noqa: BLE001 - bentuk tool tidak didukung versi ini
            logging.warning(f"[WEB SEARCH] Spesifikasi tool {tool_spec!r} gagal: {e}")
            continue
    logging.warning("[WEB SEARCH] Tidak ada spesifikasi tool yang didukung; lanjut tanpa pencarian web.")
    return genai.GenerativeModel(**base_kwargs)


# --- Flask App & Routes ---
app = Flask(__name__)
CORS(app)
app.secret_key = config.FLASK_SECRET_KEY
app.permanent_session_lifetime = timedelta(minutes=5)

limiter = Limiter(
    key_func=get_remote_address,                 # kunci default = alamat IP (lapisan backstop)
    app=app,
    default_limits=config.RATE_LIMIT_DEFAULTS,   # batas global kasar per-IP
    storage_uri=config.RATELIMIT_STORAGE_URI,    # "memory://" default; gunakan redis:// untuk multi-worker
    strategy="fixed-window",
)


# --- Anti-Abuse Helpers ---
def get_session_id():
    """
    Identifier stabil per-browser, dipakai sebagai kunci rate-limit PER-SESI.
    Penting untuk lingkungan kampus: banyak mahasiswa berbagi satu IP publik (NAT),
    sehingga membatasi per-IP saja akan menjegal pengguna sah. Kunci per-sesi
    memberi tiap browser kuotanya sendiri, sementara per-IP tetap jadi backstop.
    """
    sid = session.get("sid")
    if not sid:
        sid = secrets.token_hex(16)
        session["sid"] = sid
        session.modified = True
    return sid


def validate_message(message):
    """
    Validasi pesan masuk SEBELUM menyentuh Gemini (hemat token).
    Mengembalikan (error_dict, status_code) bila tidak valid, atau (None, None) bila valid.
    """
    if not isinstance(message, str) or not message.strip():
        return ({
            "status": "error",
            "response": {"type": "paragraph", "content": "Error: Pertanyaan tidak boleh kosong."}
        }, 400)

    if len(message) > config.MAX_MESSAGE_LENGTH:
        return ({
            "status": "error",
            "code": "too_long",
            "max_length": config.MAX_MESSAGE_LENGTH,
            "response": {
                "type": "paragraph",
                "content": (
                    f"Pesan terlalu panjang. Maksimal <strong>{config.MAX_MESSAGE_LENGTH} karakter</strong>, "
                    f"sedangkan pesan Anda {len(message)} karakter. Mohon persingkat pertanyaan Anda."
                )
            }
        }, 400)

    return (None, None)


def cooldown_remaining():
    """
    Sisa detik cooldown untuk sesi ini (0 = boleh kirim).
    Disimpan di session (cookie), divalidasi di server, sehingga tetap berlaku
    walau halaman di-refresh/reload atau localStorage klien dihapus.
    Memakai time.time() (epoch) agar konsisten lintas proses & restart server.
    """
    last = session.get("last_message_ts")
    if isinstance(last, (int, float)):
        elapsed = time.time() - last
        if 0 <= elapsed < config.COOLDOWN_SECONDS:
            return max(1, int(round(config.COOLDOWN_SECONDS - elapsed)))
    return 0


def stamp_cooldown():
    """Tandai waktu pesan diterima; jendela cooldown berikutnya dimulai dari sini."""
    session["last_message_ts"] = time.time()
    session.modified = True


@app.errorhandler(429)
def ratelimit_handler(e):
    """Kembalikan 429 dari flask-limiter sebagai JSON ramah-klien (bukan HTML default)."""
    return jsonify({
        "status": "error",
        "code": "rate_limited",
        "response": {
            "type": "paragraph",
            "content": "⚠️ Terlalu banyak permintaan dalam waktu singkat. Mohon tunggu sebentar, lalu coba lagi."
        }
    }), 429


def extract_retry_seconds(error):
    """
    Ambil estimasi waktu tunggu (detik) dari error kuota Gemini, bila tersedia.
    Mencoba atribut terstruktur lebih dulu, lalu fallback mem-parsing teks error
    ("Please retry in 25.47s"). Mengembalikan None bila tidak ditemukan.
    """
    delay = getattr(error, "retry_delay", None)
    seconds = getattr(delay, "seconds", None) if delay is not None else None
    if seconds:
        return int(seconds)
    match = re.search(r'retry in (\d+(?:\.\d+)?)s', str(error), re.IGNORECASE)
    if match:
        return int(float(match.group(1))) + 1  # bulatkan ke atas agar aman
    return None


def build_quota_notice(retry_seconds=None):
    """
    Pesan ramah-pengguna saat kuota Gemini habis (HTTP 429 dari Google).
    Diksinya sengaja sederhana: alih-alih istilah teknis "knowledge base lokal",
    pengguna diarahkan untuk menanyakan topik umum yang jawabannya sudah tersedia
    langsung di sistem (sehingga tidak perlu memanggil AI sama sekali).
    """
    wait_line = ""
    if retry_seconds:
        wait_line = f"Anda dapat mencobanya lagi dalam kurang lebih <strong>{retry_seconds} detik</strong>. "

    content = (
        "Mohon maaf 🙏, layanan <strong>asisten AI</strong> sedang menerima sangat banyak "
        "permintaan saat ini, sehingga untuk sementara belum dapat menjawab pertanyaan "
        "yang membutuhkan bantuan AI.<br><br>"
        f"{wait_line}Sambil menunggu, Anda tetap bisa langsung memperoleh jawaban untuk "
        "<strong>pertanyaan umum</strong> yang informasinya sudah tersedia di sistem kami, contohnya:"
        "<ul>"
        "<li>Cara dan syarat <strong>pendaftaran mahasiswa baru (PMB)</strong></li>"
        "<li>Informasi <strong>biaya kuliah / UKT</strong></li>"
        "<li><strong>Beasiswa</strong> yang tersedia</li>"
        "<li>Daftar <strong>program studi &amp; fakultas</strong></li>"
        "<li><strong>Kontak dan lokasi</strong> kampus</li>"
        "</ul>"
        "Silakan ketik salah satu topik di atas, atau coba lagi beberapa saat lagi. 🙏"
    )
    return {"type": "paragraph", "content": content}

def format_history_for_prompt(history):
    if not history:
        return ""
    formatted_text = ""
    for message in history:
        role = "User" if message["role"] == "user" else "Virtual Assistant"
        content = message["content"]
        
        if isinstance(content, str) and content.startswith("{"):
            try:
                import ast
                content_dict = ast.literal_eval(content)
                content = content_dict.get('content', '') or content_dict.get('title', '')
            except (ValueError, SyntaxError):
                 pass
        
        clean_content = re.sub('<[^<]+?>', '', str(content))
        formatted_text += f"{role}: {clean_content}\n"
    return formatted_text

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route("/")
def index():
    if "history" not in session:
        session["history"] = []
    return render_template(
        "index.html",
        max_message_length=config.MAX_MESSAGE_LENGTH,
        cooldown_seconds=config.COOLDOWN_SECONDS,
    )


@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    q = request.args.get("q", "").lower().strip()
    if not q:
        return jsonify([])
    suggestions = [term for term in AUTOCOMPLETE_TERMS_ID if q in term.lower()]
    return jsonify(suggestions[:7])  # Batasi 7 hasil


@app.route("/set_user_type", methods=["POST"])
def set_user_type():
    data = request.json
    user_type = data.get("user_type", "").strip()
    if user_type in ["Mahasiswa", "Non-Mahasiswa"]:
        session["user_type"] = user_type
        session.modified = True
        return jsonify({"status": "success", "user_type": user_type})
    return jsonify({"status": "error", "message": "Tipe pengguna tidak valid"}), 400


@app.route("/chat", methods=["POST"])
@limiter.limit(config.RATE_LIMIT_PER_IP)                                   # backstop kasar per-IP (longgar, aman NAT)
@limiter.limit(config.RATE_LIMIT_PER_SESSION, key_func=get_session_id)     # batas utama per-sesi (per-browser)
def chat():
    user_ip = get_remote_address()
    try:
        data = request.json or {}
        raw_message = data.get("message", "")
        user_message = raw_message.strip() if isinstance(raw_message, str) else ""

        # --- 1) Validasi pesan: tolak kosong / >MAX_MESSAGE_LENGTH SEBELUM ke Gemini (hemat token) ---
        error_payload, error_code = validate_message(user_message)
        if error_payload:
            return jsonify(error_payload), error_code

        # --- 2) Perintah kontrol "/reset": bersihkan riwayat di SERVER tanpa memanggil Gemini. ---
        # (Sebelumnya "/reset" diteruskan & diproses sebagai pertanyaan biasa -> boros token
        #  dan riwayat server tidak benar-benar terhapus. Frontend kini memanggil endpoint /reset,
        #  tetapi pengaman ini tetap ada bila "/reset" sampai ke sini.)
        if user_message.lower() == "/reset":
            session.pop("history", None)
            session.modified = True
            return jsonify({
                "status": "success",
                "source": "system",
                "response": {"type": "paragraph", "content": "Riwayat percakapan telah dihapus."},
                "follow_ups": None
            })

        # --- 3) Cooldown anti-spam (server-side, tahan refresh). ---
        remaining = cooldown_remaining()
        if remaining > 0:
            resp = jsonify({
                "status": "error",
                "code": "cooldown",
                "retry_after": remaining,
                "response": {
                    "type": "paragraph",
                    "content": f"Mohon tunggu <strong>{remaining} detik</strong> sebelum mengirim pesan berikutnya."
                }
            })
            resp.headers["Retry-After"] = str(remaining)
            return resp, 429
        # Lolos validasi & cooldown -> mulai jendela cooldown berikutnya dari sekarang.
        stamp_cooldown()

        if "history" not in session:
            session["history"] = []

        is_more_details_request = user_message.lower() in ['bisa lebih detail?', 'jelaskan lebih detail']
        
        original_query = user_message
        previous_answer = None
        if is_more_details_request:
            if len(session.get("history", [])) >= 2:
                # Ambil pertanyaan asli (user terakhir) DAN jawaban resmi terakhir (bot terakhir).
                for i in range(len(session["history"]) - 1, -1, -1):
                    role = session["history"][i]["role"]
                    if role == "bot" and previous_answer is None:
                        previous_answer = session["history"][i]["content"]
                    if role == "user":
                        original_query = session["history"][i]["content"]
                        break
            else:
                return jsonify({
                    "status": "success",
                    "source": "local",
                    "response": {"type": "paragraph", "content": "Silakan ajukan pertanyaan terlebih dahulu sebelum meminta detail lebih lanjut."},
                    "follow_ups": None
                })
        else:
            session["history"].append({"role": "user", "content": user_message})
            session.modified = True
            
        json_response = {"status": "success", "source": "local", "response": {}, "follow_ups": None}
        
        user_type = session.get('user_type', 'Tidak Diketahui')
        
        local_answer = None
        if not is_more_details_request:
            local_answer = search_knowledge_base(original_query)
            if local_answer:
                logging.info(f"[LOCAL DB] Query: \"{original_query}\" → Jawaban ditemukan di knowledge base lokal.")
            else:
                logging.info(f"[API] Query: \"{original_query}\" → Tidak ditemukan di lokal, diteruskan ke Gemini API.")
        
        if local_answer:
            json_response["response"] = local_answer
            log_activity(user_ip, original_query, "local", user_type, str(local_answer))
            session["history"].append({"role": "bot", "content": str(local_answer)})
            session.modified = True
        else:
            if not config.GOOGLE_API_KEY:
                logging.error("[API] GOOGLE_API_KEY tidak ditemukan di .env / environment variable!")
                return jsonify({
                    "status": "error",
                    "response": {"type": "paragraph", "content": "⚠️ API key tidak dikonfigurasi. Hubungi administrator."}
                }), 503
            
            json_response["source"] = "api"
            use_search = bool(getattr(config, "ENABLE_WEB_SEARCH", False))
            model = _build_gemini_model(with_search=use_search)

            # Untuk permintaan "lebih detail": buang pasangan (user, bot) terakhir dari history
            # karena jawaban resmi itu kita suntikkan ulang secara eksplisit pada prompt di bawah.
            trim = 2 if is_more_details_request else 1
            hist = session.get("history", [])
            hist = hist[:-trim] if len(hist) >= trim else []

            # Bangun history Gemini; gabungkan giliran beruntun yang berperan sama agar
            # tidak melanggar aturan "alternating roles" milik Gemini.
            gemini_history = []
            for msg in hist:
                role = "model" if msg["role"] == "bot" else "user"
                text = str(msg["content"])
                if gemini_history and gemini_history[-1]["role"] == role:
                    gemini_history[-1]["parts"][0]["text"] += "\n" + text
                else:
                    gemini_history.append({"role": role, "parts": [{"text": text}]})

            # Tentukan pesan yang dikirim ke Gemini.
            if is_more_details_request and previous_answer:
                # Sematkan jawaban resmi (knowledge base) sebagai SUMBER KEBENARAN agar Gemini
                # hanya memperluas penjelasan TANPA menambah/mengubah fakta (nama, jumlah, daftar).
                fakta_resmi = _strip_html(previous_answer)
                message_to_send = (
                    "Pengguna meminta penjelasan LEBIH DETAIL atas jawaban resmi di bawah ini.\n\n"
                    f"PERTANYAAN ASLI PENGGUNA:\n{original_query}\n\n"
                    f"JAWABAN RESMI DARI KNOWLEDGE BASE UMBANDUNG (sumber kebenaran):\n{fakta_resmi}\n\n"
                    "INSTRUKSI WAJIB:\n"
                    "1. Jelaskan ulang dan perluas jawaban resmi di atas agar lebih mudah dipahami.\n"
                    "2. Ikuti SEMUA fakta pada jawaban resmi PERSIS apa adanya — nama, jumlah, daftar "
                    "item, angka, dan tautan TIDAK BOLEH ditambah, dikurangi, atau diubah.\n"
                    "3. DILARANG menambahkan program studi, fakultas, layanan, atau data lain yang tidak "
                    "tercantum pada jawaban resmi tersebut.\n"
                    "4. Bila ada hal yang tidak tercantum pada jawaban resmi, arahkan pengguna untuk "
                    "mengonfirmasi ke unit terkait UMBandung — jangan mengarang.\n"
                    "5. Jawab dalam Bahasa Indonesia yang ringkas dan rapi."
                )
            else:
                # Suntikkan konteks database yang relevan agar Gemini "membaca database
                # dulu" dan dapat memakai informasi terkait meski tak ada kecocokan persis.
                kb_context = gather_kb_context(original_query)
                if kb_context:
                    message_to_send = (
                        "KONTEKS DARI DATABASE UMBANDUNG (sumber kebenaran utama, "
                        "gunakan dan simpulkan dari sini lebih dulu):\n"
                        f"{kb_context}\n\n"
                        "Bila konteks di atas belum menjawab sepenuhnya, lengkapi dengan "
                        "pencarian web (utamakan sumber resmi umbandung.ac.id / BAN-PT) "
                        "atau pengetahuan umum, sesuai panduan.\n\n"
                        f"PERTANYAAN PENGGUNA:\n{original_query}"
                    )
                else:
                    message_to_send = original_query

            chat_session = model.start_chat(history=gemini_history)
            try:
                response = chat_session.send_message(message_to_send)
            except google_api_exceptions.InvalidArgument as e:
                # Beberapa model/versi menolak tool pencarian saat generate.
                # Ulangi sekali tanpa pencarian web agar pengguna tetap dapat jawaban.
                if use_search:
                    logging.warning(f"[WEB SEARCH] Ditolak saat generate ({e}); ulang tanpa pencarian web.")
                    model = _build_gemini_model(with_search=False)
                    chat_session = model.start_chat(history=gemini_history)
                    response = chat_session.send_message(message_to_send)
                else:
                    raise
            
            bot_message = response.text.strip()
            session["history"].append({"role": "bot", "content": bot_message})
            session.modified = True

            json_response["response"] = parse_bot_response(bot_message)
            log_activity(user_ip, original_query, "api", user_type, bot_message)
        
        # Sematkan footer tanpa memutasi objek dict bersama di knowledge base
        if isinstance(json_response["response"], dict):
            json_response["response"] = {
                **json_response["response"],
                "footer": {"text": "umbandung.ac.id", "link": "https://umbandung.ac.id"},
            }
        
        follow_ups = get_follow_ups(original_query)
        if follow_ups:
            json_response["follow_ups"] = follow_ups
        
        return jsonify(json_response)

    except google_api_exceptions.ResourceExhausted as e:
        # Kuota/limit Gemini habis (429 dari Google) — BUKAN error sistem kita.
        retry_seconds = extract_retry_seconds(e)
        logging.warning(
            f"[QUOTA] Kuota Gemini habis untuk IP {user_ip}. Estimasi retry≈{retry_seconds}s."
        )
        # Lepas giliran 'user' yang menggantung agar percakapan tetap rapi saat dicoba ulang.
        history = session.get("history")
        if history and history[-1].get("role") == "user":
            history.pop()
            session.modified = True
        # Status 200 + source "system" => tampil sebagai gelembung chat biasa,
        # tanpa toolbar feedback maupun disclaimer AI (lihat penyesuaian di index.html).
        return jsonify({
            "status": "success",
            "source": "system",
            "response": build_quota_notice(retry_seconds),
            "follow_ups": None
        })

    except Exception as e:
        logging.error(f"[ERROR] API/Config error untuk IP {user_ip}: {e}", exc_info=True)
        return jsonify({"status": "error", "response": {"type": "paragraph", "content": "⚠️ Maaf, terjadi gangguan pada sistem. Silakan coba lagi nanti."}}), 503

@app.route("/reset", methods=["POST"])
def reset():
    session.pop("history", None)
    return jsonify({"status": "success", "message": "Riwayat percakapan dihapus."})

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    feedback_text = data.get("feedback", "").strip()
    bot_message = data.get("message", "").strip()
    if feedback_text:
        # Ditulis ke stdout lewat logging agar TAMPIL di Render dan bisa difilter
        # dengan kata kunci [FEEDBACK] pada kotak "Search logs".
        log_line = f"[FEEDBACK] IP: {get_remote_address()} | Feedback: {feedback_text}"
        if bot_message:
            log_line += f' | Message: "{bot_message}"'
        logging.getLogger("feedback").info(log_line)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Masukan tidak boleh kosong."}), 400

@app.route("/log_reaction", methods=["POST"])
def log_reaction():
    data = request.json
    reaction = data.get("reaction")
    message = data.get("message", "")
    if reaction and message:
        # Difilter di Render dengan kata kunci [REACTION].
        logging.getLogger("reaction").info(
            f'[REACTION] IP: {get_remote_address()} | Reaction: {reaction} | Message: "{message}"'
        )
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Data reaksi tidak valid."}), 400

@app.route("/formalize_text", methods=["POST"])
@limiter.limit(config.RATE_LIMIT_PER_IP)
@limiter.limit(config.RATE_LIMIT_PER_SESSION, key_func=get_session_id)
def formalize_text():
    user_ip = get_remote_address()
    try:
        history = session.get("history", [])
        if len(history) < 2:
            return jsonify({"result": "Tidak ada percakapan yang cukup untuk diformalisasikan."})

        data = request.json or {}
        target_type = data.get("target_type", "umum").strip().lower()

        # Penyesuaian gaya bahasa berdasarkan target
        target_descriptions = {
            "dosen": "kepada dosen atau tenaga pengajar di lingkungan Universitas Muhammadiyah Bandung. Gunakan gaya bahasa akademik yang sopan, hormat, dan formal sesuai etika komunikasi mahasiswa kepada pendidik.",
            "kampus": "kepada pihak institusi/administrasi kampus Universitas Muhammadiyah Bandung (misalnya: Biro Akademik, Kemahasiswaan, atau unit kerja kampus). Gunakan gaya bahasa administratif yang resmi, tertib, dan lugas.",
            "umum": "untuk keperluan umum (misalnya: rekan sejawat, mitra, atau pihak luar kampus). Gunakan gaya bahasa yang formal namun tetap komunikatif dan mudah dipahami."
        }
        target_desc = target_descriptions.get(target_type, target_descriptions["umum"])

        conversation_text = format_history_for_prompt(history)

        prompt = f"""
Anda adalah asisten layanan informasi Universitas Muhammadiyah Bandung yang ahli dalam menyusun komunikasi tertulis formal.

Berdasarkan riwayat percakapan berikut antara pengguna dan asisten virtual UMBandung, susunlah sebuah teks formal yang sesuai konteks. Teks ini ditujukan {target_desc}

Panduan penyusunan:
- Identifikasi inti permasalahan atau informasi yang dibahas dalam percakapan.
- Tentukan format yang paling tepat secara kontekstual: bisa berupa pesan singkat formal, surat singkat, atau permohonan tertulis — TIDAK harus selalu berbentuk email.
- Sesuaikan gaya bahasa dengan konteks akademik, administratif, atau umum sesuai isi percakapan.
- Gunakan bahasa yang jelas, sopan, dan ringkas.
- Akhiri dengan placeholder "[Nama Anda]" atau "[Nama & NIM Anda]" bila relevan.
- Jika topik percakapan tidak relevan untuk diformalisasikan (misalnya hanya berupa sapaan atau pertanyaan trivial), nyatakan dengan sopan bahwa percakapan ini tidak perlu diformalisasikan, dan berikan saran singkat apa yang sebaiknya disampaikan secara formal.

Percakapan:
{conversation_text}

Teks Formal:
"""

        model = genai.GenerativeModel(model_name=config.GEMINI_MODEL)
        response = model.generate_content(prompt)

        result = response.text.strip()
        user_type = session.get('user_type', 'Tidak Diketahui')
        log_activity(user_ip, f"formalize_text_request:{target_type}", "api", user_type, result)

        return jsonify({"result": result})

    except google_api_exceptions.ResourceExhausted as e:
        retry_seconds = extract_retry_seconds(e)
        wait = f" Silakan coba lagi dalam ±{retry_seconds} detik." if retry_seconds else ""
        logging.warning(f"[QUOTA] Kuota Gemini habis (formalize) untuk IP {user_ip}.")
        return jsonify({"result": (
            "Mohon maaf, fitur penyusunan teks formal sedang sibuk karena layanan AI "
            "menerima banyak permintaan saat ini." + wait +
            " Sambil menunggu, Anda dapat menyalin isi percakapan secara manual terlebih dahulu."
        )})

    except Exception as e:
        logging.error(f"Formalize text error for IP {user_ip}: {e}")
        return jsonify({"error": "Gagal memformalisasi teks."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)