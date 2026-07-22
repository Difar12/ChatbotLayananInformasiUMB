# detail_mode.py
"""
Modul khusus untuk fitur "Lebih Detail" pada Chatbot UMBandung.

Dipisah dari chatbot_web.py dengan alasan:
- Prompt bisa di-tuning tanpa menyentuh routing Flask.
- Logika deteksi & ekstraksi konteks dapat diuji unit-test secara terpisah.
- Menghindari chatbot_web.py membengkak (sudah 563 baris).

Perubahan perilaku dibanding implementasi lama:
- Jawaban sebelumnya diposisikan sebagai KONTEKS BACAAN, bukan bahan tulis ulang.
- Model wajib mendeteksi "celah informasi" antara pertanyaan asli dan jawaban lama.
- Konteks tambahan dari database ikut disuntikkan (gather_kb_context).
- Ada guard pasca-generate yang mendeteksi jawaban hasil tulis ulang.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Konstanta tuning
# ---------------------------------------------------------------------------

# Batas karakter jawaban sebelumnya yang disuntikkan ke prompt.
# Jawaban KB UMBandung bisa sangat panjang (profil prodi ~2000 karakter);
# memotongnya menghemat token tanpa kehilangan konteks inti.
MAX_PREV_ANSWER_CHARS = 3000
MAX_KB_CONTEXT_CHARS = 4000

# Ambang kemiripan (rasio kata unik yang beririsan). Di atas nilai ini,
# jawaban dianggap sekadar parafrase jawaban lama -> perlu regenerasi.
REWRITE_SIMILARITY_THRESHOLD = 0.62

# Kata yang diabaikan saat menghitung kemiripan (stopword Bahasa Indonesia ringkas).
_STOPWORDS = frozenset("""
yang dan di ke dari untuk dengan pada adalah ini itu atau juga dalam sebagai
akan tidak bisa dapat oleh serta agar bagi para telah sudah karena namun
""".split())


# ---------------------------------------------------------------------------
# 1) Deteksi permintaan "lebih detail"
# ---------------------------------------------------------------------------

# Menangkap variasi natural + fokus opsional.
# Contoh yang cocok:
#   "bisa lebih detail?"          -> focus = None
#   "lebih detail"                -> focus = None
#   "jelaskan lebih rinci"        -> focus = None
#   "lebih detail tentang biaya"  -> focus = "biaya"
#   "detail soal jalur reguler"   -> focus = "jalur reguler"
_DETAIL_TRIGGER = re.compile(
    r"^(?:bisa|boleh|tolong|coba)?\s*"
    r"(?:jelaskan|jabarkan|uraikan|beri(?:kan)?|kasih|minta)?\s*"
    r"(?:info(?:rmasi)?\s+)?"
    r"(?:yang\s+|secara\s+)?"
    r"(?:lebih\s+)?(?:detail|rinci|terperinci|lengkap|spesifik|mendalam)"
    r"(?:\s*(?:lagi|dong|ya|nya))?"
    r"(?:\s*(?:tentang|mengenai|soal|terkait|perihal|untuk|bagian|di\s*bagian)\s+(?P<focus>.+?))?"
    r"[\s.?!]*$",
    re.IGNORECASE,
)


def normalize_message(message: str) -> str:
    """Rapikan pesan untuk keperluan pencocokan pola (bukan untuk ditampilkan)."""
    text = str(message or "").strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def parse_detail_request(message: str) -> Tuple[bool, Optional[str]]:
    """
    Deteksi apakah pesan merupakan permintaan pendalaman jawaban.

    Returns:
        (is_detail_request, focus)
        focus = topik spesifik yang ingin didalami pengguna, atau None.

    Catatan: pengecekan panjang mencegah kalimat panjang yang kebetulan
    mengandung kata "detail" (mis. "saya butuh detail biaya kuliah lengkap
    beserta cicilannya untuk semester depan") ikut tertangkap sebagai trigger.
    """
    text = normalize_message(message)
    if not text or len(text) > 80:
        return (False, None)

    match = _DETAIL_TRIGGER.match(text)
    if not match:
        return (False, None)

    focus = (match.group("focus") or "").strip(" .?!,") or None
    return (True, focus)


# ---------------------------------------------------------------------------
# 2) Ekstraksi konteks dari riwayat percakapan
# ---------------------------------------------------------------------------

def extract_last_exchange(history: List[Dict]) -> Tuple[Optional[str], Optional[str]]:
    """
    Ambil (pertanyaan_asli, jawaban_terakhir) dari riwayat.

    Berbeda dari implementasi lama, fungsi ini:
    - Melewati giliran bot beruntun (yang muncul setelah permintaan detail
      sebelumnya) sehingga pertanyaan asli pengguna tidak ikut hilang.
    - Mengembalikan (None, None) bila belum ada pasangan yang valid, sehingga
      pemanggil bisa menampilkan pesan ramah alih-alih memanggil Gemini.
    """
    if not history:
        return (None, None)

    # Langkah 1: mundur sampai menemukan jawaban bot terakhir.
    # Giliran 'user' yang menggantung di ekor riwayat (mis. permintaan yang gagal
    # karena kuota) dilewati, bukan dijadikan jawaban.
    idx = len(history) - 1
    while idx >= 0 and history[idx].get("role") != "bot":
        idx -= 1
    if idx < 0:
        return (None, None)

    last_answer = str(history[idx].get("content") or "").strip()
    if not last_answer:
        return (None, None)

    # Langkah 2: mundur lagi mencari pertanyaan substantif pengguna.
    # Giliran user yang isinya sekadar pemicu ("bisa lebih detail?") DILEWATI,
    # supaya penekanan tombol berulang tetap merujuk ke pertanyaan asli.
    for j in range(idx - 1, -1, -1):
        entry = history[j]
        if entry.get("role") != "user":
            continue
        content = str(entry.get("content") or "").strip()
        if not content:
            continue
        if parse_detail_request(content)[0]:
            continue
        return (content, last_answer)

    return (None, last_answer)


def _truncate(text: str, limit: int) -> str:
    """Potong teks di batas kata terdekat agar prompt tidak membengkak."""
    text = str(text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return f"{cut} …[dipotong]"


# ---------------------------------------------------------------------------
# 3) Prompt builder
# ---------------------------------------------------------------------------

def build_detail_prompt(
    original_query: str,
    previous_answer: str,
    kb_context: Optional[str] = None,
    focus: Optional[str] = None,
    strict_retry: bool = False,
) -> str:
    """
    Susun prompt mode pendalaman.

    Prinsip desain (berbeda total dari prompt lama):
    - KONTEKS-1 (jawaban lama) diberi label "SUDAH DIBACA PENGGUNA" dan secara
      eksplisit dilarang ditulis ulang. Model hanya boleh menganalisisnya.
    - Model diminta mendeteksi CELAH INFORMASI lebih dulu, lalu menjawab celah
      itu saja. Ini yang membuat jawaban jadi to the point.
    - KONTEKS-2 (database) menjadi satu-satunya sumber fakta baru.
    - Ada instruksi eksplisit untuk kasus "tidak ada data": jawab singkat,
      JANGAN menambal kekosongan dengan pengulangan.

    Args:
        strict_retry: aktifkan bila percobaan pertama terdeteksi sebagai
                      tulis ulang; menambah penegasan larangan.
    """
    prev = _truncate(previous_answer, MAX_PREV_ANSWER_CHARS)
    kb = _truncate(kb_context, MAX_KB_CONTEXT_CHARS) if kb_context else ""

    focus_line = (
        f"{focus}"
        if focus
        else "(tidak disebut spesifik — dalami bagian yang paling relevan dengan PERTANYAAN ASLI)"
    )
    kb_block = kb if kb else "(tidak ada data tambahan yang relevan di database)"

    retry_block = ""
    if strict_retry:
        retry_block = (
            "\nPERINGATAN: Percobaan sebelumnya GAGAL karena hanya mengulang KONTEKS-1. "
            "Kali ini tulis HANYA informasi yang belum ada di KONTEKS-1. "
            "Bila memang tidak ada informasi baru, cukup jawab 2–3 kalimat sesuai aturan "
            "'BILA DATA TIDAK TERSEDIA'. Jangan menambah panjang jawaban dengan pengulangan.\n"
        )

    return f"""MODE: PENDALAMAN JAWABAN (BUKAN PENULISAN ULANG)

PERTANYAAN ASLI PENGGUNA:
{original_query}

BAGIAN YANG INGIN DIDALAMI:
{focus_line}

===== KONTEKS-1 — JAWABAN YANG SUDAH DIBACA PENGGUNA =====
{prev}
===== AKHIR KONTEKS-1 =====

===== KONTEKS-2 — DATA DARI DATABASE UMBANDUNG (sumber kebenaran fakta baru) =====
{kb_block}
===== AKHIR KONTEKS-2 =====

CARA KERJA ANDA (lakukan langkah 1–2 di dalam kepala, JANGAN ditulis):
1. Analisis KONTEKS-1. Pengguna SUDAH membacanya — isinya bukan bahan jawaban Anda.
2. Tentukan CELAH INFORMASI: bagian mana dari PERTANYAAN ASLI (atau BAGIAN YANG INGIN
   DIDALAMI) yang belum terjawab, masih dangkal, atau belum operasional di KONTEKS-1.
3. Tulis jawaban yang HANYA mengisi celah tersebut.

ATURAN OUTPUT — WAJIB DIPATUHI:
- DILARANG menulis ulang, meringkas ulang, atau memparafrase isi KONTEKS-1. Termasuk
  dilarang mengulang visi, misi, daftar mata kuliah, jumlah SKS, prospek lulusan, dan
  tautan yang sudah tercantum di sana.
- Boleh menyebut ulang satu frasa pendek dari KONTEKS-1 HANYA sebagai penanda ("Terkait
  144 SKS tersebut, …") lalu langsung lanjut ke informasi baru.
- Kalimat pertama harus langsung berisi substansi jawaban. DILARANG memakai pembuka
  seperti "Tentu, berikut penjelasan lebih detail…", "Berdasarkan informasi yang
  tersedia…", atau menuliskan judul profil.
- Fakta baru HANYA boleh diambil dari KONTEKS-2. DILARANG mengarang nama, angka,
  tanggal, biaya, syarat, jalur pendaftaran, atau tautan yang tidak ada di KONTEKS-1
  maupun KONTEKS-2.
- Panjang maksimal ±200 kata. Gunakan poin bernomor/bullet bila isinya berupa
  langkah, syarat, atau daftar.
- BILA DATA TIDAK TERSEDIA: jawab dalam 2–3 kalimat bahwa informasi spesifik tersebut
  belum tersedia di basis data UMBandung, sebutkan unit yang tepat untuk dihubungi
  (mis. Panitia PMB / Biro Akademik), dan berhenti. JANGAN menambal kekosongan dengan
  mengulang KONTEKS-1.
- Bahasa Indonesia, lugas, tanpa basa-basi penutup.
{retry_block}
JAWABAN PENDALAMAN:"""


# ---------------------------------------------------------------------------
# 4) Guard pasca-generate
# ---------------------------------------------------------------------------

def _significant_words(text: str) -> set:
    """Ambil himpunan kata bermakna (>3 huruf, bukan stopword) untuk uji kemiripan."""
    words = re.findall(r"[a-zA-Zà-üÀ-Ü]{4,}", str(text or "").lower())
    return {w for w in words if w not in _STOPWORDS}


def looks_like_rewrite(new_answer: str, previous_answer: str) -> bool:
    """
    Deteksi heuristik: apakah jawaban baru sekadar menulis ulang jawaban lama?

    Metode: rasio kata bermakna pada jawaban BARU yang juga muncul di jawaban LAMA.
    Rasio tinggi = hampir semua kosakata berasal dari jawaban lama = parafrase.

    Dipakai sebagai guard opsional; bila True, panggil ulang Gemini dengan
    build_detail_prompt(..., strict_retry=True).
    """
    new_words = _significant_words(new_answer)
    old_words = _significant_words(previous_answer)

    # Jawaban sangat pendek (mis. "informasi belum tersedia, hubungi PMB")
    # memang wajar dan tidak boleh dianggap tulis ulang.
    if len(new_words) < 25 or not old_words:
        return False

    overlap = len(new_words & old_words) / len(new_words)
    return overlap >= REWRITE_SIMILARITY_THRESHOLD