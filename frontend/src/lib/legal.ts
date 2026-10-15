// Content for /syarat-ketentuan and /kebijakan-privasi.
// Plain data so the copy can be reviewed (and later moved to the CMS) without touching the layout.

export type LegalSection = { id: string; title: string; body: (string | string[])[] };
export type LegalDoc = {
  slug: string;
  title: string;
  lead: string;
  mono: string;
  updated: string;
  intro: string;
  summary: [string, string][];
  sections: LegalSection[];
};

export const LEGAL_UPDATED = "15 Oktober 2026";

export const terms: LegalDoc = {
  slug: "syarat-ketentuan",
  title: "Syarat & Ketentuan",
  lead: "Syarat &",
  mono: "ketentuan.",
  updated: LEGAL_UPDATED,
  intro: "Syarat ini mengatur penggunaan Rawuh, layanan untuk membuat dan membagikan undangan digital. Dengan membuat akun atau memakai layanan kami, kamu menyetujui syarat di bawah ini.",
  summary: [
    ["Undanganmu, kontenmu", "Foto, teks, dan musik yang kamu unggah tetap milikmu. Pastikan kamu berhak memakainya."],
    ["Sekali bayar", "Paket berbayar aktif sesuai masa berlakunya, tanpa langganan otomatis."],
    ["Pakai dengan baik", "Undangan tidak boleh berisi konten yang melanggar hukum atau merugikan orang lain."],
  ],
  sections: [
    {
      id: "layanan",
      title: "Tentang layanan",
      body: [
        "Rawuh menyediakan platform untuk membuat undangan digital berbentuk website, termasuk fitur pengelolaan tamu, RSVP, buku ucapan, galeri, musik latar, amplop digital, dan QR check-in.",
        "Kami dapat menambah, mengubah, atau menghentikan fitur tertentu untuk meningkatkan layanan. Jika perubahan berdampak besar pada paket yang sudah kamu bayar, kami akan memberi tahu lebih dulu.",
      ],
    },
    {
      id: "akun",
      title: "Akun",
      body: [
        "Kamu perlu membuat akun dengan data yang benar untuk memakai dashboard Rawuh. Kamu bertanggung jawab menjaga kerahasiaan kata sandi dan atas semua aktivitas di akunmu.",
        "Segera hubungi kami jika kamu menduga akunmu dipakai tanpa izin.",
      ],
    },
    {
      id: "konten",
      title: "Konten undangan",
      body: [
        "Semua konten yang kamu unggah, seperti nama, foto, cerita, lokasi, dan musik, tetap menjadi milikmu. Kamu memberi Rawuh izin terbatas untuk menyimpan dan menampilkan konten tersebut semata-mata agar undanganmu bisa diakses oleh tamu.",
        "Kamu menjamin bahwa kamu berhak memakai konten tersebut, termasuk hak cipta atas musik dan foto, serta izin dari orang yang wajahnya tampil di foto.",
        "Kamu tidak boleh memakai Rawuh untuk:",
        [
          "konten yang melanggar hukum, mengandung SARA, kekerasan, pornografi, atau ujaran kebencian;",
          "penipuan, termasuk undangan palsu untuk meminta transfer uang;",
          "mengirim pesan massal yang tidak diinginkan (spam);",
          "melanggar hak cipta, merek, atau privasi pihak lain.",
        ],
        "Kami berhak menurunkan undangan atau menangguhkan akun yang melanggar ketentuan ini, dengan atau tanpa pemberitahuan sebelumnya bila pelanggarannya serius.",
      ],
    },
    {
      id: "tema",
      title: "Tema & desain",
      body: [
        "Tema, ilustrasi, kode, dan desain Rawuh adalah milik Rawuh atau pemberi lisensinya. Kamu boleh memakainya untuk undanganmu sendiri, tetapi tidak boleh menyalin, menjual ulang, atau mendistribusikan tema di luar Rawuh.",
        "Beberapa tema terinspirasi gaya aplikasi populer secara parodi. Tema tersebut tidak berafiliasi dengan, dan tidak didukung oleh, pemilik merek aslinya.",
      ],
    },
    {
      id: "pembayaran",
      title: "Paket & pembayaran",
      body: [
        "Harga paket tercantum di halaman Harga dan dapat berubah sewaktu-waktu. Perubahan harga tidak berlaku untuk paket yang sudah kamu bayar.",
        "Pembayaran diproses oleh mitra pembayaran resmi (misalnya QRIS, virtual account, dan e-wallet). Rawuh tidak menyimpan data kartu atau PIN pembayaranmu.",
        "Paket berbayar aktif selama masa berlaku yang tertera saat pembelian dan tidak diperpanjang otomatis.",
      ],
    },
    {
      id: "pengembalian-dana",
      title: "Pengembalian dana",
      body: [
        "Jika undangan tidak bisa diakses karena kesalahan di sisi Rawuh dan tidak dapat kami perbaiki dalam waktu wajar, kamu dapat mengajukan pengembalian dana penuh.",
        "Pengajuan lain, misalnya karena berubah pikiran, kami tinjau per kasus selama undangan belum dibagikan ke tamu. Hubungi tim kami melalui WhatsApp dengan menyertakan bukti pembayaran.",
      ],
    },
    {
      id: "amplop-digital",
      title: "Amplop digital",
      body: [
        "Fitur amplop digital menampilkan informasi rekening, e-wallet, atau QRIS yang kamu masukkan sendiri. Transfer dari tamu masuk langsung ke rekening atau dompet tersebut, bukan melalui Rawuh.",
        "Rawuh tidak bertanggung jawab atas kesalahan nomor rekening yang kamu masukkan atau atas transaksi antara kamu dan tamu.",
      ],
    },
    {
      id: "ketersediaan",
      title: "Ketersediaan & tanggung jawab",
      body: [
        "Kami berusaha menjaga undanganmu tetap dapat diakses, tetapi layanan disediakan “sebagaimana adanya”. Gangguan dapat terjadi karena pemeliharaan, jaringan, atau hal di luar kendali kami.",
        "Sepanjang diizinkan hukum, tanggung jawab Rawuh atas kerugian yang timbul dari penggunaan layanan terbatas pada jumlah yang kamu bayarkan untuk undangan terkait.",
      ],
    },
    {
      id: "penghentian",
      title: "Menghapus akun",
      body: [
        "Kamu dapat berhenti memakai Rawuh dan meminta penghapusan akun kapan saja. Setelah dihapus, undangan dan data tamu tidak lagi dapat diakses dan tidak dapat dipulihkan.",
      ],
    },
    {
      id: "hukum",
      title: "Hukum yang berlaku",
      body: [
        "Syarat ini tunduk pada hukum Republik Indonesia. Kami mengutamakan penyelesaian secara musyawarah; jika tidak tercapai, sengketa diselesaikan melalui pengadilan yang berwenang di Indonesia.",
        "Kami dapat memperbarui syarat ini. Tanggal pembaruan terakhir selalu tercantum di bagian atas halaman, dan perubahan penting akan kami beritahukan melalui email atau dashboard.",
      ],
    },
  ],
};

