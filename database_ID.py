# database_ID.py — Knowledge Base Asisten Virtual UMBandung
# ============================================================================
# SUMBER DATA (terverifikasi, riset 2026):
#   [1] Situs resmi   : https://umbandung.ac.id/  dan  https://umbandung.ac.id/profil
#                       -> tagline, visi/misi, tahun berdiri, akreditasi, rektor
#   [2] Portal PMB    : https://pmb.umbandung.ac.id/  -> jalur (termasuk KIP-K),
#                       biaya, beasiswa
#   [3] Wikipedia ID  : https://id.wikipedia.org/wiki/Universitas_Muhammadiyah_Bandung
#                       -> sejarah penggabungan STIE & STAI, alamat
#   [4] EVERY UMBANDUNG LINK.txt -> seluruh tautan fakultas/prodi/layanan
#
# CATATAN: nominal biaya & jadwal dapat berubah tiap tahun ajaran -> entri terkait
# tetap mengarahkan ke halaman resmi. Item yang belum dapat dikonfirmasi diberi
# komentar "# >>> PERLU VERIFIKASI <<<".
#
# Variabel utama yang di-import oleh utils.py:
#   PETA_LOKASI, KNOWLEDGE_BASE_ID, ALIAS_KEYWORD_ID, AUTOCOMPLETE_TERMS_ID,
#   FOLLOW_UP_SUGGESTIONS_ID.
#   (ALIAS_KEYWORD_ID memetakan alias prodi/fakultas/topik -> kunci entri KB;
#    sebelumnya bernama CITY_TO_COUNTRY saat masih memakai data lama.)
# ============================================================================


import re


def wa_link(nomor: str) -> str:
    """Ubah nomor tampilan (mis. '+62 896-2315-6677') menjadi tautan WhatsApp wa.me.
    Membuang semua karakter non-digit dan menormalkan awalan 0 -> 62."""
    digit = re.sub(r"\D", "", nomor)          # sisakan angka saja
    if digit.startswith("0"):
        digit = "62" + digit[1:]              # 08xx -> 628xx
    return "https://wa.me/" + digit


def wa_tag(label: str, kontak_key: str) -> str:
    """Bangun anchor HTML WhatsApp yang bisa dipencet untuk satu unit KONTAK_UMB."""
    nomor = KONTAK_UMB[kontak_key]
    return (
        label + ": <a href='" + wa_link(nomor) + "' target='_blank' "
        "style='color:blue;'><strong>" + nomor + "</strong></a>"
    )


# --- 0. Pusat Tautan Resmi UMBandung (sumber: EVERY UMBANDUNG LINK.txt + PMB) ---
LINK_UMB = {
    # Portal & Profil
    "portal": "https://umbandung.ac.id/",
    "profil": "https://umbandung.ac.id/profil",
    "logo": "https://umbandung.ac.id/unduh_logo/",

    # Fakultas
    "fst": "https://fst.umbandung.ac.id/",
    "soshum": "https://umbandung.ac.id/fakultas/sosial_humaniora",
    "feb": "https://feb.umbandung.ac.id/",
    "fai": "https://fai.umbandung.ac.id/",
    "farmasi": "https://umbandung.ac.id/fakultas/farmasi",

    # Program Studi - FST
    "teknik_elektro": "https://umbandung.ac.id/program_studi/teknik-elektro",
    "informatika": "https://umbandung.ac.id/program_studi/informatika",
    "teknik_industri": "https://umbandung.ac.id/program_studi/teknik-industri",
    "teknologi_pangan": "https://umbandung.ac.id/program_studi/teknologi-pangan",
    "bioteknologi": "https://umbandung.ac.id/program_studi/bioteknologi",
    "agribisnis": "https://umbandung.ac.id/program_studi/agribisnis",
    # Program Studi - Sosial & Humaniora
    "ilmu_komunikasi": "https://umbandung.ac.id/program_studi/ilmu-komunikasi",
    "psikologi": "https://umbandung.ac.id/program_studi/psikologi",
    "kriya": "https://umbandung.ac.id/program_studi/kriya/",
    "administrasi_publik": "https://umbandung.ac.id/program_studi/administrasi-publik",
    # Program Studi - FEB
    "magister_manajemen": "https://umbandung.ac.id/program_studi/magister-manajemen",
    "akuntansi": "https://umbandung.ac.id/program_studi/akuntansi",
    "manajemen": "https://umbandung.ac.id/program_studi/manajemen",
    # Program Studi - FAI
    "pai": "https://umbandung.ac.id/program_studi/pendidikan-agama-islam",
    "piaud": "https://umbandung.ac.id/program_studi/pendidikan-islam-anak-usia-dini",
    "hukum_keluarga_islam": "https://umbandung.ac.id/program_studi/hukum-keluarga-islam",
    "kpi": "https://umbandung.ac.id/program_studi/komunikasi-dan-penyiaran-islam",
    "ekonomi_syariah": "https://umbandung.ac.id/program_studi/ekonomi-syariah",
    # Program Studi - Farmasi
    "prodi_farmasi": "https://umbandung.ac.id/program_studi/farmasi",
    "profesi_apoteker": "https://umbandung.ac.id/program_studi/profesi-apoteker",

    # Penelitian & Pengabdian (PPM)
    "pedoman_ppm": "https://umbandung.ac.id/penelitian_pengabdian/pedoman_ppm",
    "permohonan_ki": "https://umbandung.ac.id/penelitian_pengabdian/permohonan_ki",

    # Fasilitas & Perpustakaan
    "fasilitas": "https://umbandung.ac.id/fasilitas",
    "perpustakaan": "https://perpus.umbandung.ac.id/",
    "repository": "https://repository.umbandung.ac.id/",
    "opac": "https://opac.umbandung.ac.id/",

    # Berita
    "kabar": "https://umbandung.ac.id/kabar_umbdg",

    # Karier
    "karier": "https://umbandung.ac.id/karier",
    "karier_dosen": "https://umbandung.ac.id/karier/dosen",
    "karier_tendik": "https://umbandung.ac.id/karier/tenaga_kependidikan",
    # Detail lowongan Tenaga Kependidikan (sumber: EVERY UMBANDUNG LINK.txt)
    "tendik_laboran_ilkom": "https://umbandung.ac.id/karier/tenaga_kependidikan/laboran_ilmu_komunikasi",
    "tendik_laboran_psikologi": "https://umbandung.ac.id/karier/tenaga_kependidikan/laboran_psikologi",
    "tendik_laboran_farmasi": "https://umbandung.ac.id/karier/tenaga_kependidikan/laboran_farmasi",
    "tendik_fakultas_farmasi": "https://umbandung.ac.id/karier/tenaga_kependidikan/fakultas_farmasi",
    "tendik_sarana_prasarana": "https://umbandung.ac.id/karier/tenaga_kependidikan/sarana_prasarana",
    # >>> PERLU VERIFIKASI <<< : pada sumber, tautan "Tendik Sistem Informasi"
    # memakai URL yang sama dengan Sarana & Prasarana.
    "tendik_sistem_informasi": "https://umbandung.ac.id/karier/tenaga_kependidikan/sarana_prasarana",
    "email_rekrutmen": "sdm.rekrutmen@umbandung.ac.id",

    # PMB (Penerimaan Mahasiswa Baru)
    "pmb": "https://pmb.umbandung.ac.id/",
    "pmb_petunjuk": "https://pmb.umbandung.ac.id/petunjuk-pendaftaran",
    "pmb_biaya": "https://pmb.umbandung.ac.id/biaya-perkuliahan",
    "jalur_reguler": "https://pmb.umbandung.ac.id/jalur-pendaftaran/jalur-reguler",
    "jalur_karyawan": "https://pmb.umbandung.ac.id/jalur-pendaftaran/jalur-karyawan",
    "jalur_mahasiswa_asing": "https://pmb.umbandung.ac.id/jalur-pendaftaran/jalur-mahasiswa-asing",
    "jalur_rpl": "https://pmb.umbandung.ac.id/jalur-pendaftaran/jalur-rpl",
    "jalur_kip": "https://pmb.umbandung.ac.id/jalur-pendaftaran/jalur-kip-k",  # sumber [2]

    # Beasiswa
    "beasiswa_prestasi": "https://pmb.umbandung.ac.id/beasiswa/beasiswa-prestasi-akademik",
    "beasiswa_kader": "https://pmb.umbandung.ac.id/beasiswa/beasiswa-kader-muhammadiyah",
    "beasiswa_minat_bakat": "https://pmb.umbandung.ac.id/beasiswa/beasiswa-minat-dan-bakat",
    "beasiswa_peduli_anak_bangsa": "https://pmb.umbandung.ac.id/beasiswa/beasiswa-peduli-anak-bangsa",
    "beasiswa_tokoh_muda": "https://pmb.umbandung.ac.id/beasiswa/beasiswa-tokoh-muda-berpengaruh",
    "beasiswa_hafizh": "https://pmb.umbandung.ac.id/beasiswa/beasiswa-hafizh-quran",
    "beasiswa_putm": "https://pmb.umbandung.ac.id/beasiswa/beasiswa-putm",

    # Sistem / Portal lain
    "mentari": "https://mentari.umbandung.ac.id/",

    # Akademik / Kalender
    # >>> PERLU VERIFIKASI <<< : berkas PDF dilayani oleh Flask dari folder "static/".
    # Letakkan file "Perubahan_Kalender_Akademik_2025-2026.pdf" di dalam folder static/
    # aplikasi (chatbot_web.py). Bila di-host di domain resmi, ganti URL ini dengan
    # tautan resmi umbandung.ac.id.
    "kalender_akademik": "/static/Perubahan_Kalender_Akademik_2025-2026.pdf",

    # Media Sosial
    "facebook": "https://www.facebook.com/universitasmuhammadiyahbandung/",
    "instagram": "https://www.instagram.com/umbandung",
    "tiktok": "https://www.tiktok.com/@umbandung",
}


# --- 0b. Kontak Layanan per Unit UMBandung (sumber: KONTAK_UMB.txt) ---
# Nomor WhatsApp/HP layanan tiap unit. Disimpan sebagai string agar mudah
# dirujuk di entri knowledge base (mis. KONTAK_UMB["kemahasiswaan"]).
KONTAK_UMB = {
    "kemahasiswaan": "+62 896-2315-6677",
    "keuangan_2019_2021": "+62 857-9528-9679",
    "keuangan_2022_2023": "+62 811-2099-906",
    "keuangan_2024_2025": "+62 878-2134-6213",
    "sistem_informasi": "+62 838-2224-4926",
    "perpustakaan": "+62 895-3580-15919",   # >>> PERLU VERIFIKASI <<< : jumlah digit pada sumber tidak biasa
    "lppaik": "+62 857-9793-9009",
    "akademik": "+62 878-6043-2630",
    "security_parkir": "+62 821-1811-904",
}


# --- 1. Peta Lokasi (lokasi kampus UMBandung; isi lama sudah diganti penuh) ---
# Alamat terverifikasi [sumber 2 & 3]: Jl. Soekarno-Hatta No. 752, Cipadung Kidul,
# Panyileukan, Kota Bandung 40614, Jawa Barat.
PETA_LOKASI = {
    "kampus utama": "https://maps.google.com/?q=Universitas+Muhammadiyah+Bandung+Jl+Soekarno+Hatta+752+Cipadung+Kidul+Panyileukan+Bandung",
    "umbandung": "https://maps.google.com/?q=Universitas+Muhammadiyah+Bandung+Jl+Soekarno+Hatta+752+Cipadung+Kidul+Panyileukan+Bandung",
}


