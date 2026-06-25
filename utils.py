# chatbot-umbandung/utils.py

import logging
import re
import sys

# Impor dari file database UMBandung
from database_ID import (
    KNOWLEDGE_BASE_ID,
    ALIAS_KEYWORD_ID,  # alias prodi/fakultas/topik -> kunci KB
    FOLLOW_UP_SUGGESTIONS_ID,
    PETA_LOKASI as PETA_LOKASI_ID
)


# --- Logging ---
# Render HANYA menampilkan log dari stdout/stderr. File di disk (RotatingFileHandler)
# tidak muncul di tab Logs DAN terhapus tiap restart/deploy (disk Render ephemeral).
# Karena itu semua log diarahkan ke stdout, dengan prefix berlabel agar mudah difilter
# lewat kotak "Search logs" di Render (mis. ketik: [ACTIVITY], [FEEDBACK], [REACTION]).
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Logger khusus aktivitas (memakai root handler di atas -> ikut tampil di Render).
activity_logger = logging.getLogger('activity_logger')


def log_activity(ip, query, source, user_type, response):
    clean_response = ' '.join(str(response).splitlines())
    activity_logger.info(
        f'[ACTIVITY] IP: {ip} | Query: "{query}" | Source: {source} | '
        f'UserType: {user_type} | Response: "{clean_response}"'
    )


# Kunci sapaan: hanya dicocokkan secara PERSIS (exact), tidak boleh ikut pada
# pencarian per-kata agar tidak salah-picu di tengah kalimat
# (mis. "apa kabar pmb" tidak boleh balas sapaan).
SAPAAN_KEYS = {
    "assalamualaikum", "salam", "hello", "hi", "halo", "hai",
    "selamat pagi", "selamat siang", "selamat sore", "selamat malam",
    "apa kabar", "siapa kamu", "kamu siapa", "bisa bantu apa",
    "terima kasih", "makasih", "sama sama", "oke", "sampai jumpa",
}


def _normalize_query(query):
    """Samakan penyebutan nama kampus menjadi 'umbandung' agar pencarian konsisten."""
    q = query.lower().strip()
    q = re.sub(r'\buniversitas muhammadiyah bandung\b', 'umbandung', q)
    q = re.sub(r'\bum bandung\b', 'umbandung', q)
    q = re.sub(r'\bumb\b', 'umbandung', q)
    return q


def _contains_all_words(text, keyword):
    """True jika SEMUA kata pada keyword muncul (utuh) di text."""
    return all(re.search(r'\b' + re.escape(w) + r'\b', text) for w in keyword.split())

# Kata kunci "topik profil prodi". Bila salah satunya muncul BERSAMA nama prodi
# (mis. "visi misi teknik elektro"), jawaban yang tepat adalah entri profil prodi,
# bukan entri umum tingkat universitas (mis. "visi misi").
PROFIL_TOPIC_KEYS = {
    "visi", "misi", "tujuan", "kurikulum", "profil", "tentang",
    "kompetensi", "prospek", "konsentrasi", "strategi",
}


def _find_prodi_key(text):
    """
    Kembalikan kunci KB profil prodi ("program studi <prodi>") bila ada nama/alias
    prodi pada text. Sumbernya ALIAS_KEYWORD_ID (nilai berawalan "program studi "),
    dengan pencocokan kata utuh; alias terpanjang (paling spesifik) menang.
    Entri ringkasan "program studi umbandung" dikecualikan (bukan prodi spesifik).
    """
    best_key = None
    longest = 0
    for alias, kb_key in ALIAS_KEYWORD_ID.items():
        if not kb_key.startswith("program studi "):
            continue
        if kb_key == "program studi umbandung":
            continue
        if re.search(r'\b' + re.escape(alias) + r'\b', text) and len(alias) > longest:
            longest = len(alias)
            best_key = kb_key
    return best_key


# Alias generik yang sering MUNCUL KEBETULAN di tengah kalimat (mis. kata
# "prodi" pada "cara mengajukan cuti ke prodi"). Pada langkah (4) alias ini
# hanya dipakai bila menjadi FOKUS query, bukan sekadar nyempil.
# Tambah/kurangi sesuai kebutuhan.
WEAK_ALIASES = {
    "prodi", "jurusan", "program studi", "fakultas",
    "jalur", "tujuan", "sambutan", "lab", "biaya",
}

# Kata pengisi/penanya yang diabaikan saat menilai 'fokus' sebuah query.
_ALIAS_STOPWORDS = {
    "apa", "saja", "yang", "tersedia", "ada", "adakah", "apakah", "berapa", "jumlah",
    "daftar", "list", "info", "informasi", "tentang", "mengenai", "soal",
    "di", "ke", "dari", "pada", "untuk", "dengan", "dan", "atau",
    "mau", "ingin", "pengen", "pengin", "lihat", "melihat", "tahu", "tau", "cek",
    "itu", "ini", "nya", "sih", "dong", "ya", "kak", "min", "admin", "tolong", "mohon",
    "bagaimana", "gimana", "cara", "caranya", "kalau", "jika",
    "umbandung", "umb", "kampus", "universitas", "muhammadiyah", "bandung",
}