export const privacy: LegalDoc = {
  slug: "kebijakan-privasi",
  title: "Kebijakan Privasi",
  lead: "Kebijakan",
  mono: "privasi.",
  updated: LEGAL_UPDATED,
  intro: "Undangan menyimpan data orang-orang terdekatmu. Kebijakan ini menjelaskan data apa yang kami kumpulkan, untuk apa, dan bagaimana kamu mengendalikannya, sejalan dengan UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi.",
  summary: [
    ["Tidak dijual", "Kami tidak menjual data kamu maupun data tamumu ke siapa pun."],
    ["Secukupnya", "Kami hanya mengumpulkan data yang diperlukan agar undangan berjalan."],
    ["Kamu yang pegang kendali", "Data bisa diakses, diperbaiki, atau dihapus kapan saja."],
  ],
  sections: [
    {
      id: "data-yang-dikumpulkan",
      title: "Data yang kami kumpulkan",
      body: [
        "Dari pemilik akun:",
        [
          "nama, email, nomor WhatsApp, dan kata sandi (disimpan dalam bentuk terenkripsi);",
          "isi undangan: nama mempelai, orang tua, tanggal dan lokasi acara, cerita, foto, dan musik;",
          "informasi amplop digital yang kamu masukkan, seperti nama bank dan nomor rekening;",
          "riwayat transaksi paket (tanpa data kartu atau PIN).",
        ],
        "Dari tamu undangan:",
        [
          "nama dan nomor telepon yang kamu masukkan ke daftar tamu;",
          "jawaban RSVP, jumlah tamu, ucapan, dan waktu check-in.",
        ],
        "Secara otomatis: alamat IP, jenis perangkat dan browser, serta halaman yang dibuka, untuk keamanan dan statistik kunjungan undangan.",
      ],
    },
    {
      id: "penggunaan",
      title: "Cara kami memakai data",
      body: [
        [
          "menampilkan undangan kepada tamu yang kamu undang;",
          "menyajikan RSVP, ucapan, dan statistik kehadiran di dashboard-mu;",
          "memproses pembayaran dan mengirim bukti transaksi;",
          "memberikan bantuan pelanggan dan pemberitahuan penting tentang akunmu;",
          "mencegah penyalahgunaan dan menjaga keamanan layanan.",
        ],
        "Kami tidak memakai data tamumu untuk iklan dan tidak menghubungi tamumu untuk kepentingan pemasaran Rawuh.",
      ],
    },
    {
      id: "tanggung-jawab-pemilik",
      title: "Data tamu adalah tanggung jawab bersama",
      body: [
        "Saat kamu memasukkan nama dan nomor tamu, kamu bertindak sebagai pengendali data tersebut dan Rawuh memprosesnya atas namamu. Pastikan kamu memakai data tamu hanya untuk keperluan acara.",
      ],
    },
    {
      id: "berbagi",
      title: "Dengan siapa data dibagikan",
      body: [
        "Kami hanya berbagi data dengan pihak yang membantu menjalankan layanan, dan hanya sebatas yang diperlukan:",
        [
          "penyedia server dan penyimpanan file untuk menyimpan undangan dan foto;",
          "mitra pembayaran untuk memproses transaksi paket;",
          "penyedia email dan pesan untuk notifikasi akun.",
        ],
        "Kami juga dapat membuka data jika diwajibkan oleh hukum atau permintaan resmi aparat yang berwenang.",
      ],
    },
    {
      id: "visibilitas",
      title: "Siapa yang bisa melihat undanganmu",
      body: [
        "Undangan yang sudah diterbitkan dapat dibuka oleh siapa saja yang memiliki tautannya. Daftar tamu, nomor telepon, dan jawaban RSVP tidak pernah ditampilkan di halaman undangan; ucapan hanya tampil jika kamu menyetujuinya.",
        "Kamu bisa menyembunyikan undangan kapan saja dengan membatalkan penerbitannya dari dashboard.",
      ],
    },
    {
      id: "penyimpanan",
      title: "Lama penyimpanan",
      body: [
        "Data undangan kami simpan selama akunmu aktif. Undangan dan data tamu dapat kamu hapus sendiri dari dashboard; setelah dihapus, data dihapus dari sistem utama dan cadangan dalam waktu paling lama 30 hari.",
        "Catatan transaksi kami simpan lebih lama bila diwajibkan oleh ketentuan perpajakan dan akuntansi.",
      ],
    },
    {
      id: "keamanan",
      title: "Keamanan",
      body: [
        "Koneksi ke Rawuh dienkripsi (HTTPS), kata sandi disimpan dengan hashing, dan akses internal ke data dibatasi hanya untuk tim yang membutuhkannya. Jika terjadi insiden yang memengaruhi datamu, kami akan memberi tahu sesuai ketentuan hukum yang berlaku.",
      ],
    },
    {
      id: "hak-kamu",
      title: "Hak kamu",
      body: [
        "Sesuai UU Pelindungan Data Pribadi, kamu berhak untuk:",
        [
          "mengakses dan mendapatkan salinan data pribadimu;",
          "memperbaiki data yang tidak akurat;",
          "meminta penghapusan data dan akun;",
          "menarik persetujuan pemrosesan data.",
        ],
        "Tamu yang ingin datanya dihapus dari sebuah undangan dapat menghubungi pemilik undangan atau tim Rawuh.",
      ],
    },
    {
      id: "cookie",
      title: "Cookie & penyimpanan lokal",
      body: [
        "Kami memakai penyimpanan lokal di browser untuk menjaga sesi masuk dan mengingat preferensi tampilan. Kami tidak memakai cookie iklan pihak ketiga.",
      ],
    },
    {
      id: "anak",
      title: "Anak-anak",
      body: [
        "Akun Rawuh ditujukan untuk pengguna berusia 17 tahun ke atas. Undangan acara anak, seperti aqiqah, khitan, atau ulang tahun, dibuat dan dikelola oleh orang tua atau wali.",
      ],
    },
    {
      id: "perubahan",
      title: "Perubahan kebijakan",
      body: [
        "Kebijakan ini dapat kami perbarui. Tanggal pembaruan terakhir tercantum di bagian atas halaman, dan perubahan penting akan kami beritahukan melalui email atau dashboard.",
      ],
    },
  ],
};