KNOWLEDGE_BASE_ID = {

    # ================== A. IDENTITAS & PROFIL ==================
    "profil umbandung": {
        "type": "paragraph",
        "content": (
            "<strong>Universitas Muhammadiyah Bandung (UMBandung)</strong> adalah perguruan tinggi "
            "swasta milik Persyarikatan Muhammadiyah di Kota Bandung yang berdiri pada "
            "<strong>14 Juni 2016</strong> dan mengusung identitas sebagai "
            "<em>Islamic Technopreneurial University</em> dengan tiga pilar: kampus Islami, "
            "kampus teknologi, dan kampus <em>entrepreneurship</em>. "
            "Profil lengkap dapat dibaca di "
            "<a href='" + LINK_UMB["profil"] + "' target='_blank' style='color:blue;'>Profil UMBandung</a>."
        )
    },
    "visi misi": {
        "type": "paragraph",
        "content": (
            "<strong>Visi UMBandung:</strong> menjadi <em>Islamic Technopreneurial University</em> "
            "yang unggul dan memberi manfaat nyata bagi umat dan bangsa pada tahun <strong>2045</strong>.<br>"
            "<strong>Misi UMBandung:</strong>"
            "<ul>"
            "<li>Menyelenggarakan pendidikan dan pembelajaran yang unggul dalam inovasi dan berjiwa entrepreneur.</li>"
            "<li>Menyelenggarakan penelitian yang berkontribusi pada pengembangan ilmu pengetahuan, teknologi, dan seni serta peningkatan inovasi.</li>"
            "<li>Menyelenggarakan pengabdian kepada masyarakat berdasarkan hasil-hasil penelitian.</li>"
            "<li>Menyelenggarakan pembinaan internalisasi dan penguatan nilai-nilai Al-Islam Kemuhammadiyahan.</li>"
            "<li>Menyelenggarakan tata kelola universitas dengan prinsip good university governance secara berkelanjutan.</li>"
            "</ul>"
            "Rumusan resmi selengkapnya di "
            "<a href='" + LINK_UMB["profil"] + "' target='_blank' style='color:blue;'>halaman Profil</a>."
        )
    },
    "islamic technopreneurial university": {
        "type": "paragraph",
        "content": (
            "<em>Islamic Technopreneurial University</em> adalah tagline dan visi akademik "
            "<strong>UMBandung</strong>, yang berdiri di atas tiga pilar: <strong>kampus Islami</strong>, "
            "<strong>kampus teknologi</strong>, dan <strong>kampus entrepreneurship</strong>. "
            "Tujuannya melahirkan teknopreneur muda Islami yang unggul secara akademik sekaligus berjiwa wirausaha. "
            "Selengkapnya di <a href='" + LINK_UMB["profil"] + "' target='_blank' style='color:blue;'>halaman Profil</a>."
        )
    },
    "sejarah umbandung": {
        "type": "paragraph",
        "content": (
            "<strong>UMBandung</strong> didirikan pada <strong>14 Juni 2016</strong> (bertepatan 9 Ramadan 1437 H) "
            "berdasarkan Surat Izin Kemenristekdikti <strong>No. 205/KPT/I/2016</strong> dengan 11 program studi awal. "
            "Perkembangan berikutnya mencakup penggabungan <strong>STIE Muhammadiyah Bandung</strong> "
            "(SK Mendikbud No. 1195/M/2020) dan perubahan <strong>STAI Muhammadiyah Bandung</strong> "
            "menjadi <strong>Fakultas Agama Islam</strong> (SK Menag No. 328 Tahun 2021). "
            "Selengkapnya di <a href='" + LINK_UMB["profil"] + "' target='_blank' style='color:blue;'>Profil UMBandung</a>."
        )
    },
    "akreditasi umbandung": {
        "type": "paragraph",
        "content": (
            "UMBandung telah memperoleh <strong>Akreditasi Institusi \"Baik Sekali\"</strong> dari "
            "<strong>BAN-PT</strong> (SK No. 323/SK/BAN-PT/Ak/PT/III/2024, tahun 2024). Akreditasi tiap program studi dapat berbeda dan dapat dicek "
            "melalui <a href='https://pddikti.kemdiktisaintek.go.id' target='_blank' style='color:blue;'>PDDikti</a>. "
            "Karena status akreditasi dapat diperbarui, mohon konfirmasi data terkini melalui "
            "<a href='" + LINK_UMB["profil"] + "' target='_blank' style='color:blue;'>situs resmi UMBandung</a>."
        )
    },
    "rektor umbandung": {
        # Sumber [1]: berita resmi umbandung.ac.id (Mei 2026). Konfirmasi berkala bila ada pergantian.
        "type": "paragraph",
        "content": (
            "Rektor Universitas Muhammadiyah Bandung saat ini adalah <strong>Prof. Dr. Herry Suhardiyanto, M.Sc., IPU.</strong> "
            "Beliau didampingi jajaran Wakil Rektor. Informasi kepemimpinan terbaru dapat dilihat di "
            "<a href='" + LINK_UMB["kabar"] + "' target='_blank' style='color:blue;'>Kabar UMBandung</a> "
            "atau <a href='" + LINK_UMB["profil"] + "' target='_blank' style='color:blue;'>halaman Profil</a>."
        )
    },
    "logo umbandung": {
        "type": "paragraph",
        "content": (
            "Logo resmi UMBandung dapat diunduh pada halaman "
            "<a href='" + LINK_UMB["logo"] + "' target='_blank' style='color:blue;'>Unduh Logo UMBandung</a>."
        )
    },
    "afiliasi muhammadiyah": {
        "type": "paragraph",
        "content": (
            "UMBandung adalah <strong>Perguruan Tinggi Muhammadiyah (PTM)</strong> yang diselenggarakan oleh "
            "Persyarikatan Muhammadiyah, dan merupakan PTM pertama yang mengusung semangat "
            "<em>Islamic Technopreneurial University</em>. Nilai Al-Islam Kemuhammadiyahan menjadi bagian "
            "dari pembinaan dan tata kelolanya."
        )
    },

    # ================== Keunggulan, Tujuan & Sambutan ==================
    "keunggulan umbandung": {
        "type": "list",
        "title": "Keunggulan Universitas Muhammadiyah Bandung:",
        "items": [
            "<strong>Terakreditasi \"Baik Sekali\"</strong> berdasarkan SK BAN-PT No. 323/SK/BAN-PT/Ak/PT/III/2024.",
            "<strong>Islamic Integrated Curriculum</strong> dengan karakter \"Islamic Technopreneur\".",
            "<strong>Aplikasi kurikulum</strong> diarahkan pada inovasi produk berbasis teknopreneurship (hardskill &amp; softskill).",
            "<strong>Dosen profesional</strong> lulusan S2, S3, dan profesor dari perguruan tinggi ternama.",
            "<strong>Sarana &amp; prasarana lengkap</strong>: laboratorium, perpustakaan digital, digital class, dan ballroom.",
            "<strong>Kampus di lokasi strategis</strong> dengan gedung baru penunjang perkuliahan dan riset.",
            "<strong>Banyak beasiswa</strong> bagi calon mahasiswa.",
        ]
    },
    "tujuan umbandung": {
        "type": "list",
        "title": "Tujuan Universitas Muhammadiyah Bandung:",
        "items": [
            "Menghasilkan lulusan yang beriman, berakhlak, berkompetensi profesional tinggi, serta unggul dalam inovasi dan kerja sama.",
            "Menghasilkan publikasi dan inovasi yang berkontribusi pada pengembangan ilmu pengetahuan, teknologi, seni, serta perekonomian dan kemaslahatan.",
            "Menghasilkan dampak positif pengabdian dan pemberdayaan masyarakat secara berkelanjutan.",
            "Menghasilkan penguatan nilai-nilai Al-Islam Kemuhammadiyahan serta suasana kampus yang Islami.",
            "Mewujudkan tata kelola universitas dengan prinsip good university governance untuk mutu yang berkelanjutan.",
        ]
    },
    "sambutan rektor umbandung": {
        "type": "paragraph",
        "content": (
            "Dalam sambutannya, Rektor <strong>Prof. Dr. Herry Suhardiyanto, M.Sc., IPU.</strong> menyampaikan bahwa "
            "UMBandung telah memperoleh Akreditasi Institusi <strong>\"Baik Sekali\"</strong> dari BAN-PT tahun 2024. "
            "Didirikan pada 2016 di Kota Bandung, UMBandung merupakan perguruan tinggi Muhammadiyah pertama yang mengusung "
            "semangat <em>Islamic Technopreneurial University</em> dan berkomitmen mencetak generasi berkarakter Islami "
            "dan technopreneurial. Selengkapnya di "
            "<a href='" + LINK_UMB["profil"] + "' target='_blank' style='color:blue;'>halaman Profil</a>."
        )
    },

    # ================== Lokasi & Kontak ==================
    "alamat kampus umbandung": {
        "type": "paragraph",
        "content": (
            "<strong>Alamat Kampus UMBandung:</strong><br>"
            "Jl. Soekarno-Hatta No. 752, Cipadung Kidul, Kec. Panyileukan, Kota Bandung 40614, Jawa Barat.<br>"
            "<a href='" + PETA_LOKASI["kampus utama"] + "' target='_blank' style='color:blue;'>Buka di Google Maps</a>"
        )
    },
    "kontak umbandung": {
        # Nomor telepon: sumber sekunder (profil schmu.id / akupintar); mohon konfirmasi ke Humas bila perlu.
        "type": "paragraph",
        "content": (
            "<strong>Kontak UMBandung</strong><br>"
            "Alamat: Jl. Soekarno-Hatta No. 752, Cipadung Kidul, Panyileukan, Kota Bandung 40614.<br>"
            "Telepon: <strong>(022) 63744992 / 63745992</strong><br>"
            "Email rekrutmen/SDM: <strong>" + LINK_UMB["email_rekrutmen"] + "</strong><br>"
            "Website: <a href='" + LINK_UMB["portal"] + "' target='_blank' style='color:blue;'>umbandung.ac.id</a><br>"
            "Instagram: <a href='" + LINK_UMB["instagram"] + "' target='_blank' style='color:blue;'>@umbandung</a>"
        )
    },
    "kontak layanan umbandung": {
        # Sumber: KONTAK_UMB.txt -> nomor WhatsApp/HP layanan tiap unit.
        # Setiap nomor ditampilkan sebagai tautan wa.me yang dapat langsung dipencet.
        "type": "list",
        "title": "Kontak layanan tiap unit UMBandung (klik untuk chat WhatsApp):",
        "items": [
            wa_tag("Kemahasiswaan", "kemahasiswaan"),
            wa_tag("Admin Akademik", "akademik"),
            wa_tag("Admin Keuangan (angkatan 2019&ndash;2021)", "keuangan_2019_2021"),
            wa_tag("Admin Keuangan (angkatan 2022&ndash;2023)", "keuangan_2022_2023"),
            wa_tag("Admin Keuangan (angkatan 2024&ndash;2025)", "keuangan_2024_2025"),
            wa_tag("Sistem Informasi", "sistem_informasi"),
            wa_tag("Admin Perpustakaan", "perpustakaan"),
            wa_tag("Admin LPPAIK", "lppaik"),
            wa_tag("Security / Parkir UMB", "security_parkir"),
        ]
    },
    "media sosial umbandung": {
        "type": "list",
        "title": "Akun media sosial resmi UMBandung:",
        "items": [
            "Instagram: <a href='" + LINK_UMB["instagram"] + "' target='_blank' style='color:blue;'>@umbandung</a>",
            "Facebook: <a href='" + LINK_UMB["facebook"] + "' target='_blank' style='color:blue;'>Universitas Muhammadiyah Bandung</a>",
            "TikTok: <a href='" + LINK_UMB["tiktok"] + "' target='_blank' style='color:blue;'>@umbandung</a>",
        ]
    },
    "website umbandung": {
        "type": "paragraph",
        "content": (
            "Situs resmi UMBandung adalah "
            "<a href='" + LINK_UMB["portal"] + "' target='_blank' style='color:blue;'>umbandung.ac.id</a>."
        )
    },

    # ================== B. PENERIMAAN MAHASISWA BARU (PMB) ==================
    "pmb umbandung": {
        "type": "paragraph",
        "content": (
            "<strong>Penerimaan Mahasiswa Baru (PMB) UMBandung</strong> dikelola melalui portal "
            "<a href='" + LINK_UMB["pmb"] + "' target='_blank' style='color:blue;'>pmb.umbandung.ac.id</a>. "
            "Di sana tersedia petunjuk pendaftaran, pilihan jalur masuk, rincian biaya, dan program beasiswa."
        )
    },
    "cara daftar pmb umbandung": {
        "type": "list",
        "title": "Langkah umum pendaftaran PMB UMBandung:",
        "items": [
            "Buka portal PMB di <a href='" + LINK_UMB["pmb"] + "' target='_blank' style='color:blue;'>pmb.umbandung.ac.id</a>.",
            "Baca <a href='" + LINK_UMB["pmb_petunjuk"] + "' target='_blank' style='color:blue;'>Petunjuk Pendaftaran</a> dan pilih jalur yang sesuai.",
            "Buat akun, isi formulir, dan unggah berkas persyaratan sesuai instruksi.",
            "Lakukan pembayaran biaya pendaftaran, lalu ikuti tahap seleksi dan daftar ulang bila diterima.",
        ]
    },
    "jalur pendaftaran umbandung": {
        "type": "list",
        "title": "Jalur pendaftaran yang tersedia di UMBandung:",
        "items": [
            "<a href='" + LINK_UMB["jalur_reguler"] + "' target='_blank' style='color:blue;'>Jalur Reguler</a>",
            "<a href='" + LINK_UMB["jalur_karyawan"] + "' target='_blank' style='color:blue;'>Jalur Karyawan</a>",
            "<a href='" + LINK_UMB["jalur_mahasiswa_asing"] + "' target='_blank' style='color:blue;'>Jalur Mahasiswa Asing</a>",
            "<a href='" + LINK_UMB["jalur_rpl"] + "' target='_blank' style='color:blue;'>Jalur RPL (Rekognisi Pembelajaran Lampau)</a>",
            "<a href='" + LINK_UMB["jalur_kip"] + "' target='_blank' style='color:blue;'>Jalur KIP-Kuliah</a>",
        ]
    },
    "kip kuliah umbandung": {
        "type": "paragraph",
        "content": (
            "UMBandung menyediakan <strong>jalur KIP-Kuliah (Kartu Indonesia Pintar Kuliah)</strong> bagi calon "
            "mahasiswa berprestasi dari keluarga kurang mampu secara ekonomi. Persyaratan dan cara daftar "
            "selengkapnya di <a href='" + LINK_UMB["jalur_kip"] + "' target='_blank' style='color:blue;'>halaman Jalur KIP-Kuliah</a>. "
            "Ketentuan dan kuota dapat berubah tiap tahun ajaran, mohon cek halaman resmi untuk info terbaru."
        )
    },
    "syarat pendaftaran umbandung": {
        # >>> PERLU VERIFIKASI <<< : rincian dokumen/nilai per jalur sebaiknya dirujuk ke halaman petunjuk.
        "type": "list",
        "title": "Persyaratan umum pendaftaran (rujuk halaman resmi untuk rincian per jalur):",
        "items": [
            "Lulusan <strong>SMA/SMK/MA</strong> atau setara, dengan ijazah/SKL yang dilegalisir.",
            "Identitas diri (KTP/Kartu Pelajar) dan dokumen pendukung lain.",
            "Pas foto terbaru sesuai ketentuan.",
            "Detail tiap jalur ada di <a href='" + LINK_UMB["pmb_petunjuk"] + "' target='_blank' style='color:blue;'>Petunjuk Pendaftaran</a>.",
        ]
    },
    "biaya kuliah umbandung": {
        # Nominal dari portal PMB resmi; dapat berubah tiap tahun ajaran -> selalu arahkan ke halaman resmi.
        "type": "paragraph",
        "content": (
            "Rincian biaya kuliah UMBandung tersedia resmi di "
            "<a href='" + LINK_UMB["pmb_biaya"] + "' target='_blank' style='color:blue;'>halaman Biaya Perkuliahan</a>. "
            "Sebagai gambaran, biaya registrasi pendaftaran sekitar <strong>Rp300.000</strong> dan terdapat komponen "
            "Daftar Ulang serta Biaya Pengembangan Pendidikan (BPP). Nominal dapat berbeda antarprogram studi dan "
            "berubah tiap tahun ajaran, sehingga mohon konfirmasi angka terbaru ke Panitia PMB.<br>"
            "<strong>Admin Keuangan (WhatsApp):</strong> "
            "angkatan 2019&ndash;2021 <a href='" + wa_link(KONTAK_UMB["keuangan_2019_2021"]) + "' target='_blank' style='color:blue;'>" + KONTAK_UMB["keuangan_2019_2021"] + "</a>, "
            "angkatan 2022&ndash;2023 <a href='" + wa_link(KONTAK_UMB["keuangan_2022_2023"]) + "' target='_blank' style='color:blue;'>" + KONTAK_UMB["keuangan_2022_2023"] + "</a>, "
            "angkatan 2024&ndash;2025 <a href='" + wa_link(KONTAK_UMB["keuangan_2024_2025"]) + "' target='_blank' style='color:blue;'>" + KONTAK_UMB["keuangan_2024_2025"] + "</a>."
        )
    },
    "jadwal pmb umbandung": {
        # >>> PERLU VERIFIKASI <<< : tanggal gelombang berubah tiap tahun; arahkan ke sumber resmi.
        "type": "paragraph",
        "content": (
            "Jadwal dan gelombang pendaftaran PMB UMBandung dibagi dalam beberapa gelombang setiap tahun ajaran "
            "dan diumumkan di portal <a href='" + LINK_UMB["pmb"] + "' target='_blank' style='color:blue;'>pmb.umbandung.ac.id</a> "
            "serta <a href='" + LINK_UMB["instagram"] + "' target='_blank' style='color:blue;'>Instagram @umbandung</a>. "
            "Mohon cek sumber resmi untuk tanggal terbaru."
        )
    },

    # ================== C. FAKULTAS & PROGRAM STUDI ==================
    "fakultas umbandung": {
        "type": "list",
        "title": "Fakultas di Universitas Muhammadiyah Bandung:",
        "items": [
            "<a href='" + LINK_UMB["fst"] + "' target='_blank' style='color:blue;'>Fakultas Sains dan Teknologi (FST)</a>",
            "<a href='" + LINK_UMB["soshum"] + "' target='_blank' style='color:blue;'>Fakultas Sosial dan Humaniora</a>",
            "<a href='" + LINK_UMB["feb"] + "' target='_blank' style='color:blue;'>Fakultas Ekonomi dan Bisnis (FEB)</a>",
            "<a href='" + LINK_UMB["fai"] + "' target='_blank' style='color:blue;'>Fakultas Agama Islam (FAI)</a>",
            "<a href='" + LINK_UMB["farmasi"] + "' target='_blank' style='color:blue;'>Fakultas Farmasi</a>",
        ]
    },
    "program studi umbandung": {
        "type": "paragraph",
        "content": (
            "<strong>Program Studi UMBandung berdasarkan fakultas:</strong>"
            "<ul>"
            "<li><strong>Sains &amp; Teknologi:</strong> Teknik Elektro, Informatika, Teknik Industri, "
            "Teknologi Pangan, Bioteknologi, Agribisnis.</li>"
            "<li><strong>Sosial &amp; Humaniora:</strong> Ilmu Komunikasi, Psikologi, "
            "Kriya Tekstil &amp; Fashion, Administrasi Publik.</li>"
            "<li><strong>Ekonomi &amp; Bisnis:</strong> Manajemen, Akuntansi, Magister Manajemen (S2).</li>"
            "<li><strong>Agama Islam:</strong> Pendidikan Agama Islam, Pendidikan Islam Anak Usia Dini, "
            "Hukum Keluarga Islam, Komunikasi dan Penyiaran Islam, Ekonomi Syariah.</li>"
            "<li><strong>Farmasi:</strong> Farmasi, Profesi Apoteker.</li>"
            "</ul>"
            "Detail tiap prodi dapat dibuka di "
            "<a href='" + LINK_UMB["portal"] + "' target='_blank' style='color:blue;'>umbandung.ac.id</a>."
            "<br><br>"
            "<em>Untuk info lengkap sebuah prodi (deskripsi, visi, misi, tujuan), cukup ketik "
            "<strong>nama prodinya</strong> &mdash; misalnya <strong>Farmasi</strong>, "
            "<strong>Informatika</strong>, atau <strong>Psikologi</strong>. Untuk daftar pengajar, "
            "ketik <strong>dosen</strong> diikuti nama prodi, contoh <strong>dosen Teknik Elektro</strong>.</em>"
        )
    },
    "fakultas sains dan teknologi": {
        "type": "paragraph",
        "content": (
            "<strong>Fakultas Sains dan Teknologi (FST)</strong> menaungi prodi: Teknik Elektro, Informatika, "
            "Teknik Industri, Teknologi Pangan, Bioteknologi, dan Agribisnis. "
            "Selengkapnya: <a href='" + LINK_UMB["fst"] + "' target='_blank' style='color:blue;'>fst.umbandung.ac.id</a>."
            " <em>Ketik nama prodinya untuk profil lengkap, mis. <strong>Informatika</strong>.</em>"
        )
    },
    "fakultas sosial dan humaniora": {
        "type": "paragraph",
        "content": (
            "<strong>Fakultas Sosial dan Humaniora</strong> menaungi prodi: Ilmu Komunikasi, Psikologi, "
            "Kriya Tekstil &amp; Fashion, dan Administrasi Publik. "
            "Selengkapnya: <a href='" + LINK_UMB["soshum"] + "' target='_blank' style='color:blue;'>halaman Fakultas Sosial &amp; Humaniora</a>."
            " <em>Ketik nama prodinya untuk profil lengkap, mis. <strong>Psikologi</strong>.</em>"
        )
    },
    "fakultas ekonomi dan bisnis": {
        "type": "paragraph",
        "content": (
            "<strong>Fakultas Ekonomi dan Bisnis (FEB)</strong> menaungi prodi: Manajemen, Akuntansi, dan "
            "Magister Manajemen (S2). "
            "Selengkapnya: <a href='" + LINK_UMB["feb"] + "' target='_blank' style='color:blue;'>feb.umbandung.ac.id</a>."
            " <em>Ketik nama prodinya untuk profil lengkap, mis. <strong>Manajemen</strong>.</em>"
        )
    },
    "fakultas agama islam": {
        "type": "paragraph",
        "content": (
            "<strong>Fakultas Agama Islam (FAI)</strong> menaungi prodi: Pendidikan Agama Islam, "
            "Pendidikan Islam Anak Usia Dini, Hukum Keluarga Islam, Komunikasi dan Penyiaran Islam, dan "
            "Ekonomi Syariah. FAI merupakan transformasi dari STAI Muhammadiyah Bandung (2021). "
            "Selengkapnya: <a href='" + LINK_UMB["fai"] + "' target='_blank' style='color:blue;'>fai.umbandung.ac.id</a>."
            " <em>Ketik nama prodinya untuk profil lengkap, mis. <strong>Pendidikan Agama Islam</strong>.</em>"
        )
    },
    "fakultas farmasi": {
        "type": "paragraph",
        "content": (
            "<strong>Fakultas Farmasi</strong> menaungi prodi Farmasi dan Profesi Apoteker. "
            "Selengkapnya: <a href='" + LINK_UMB["farmasi"] + "' target='_blank' style='color:blue;'>halaman Fakultas Farmasi</a>."
            " <em>Ketik nama prodinya untuk profil lengkap, mis. <strong>Farmasi</strong>.</em>"
        )
    },
    # (entri "program studi informatika" kini dibangun otomatis dari PROFIL_PRODI_UMB)
    # (entri "program studi psikologi" kini dibangun otomatis dari PROFIL_PRODI_UMB)
    # (entri "program studi manajemen" kini dibangun otomatis dari PROFIL_PRODI_UMB)
    # (entri "program studi farmasi" kini dibangun otomatis dari PROFIL_PRODI_UMB)
    "pascasarjana umbandung": {
        "type": "paragraph",
        "content": (
            "Program pascasarjana di UMBandung antara lain <strong>Magister Manajemen (S2)</strong> di Fakultas "
            "Ekonomi dan Bisnis, dengan kurikulum yang dirancang relevan dengan kebutuhan industri. "
            "Info: <a href='" + LINK_UMB["magister_manajemen"] + "' target='_blank' style='color:blue;'>Magister Manajemen UMBandung</a>."
        )
    },

    # ================== D. BEASISWA ==================
    "beasiswa umbandung": {
        "type": "list",
        "title": "Program beasiswa UMBandung (via portal PMB):",
        "items": [
            "<a href='" + LINK_UMB["beasiswa_prestasi"] + "' target='_blank' style='color:blue;'>Beasiswa Prestasi Akademik</a>",
            "<a href='" + LINK_UMB["beasiswa_kader"] + "' target='_blank' style='color:blue;'>Beasiswa Kader Muhammadiyah</a>",
            "<a href='" + LINK_UMB["beasiswa_minat_bakat"] + "' target='_blank' style='color:blue;'>Beasiswa Minat dan Bakat (Apresiasi Seni &amp; Olahraga)</a>",
            "<a href='" + LINK_UMB["beasiswa_peduli_anak_bangsa"] + "' target='_blank' style='color:blue;'>Beasiswa Peduli Anak Bangsa</a>",
            "<a href='" + LINK_UMB["beasiswa_tokoh_muda"] + "' target='_blank' style='color:blue;'>Beasiswa Tokoh Muda Berpengaruh</a>",
            "<a href='" + LINK_UMB["beasiswa_hafizh"] + "' target='_blank' style='color:blue;'>Beasiswa Hafizh Quran</a>",
            "<a href='" + LINK_UMB["beasiswa_putm"] + "' target='_blank' style='color:blue;'>Beasiswa PUTM</a>",
            "Selain itu tersedia <a href='" + LINK_UMB["jalur_kip"] + "' target='_blank' style='color:blue;'>jalur KIP-Kuliah</a> dari pemerintah.",
        ]
    },
    "beasiswa kader muhammadiyah": {
        "type": "paragraph",
        "content": (
            "<strong>Beasiswa Kader Muhammadiyah</strong> diberikan UMBandung kepada kader yang aktif di "
            "Organisasi Otonom (Ortom) Muhammadiyah seperti IPM, Hizbul Wathan (HW), dan Tapak Suci. "
            "Syarat antara lain lulus SMA/SMK/MA atau setara, ijazah/SKL dilegalisir, identitas diri, pas foto, "
            "dan kartu tanda anggota Ortom. Detail: "
            "<a href='" + LINK_UMB["beasiswa_kader"] + "' target='_blank' style='color:blue;'>halaman Beasiswa Kader Muhammadiyah</a>."
        )
    },

    "laboratorium umbandung": {
        "type": "list",
        "title": "Laboratorium di UMBandung (sarana praktik per program studi):",
        "items": [
            "Lab Kimia", "Lab Bioteknologi", "Lab Farmasetika", "Lab Psikologi",
            "Lab Ilmu Komunikasi", "Lab Teknologi Pangan", "Lab Komunikasi Penyiaran Islam",
            "Lab Biologi", "Lab Komputer", "Lab Elektro", "Lab Informatika",
        ]
    },

    # ================== E. FASILITAS & PERPUSTAKAAN ==================
    "fasilitas umbandung": {
        "type": "paragraph",
        "content": (
            "Informasi fasilitas kampus UMBandung dapat dilihat pada halaman "
            "<a href='" + LINK_UMB["fasilitas"] + "' target='_blank' style='color:blue;'>Fasilitas UMBandung</a>. "
            "Kampus memiliki <strong>Auditorium K.H. Ahmad Dahlan</strong>, beragam <strong>laboratorium</strong> "
            "(lihat \"laboratorium umbandung\"), perpustakaan, dan ruang kelas ber-LCD. "
            "Fasilitas lainnya: <strong>Mushola, Galeri Investasi, Graha Mahasiswa,</strong> dan <strong>Kantin Opieun Bandung</strong>."
        )
    },
    "perpustakaan umbandung": {
        "type": "list",
        "title": "Layanan Perpustakaan UMBandung:",
        "items": [
            "Portal Perpustakaan: <a href='" + LINK_UMB["perpustakaan"] + "' target='_blank' style='color:blue;'>perpus.umbandung.ac.id</a>",
            "Repository (karya ilmiah): <a href='" + LINK_UMB["repository"] + "' target='_blank' style='color:blue;'>repository.umbandung.ac.id</a>",
            "Katalog OPAC: <a href='" + LINK_UMB["opac"] + "' target='_blank' style='color:blue;'>opac.umbandung.ac.id</a>",
            "Admin Perpustakaan (WhatsApp): <a href='" + wa_link(KONTAK_UMB["perpustakaan"]) + "' target='_blank' style='color:blue;'><strong>" + KONTAK_UMB["perpustakaan"] + "</strong></a>",
        ]
    },

    # ================== F. LAYANAN AKADEMIK & ADMINISTRASI ==================
    "kalender akademik umbandung": {
        # Sumber: SK Rektor No. 149/REK/II.3.AU/A/2026 tentang Perubahan Kalender
        # Akademik UMBandung TA 2025/2026 (ditetapkan 11 Februari 2026).
        # >>> PERLU VERIFIKASI <<< : tautan PDF mengarah ke folder static/ aplikasi;
        # pastikan berkas PDF tersedia di sana atau ganti dengan URL resmi.
        "type": "list",
        "title": (
            "Kalender Akademik UMBandung TA 2025/2026 "
            "(SK Rektor No. 149/REK/II.3.AU/A/2026). Berikut agenda utamanya:"
        ),
        "items": [
            "<strong>Semester Gasal</strong>",
            "Perkuliahan Semester Gasal: 29 September 2025 s.d 26 Januari 2026",
            "PESONAMU (Orientasi Mahasiswa Baru): 22 s.d 27 September 2025",
            "Pengukuhan Mahasiswa Baru: 27 September 2025",
            "UTS Gasal: 17 s.d 29 November 2025",
            "Pekan Tenang &amp; Persiapan UAS Gasal: 19 s.d 24 Januari 2026",
            "UAS Gasal: 26 Januari s.d 7 Februari 2026",
            "Wisuda Sarjana ke-9: April 2026",
            "<strong>Semester Genap</strong>",
            "Penginputan KRS/Perwalian Genap: 23 Februari s.d 7 Maret 2026",
            "Perkuliahan Semester Genap: 9 Maret s.d 11 Juli 2026",
            "Libur Idul Fitri: 18 s.d 24 Maret 2026",  # >>> PERLU VERIFIKASI <<< : tahun Hijriah pada sumber tidak konsisten (1445 H / 1447 H)
            "UTS Genap: 11 s.d 23 Mei 2026",
            "Milad/Dies Natalis ke-9 UM Bandung: 14 Juni 2026",
            "UAS Genap: 13 s.d 25 Juli 2026",
            "KKN: Agustus s.d September 2026",
            "Wisuda Sarjana ke-10: September 2026",
            (
                "Unduh dokumen lengkap: "
                "<a href='" + LINK_UMB["kalender_akademik"] + "' target='_blank' style='color:blue;'>"
                "Kalender Akademik UMBandung TA 2025/2026 (PDF)</a>"
            ),
        ]
    },
    "portal akademik umbandung": {
        # >>> PERLU VERIFIKASI <<< : fungsi spesifik "Mentari" (KRS/KHS) sebaiknya dikonfirmasi ke BAAK.
        "type": "paragraph",
        "content": (
            "UMBandung memiliki portal/sistem daring <strong>Mentari</strong> di "
            "<a href='" + LINK_UMB["mentari"] + "' target='_blank' style='color:blue;'>mentari.umbandung.ac.id</a>. "
            "Untuk fungsi spesifik (KRS, KHS, layanan akademik) mohon dikonfirmasi ke BAAK."
        )
    },
    "krs umbandung": {
        # >>> PERLU VERIFIKASI <<< : periode & prosedur KRS belum dirinci pada sumber resmi.
        "type": "paragraph",
        "content": (
            "Pengisian KRS dilakukan melalui portal akademik UMBandung "
            "(<a href='" + LINK_UMB["mentari"] + "' target='_blank' style='color:blue;'>mentari.umbandung.ac.id</a>). "
            "Periode pengisian mengikuti kalender akademik; mohon konfirmasi jadwal pastinya ke BAAK. "
            "Kendala teknis akun/portal dapat menghubungi <strong>Sistem Informasi</strong> (WhatsApp): "
            "<a href='" + wa_link(KONTAK_UMB["sistem_informasi"]) + "' target='_blank' style='color:blue;'><strong>" + KONTAK_UMB["sistem_informasi"] + "</strong></a>."
        )
    },
    "baak umbandung": {
        "type": "paragraph",
        "content": (
            "Layanan administrasi akademik (surat keterangan aktif, transkrip, legalisir ijazah, dll.) dilayani "
            "oleh <strong>BAAK UMBandung</strong>. Untuk informasi cepat dapat menghubungi "
            "Admin Akademik (WhatsApp): <a href='" + wa_link(KONTAK_UMB["akademik"]) + "' target='_blank' "
            "style='color:blue;'><strong>" + KONTAK_UMB["akademik"] + "</strong></a>, atau melalui "
            "<a href='" + LINK_UMB["portal"] + "' target='_blank' style='color:blue;'>umbandung.ac.id</a>."
        )
    },
    "cuti akademik umbandung": {
        # >>> PERLU VERIFIKASI <<< : prosedur, syarat, & formulir cuti belum tersedia di sumber resmi.
        "type": "paragraph",
        "content": (
            "Pengajuan <strong>cuti akademik (cuti kuliah)</strong> umumnya diproses melalui "
            "<strong>BAAK / Bagian Akademik</strong> mengikuti kalender akademik, biasanya dengan "
            "mengisi formulir serta persetujuan dosen wali dan Program Studi. Karena prosedur dan "
            "syarat rinci dapat berbeda tiap periode, mohon konfirmasi langsung ke BAAK melalui "
            "<a href='" + LINK_UMB["portal"] + "' target='_blank' style='color:blue;'>umbandung.ac.id</a>."
        )
    },
    "wisuda umbandung": {
        # >>> PERLU VERIFIKASI <<< : periode, syarat, biaya wisuda belum tersedia di sumber.
        "type": "paragraph",
        "content": (
            "Informasi periode, syarat, dan biaya pendaftaran wisuda UMBandung dapat dikonfirmasi ke BAAK / "
            "Bagian Akademik melalui <a href='" + LINK_UMB["portal"] + "' target='_blank' style='color:blue;'>umbandung.ac.id</a>. "
            "Detail jadwal dapat berbeda tiap periode."
        )
    },
    "skripsi umbandung": {
        # >>> PERLU VERIFIKASI <<< : minimal SKS/IPK & prosedur per prodi belum tersedia.
        "type": "paragraph",
        "content": (
            "Syarat pengajuan skripsi/tugas akhir (minimal SKS, IPK, dan prosedur) mengikuti panduan akademik "
            "masing-masing program studi. Mohon merujuk ke panduan prodi atau BAAK untuk ketentuan rincinya."
        )
    },

    # ================== Penelitian & Pengabdian ==================
    "penelitian dan pengabdian": {
        "type": "list",
        "title": "Penelitian & Pengabdian kepada Masyarakat (PPM) UMBandung:",
        "items": [
            "Pedoman PPM: <a href='" + LINK_UMB["pedoman_ppm"] + "' target='_blank' style='color:blue;'>Pedoman PPM</a>",
            "Permohonan Kekayaan Intelektual (KI) Internal: <a href='" + LINK_UMB["permohonan_ki"] + "' target='_blank' style='color:blue;'>Permohonan KI</a>",
            "Skema pendanaan internal: <strong>Penelitian Dosen Pemula</strong> dan <strong>Pengabdian Masyarakat Kompetisi</strong> (besaran &amp; kuota mengikuti tahun anggaran &mdash; cek Pedoman PPM).",
        ]
    },

    # ================== Karier / Rekrutmen ==================
    "karier umbandung": {
        "type": "paragraph",
        "content": (
            "Informasi lowongan di UMBandung tersedia pada halaman "
            "<a href='" + LINK_UMB["karier"] + "' target='_blank' style='color:blue;'>Karier UMBandung</a>, "
            "meliputi <a href='" + LINK_UMB["karier_dosen"] + "' target='_blank' style='color:blue;'>Karier Dosen</a> dan "
            "<a href='" + LINK_UMB["karier_tendik"] + "' target='_blank' style='color:blue;'>Tenaga Kependidikan</a>.<br>"
            "Berkas lamaran dikirim dalam format <strong>PDF</strong> ke "
            "<strong>" + LINK_UMB["email_rekrutmen"] + "</strong> dengan subjek sesuai ketentuan lowongan."
        )
    },

    "tenaga kependidikan umbandung": {
        "type": "list",
        "title": (
            "Lowongan Tenaga Kependidikan UMBandung (berkas lamaran PDF dikirim ke "
            "<strong>" + LINK_UMB["email_rekrutmen"] + "</strong>):"
        ),
        "items": [
            "<a href='" + LINK_UMB["tendik_laboran_ilkom"] + "' target='_blank' style='color:blue;'>Laboran Ilmu Komunikasi</a>",
            "<a href='" + LINK_UMB["tendik_laboran_psikologi"] + "' target='_blank' style='color:blue;'>Laboran Psikologi</a>",
            "<a href='" + LINK_UMB["tendik_laboran_farmasi"] + "' target='_blank' style='color:blue;'>Laboran Farmasi</a>",
            "<a href='" + LINK_UMB["tendik_fakultas_farmasi"] + "' target='_blank' style='color:blue;'>Tenaga Kependidikan Fakultas Farmasi</a>",
            "<a href='" + LINK_UMB["tendik_sarana_prasarana"] + "' target='_blank' style='color:blue;'>Sarana dan Prasarana</a>",
            "<a href='" + LINK_UMB["tendik_sistem_informasi"] + "' target='_blank' style='color:blue;'>Sistem Informasi</a>",
        ]
    },

    # ================== Berita ==================
    "berita umbandung": {
        "type": "paragraph",
        "content": (
            "Kabar dan berita terbaru UMBandung dapat diikuti di "
            "<a href='" + LINK_UMB["kabar"] + "' target='_blank' style='color:blue;'>Kabar UMBandung</a> "
            "dan <a href='" + LINK_UMB["instagram"] + "' target='_blank' style='color:blue;'>Instagram @umbandung</a>."
        )
    },

    # ================== G. KEMAHASISWAAN ==================
    "kemahasiswaan umbandung": {
        # Ortom Muhammadiyah dikonfirmasi dari pemberitaan resmi (IMM, HW, Tapak Suci). Daftar UKM lengkap: verifikasi.
        "type": "paragraph",
        "content": (
            "Di lingkungan UMBandung terdapat organisasi kemahasiswaan serta organisasi otonom Muhammadiyah, "
            "antara lain <strong>Ikatan Mahasiswa Muhammadiyah (IMM)</strong>, <strong>Tapak Suci</strong>, dan "
            "<strong>Hizbul Wathan (HW)</strong>, di samping UKM lainnya. Untuk daftar lengkap UKM dan cara bergabung, "
            "silakan hubungi <strong>Bagian Kemahasiswaan</strong> (WhatsApp): "
            "<a href='" + wa_link(KONTAK_UMB["kemahasiswaan"]) + "' target='_blank' style='color:blue;'><strong>" + KONTAK_UMB["kemahasiswaan"] + "</strong></a> atau "
            "<a href='" + LINK_UMB["portal"] + "' target='_blank' style='color:blue;'>umbandung.ac.id</a>."
        )
    },

    # ================== H. SAPAAN & RESPONS UMUM ==================
    "assalamualaikum": {
        "type": "paragraph",
        "content": "Wa'alaikumussalam warahmatullahi wabarakatuh. 🙏 Selamat datang di <strong>Asisten Virtual UMBandung</strong>. Ada yang bisa saya bantu seputar PMB, prodi, beasiswa, atau layanan akademik?"
    },
    "salam": {
        "type": "paragraph",
        "content": "Wa'alaikumussalam. Selamat datang di Asisten Virtual UMBandung. Silakan sampaikan pertanyaan Anda. 😊"
    },
    "hello": {
        "type": "paragraph",
        "content": "Halo! Selamat datang di <strong>Asisten Virtual UMBandung</strong>. Saya siap membantu seputar <strong>PMB, biaya kuliah, beasiswa, program studi, fasilitas,</strong> dan layanan akademik UMBandung."
    },
    "hi": {
        "type": "paragraph",
        "content": "Halo! Saya Asisten Virtual Universitas Muhammadiyah Bandung. Silakan ajukan pertanyaan Anda seputar layanan akademik dan kemahasiswaan UMBandung."
    },
    "halo": {
        "type": "paragraph",
        "content": "Halo! Saya Asisten Virtual UMBandung, <em>Islamic Technopreneurial University</em>. Apa yang ingin Anda ketahui hari ini?"
    },
    "hai": {
        "type": "paragraph",
        "content": "Halo! Senang bertemu dengan Anda. Ada yang bisa saya bantu seputar UMBandung — PMB, prodi, beasiswa, atau layanan akademik?"
    },
    "selamat pagi": {
        "type": "paragraph",
        "content": "Selamat pagi! 🌅 Ada yang bisa saya bantu seputar layanan akademik UMBandung hari ini?"
    },
    "selamat siang": {
        "type": "paragraph",
        "content": "Selamat siang! Ada yang bisa saya bantu seputar UMBandung?"
    },
    "selamat sore": {
        "type": "paragraph",
        "content": "Selamat sore! Silakan, ada yang bisa saya bantu seputar UMBandung?"
    },
    "selamat malam": {
        "type": "paragraph",
        "content": "Selamat malam! Ada yang bisa saya bantu seputar UMBandung?"
    },
    "apa kabar": {
        "type": "paragraph",
        "content": "Alhamdulillah, saya siap membantu Anda! 😊 Ada yang ingin ditanyakan seputar UMBandung?"
    },
    "siapa kamu": {
        "type": "paragraph",
        "content": "Saya adalah <strong>Asisten Virtual Universitas Muhammadiyah Bandung</strong>, siap membantu Anda menemukan informasi seputar PMB, program studi, beasiswa, biaya kuliah, fasilitas, dan layanan akademik UMBandung."
    },
    "kamu siapa": {
        "type": "paragraph",
        "content": "Saya <strong>Asisten Virtual UMBandung</strong> — asisten informasi resmi untuk membantu pertanyaan seputar akademik dan kemahasiswaan Universitas Muhammadiyah Bandung."
    },
    "bisa bantu apa": {
        "type": "list",
        "title": "Saya dapat membantu Anda dengan informasi seputar:",
        "items": [
            "Penerimaan Mahasiswa Baru (PMB): jalur, syarat, dan jadwal.",
            "Biaya kuliah dan program beasiswa (termasuk KIP-Kuliah).",
            "Fakultas dan program studi.",
            "Layanan akademik (BAAK, KRS, wisuda) dan fasilitas kampus.",
        ]
    },
    "terima kasih": {
        "type": "paragraph",
        "content": "Sama-sama! Senang bisa membantu. Jika ada pertanyaan lain seputar UMBandung, silakan tanyakan kembali. 😊"
    },
    "makasih": {
        "type": "paragraph",
        "content": "Sama-sama! Semoga informasinya bermanfaat. 😊"
    },
    "sama sama": {
        "type": "paragraph",
        "content": "Tentu! Jangan ragu bertanya lagi bila ada yang ingin Anda ketahui tentang UMBandung."
    },
    "oke": {
        "type": "paragraph",
        "content": "Baik! Jika ada pertanyaan lain seputar UMBandung, silakan sampaikan. 😊"
    },
    "sampai jumpa": {
        "type": "paragraph",
        "content": "Sampai jumpa! Semoga sukses, dan jangan ragu kembali bila butuh informasi UMBandung. 👋"
    },
}