def _alias_is_focused(text, alias):
    """
    True jika, setelah membuang kata alias dan kata pengisi, nyaris tidak ada
    kata 'isi' lain yang tersisa (toleransi 1 kata). Membatasi alias generik
    agar tidak salah-picu pada kalimat berintent lain.
    """
    alias_words = set(alias.split())
    leftover = [w for w in text.split()
                if w not in alias_words and w not in _ALIAS_STOPWORDS]
    return len(leftover) <= 1


# --- Knowledge Base Function ---
def search_knowledge_base(query):
    """
    Mencari knowledge base lokal (Bahasa Indonesia) untuk konteks UMBandung.
    Urutan pencarian (dari paling spesifik ke paling longgar):
      (1) Peta / lokasi kampus.
      (2) Cocok PERSIS dengan kunci KB (termasuk sapaan).
      (2.5) Topik profil (visi/misi/tujuan/dll) + nama prodi -> entri profil prodi.
      (3) Cocok semua-kata pada kunci, kunci PALING SPESIFIK (kata terbanyak) didahulukan.
      (4) Cadangan: alias prodi/fakultas/topik (alias terpanjang menang).
    """
    nq = _normalize_query(query)

    # (1) Peta / lokasi kampus UMBandung
    if "peta" in nq or "lokasi" in nq:
        for key, map_link in PETA_LOKASI_ID.items():
            if key in nq:
                return {
                    "type": "paragraph",
                    "content": (
                        "Berikut lokasi kampus <strong>Universitas Muhammadiyah Bandung</strong>:<br>"
                        "Jl. Soekarno-Hatta No. 752, Cipadung Kidul, Panyileukan, Kota Bandung 40614.<br>"
                        f"<a href='{map_link}' target='_blank' style='color:blue;'>Buka di Google Maps</a>"
                    )
                }
        if "kampus" in nq or "umbandung" in nq:
            return KNOWLEDGE_BASE_ID.get("alamat kampus umbandung")

    # (2) Cocok PERSIS (paling diutamakan; juga menangani sapaan)
    if nq in KNOWLEDGE_BASE_ID:
        return KNOWLEDGE_BASE_ID[nq]

    # (2.5) Topik profil + nama prodi -> arahkan ke PROFIL prodi.
    #       Mis. "visi misi teknik elektro" harus mengembalikan profil Teknik Elektro,
    #       bukan entri umum "visi misi". Query yang mengandung "dosen" dikecualikan
    #       agar "dosen <prodi>" tetap mengembalikan daftar dosen.
    if "dosen" not in nq.split():
        if any(re.search(r'\b' + re.escape(w) + r'\b', nq) for w in PROFIL_TOPIC_KEYS):
            prodi_key = _find_prodi_key(nq)
            if prodi_key:
                entry = KNOWLEDGE_BASE_ID.get(prodi_key)
                if entry:
                    return entry

    # (3) Cocok semua-kata, kunci paling spesifik (kata terbanyak) lebih dulu.
    #     Kunci sapaan dilewati agar tidak salah-picu di tengah kalimat.
    for keyword in sorted(KNOWLEDGE_BASE_ID, key=lambda k: len(k.split()), reverse=True):
        if keyword in SAPAAN_KEYS or len(keyword.split()) < 2:
            continue
        if _contains_all_words(nq, keyword):
            return KNOWLEDGE_BASE_ID[keyword]

    # (4) Cadangan: alias prodi/fakultas/topik (alias terpanjang menang).
    #     Alias generik (WEAK_ALIASES) hanya dipakai bila menjadi FOKUS query,
    #     agar kata umum (mis. "prodi" pada "cara mengajukan cuti ke prodi")
    #     tidak salah-picu entri yang tidak relevan.
    matched_key = None
    longest_alias = 0
    for alias, kb_key in ALIAS_KEYWORD_ID.items():
        if not re.search(r'\b' + re.escape(alias) + r'\b', nq):
            continue
        if alias in WEAK_ALIASES and not _alias_is_focused(nq, alias):
            continue
        if len(alias) > longest_alias:
            longest_alias = len(alias)
            matched_key = kb_key
    if matched_key:
        return KNOWLEDGE_BASE_ID.get(matched_key)

    return None


def _entry_to_text(entry):
    """Ubah satu entri knowledge base (paragraph/list) menjadi teks polos."""
    if not isinstance(entry, dict):
        return str(entry)
    parts = []
    if entry.get("title"):
        parts.append(str(entry["title"]))
    if entry.get("content"):
        parts.append(str(entry["content"]))
    for it in entry.get("items", []):
        parts.append("- " + str(it))
    teks = " ".join(parts)
    # Buang tag HTML, pertahankan tautan sebagai "teks (url)".
    teks = re.sub(r"<a\s[^>]*href=['\"]?([^'\" >]+)[^>]*>(.*?)</a>", r"\2 (\1)", teks,
                  flags=re.IGNORECASE | re.DOTALL)
    teks = re.sub(r"<[^>]+>", " ", teks)
    teks = re.sub(r"&ndash;", "-", teks)
    teks = re.sub(r"&amp;", "&", teks)
    teks = re.sub(r"\s+", " ", teks)
    return teks.strip()


# Kata yang tidak ikut diperhitungkan saat mencari entri KB yang relevan.
_CONTEXT_STOPWORDS = {
    "yang", "dan", "di", "ke", "dari", "untuk", "pada", "apa", "apakah",
    "bagaimana", "berapa", "kapan", "dimana", "di mana", "siapa", "saya",
    "tentang", "mengenai", "info", "informasi", "umbandung", "umb", "adalah",
    "itu", "ini", "ada", "bisa", "boleh", "tolong", "mohon", "saja",
    # Kata umum kampus yang nyaris muncul di mana-mana -> jangan jadi penentu.
    "program", "studi", "prodi", "jurusan", "kuliah", "kampus", "universitas",
    "fakultas", "mahasiswa",
}


def gather_kb_context(query, max_entries=6):
    """
    Mengumpulkan entri knowledge base yang PALING RELEVAN dengan query (berbasis
    irisan kata), lalu mengembalikannya sebagai satu blok teks ringkas untuk
    disuntikkan sebagai konteks ke Gemini. Tujuannya: Gemini "membaca database
    dulu" dan dapat memanfaatkan informasi terkait meski tidak ada kecocokan persis.

    Mengembalikan string kosong bila tidak ada entri yang cukup relevan.
    """
    nq = _normalize_query(query)
    q_words = {w for w in re.findall(r"[a-z0-9]+", nq) if w not in _CONTEXT_STOPWORDS and len(w) > 2}
    if not q_words:
        return ""

    skor = []
    for key, entry in KNOWLEDGE_BASE_ID.items():
        if key in SAPAAN_KEYS:
            continue
        # Gabungkan kata pada kunci entri + isi entri sebagai bahan pencocokan.
        bahan = (key + " " + _entry_to_text(entry)).lower()
        bahan_words = set(re.findall(r"[a-z0-9]+", bahan))
        overlap = q_words & bahan_words
        if not overlap:
            continue
        # Bobot: irisan kata + bonus bila kata query muncul di KUNCI entri.
        skor_kunci = sum(1 for w in q_words if w in key)
        skor.append((len(overlap) + 2 * skor_kunci, key, entry))

    if not skor:
        return ""

    skor.sort(key=lambda x: x[0], reverse=True)
    blok = []
    for _, key, entry in skor[:max_entries]:
        teks = _entry_to_text(entry)
        if teks:
            blok.append(f"[{key}]\n{teks}")
    return "\n\n".join(blok)


def get_follow_ups(query):
    """
    Mencari saran pertanyaan lanjutan berdasarkan topik yang terdeteksi pada query.
    Mengembalikan kecocokan kata kunci terpanjang (paling spesifik).
    """
    normalized_query = query.lower().strip()
    best_match = None
    longest_match = 0

    for keyword, data in FOLLOW_UP_SUGGESTIONS_ID.items():
        if keyword in normalized_query:
            if len(keyword) > longest_match:
                longest_match = len(keyword)
                best_match = data

    return best_match


# --- Parse Response Function ---
def parse_bot_response(text: str) -> dict:
    """
    Membersihkan respons dari AI, mendeteksi poin-poin dan penomoran,
    lalu memformatnya sebagai HTML.
    """
    if not text.strip():
        return {"type": "paragraph", "content": "Maaf, saya tidak dapat memberikan jawaban saat ini."}

    match = re.search(r'```html(.*)```', text, re.DOTALL | re.IGNORECASE)
    if match:
        text = match.group(1).strip()

    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

    lines = text.split('\n')
    html_output = []
    in_ul_list = False
    in_ol_list = False

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith(('* ', '- ')):
            if in_ol_list:
                html_output.append('</ol>')
                in_ol_list = False
            if not in_ul_list:
                html_output.append('<ul>')
                in_ul_list = True
            list_item = stripped_line[2:]
            html_output.append(f'<li>{list_item}</li>')
        elif re.match(r'^\d+\.\s', stripped_line):
            if in_ul_list:
                html_output.append('</ul>')
                in_ul_list = False
            if not in_ol_list:
                html_output.append('<ol>')
                in_ol_list = True
            list_item = re.sub(r'^\d+\.\s', '', stripped_line)
            html_output.append(f'<li>{list_item}</li>')
        else:
            if in_ul_list:
                html_output.append('</ul>')
                in_ul_list = False
            if in_ol_list:
                html_output.append('</ol>')
                in_ol_list = False
            if stripped_line:
                 html_output.append(f'<p>{line}</p>')

    if in_ul_list:
        html_output.append('</ul>')
    if in_ol_list:
        html_output.append('</ol>')

    final_html = ''.join(html_output)
    return {"type": "paragraph", "content": final_html}