# --- 2. Data Dosen per Program Studi (sumber: DOSEN_UMB.txt) ---
# DOSEN_UMB adalah SUMBER KEBENARAN TUNGGAL untuk data dosen.
# Untuk menambah/mengubah dosen, cukup edit dict ini; entri knowledge base
# "dosen <prodi>" dibangun otomatis oleh generator di bawah (lihat bagian 2b).
# Struktur tiap prodi: {"prodi": <nama tampil>, "link": <kunci LINK_UMB>,
#                       "dosen": [{"nama": ..., "jabatan": ...}, ...]}
DOSEN_UMB = {
    "teknik elektro": {
        "prodi": "Teknik Elektro",
        "link": "teknik_elektro",
        "dosen": [
            {"nama": "Jaya Kuncara Rosa Susila S.T., M.T.", "jabatan": "Dosen"},
            {"nama": "Muhammad Afit S.T., M.T.", "jabatan": "Dosen"},
            {"nama": "Mulki Rezka Budi Pratama", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Pujo Laksono S.T., M.T.", "jabatan": "Dosen"},
            {"nama": "Prof. Mad. Dr. Ir. Syafrudin Masri S.T., M.Eng., IPU.", "jabatan": "Dosen"},
            {"nama": "Fajrin Nurul Haq Lc., M.Hum.", "jabatan": "Dosen"},
            {"nama": "Dwi Purliantoro S.Si., M.Pd.", "jabatan": "Dosen"},
            {"nama": "Dr. Ihsan Imaduddin S.Si., M.Si", "jabatan": "Dosen"},
        ],
    },
    "informatika": {
        "prodi": "Informatika",
        "link": "informatika",
        "dosen": [
            {"nama": "Aila Gema Safitri S.T., M.T.", "jabatan": "Dosen"},
            {"nama": "Rinanda Febriani S.ST., M.T.", "jabatan": "Dosen"},
            {"nama": "Ririn Suharsih S.Pd., M.T.", "jabatan": "Ketua Program Studi"},
            {"nama": "Sutadi Triputra S.ST., M.T.", "jabatan": "Dosen"},
            {"nama": "Nana Karyana Kurdi S.E., M.Kom.", "jabatan": "Dosen"},
            {"nama": "Dianti Eka Aprilia S.Kom., M.T.", "jabatan": "Dosen"},
            {"nama": "Ahmad Suryan S.T., M.T.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Taufik Rahmat Kurniawan S.Kom., M.T.", "jabatan": "Dosen"},
            {"nama": "Fajar Winata S.Kom., M.T.", "jabatan": "Dosen"},
            {"nama": "Rizky Kharisma N. E. P. S.Tr.Kom., M.T.", "jabatan": "Dosen"},
            {"nama": "Dina Budhi Utami S.Kom., M.T.", "jabatan": "Dosen"},
            {"nama": "Vitradisa Pratama", "jabatan": "Dosen"},
            {"nama": "Ferra Arik Tridalestari S.T., M.T.", "jabatan": "Dosen"},
        ],
    },
    "teknik industri": {
        "prodi": "Teknik Industri",
        "link": "teknik_industri",
        "dosen": [
            {"nama": "Achmad Miftah Faridl S.T., M.T.", "jabatan": "Dosen"},
            {"nama": "Inten Tejaasih M.T.", "jabatan": "Dosen"},
            {"nama": "Vivayani Wahyu Dewanti M.T.", "jabatan": "Dosen"},
            {"nama": "Budiyan Mariyadi S.T., M.T.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Dr. Ir. Arief Yunan M.Si., IPU., ASEAN Eng.", "jabatan": "Dosen"},
            {"nama": "Dedy Chandra H S.T., M.T.", "jabatan": "Dosen"},
            {"nama": "Rangga Wirawan S.Si., M.Si.", "jabatan": "Dosen"},
        ],
    },
    "teknologi pangan": {
        "prodi": "Teknologi Pangan",
        "link": "teknologi_pangan",
        "dosen": [
            {"nama": "Mae Amelianawati S.T.P., M.Si.", "jabatan": "Dosen"},
            {"nama": "Dr. Khairiah SP., M.T.", "jabatan": "Dosen"},
            {"nama": "Ratna Sari Listyaningrum S.T.P., M.Si.", "jabatan": "Dosen"},
            {"nama": "Dr. Saepul Adnan S.Si., M.Si.", "jabatan": "Dosen"},
            {"nama": "Dr. Sakina Yeti Kiptiyah S.TP., M.Sc.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Fahmi Ilman Fahrudin S.T.P., MoFT., Ph.D.", "jabatan": "Dosen"},
            {"nama": "Ana Nadiya Afinatul Fishi S.T.P., M.T.P.", "jabatan": "Dosen"},
            {"nama": "Redoyan Refli S.Si., M.Si., Ph.D.", "jabatan": "Dosen"},
        ],
    },
    "bioteknologi": {
        "prodi": "Bioteknologi",
        "link": "bioteknologi",
        "dosen": [
            {"nama": "Luthfia Hastiani Muharram S.Si., M.Si.", "jabatan": "Dosen"},
            {"nama": "Nelis Hernahadini S.Si., M.Si.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Nisa Ihsani S.Si., M.Si.", "jabatan": "Dosen"},
            {"nama": "Noviani Arifina Istiqomah S.Si., M.Si.", "jabatan": "Dosen"},
            {"nama": "Wulan Pertiwi S.Si., M.Si.", "jabatan": "Dosen"},
            {"nama": "Muhammad Fauzi S.P., M.P.", "jabatan": "Dosen"},
            {"nama": "Haryanto S.Si., M.Si.", "jabatan": "Dosen"},
            {"nama": "Dra. Maelita R. Moeis Ph.D.", "jabatan": "Dosen"},
            {"nama": "Qori Atur Rodiah Suhada M.Si.", "jabatan": "Dosen"},
        ],
    },
    "agribisnis": {
        "prodi": "Agribisnis",
        "link": "agribisnis",
        "dosen": [
            {"nama": "Tri Hanifawati S.Si., M.Sc.", "jabatan": "Dosen"},
            {"nama": "Dr. Widhi Netraning Pertiwi S.Pd., M.Sc.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Dr. Ivonne Ayesha S.P., M.P.", "jabatan": "Dosen"},
            {"nama": "Agus Sutandi S.T.P., M.P.", "jabatan": "Dosen"},
            {"nama": "Eni Kusumawati S.P., M.Si.", "jabatan": "Dosen"},
            {"nama": "Yayu Ulfah Marliani S.P., M.Si.", "jabatan": "Dosen"},
            {"nama": "Reza Fikri Alfatah S.P., M.Sc.", "jabatan": "Dosen"},
        ],
    },
    "ilmu komunikasi": {
        "prodi": "Ilmu Komunikasi",
        "link": "ilmu_komunikasi",
        "dosen": [
            {"nama": "Dra. Euis Evi Puspitasari M.Si.", "jabatan": "Dosen"},
            {"nama": "Roni Tabroni S.Sos., M.Si.", "jabatan": "Dosen"},
            {"nama": "Ulfa Yuniati S.I.Kom., M.Si.", "jabatan": "Dosen"},
            {"nama": "Agung Tirta Wibawa S.Sos, M. Ag", "jabatan": "Dosen"},
            {"nama": "Yuti Yuniarti S.Pd., M.Pd.", "jabatan": "Dosen"},
            {"nama": "Dr. Ijang Faisal M.Si.", "jabatan": "Dosen"},
            {"nama": "Dr. Nenny Kencanawati M.Si.", "jabatan": "Dosen"},
            {"nama": "Dr. Aziz Taufik Hirzi S.I.P., M.Si.", "jabatan": "Dosen"},
            {"nama": "Resti Ernawati S.Sos., M.Ikom.", "jabatan": "Dosen"},
            {"nama": "Arief Permadi M.Sos.", "jabatan": "Dosen"},
            {"nama": "Endrian Kurniadi S.Kom., M.I.Kom.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Hadi Muhammad Rizal S.I.Kom., M.I.Kom.", "jabatan": "Dosen"},
            {"nama": "Vera Martikasari S.P., M.I.Kom.", "jabatan": "Dosen"},
            {"nama": "Naditha Rizkya Hantoro S.I.Kom., M.I.Kom.", "jabatan": "Dosen"},
        ],
    },
    "psikologi": {
        "prodi": "Psikologi",
        "link": "psikologi",
        "dosen": [
            {"nama": "Novy Yulianty S.Psi., M.Psi., Psikolog.", "jabatan": "Dosen"},
            {"nama": "Rovi Husnaini S.Th.I, M.Ag.", "jabatan": "Dosen"},
            {"nama": "Riyanda Utari S.Psi., M.Psi., Psikolog.", "jabatan": "Dosen"},
            {"nama": "Anggi Anggraeni S.Psi., M.Psi., Psikolog.", "jabatan": "Dosen"},
            {"nama": "Rika Dwi Agustiningsih S.Psi., M.Psi., Psikolog.", "jabatan": "Dosen"},
            {"nama": "Dr. Irianti Usman M.A.", "jabatan": "Dosen"},
            {"nama": "Dr. Lili Suryani Batubara M.Hum.", "jabatan": "Dosen"},
            {"nama": "Isman Rahmani Yusron M.A.", "jabatan": "Dosen"},
            {"nama": "Nurlaela Hamidah S.Psi., M.M., M.Psi., Psikolog", "jabatan": "Dosen"},
            {"nama": "Arina Shabrina S.Psi., M.Psi.", "jabatan": "Dosen"},
            {"nama": "Vina Lusiana Nadianti S.Psi., M.Psi., Psikolog.", "jabatan": "Dosen"},
            {"nama": "Adzanishari Mawaddah Rahmah S.Psi., M.Psi., Psikolog.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Naera Zhafira Azkiati Zamzami S.Psi., M.Psi., Psikolog.", "jabatan": "Dosen"},
            {"nama": "Ainin Rahmanawati S.Psi., M.A.", "jabatan": "Dosen"},
            {"nama": "Novita Sari S.Psi., M.Psi.", "jabatan": "Dosen"},
            {"nama": "Tasya Augustiya S.Psi., M.A", "jabatan": "Dosen"},
            {"nama": "Dr. Tita Rosita, S.Psi., M.Pd", "jabatan": "Dosen"},
            {"nama": "Ilham Ibrahim S.Pd., M.A.", "jabatan": "Dosen"},
        ],
    },
    "kriya tekstil dan fashion": {
        "prodi": "Kriya Tekstil dan Fashion",
        "link": "kriya",
        "dosen": [
            {"nama": "Dewi Werdayani M.Pd.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Dr. Komarudin Kudiya S.I.P., M.Ds.", "jabatan": "Dosen"},
            {"nama": "Dra. Saftiyaningsih Ken Atik M.Ds.", "jabatan": "Dosen"},
            {"nama": "Prof., Dr. Nanang Rizali M.S.D.", "jabatan": "Dosen"},
            {"nama": "Faisal Amien Prawira S.Sn., M.Ds.", "jabatan": "Dosen"},
            {"nama": "Ghaida Nasya Putri S.Ds., M.Ds.", "jabatan": "Dosen"},
        ],
    },
    "administrasi publik": {
        "prodi": "Administrasi Publik",
        "link": "administrasi_publik",
        "dosen": [
            {"nama": "Meti Mediyastuti Sofyan S.Sos., M.A.P.", "jabatan": "Dosen"},
            {"nama": "Rikki Maulana Yusup S.IP., M.A.P.", "jabatan": "Dosen"},
            {"nama": "Fatmawati S.IP., M.A.P.", "jabatan": "Dosen"},
            {"nama": "Dr., Ir. Latifah M.T.", "jabatan": "Dosen"},
            {"nama": "Dr. Drs. Dikdik Dahlan Lukman M.Hum.", "jabatan": "Dosen"},
            {"nama": "Mohamad Hilal Numan S.H., M.Kn.", "jabatan": "Dosen"},
            {"nama": "Ramaditya Rahardian S.Sos., M.KP", "jabatan": "Dosen"},
            {"nama": "Yayan Andri S.Pd., M.A.P.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Dr. Ai Nunung M.A.P.", "jabatan": "Dosen"},
            {"nama": "Ara Aydia Van Is S.IP., M.A.P., M.A.", "jabatan": "Dosen"},
        ],
    },
    "magister manajemen": {
        "prodi": "Magister Manajemen",
        "link": "magister_manajemen",
        "dosen": [
            {"nama": "Dr. Eris Sudariswan S.E., M.M., CPMA.", "jabatan": "Dosen"},
            {"nama": "Dr. Helin Garlinia Yudawisastra S.E., M.Si.", "jabatan": "Dosen"},
            {"nama": "Dr., Dra. Alfiana M.M.", "jabatan": "Dosen"},
            {"nama": "Dr. Suparjiman S.Sos., M.M.", "jabatan": "Dosen"},
            {"nama": "Dr. Rita Zulbetti S.Si., M.M", "jabatan": "Dosen"},
            {"nama": "Dr. Perwito S.E., M.M.", "jabatan": "Dosen"},
        ],
    },
    "akuntansi": {
        "prodi": "Akuntansi",
        "link": "akuntansi",
        "dosen": [
            {"nama": "Agus Bagianto S.E., M.M., M.Ak.", "jabatan": "Dosen"},
            {"nama": "Verawaty S.E.Akt., M.Ak.", "jabatan": "Dosen"},
            {"nama": "Erfan Erfiansyah S.Ak., Ak., M.Ak.", "jabatan": "Dosen"},
            {"nama": "Rustandi S.E., M.Ak., Ak., CA.", "jabatan": "Dosen"},
            {"nama": "Dr. Toto Sugihyanto S.E., M.Ak.", "jabatan": "Dosen"},
            {"nama": "Dr. Wasifah Hanim S.E., M.Si.", "jabatan": "Dosen"},
            {"nama": "Dr. Hendriyana M.Ak., Ak., Ca., ASEAN CPA.", "jabatan": "Dosen"},
            {"nama": "Dr. Yuniati S.E., M.Ak.", "jabatan": "Dosen"},
            {"nama": "Dr. Inugrah Ratia Pratiwi S.E., M.Ak., Ak., CA.", "jabatan": "Dosen"},
            {"nama": "Dr. Sugiartiningsih S.E., M.Si.", "jabatan": "Dosen"},
            {"nama": "H. Qur'ani Noor S.E., M.E., Ak., CA.", "jabatan": "Dosen"},
            {"nama": "Siti Kodariah S.S., M.Hum.", "jabatan": "Dosen"},
            {"nama": "Dr. Lisna Lisnawati S.E., M.Ak.", "jabatan": "Dosen"},
            {"nama": "Iman Harjono SE., MOS., M.Ak., CHFrP.", "jabatan": "Dosen"},
            {"nama": "Dr Yati Nurhajati S.E., M.Si., Ak., CA", "jabatan": "Dosen"},
        ],
    },
    "manajemen": {
        "prodi": "Manajemen",
        "link": "manajemen",
        "dosen": [
            {"nama": "Dr. Drs. Ia Kurnia M.Pd.", "jabatan": "Dosen"},
            {"nama": "Dra. Neneng Nurbaeti Amien S.E., M.Si.", "jabatan": "Dosen"},
            {"nama": "Abin Suarsa", "jabatan": "Dosen"},
            {"nama": "Rifqi Ali Mubarok S.Ag., M.Si., CHRM, CHRP, CHRL, CBSB, CIFA", "jabatan": "Dosen"},
            {"nama": "Yeni Andriyani S.S., M.Pd.", "jabatan": "Dosen"},
            {"nama": "Indra Sasangka S.E., M.M.", "jabatan": "Dosen"},
            {"nama": "Dr. Wandy Zulkarnaen S.E., M.M.", "jabatan": "Dosen"},
            {"nama": "Budi Sadarman S.E., M.M.", "jabatan": "Dosen"},
            {"nama": "Asep Suwarna", "jabatan": "Dosen"},
            {"nama": "Iis Dewi Fitriani", "jabatan": "Dosen"},
            {"nama": "Sawalni S.Pd., M.M.", "jabatan": "Dosen"},
            {"nama": "Ikhsan Kamil S.E., M.M.", "jabatan": "Dosen"},
            {"nama": "Ridlo Abdillah S.Pd., M.Si.", "jabatan": "Dosen"},
            {"nama": "Dr., Ir. Siti Mardiana M.T., M.S.I.S.ec.", "jabatan": "Dosen"},
            {"nama": "Ahmad Diponegoro", "jabatan": "Dosen"},
            {"nama": "Nadya Larasati Aghnia", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Hani Humaeriyah S.E., M.M.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Dini Mardiani S.E., M.B.A.", "jabatan": "Dosen"},
            {"nama": "Sofa Parihah Nurasiah S.E., M.S.M.", "jabatan": "Dosen"},
            {"nama": "Alia Tri Utami", "jabatan": "Dosen"},
            {"nama": "Dr. Megha Sakova S.M.B., M.M", "jabatan": "Dosen"},
            {"nama": "Halimah Zahrah S.E., M.M., M.H.", "jabatan": "Dosen"},
        ],
    },
    "pendidikan agama islam": {
        "prodi": "Pendidikan Agama Islam",
        "link": "pai",
        "dosen": [
            {"nama": "Muhtadin M.Ag.", "jabatan": "Dosen"},
            {"nama": "Dr. Hendar Riyadi M.Ag.", "jabatan": "Dosen"},
            {"nama": "Supala M.Ag.", "jabatan": "Dosen"},
            {"nama": "Dr. Miftahul Huda S.Pd.I., M.Ag.", "jabatan": "Dosen"},
            {"nama": "Mukhlishah M.Ag.", "jabatan": "Dosen"},
            {"nama": "Dr. Sitti Chadidjah M.Pd.", "jabatan": "Dosen"},
            {"nama": "Dr. Ace Somantri M.Ag.", "jabatan": "Dosen"},
            {"nama": "Mochamad Fadlani Salam", "jabatan": "Dosen"},
            {"nama": "Dr. Iim Ibrohim M.Ag", "jabatan": "Dosen"},
            {"nama": "Dr. Hernawati S.Pd., M.Pd.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Dr. Rahmat Fadhli Ed.M.", "jabatan": "Dosen"},
            {"nama": "Prof. Dr. Afif Muhammad M.A.", "jabatan": "Dosen"},
            {"nama": "Dadang Syaripudin", "jabatan": "Dosen"},
        ],
    },
    "pendidikan islam anak usia dini": {
        "prodi": "Pendidikan Islam Anak Usia Dini",
        "link": "piaud",
        "dosen": [
            {"nama": "Dita Handayani M.Ag.", "jabatan": "Dosen"},
            {"nama": "Dr. Esty Faatinisa S.Psi., M.Pd.", "jabatan": "Dosen"},
            {"nama": "Isya Siti Aisyatul Mbz M.Pd.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Taufik Maulana S.Pd.I., M.Pd.", "jabatan": "Dosen"},
            {"nama": "Yulia Nur Annisa S.Psi., M.Pd.", "jabatan": "Dosen"},
            {"nama": "Rizka Saputri", "jabatan": "Dosen"},
            {"nama": "Yenny Yuanita M.Sn.", "jabatan": "Dosen"},
            {"nama": "Dian Kusumawati M.Pd.", "jabatan": "Dosen"},
            {"nama": "Lilis Lismarina", "jabatan": "Dosen"},
            {"nama": "Dr. Taty Setiaty M.Pd.", "jabatan": "Dosen"},
        ],
    },
    "hukum keluarga islam": {
        "prodi": "Hukum Keluarga Islam",
        "link": "hukum_keluarga_islam",
        "dosen": [
            {"nama": "Dr. Yudi Daryadi S.Fil.I., M.Ag.", "jabatan": "Dosen"},
            {"nama": "Mochamad Faizal Almaududi Aziz Dachlan S.Th.I., M.Ag.", "jabatan": "Dosen"},
            {"nama": "Dr. Fikfik Taufik S.S., M.Sy.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Dr. Indra Budi Jaya S.H., M.H.", "jabatan": "Dosen"},
            {"nama": "Azhar Muhammad Akbar S.Sy., M.H.", "jabatan": "Dosen"},
            {"nama": "Sopha Hafitriani M.H.", "jabatan": "Dosen"},
            {"nama": "Dr Diana Farid S.Ag., S.H., M.E.Sy", "jabatan": "Dosen"},
        ],
    },
    "komunikasi dan penyiaran islam": {
        "prodi": "Komunikasi dan Penyiaran Islam",
        "link": "kpi",
        "dosen": [
            {"nama": "Mohammad Fahmi Amrullah M.Ag.", "jabatan": "Dosen"},
            {"nama": "Dr. Ahmad Rifai M.Ag.", "jabatan": "Dosen"},
            {"nama": "Femi Fauziah Alamsyah M.Hum.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Dr. Rahmat Alamsyah M.Ag.", "jabatan": "Dosen"},
            {"nama": "Siti Marlida M.Ag.", "jabatan": "Dosen"},
            {"nama": "Syarif Syahidin M.Sos.", "jabatan": "Dosen"},
            {"nama": "Sopaat Rahmat Selamet M.Hum.", "jabatan": "Dosen"},
            {"nama": "Dr. Cecep Taufikurrohman M.Ag.", "jabatan": "Dosen"},
            {"nama": "Prof. Dr. Dadang Kahmad M.Si.", "jabatan": "Dosen"},
            {"nama": "Kelik Nursetiyo Widiyanto S.Sos., M.I.Kom.", "jabatan": "Dosen"},
        ],
    },
    "ekonomi syariah": {
        "prodi": "Ekonomi Syariah",
        "link": "ekonomi_syariah",
        "dosen": [
            {"nama": "Lina Marlina Susana S.Pd., M.E.Sy.", "jabatan": "Dosen"},
            {"nama": "Dadang Mulyana S.H., M.E.", "jabatan": "Dosen"},
            {"nama": "Molly Mustikasari S.Sos., M.E.", "jabatan": "Dosen"},
            {"nama": "Yudistia Teguh A Fikri S.E.Sy., M.E.", "jabatan": "Dosen"},
            {"nama": "Yudi Haryadi", "jabatan": "Dosen"},
            {"nama": "Irawati M.E.Sy.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Arif Nurrakhman S.E., M.M.", "jabatan": "Dosen"},
            {"nama": "Dr. Heni Mulyasari S.T., M.Ag.", "jabatan": "Dosen"},
        ],
    },
    "farmasi": {
        "prodi": "Farmasi",
        "link": "prodi_farmasi",
        "dosen": [
            {"nama": "Apt. Anis Puji Rahayu S.Farm., M.Si.", "jabatan": "Dosen"},
            {"nama": "Apt. Fauzia Ningrum Syaputri S.Farm., M.Farm.", "jabatan": "Dosen"},
            {"nama": "Titian Daru Asmara Tugon S.Farm., M.Farm.", "jabatan": "Dosen"},
            {"nama": "Ahmad Hidayatullah M.Pd.", "jabatan": "Dosen"},
            {"nama": "Abdurahman Ridho S.Farm., M.Farm.", "jabatan": "Dosen"},
            {"nama": "Maulidwina Bethasari S.Farm., M.Farm.", "jabatan": "Dosen"},
            {"nama": "Nurul Ambardhani S.Si., M.Si.", "jabatan": "Dosen"},
            {"nama": "Zulkaida S.Farm., M.S.Farm.", "jabatan": "Dosen"},
            {"nama": "Apt. Ardian Baitariza S.Si., M.Si.", "jabatan": "Dosen"},
            {"nama": "Apt., Dr. Khusnul Fadhilah S.Farm", "jabatan": "Dosen"},
            {"nama": "Apt. Kartika Sari M.S.Farm.", "jabatan": "Dosen"},
            {"nama": "Apt. Mutiara Imansari S.Farm., M.Si.", "jabatan": "Dosen"},
            {"nama": "Apt. Diantinofriani S.Farm., M.S.Farm.", "jabatan": "Sekretaris Program Studi"},
            {"nama": "Apt. Dwi Larasati Setyaningrum S.Farm., M.Sc.", "jabatan": "Dosen"},
            {"nama": "Apt. Nurul Zakiyah M.S.Farm", "jabatan": "Dosen"},
            {"nama": "Apt Feris Dzaky Ridwan Nafis M.Farm", "jabatan": "Dosen"},
            {"nama": "Muhamad Iqbal Rhamadianto M.S.Farm.", "jabatan": "Dosen"},
            {"nama": "Apt. Alfi Fitriyani S.Farm., M.S.Farm.", "jabatan": "Dosen"},
            {"nama": "Apt. Dr. Meiti Rosmiati S.Si., M.Farm", "jabatan": "Dosen"},
            {"nama": "Dra. Livia Syafnir M.Si.", "jabatan": "Dosen"},
            {"nama": "Andinny Nur Permatasari", "jabatan": "Dosen"},
            {"nama": "apt Nurul Fitri Rahmawati S.Farm., M.S.Farm", "jabatan": "Dosen"},
            {"nama": "Apt. Haristika Chresna Pamungkas M.S.Farm.", "jabatan": "Dosen"},
            {"nama": "Apt. Ainun Habibah S.Farm., M.S.Farm.", "jabatan": "Dosen"},
        ],
    },
    "profesi apoteker": {
        "prodi": "Profesi Apoteker",
        "link": "profesi_apoteker",
        "dosen": [
            {"nama": "Dr., Apt. Dwintha Lestari S.Farm., M.Si.", "jabatan": "Dosen"},
            {"nama": "Apt. Ardilla Kemala Dewi M.S.Farm", "jabatan": "Dosen"},
            {"nama": "Apt. Sani Asmi Ramdani Lestari M.Farm.Klin", "jabatan": "Dosen"},
            {"nama": "Apt. Rizzqi Septiprajaamalia Rosdianto S.Farm., M.S.Farm", "jabatan": "Sekretaris Program Studi"},
            {"nama": "apt. Adam Aulia Rahman M.S.Farm", "jabatan": "Dosen"},
        ],
    },
}


# --- 2b. Generator entri Knowledge Base untuk dosen ---
# Catatan: ini hanya MENYUSUN DATA agar konsisten dengan format
# KNOWLEDGE_BASE_ID (type "list"); tidak mengubah logika pencarian di utils.py.
def _build_dosen_kb_entries(data):
    """Bangun entri "dosen <prodi>" bertipe list dari DOSEN_UMB."""
    entries = {}
    for prodi_key, info in data.items():
        items = []
        for d in info["dosen"]:
            if d["jabatan"].lower() == "dosen":
                items.append(d["nama"])
            else:
                items.append(d["nama"] + " &mdash; <strong>" + d["jabatan"] + "</strong>")
        link = LINK_UMB.get(info["link"])
        if link:
            items.append(
                "Profil prodi: <a href='" + link + "' target='_blank' style='color:blue;'>"
                + info["prodi"] + " UMBandung</a>"
            )
        entries["dosen " + prodi_key] = {
            "type": "list",
            "title": "Dosen Program Studi " + info["prodi"] + " UMBandung:",
            "items": items,
        }
    return entries


KNOWLEDGE_BASE_ID.update(_build_dosen_kb_entries(DOSEN_UMB))

# Entri ringkasan ditambahkan PALING AKHIR agar query spesifik per-prodi
# (mis. "dosen psikologi umbandung") tetap menang atas ringkasan umum
# pada pencocokan semua-kata di utils.py (urutan stabil).
KNOWLEDGE_BASE_ID["dosen umbandung"] = {
    "type": "list",
    "title": (
        "Informasi dosen UMBandung tersedia per program studi. Silakan sebutkan "
        "prodinya, contoh: <strong>\"dosen informatika\"</strong>. Program studi yang tersedia:"
    ),
    "items": [info["prodi"] for info in DOSEN_UMB.values()],
}



# --- 3. Profil Program Studi (sumber: DATABASE_TAMBAHAN_UMB.txt) ---
# PROFIL_PRODI_UMB = SUMBER KEBENARAN TUNGGAL untuk profil tiap prodi.
# Untuk mengubah/menambah profil, cukup edit dict ini; entri knowledge base
# "program studi <prodi>" dibangun otomatis oleh generator (bagian 3b).
# Field: prodi, link (kunci LINK_UMB), tagline, deskripsi, visi, misi[], tujuan[], extra{label:[...]}
# Nilai None berarti tidak tersedia pada sumber (perlu verifikasi).
PROFIL_PRODI_UMB = {
    "teknik elektro": {
        "prodi": "Teknik Elektro",
        "link": "teknik_elektro",
        "tagline": "Membuka cakrawala teknologi masa depan bagi technopreneur unggulan bangsa.",
        "deskripsi": "Bidang Teknik Elektro adalah salah satu bidang rekayasa yang banyak berpengaruh dalam perkembangan peradaban dunia. Program studi sarjana Teknik Elektro berdiri pada 14 Juni 2016 melalui SK No. 205/KPT/I/2016 dan menerima mahasiswa pertama pada tahun 2017.",
        "visi": "Menjadi Program Studi Teknik Elektro yang unggul dalam rekayasa teknik kendali dan komputer yang selaras dengan nilai-nilai Al-Islam Kemuhammadiyahan dan teknopreneurial untuk menghasilkan lulusan yang profesional, kreatif, inovatif, dan berdaya saing.",
        "misi": [
            "Menyelenggarakan pendidikan tinggi bidang teknik elektro yang menguasai ilmu pengetahuan, rekayasa, dan teknologi serta berwawasan islami.",
            "Melaksanakan penelitian bidang teknik elektro yang dapat meningkatkan taraf hidup masyarakat, bangsa, dan negara.",
            "Berperan aktif dalam pengabdian masyarakat bidang Teknik Elektro yang berwawasan lingkungan, berkelanjutan, serta berjiwa kewirausahaan.",
            "Menjalin kerja sama dengan stakeholder, baik instansi pemerintah maupun pihak swasta.",
        ],
        "tujuan": None,
        "extra": {
            "Kuliah Penciri": [
                "Al-Islam dan Kemuhammadiyahan (AIK) serta Technopreneur.",
                "Penciri prodi: Internet of Things (IoT) dan Kecerdasan Buatan (AI).",
                "Menerapkan konsep Merdeka Belajar Kampus Merdeka (MBKM) dan pedoman FORTEI.",
            ],
        },
    },
    "informatika": {
        "prodi": "Informatika",
        "link": "informatika",
        "tagline": "Mewujudkan Software Engineer terbaik dengan solusi aplikatif bagi Indonesia.",
        "deskripsi": "Program Studi Teknik Informatika memberi perhatian khusus pada teknologi terkini seperti Virtual Reality, Data Warehouse, Integrated Database, Internet of Things, dan Augmented Reality. Pembelajaran ditempuh 8 semester (144 SKS) yang dibagi menjadi Informatika Dasar, Informatika Lanjut, dan Penerapan Bisnis Startup, untuk menghasilkan lulusan berkompetensi Junior Programmer dan startup bisnis produk digital.",
        "visi": "Menjadi program studi yang sangat baik dalam menghasilkan lulusan Teknik Informatika berjiwa technopreneur yang memiliki kecerdasan spiritual, emosional, dan sosial di bidang Rekayasa Perangkat Lunak.",
        "misi": [
            "Menyelenggarakan pendidikan sesuai teknologi terbaru yang berorientasi pada perkembangan industri informatika terkini.",
            "Melaksanakan penelitian dan pengabdian melalui penerapan teknologi informasi dan komunikasi sesuai kebutuhan masyarakat.",
            "Melaksanakan kerja sama dengan berbagai instansi dan industri bidang teknologi informasi dan komunikasi.",
            "Membangun unit-unit bisnis terkait.",
        ],
        "tujuan": None,
        "extra": {
            "Kurikulum Unggulan": [
                "Saung Kreasi & Wirausaha.",
                "Laboratorium Komputer performa tinggi untuk pengembangan produk digital (game, video, aplikasi bergerak).",
                "Jaringan industri digital dan komunitas teknologi.",
                "Business matching dengan investor, BUMN, BUMD, dan lainnya.",
            ],
            "Prospek Lulusan": [
                "Wirausaha bidang Rekayasa Perangkat Lunak dengan kompetensi manajemen proyek.",
                "Software Engineer yang menguasai pengembangan perangkat lunak dari scratch hingga installer siap pakai.",
            ],
        },
    },
    "teknik industri": {
        "prodi": "Teknik Industri",
        "link": "teknik_industri",
        "tagline": "Menghasilkan industrial engineer yang fleksibel dan dinamis.",
        "deskripsi": "Teknik Industri adalah bidang ilmu yang fokus pada perancangan, pengelolaan, dan perbaikan sistem, baik barang maupun jasa. Berorientasi teknopreneurship, prodi ini membekali ilmu kewirausahaan mulai dari merancang produk, merencanakan produksi, pengendalian kualitas, perancangan pabrik, hingga pemasaran.",
        "visi": "Mengembangkan keilmuan teknik industri berbasis nilai-nilai keislaman dan teknoprenerial dengan memperhatikan kebutuhan lingkungan sehingga memberikan dampak sosial yang berarti.",
        "misi": None,
        "tujuan": None,
        "extra": {
            "Kompetensi Lulusan (CPL, mengacu KKNI & BKSTI)": [
                "Menerapkan matematika, ilmu alam/material, teknologi informasi, dan keteknikan pada prinsip keteknikindustrian.",
                "Merancang sistem terintegrasi dengan berbagai batasan multi-aspek yang realistis.",
                "Merancang dan melakukan eksperimen serta menganalisis data untuk pengambilan keputusan.",
                "Mengidentifikasi, merumuskan, dan menyelesaikan permasalahan kompleks teknik industri.",
                "Berkomunikasi efektif, bekerja dalam tim, dan menjalankan etika profesi sesuai nilai AIK.",
                "Mengidentifikasi peluang bisnis, menyusun rencana bisnis, dan analisis kelayakan dengan memanfaatkan teknologi.",
            ],
        },
    },
    "teknologi pangan": {
        "prodi": "Teknologi Pangan",
        "link": "teknologi_pangan",
        "tagline": None,
        "deskripsi": "Teknologi Pangan UMBandung (S-1) merancang kurikulum dengan tiga kompetensi terintegrasi: keislaman (pangan halal dan tayib), technopreneurship, dan ilmu teknologi pangan berbasis potensi bahan pangan lokal.",
        "visi": "Menjadi program studi unggul dan inovatif dalam mengembangkan keilmuan sains dan teknologi pangan halal berbasis keanekaragaman pangan Nusantara melalui sistem biorefinery sirkular berkelanjutan, untuk menghasilkan lulusan profesional dan teknopreneur berkarakter islami yang berdaya saing global.",
        "misi": [
            "Pendidikan: menyelenggarakan pendidikan berkualitas bidang sains dan teknologi pangan lokal, kehalalan pangan, biorefinery sirkular, dan teknopreneur.",
            "Penelitian: menyelenggarakan penelitian inovatif berbasis keanekaragaman pangan Nusantara untuk produk pangan aman, bermutu, dan halal.",
            "Pengabdian: melaksanakan pengabdian melalui hilirisasi hasil riset dan penerapan biorefinery sirkular berkelanjutan.",
            "AIK: mengintegrasikan nilai Al-Islam dan Kemuhammadiyahan secara menyeluruh dalam tridharma.",
        ],
        "tujuan": [
            "Menghasilkan lulusan kompeten, profesional, berdaya saing, dan berkarakter Islami.",
            "Menghasilkan penelitian inovatif berbasis keanekaragaman pangan Nusantara.",
            "Memberikan solusi nyata atas permasalahan pangan, keamanan pangan, dan gizi.",
            "Menghasilkan lulusan berakhlak karimah dan berjiwa teknopreneur.",
        ],
        "extra": None,
    },
    "bioteknologi": {
        "prodi": "Bioteknologi",
        "link": "bioteknologi",
        "tagline": "Solutive Biotechnology for ummah.",
        "deskripsi": "Bioteknologi adalah disiplin ilmu pemanfaatan makhluk hidup, metabolit, dan virus dalam proses produksi untuk menghasilkan produk bernilai tambah. Penerapannya luas: pangan, kesehatan, energi, lingkungan, pertanian, perikanan, dan kelautan.",
        "visi": "Mengembangkan keilmuan bioteknologi melalui pemanfaatan biodiversitas tropis Nusantara yang berdampak pada peningkatan kualitas kehidupan manusia dan pembangunan berkelanjutan, untuk menghasilkan lulusan berkompetensi peneliti muda, bioteknopreneur, dan praktisi yang berkarakter rahmatan lil 'alamiin.",
        "misi": [
            "Menyelenggarakan pendidikan berkualitas di berbagai bidang bioteknologi berbasis sumber daya hayati tropis.",
            "Melaksanakan penelitian dan publikasi ilmiah berkualitas berbasis pemanfaatan sumber daya hayati tropis.",
            "Menyelenggarakan pengabdian masyarakat berkualitas dengan memanfaatkan kearifan lokal.",
            "Mengintegrasikan keilmuan bioteknologi dan keterampilan wirausaha berdasarkan nilai keislaman.",
        ],
        "tujuan": None,
        "extra": {
            "Kurikulum Unggulan": [
                "Terintegrasi keislaman dan implementasi MBKM yang mendukung islamic technopreneurship.",
                "Materi dari bioteknologi konvensional hingga modern (rekayasa genetika, nanobioteknologi, biologi sintetik).",
                "Perancangan melibatkan praktisi industri, akademisi, dan ilmuwan kelas dunia.",
            ],
        },
    },
    "agribisnis": {
        "prodi": "Agribisnis",
        "link": "agribisnis",
        "tagline": None,
        "deskripsi": "Program Studi Agribisnis UMBandung memiliki kekhasan pada Program Pengembangan Bisnis (Business Development) serta penguasaan nilai-nilai Islami/Kemuhammadiyahan dalam konsep agribisnis berbasis kearifan lokal, berwawasan lingkungan, dan berkelanjutan.",
        "visi": None,
        "misi": None,
        "tujuan": None,
        "extra": {
            "Kompetensi": [
                "Menerapkan prinsip syariah dan memanfaatkan jaringan organisasi Muhammadiyah dalam mengembangkan agribisnis.",
                "Memiliki soft skill dan tanggung jawab mengaplikasikan IPTEK agribisnis di masyarakat.",
                "Menguasai konsep kewirausahaan dan agribisnis pada subsistem hulu, on farm, dan hilir.",
                "Menerapkan prinsip kewirausahaan dan kepemimpinan dalam agribisnis.",
            ],
            "Kurikulum Khas (Pengembangan Bisnis)": [
                "Pengembangan Bisnis I (Perencanaan Usaha Agribisnis).",
                "Pengembangan Bisnis II (Produksi Agribisnis).",
                "Pengembangan Bisnis III (Pemasaran Agribisnis).",
                "Pengembangan Bisnis IV (Evaluasi, Inovasi, dan Pengembangan).",
            ],
        },
    },
    "ilmu komunikasi": {
        "prodi": "Ilmu Komunikasi",
        "link": "ilmu_komunikasi",
        "tagline": "Communication Studies UMBandung: courageous, creative, good attitude, and good communication in the digital era.",
        "deskripsi": "Prodi Ilmu Komunikasi UMBandung membentuk sarjana yang mampu memahami dan mengaplikasikan keterampilan komunikasi berbasis teknologi digital, sekaligus sarjana entrepreneur Islami yang kompeten dalam bisnis komunikasi, media, dan industri kreatif.",
        "visi": "Menjadi program studi yang unggul dalam bidang ilmu komunikasi berbasis teknopreneur dan berkarakter Islami tingkat internasional pada tahun 2045.",
        "misi": [
            "Menyelenggarakan pendidikan tinggi ilmu komunikasi yang berorientasi pada teori, metodologi, dan praktik dalam konteks sosial, digital, dan global berlandaskan nilai Islam dan Kemuhammadiyahan.",
            "Mengembangkan penelitian komunikasi yang inovatif dan berbasis data (jurnalistik, humas, komunikasi digital, big data).",
            "Melaksanakan pengabdian berbasis komunikasi pemberdayaan dengan pendekatan partisipatif dan beretika.",
            "Mendorong lahirnya teknopreneur bidang komunikasi melalui inkubasi bisnis komunikasi digital.",
            "Memperluas jejaring kolaboratif dengan industri, media, akademik, dan komunitas global untuk memperkuat MBKM.",
        ],
        "tujuan": None,
        "extra": None,
    },
    "psikologi": {
        "prodi": "Psikologi",
        "link": "psikologi",
        "tagline": "Menghasilkan Sarjana Psikologi terlatih, inovatif, dan kompeten yang berpedoman pada Kode Etik Psikologi.",
        "deskripsi": "Prodi Psikologi UMBandung menekankan psikologi kognitif untuk menghasilkan lulusan yang mandiri, kreatif, inovatif, dan berjiwa entrepreneur, serta mampu bekerja di bidang pendidikan, industri, maupun sosial guna meningkatkan kesehatan mental individu.",
        "visi": "Menjadi program studi Psikologi yang mengintegrasikan ilmu Psikologi dengan nilai-nilai Islam dan menghasilkan sarjana Psikologi yang berkarakter technopreneur.",
        "misi": [
            "Menyelenggarakan pendidikan psikologi berbasis pendekatan kognitif dan nilai Islam yang menghasilkan lulusan profesional, kompetitif, dan berjiwa technopreneur.",
            "Melaksanakan dan mengembangkan penelitian psikologi berbasis nilai Islam.",
            "Melaksanakan pengabdian kepada masyarakat atas dasar tanggung jawab dan kepedulian sosial.",
            "Melaksanakan kerja sama dengan lembaga pendidikan, penelitian, pemerintah, dunia usaha, dan masyarakat.",
        ],
        "tujuan": None,
        "extra": None,
    },
    "kriya tekstil dan fashion": {
        "prodi": "Kriya Tekstil dan Fashion",
        "link": "kriya",
        "tagline": "Impress and Creative Power.",
        "deskripsi": "Kriya Tekstil dan Fashion UMBandung difokuskan pada Desain Permukaan (Surface Design) dan Desain Struktur (Structure Design), mengandung muatan nilai estetik, simbolik, dan fungsional yang berlandaskan kearifan budaya lokal Nusantara (local indigenous).",
        "visi": "Menjadi program studi yang unggul dan mampu menjadi pusat pengkajian kriya, tekstil, dan fashion berbasis kearifan lokal Nusantara.",
        "misi": [
            "Meningkatkan penyelenggaraan Caturdharma untuk memenuhi kebutuhan masyarakat secara terpadu dan produktif.",
            "Menggali dan mengembangkan kekayaan seni budaya Nusantara sebagai penggerak ekonomi kreatif.",
            "Membina kehidupan kampus sebagai scientific community dan learning society untuk menghasilkan lulusan berdaya saing.",
            "Menjalin kerja sama dengan stakeholder untuk mewujudkan visi-misi prodi.",
        ],
        "tujuan": [
            "Menghasilkan lulusan bermutu dan kreatif (creativepreneur) berbasis kearifan budaya lokal.",
            "Menghasilkan penelitian dan pengabdian dalam bidang Kriya Tekstil dan Fashion.",
            "Menjalin kerja sama dengan stakeholder dalam bidang Kriya Tekstil dan Fashion.",
        ],
        "extra": None,
    },
    "administrasi publik": {
        "prodi": "Administrasi Publik",
        "link": "administrasi_publik",
        "tagline": "For Better Policies and Services.",
        "deskripsi": "Prodi Administrasi Publik UMBandung menyiapkan lulusan unggul di bidang pelayanan, kebijakan, dan manajemen publik bercorak islamic technopreneur. Berdiri 14 Juni 2016 (SK 205/KPT/I/2016) dan memperoleh akreditasi peringkat \"Baik\" (2021-2026).",
        "visi": "Menjadi lembaga pendidikan tinggi yang mampu melahirkan lulusan berkompetensi bidang administrasi publik yang berjiwa teknopreneur, profesional, mandiri, dan Islami.",
        "misi": [
            "Menyelenggarakan pendidikan profesional dan bermutu di bidang ilmu administrasi publik sesuai standar mutu.",
            "Menyelenggarakan penelitian yang bermutu di bidang ilmu administrasi publik.",
            "Menyelenggarakan pengabdian kepada masyarakat di bidang administrasi publik.",
            "Menyelenggarakan kegiatan Al-Islam dan Kemuhammadiyahan.",
            "Menjalin kerja sama untuk pengembangan Islamic Technopreneur di bidang administrasi publik.",
        ],
        "tujuan": None,
        "extra": None,
    },
    "magister manajemen": {
        "prodi": "Magister Manajemen",
        "link": "magister_manajemen",
        "tagline": "Membangun leader bisnis berbasis Islami dan teknologi.",
        "deskripsi": "Program Studi Magister Manajemen UMBandung dibuka berdasarkan SK Menteri Pendidikan Tinggi, Sains, dan Teknologi No. 208/B/O/2025, sebagai lanjutan Program Studi Manajemen (S-1) FEB, dengan tiga konsentrasi pada tahap awal.",
        "visi": "Menjadi program studi magister manajemen berbasis Islami, teknologi, dan kewirausahaan pada tingkat internasional pada tahun 2045.",
        "misi": [
            "Menyelenggarakan pendidikan manajemen bisnis berkualitas dengan nilai keislaman.",
            "Menyelenggarakan penelitian inovatif yang mendukung pengembangan manajemen dan bisnis.",
            "Memberikan kontribusi nyata atas permasalahan masyarakat melalui penerapan ilmu manajemen dan bisnis.",
            "Membangun kemitraan profesional pada tingkat nasional dan internasional.",
            "Menyelenggarakan tata kelola yang baik dan berkelanjutan.",
        ],
        "tujuan": None,
        "extra": {
            "Konsentrasi": [
                "Manajemen Sumber Daya Manusia - pengembangan SDM strategis dan organizational development.",
                "Manajemen Pemasaran - strategi pemasaran modern, consumer behavior, dan digital marketing.",
                "Manajemen Keuangan - financial planning, investment, dan corporate finance.",
            ],
        },
    },
    "akuntansi": {
        "prodi": "Akuntansi",
        "link": "akuntansi",
        "tagline": "Akuntan Islamic-preneur.",
        "deskripsi": "Berakar dari Prodi Akuntansi STIEM (sejak tahun 2000), pada 2019 resmi menjadi Prodi Akuntansi UMBandung. Telah meluluskan lebih dari 500 alumni yang tersebar di berbagai sektor: keuangan, audit, konsultan pajak, akuntan pendidik, hingga wirausaha.",
        "visi": "Menjadi Program Studi yang unggul di tingkat nasional dan internasional dalam bidang akuntansi berbasis teknopreneur berlandaskan nilai-nilai Islam untuk memberi manfaat nyata bagi masyarakat dan bangsa pada tahun 2045.",
        "misi": [
            "Menyelenggarakan pembelajaran akuntansi berbasis technopreneur dengan kurikulum terkini di era digital.",
            "Mengembangkan budaya meneliti bidang akuntansi berbasis technopreneur sebagai solusi masalah masyarakat.",
            "Mengembangkan pengabdian masyarakat yang searah dengan penelitian.",
            "Mengimplementasikan nilai-nilai Al-Islam dan Kemuhammadiyahan pada tridharma.",
        ],
        "tujuan": [
            "Menghasilkan lulusan kompeten dan berdaya saing di bidang akuntansi berbasis teknopreneur.",
            "Menghasilkan penelitian akuntansi berbasis teknopreneur sebagai solusi permasalahan masyarakat.",
            "Menghasilkan kontribusi nyata untuk masyarakat yang berkemajuan.",
            "Mengintegrasikan nilai Al-Islam dan Kemuhammadiyahan pada tridharma.",
        ],
        "extra": None,
    },
    "manajemen": {
        "prodi": "Manajemen",
        "link": "manajemen",
        "tagline": "Menghasilkan Sarjana Ekonomi yang kredibel dan berintegritas tinggi.",
        "deskripsi": "Prodi Manajemen FEB UMBandung mengembangkan manajemen bisnis dan technopreneurship berbasis nilai-nilai Islam, dengan kegiatan nyata seperti desa binaan, pendampingan UMKM dan koperasi syariah, serta MBKM.",
        "visi": "Menjadi Program Studi Manajemen yang unggul, berkontribusi dalam pengembangan Manajemen Bisnis dan technopreneurship berbasis nilai-nilai Islam di Asia Tenggara pada tahun 2045.",
        "misi": [
            "Menyelenggarakan pendidikan dan pembelajaran berkualitas di bidang manajemen bisnis berbasis technopreneurship.",
            "Menyelenggarakan penelitian yang berkontribusi terhadap pemecahan permasalahan ekonomi umat.",
            "Menyelenggarakan pengabdian berupa pembinaan, bimbingan, dan konsultasi bidang manajemen.",
            "Menjalin kerja sama dalam catur dharma berdasarkan nilai Al-Islam dan Kemuhammadiyahan.",
            "Mengelola program studi dengan prinsip tata kelola dan pelayanan yang baik.",
        ],
        "tujuan": [
            "Menghasilkan lulusan bidang ekonomi, bisnis, dan entrepreneurship yang mandiri, kompeten, dan berdaya saing global.",
            "Menghasilkan karya penelitian yang bermanfaat dan diakui secara nasional dan internasional.",
            "Menghasilkan kegiatan pengabdian yang dibutuhkan masyarakat.",
            "Menerapkan nilai Al-Islam dan Kemuhammadiyahan dalam tridharma.",
            "Memberikan pelayanan akademik terbaik kepada pemangku kepentingan.",
        ],
        "extra": None,
    },
    "pendidikan agama islam": {
        "prodi": "Pendidikan Agama Islam",
        "link": "pai",
        "tagline": "Melahirkan mahasiswa berakhlak mulia, unggul, dan berkemajuan.",
        "deskripsi": "Prodi PAI merupakan prodi pertama di STIT (berdiri 19 Juli 1987), kemudian STAIM Bandung, dan bergabung dengan UMBandung pada 2020. Meraih akreditasi Baik Sekali pada tahun 2022.",
        "visi": "Pengembangan pendidikan dan pembelajaran PAI untuk mendukung prodi unggul dan berkemajuan dalam menghasilkan lulusan profesional, edukatif, kritis, solutif, berakhlak mulia, dan edupreneurship pada tahun 2045.",
        "misi": [
            "Menyelenggarakan pendidikan agama Islam yang integratif antara nilai keislaman, IPTEK modern, dan jiwa kewirausahaan.",
            "Mengembangkan penelitian PAI yang inovatif dan aplikatif dengan teknologi.",
            "Mengimplementasikan pengabdian berbasis pemberdayaan dan penguatan nilai agama Islam.",
            "Menyelenggarakan pembinaan internalisasi nilai Al-Islam Kemuhammadiyahan.",
            "Membangun kemitraan strategis nasional dan internasional untuk technopreneurship bidang PAI.",
        ],
        "tujuan": [
            "Menghasilkan guru berkompetensi profesional, berakhlak mulia, kreatif, dan berjiwa technopreneur.",
            "Menghasilkan peneliti yang inovatif dalam pendidikan agama Islam dan teknologi pembelajaran.",
            "Menghasilkan konsultan bidang pendidikan Islam yang solutif.",
            "Menghasilkan edupreneur bidang pendidikan Islam.",
        ],
        "extra": None,
    },
    "pendidikan islam anak usia dini": {
        "prodi": "Pendidikan Islam Anak Usia Dini",
        "link": "piaud",
        "tagline": "Kreatif, Inovatif, Ceria.",
        "deskripsi": "Prodi PIAUD UMBandung mencetak pendidik anak usia dini yang profesional, kreatif, dan inovatif berbasis keislaman, siap bersaing di era digitalisasi.",
        "visi": "Menjadi Program Studi PIAUD yang unggul, profesional, dan berkemajuan pada tahun 2027.",
        "misi": [
            "Menyelenggarakan PIAUD yang berwawasan religiusitas keislaman dan adaptif dengan tantangan zaman.",
            "Meningkatkan kompetensi pembelajaran AUD Islam dengan penguatan kompetensi keguruan, manajerial, dan lifeskills berbasis entrepreneurship.",
            "Mengembangkan budaya akademik PIAUD yang berorientasi pada penelitian aplikatif.",
            "Membangun kemitraan pendidikan dengan masyarakat untuk kesadaran pendidikan Islam pada anak usia dini.",
        ],
        "tujuan": None,
        "extra": None,
    },
    "hukum keluarga islam": {
        "prodi": "Hukum Keluarga Islam",
        "link": "hukum_keluarga_islam",
        "tagline": "Unggul, berkarakter, dan berkemajuan dalam bidang Hukum Keluarga Islam tahun 2027.",
        "deskripsi": "Prodi Hukum Keluarga Islam (Ahwal Syakhsiyyah) menyiapkan sarjana hukum Islam yang profesional, berkarakter, dan berkemajuan, responsif terhadap masalah-masalah kontemporer hukum Islam.",
        "visi": "Terwujudnya prodi Hukum Keluarga Islam/AS yang unggul, berkarakter, dan berkemajuan di Jawa Barat tahun 2027 dengan lulusan kompeten dalam ilmu hukum Islam, didukung soft skill berbasis nilai keislaman dan technopreneurship.",
        "misi": [
            "Menyelenggarakan pendidikan hukum keluarga Islam yang bermutu dengan integrasi ilmu sosial dan sains kontemporer.",
            "Mengembangkan pengetahuan hukum keluarga Islam melalui pembelajaran terpadu dan riset berkelanjutan.",
            "Melatih keterampilan mahasiswa di pengelolaan lembaga hukum (Peradilan Agama, LBH, advokasi).",
            "Menyelenggarakan pengabdian berupa penyuluhan, advokasi, dan konsultasi hukum.",
            "Membina jaringan kerja sama strategis dengan berbagai lembaga.",
            "Menyebarluaskan hasil kajian keilmuan hukum keluarga Islam kepada masyarakat.",
            "Menyelenggarakan dakwah persyarikatan melalui implementasi Al-Islam dan Kemuhammadiyahan.",
        ],
        "tujuan": [
            "Menghasilkan lulusan profesional di bidang hukum Islam (Ahwal Syakhsiyyah).",
            "Menghasilkan konsep dan penelitian di bidang hukum Islam (Ahwal Syakhsiyyah).",
            "Menghasilkan lulusan yang cakap dalam bidang hukum Islam (Ahwal Syakhsiyyah).",
            "Memberikan kontribusi sosial dalam memajukan dan memberdayakan masyarakat di bidang hukum Islam.",
        ],
        "extra": None,
    },
    "komunikasi dan penyiaran islam": {
        "prodi": "Komunikasi dan Penyiaran Islam",
        "link": "kpi",
        "tagline": "Unggul, berkarakter, dan berkemajuan dalam bidang Komunikasi Penyiaran Islam tahun 2027.",
        "deskripsi": "Prodi Komunikasi Penyiaran Islam (KPI) menyiapkan sarjana jurnalis, broadcaster, dan mubaligh yang profesional, berkarakter, dan berkemajuan dalam dakwah pencerahan.",
        "visi": None,
        "misi": [
            "Menyelenggarakan pendidikan ilmu komunikasi dan penyiaran Islam yang berkualitas dan profesional.",
            "Mengembangkan penelitian di bidang komunikasi dan penyiaran Islam.",
            "Melatih keterampilan mahasiswa di bidang komunikasi dan penyiaran Islam.",
            "Menyebarluaskan dan memanfaatkan hasil kajian keilmuan KPI kepada masyarakat.",
        ],
        "tujuan": [
            "Menghasilkan lulusan profesional di bidang komunikasi dan penyiaran Islam.",
            "Menghasilkan penelitian di bidang Komunikasi dan Penyiaran Islam.",
            "Menghasilkan lulusan yang cakap dalam bidang pers, penyiaran, dan retorika.",
            "Mengembangkan konsep KPI untuk kemajuan dan pemberdayaan masyarakat.",
        ],
        "extra": None,
    },
    "ekonomi syariah": {
        "prodi": "Ekonomi Syariah",
        "link": "ekonomi_syariah",
        "tagline": None,
        "deskripsi": "Prodi Ekonomi Syariah UMBandung menyiapkan sarjana ekonomi syariah yang berkarakter dan berkemajuan, cakap mengelola lembaga keuangan syariah berbasis kecakapan technopreneurship.",
        "visi": "Menjadi program studi yang sangat baik dengan menghasilkan lulusan sarjana Ekonomi Syariah yang kompeten di Jawa Barat dalam penguasaan Ilmu Ekonomi Syariah, didukung soft skill berbasis nilai keislaman dan technopreneurship.",
        "misi": [
            "Menyelenggarakan pendidikan ekonomi syariah yang bermutu dan berkualitas.",
            "Mengembangkan pengetahuan ekonomi syariah melalui pembelajaran terpadu dan riset.",
            "Melatih keterampilan mahasiswa di bidang pengelolaan lembaga keuangan syariah.",
            "Menyebarluaskan hasil kajian keilmuan ekonomi syariah kepada masyarakat.",
        ],
        "tujuan": [
            "Menghasilkan lulusan profesional, berjiwa entrepreneur, dan berdaya saing di bidang ekonomi syariah.",
            "Menghasilkan konsep dan riset ekonomi syariah yang terpadu.",
            "Menghasilkan lulusan terampil dalam pengelolaan lembaga keuangan syariah.",
            "Memberikan kontribusi sosial dalam memajukan dan memberdayakan masyarakat.",
        ],
        "extra": None,
    },
    "farmasi": {
        "prodi": "Farmasi",
        "link": "prodi_farmasi",
        "tagline": "Pharmacy UMBandung: Growing Good and Educated Pharmacist.",
        "deskripsi": "Prodi Farmasi UMBandung (S-1) menyiapkan tenaga kefarmasian yang kompeten, kreatif, inovatif, dan berjiwa entrepreneur. Kurikulum dirancang dengan tiga kompetensi terintegrasi: keislaman, teknologi, dan entrepreneurship.",
        "visi": "Pada tahun 2022-2045 menjadi program studi farmasi yang unggul dengan menghasilkan lulusan sarjana bidang farmasi yang kompeten di negara berkembang Asia Tenggara, didukung soft skill berbasis nilai keislaman dan technopreneurship.",
        "misi": [
            "Menyelenggarakan pendidikan tinggi farmasi berkualitas berbasis sains, keislaman, dan technopreneurship.",
            "Menyelenggarakan penelitian berorientasi pada perkembangan sains farmasi, nilai keislaman, dan kemanfaatan bagi masyarakat.",
            "Melaksanakan pengabdian dan pemberdayaan masyarakat di bidang kefarmasian.",
            "Menyelenggarakan dakwah persyarikatan melalui implementasi Al-Islam dan Kemuhammadiyahan dalam tridharma.",
        ],
        "tujuan": None,
        "extra": {
            "Kurikulum (berbasis kompetensi)": [
                "Ilmu Farmasi Dasar (Kimia, Biologi, Fisika Farmasi).",
                "Farmakologi dan Toksikologi.",
                "Farmasetika dan Teknologi Sediaan.",
                "Farmasi Klinik dan Komunitas.",
                "Manajemen Farmasi dan Kewirausahaan.",
                "Nilai-nilai Keislaman dan Etika Profesi.",
            ],
            "Fasilitas": [
                "Laboratorium Kimia Farmasi, Biologi Farmasi, Farmasetika, dan Farmakologi.",
                "Apotek Pendidikan.",
                "Perpustakaan dengan koleksi referensi kefarmasian.",
            ],
        },
    },
    "profesi apoteker": {
        "prodi": "Profesi Apoteker",
        "link": "profesi_apoteker",
        "tagline": "Profesi Apoteker UMBandung: Mencetak apoteker profesional dan berakhlak.",
        "deskripsi": "Program Profesi Apoteker adalah pendidikan lanjutan setelah Sarjana Farmasi, dirancang dengan pendekatan Praktik Kerja Profesi Apoteker (PKPA) di berbagai institusi (rumah sakit, apotek, industri farmasi, dan lembaga pemerintahan).",
        "visi": "Menjadi program studi yang unggul dengan menghasilkan lulusan apoteker yang kompeten di Indonesia dalam penguasaan ilmu kefarmasian, didukung soft skill berbasis nilai keislaman dan jiwa technopreneurship.",
        "misi": [
            "Menyelenggarakan pendidikan tinggi farmasi yang berkualitas dan berbasis sains serta Islamic technopreneurship.",
            "Menyelenggarakan Praktek Kerja Profesi Apoteker (PKPA) yang berorientasi pada perkembangan sains, nilai keislaman, dan kemanfaatan bagi masyarakat.",
            "Melaksanakan pengabdian dan pemberdayaan masyarakat di bidang kefarmasian.",
            "Mengimplementasikan dakwah persyarikatan melalui Al-Islam dan Kemuhammadiyahan.",
        ],
        "tujuan": None,
        "extra": None,
    },
}


# --- 3b. Generator entri Knowledge Base untuk profil prodi ---
# Hanya menyusun data ke format KNOWLEDGE_BASE_ID (type "paragraph" berisi HTML);
# tidak mengubah logika pencarian di utils.py.
def _ul(items):
    return "<ul>" + "".join("<li>" + x + "</li>" for x in items) + "</ul>"


def _build_prodi_kb_entries(data):
    """Bangun entri "program studi <prodi>" lengkap dari PROFIL_PRODI_UMB."""
    entries = {}
    for prodi_key, p in data.items():
        parts = []
        if p.get("tagline"):
            parts.append("<em><strong>&ldquo;" + p["tagline"] + "&rdquo;</strong></em><br>")
        if p.get("deskripsi"):
            parts.append(p["deskripsi"] + "<br><br>")
        if p.get("visi"):
            parts.append("<strong>Visi:</strong> " + p["visi"] + "<br>")
        else:
            parts.append("<strong>Visi:</strong> <em>belum tersedia pada sumber (perlu verifikasi).</em><br>")
        if p.get("misi"):
            parts.append("<strong>Misi:</strong>" + _ul(p["misi"]))
        if p.get("tujuan"):
            parts.append("<strong>Tujuan:</strong>" + _ul(p["tujuan"]))
        if p.get("extra"):
            for label, items in p["extra"].items():
                parts.append("<strong>" + label + ":</strong>" + _ul(items))
        link = LINK_UMB.get(p["link"])
        if link:
            parts.append(
                "Selengkapnya: <a href='" + link + "' target='_blank' style='color:blue;'>"
                + p["prodi"] + " UMBandung</a>."
            )
        entries["program studi " + prodi_key] = {
            "type": "paragraph",
            "content": "".join(parts),
        }
    return entries


# Menimpa entri prodi ringkas lama (informatika/psikologi/manajemen/farmasi)
# dengan versi profil lengkap, sekaligus menambah 16 prodi lainnya.
KNOWLEDGE_BASE_ID.update(_build_prodi_kb_entries(PROFIL_PRODI_UMB))



# --- Alias prodi/fakultas/topik -> kunci KNOWLEDGE_BASE_ID ---
# Kunci  = istilah/singkatan yang mungkin diketik pengguna (mis. "fst", "informatika", "ukt").
# Nilai  = nama key di KNOWLEDGE_BASE_ID yang akan dikembalikan.
# Catatan: alias bermakna ganda/terlalu pendek (mis. "if"/"teknik"/"daftar" sendirian)
#          sengaja TIDAK dipakai agar tidak salah-cocok pada pencarian per-kata di utils.py.
ALIAS_KEYWORD_ID = {
    # Fakultas & singkatan
    "fst": "fakultas sains dan teknologi",
    "sains dan teknologi": "fakultas sains dan teknologi",
    "soshum": "fakultas sosial dan humaniora",
    "sosial humaniora": "fakultas sosial dan humaniora",
    "feb": "fakultas ekonomi dan bisnis",
    "ekonomi bisnis": "fakultas ekonomi dan bisnis",
    "fai": "fakultas agama islam",
    "agama islam": "fakultas agama islam",

    # Prodi -> entri prodi / fakultas terkait
    "informatika": "program studi informatika",
    "teknik informatika": "program studi informatika",
    "psikologi": "program studi psikologi",
    "manajemen": "program studi manajemen",
    "akuntansi": "fakultas ekonomi dan bisnis",
    "magister manajemen": "pascasarjana umbandung",
    "pascasarjana": "pascasarjana umbandung",
    "apoteker": "program studi farmasi",
    "profesi apoteker": "program studi farmasi",
    "teknik elektro": "fakultas sains dan teknologi",
    "teknik industri": "fakultas sains dan teknologi",
    "teknologi pangan": "fakultas sains dan teknologi",
    "bioteknologi": "fakultas sains dan teknologi",
    "agribisnis": "fakultas sains dan teknologi",
    "ilmu komunikasi": "fakultas sosial dan humaniora",
    "kriya": "fakultas sosial dan humaniora",
    "administrasi publik": "fakultas sosial dan humaniora",
    "pai": "fakultas agama islam",
    "piaud": "fakultas agama islam",
    "hukum keluarga islam": "fakultas agama islam",
    "kpi": "fakultas agama islam",
    "ekonomi syariah": "fakultas agama islam",

    # Kata umum prodi/fakultas (longest-match menjaga istilah spesifik tetap menang)
    "prodi": "program studi umbandung",
    "program studi": "program studi umbandung",
    "jurusan": "program studi umbandung",
    "fakultas": "fakultas umbandung",
    # Topik umum -> entri terkait
    "ukt": "biaya kuliah umbandung",
    "biaya": "biaya kuliah umbandung",
    "pmb": "pmb umbandung",
    "jalur pendaftaran": "jalur pendaftaran umbandung",
    "jalur": "jalur pendaftaran umbandung",
    "pendaftaran": "cara daftar pmb umbandung",
    "beasiswa": "beasiswa umbandung",
    "kip": "kip kuliah umbandung",
    "kader muhammadiyah": "beasiswa kader muhammadiyah",
    "beasiswa kader": "beasiswa kader muhammadiyah",
    "perpustakaan": "perpustakaan umbandung",
    "perpus": "perpustakaan umbandung",
    "mentari": "portal akademik umbandung",
    "krs": "krs umbandung",
    "baak": "baak umbandung",
    "wisuda": "wisuda umbandung",
    "skripsi": "skripsi umbandung",
    "karier": "karier umbandung",
    "lowongan": "karier umbandung",
    "berita": "berita umbandung",
    "kabar": "berita umbandung",
    "kontak": "kontak umbandung",
    "alamat": "alamat kampus umbandung",
    "rektor": "rektor umbandung",
    "akreditasi": "akreditasi umbandung",
    "sejarah": "sejarah umbandung",
    "visi": "visi misi",
    "misi": "visi misi",
    "logo": "logo umbandung",
    "muhammadiyah": "afiliasi muhammadiyah",
    "fasilitas": "fasilitas umbandung",
    "kemahasiswaan": "kemahasiswaan umbandung",
    "ukm": "kemahasiswaan umbandung",

    # Dosen (fallback bila pencocokan semua-kata tak menemukan kunci spesifik;
    #        alias terpanjang menang, jadi "dosen pai" mengalahkan "pai")
    "dosen": "dosen umbandung",
    "daftar dosen": "dosen umbandung",
    "dosen kriya": "dosen kriya tekstil dan fashion",
    "dosen pai": "dosen pendidikan agama islam",
    "dosen piaud": "dosen pendidikan islam anak usia dini",
    "dosen kpi": "dosen komunikasi dan penyiaran islam",
    "dosen apoteker": "dosen profesi apoteker",

    # --- Override: nama prodi diarahkan ke entri profil lengkap ---
    "teknik elektro": "program studi teknik elektro",
    "informatika": "program studi informatika",
    "teknik informatika": "program studi informatika",
    "teknik industri": "program studi teknik industri",
    "teknologi pangan": "program studi teknologi pangan",
    "bioteknologi": "program studi bioteknologi",
    "agribisnis": "program studi agribisnis",
    "ilmu komunikasi": "program studi ilmu komunikasi",
    "psikologi": "program studi psikologi",
    "kriya": "program studi kriya tekstil dan fashion",
    "kriya tekstil dan fashion": "program studi kriya tekstil dan fashion",
    "administrasi publik": "program studi administrasi publik",
    "magister manajemen": "program studi magister manajemen",
    "akuntansi": "program studi akuntansi",
    "manajemen": "program studi manajemen",
    "pendidikan agama islam": "program studi pendidikan agama islam",
    "pai": "program studi pendidikan agama islam",
    "pendidikan islam anak usia dini": "program studi pendidikan islam anak usia dini",
    "piaud": "program studi pendidikan islam anak usia dini",
    "hukum keluarga islam": "program studi hukum keluarga islam",
    "komunikasi dan penyiaran islam": "program studi komunikasi dan penyiaran islam",
    "kpi": "program studi komunikasi dan penyiaran islam",
    "ekonomi syariah": "program studi ekonomi syariah",
    "farmasi": "program studi farmasi",
    "apoteker": "program studi profesi apoteker",
    "profesi apoteker": "program studi profesi apoteker",

    # --- Topik umum baru ---
    "keunggulan": "keunggulan umbandung",
    "tujuan": "tujuan umbandung",
    "tujuan umbandung": "tujuan umbandung",
    "laboratorium": "laboratorium umbandung",
    "lab": "laboratorium umbandung",
    "sambutan rektor": "sambutan rektor umbandung",
    "sambutan": "sambutan rektor umbandung",

    # Layanan akademik
    "cuti": "cuti akademik umbandung",
    "cuti kuliah": "cuti akademik umbandung",
    "cuti akademik": "cuti akademik umbandung",

    # Kalender akademik
    "kalender akademik": "kalender akademik umbandung",
    "kalender": "kalender akademik umbandung",
    "kalender perkuliahan": "kalender akademik umbandung",
    "jadwal akademik": "kalender akademik umbandung",
    "jadwal kuliah": "kalender akademik umbandung",
    "jadwal perkuliahan": "kalender akademik umbandung",
    "jadwal uts": "kalender akademik umbandung",
    "jadwal uas": "kalender akademik umbandung",

    # Kontak layanan per unit
    "kontak layanan": "kontak layanan umbandung",
    "kontak unit": "kontak layanan umbandung",
    "nomor unit": "kontak layanan umbandung",
    "kontak kemahasiswaan": "kontak layanan umbandung",
    "kontak keuangan": "kontak layanan umbandung",
    "kontak akademik": "kontak layanan umbandung",
    "kontak perpustakaan": "kontak layanan umbandung",
    "kontak lppaik": "kontak layanan umbandung",
    "lppaik": "kontak layanan umbandung",
    "kontak sistem informasi": "kontak layanan umbandung",
    "kontak parkir": "kontak layanan umbandung",
    "kontak security": "kontak layanan umbandung",
    "nomor wa": "kontak layanan umbandung",
    "nomor whatsapp": "kontak layanan umbandung",
}


AUTOCOMPLETE_TERMS_ID = [
    # PMB & Biaya
    "Cara daftar PMB Universitas Muhammadiyah Bandung",
    "Jalur masuk UMBandung",
    "Jalur KIP-Kuliah UMBandung",
    "Syarat pendaftaran UMBandung",
    "Jadwal PMB UMBandung",
    "Biaya kuliah UMBandung",
    "Berapa UKT UMBandung?",
    # Beasiswa
    "Beasiswa UMBandung",
    "Beasiswa Kader Muhammadiyah UMBandung",
    "Beasiswa Hafizh Quran UMBandung",
    "KIP Kuliah UMBandung",
    # Prodi & Fakultas
    "Program studi UMBandung",
    "Fakultas UMBandung",
    "Prodi Informatika UMBandung",
    "Magister Manajemen UMBandung",
    "Akreditasi UMBandung",
    # Profil
    "Visi misi UMBandung",
    "Sejarah UMBandung",
    "Rektor UMBandung",
    "Profil UMBandung",
    "Tahun berdiri UMBandung",
    # Kontak & Lokasi
    "Alamat kampus UMBandung",
    "Nomor telepon UMBandung",
    "Lokasi kampus UMBandung",
    "Media sosial UMBandung",
    # Akademik & Layanan
    "Jadwal wisuda UMBandung",
    "Syarat skripsi UMBandung",
    "KRS UMBandung",
    "Portal akademik UMBandung",
    "BAAK UMBandung",
    "Kalender akademik UMBandung",
    "Jadwal UTS UAS UMBandung",
    "Kontak layanan UMBandung",
    "Nomor WhatsApp unit UMBandung",
    "Surat keterangan aktif UMBandung",
    "Transkrip nilai UMBandung",
    # Fasilitas
    "Perpustakaan UMBandung",
    "Fasilitas UMBandung",
    # Kemahasiswaan
    "UKM UMBandung",
    "IMM UMBandung",
    "KKN UMBandung",
    "MBKM UMBandung",
    # Karier
    "Lowongan kerja UMBandung",
    "Karier dosen UMBandung",
    # Dosen & Tenaga Pendidik
    "Daftar dosen UMBandung",
    "Dosen Informatika UMBandung",
    "Dosen Psikologi UMBandung",
    "Dosen Farmasi UMBandung",
    "Dosen Manajemen UMBandung",
    "Dosen Teknik Elektro UMBandung",
    # Profil & Keunggulan
    "Keunggulan UMBandung",
    "Tujuan UMBandung",
    "Profil Program Studi Informatika UMBandung",
    "Visi misi Teknik Elektro UMBandung",
    "Laboratorium UMBandung",
    "Sambutan Rektor UMBandung",
]


FOLLOW_UP_SUGGESTIONS_ID = {
    "pmb": {
        "message": "Tentu, terkait PMB UMBandung, informasi apa yang Anda butuhkan?",
        "suggestions": [
            "Cara daftar PMB UMBandung",
            "Apa saja jalur pendaftaran UMBandung?",
            "Berapa biaya kuliah UMBandung?",
        ]
    },
    "biaya": {
        "message": "Terkait biaya kuliah, berikut beberapa hal yang mungkin Anda cari:",
        "suggestions": [
            "Biaya kuliah UMBandung",
            "Beasiswa UMBandung",
            "Jalur KIP-Kuliah UMBandung",
        ]
    },
    "beasiswa": {
        "message": "UMBandung menyediakan beberapa beasiswa. Mana yang ingin Anda ketahui?",
        "suggestions": [
            "Beasiswa Kader Muhammadiyah",
            "Beasiswa Prestasi Akademik",
            "KIP Kuliah UMBandung",
        ]
    },
    "kip": {
        "message": "Terkait KIP-Kuliah di UMBandung:",
        "suggestions": [
            "Syarat KIP Kuliah UMBandung",
            "Cara daftar KIP Kuliah UMBandung",
            "Beasiswa UMBandung lainnya",
        ]
    },
    "prodi": {
        "message": "Terkait program studi UMBandung, apa yang ingin Anda lihat?",
        "suggestions": [
            "Daftar program studi UMBandung",
            "Fakultas UMBandung",
            "Akreditasi UMBandung",
        ]
    },
    "fakultas": {
        "message": "UMBandung memiliki lima fakultas. Mana yang ingin Anda ketahui?",
        "suggestions": [
            "Fakultas Sains dan Teknologi",
            "Fakultas Ekonomi dan Bisnis",
            "Fakultas Agama Islam",
        ]
    },
    "akademik": {
        "message": "Untuk layanan akademik, apa yang Anda butuhkan?",
        "suggestions": [
            "Kalender akademik UMBandung",
            "Cara isi KRS UMBandung",
            "Syarat wisuda UMBandung",
            "Layanan BAAK UMBandung",
        ]
    },
    "wisuda": {
        "message": "Terkait wisuda, berikut yang biasanya ditanyakan:",
        "suggestions": [
            "Syarat skripsi UMBandung",
            "Syarat wisuda UMBandung",
            "Layanan BAAK UMBandung",
        ]
    },
    "fasilitas": {
        "message": "Terkait fasilitas kampus, apa yang ingin Anda ketahui?",
        "suggestions": [
            "Perpustakaan UMBandung",
            "Fasilitas UMBandung",
            "UKM UMBandung",
        ]
    },
    "kontak": {
        "message": "Untuk menghubungi UMBandung, berikut beberapa opsi:",
        "suggestions": [
            "Kontak layanan UMBandung",
            "Alamat kampus UMBandung",
            "Nomor telepon UMBandung",
            "Media sosial UMBandung",
        ]
    },
    "profil": {
        "message": "Terkait profil UMBandung, apa yang ingin Anda ketahui?",
        "suggestions": [
            "Sejarah UMBandung",
            "Visi misi UMBandung",
            "Keunggulan UMBandung",
            "Tujuan UMBandung",
            "Rektor UMBandung",
        ]
    },
    "karier": {
        "message": "Terkait karier/lowongan di UMBandung:",
        "suggestions": [
            "Karier dosen UMBandung",
            "Lowongan tenaga kependidikan UMBandung",
        ]
    },
    "dosen": {
        "message": "Mau melihat daftar dosen dari program studi mana?",
        "suggestions": [
            "Dosen Informatika UMBandung",
            "Dosen Psikologi UMBandung",
            "Dosen Farmasi UMBandung",
        ]
    },
}