package db

// Theme catalog copy in Indonesian (descriptions + category labels). Only rows still carrying the
// original copy are changed, so descriptions edited by an admin are kept.
const Schema024 = `
UPDATE templates SET description = 'Adat Minang merah-emas dengan motif songket dan siluet rumah gadang.' WHERE id = 'rumah-gadang' AND description = 'Adat Minang · Merah · Songket';
UPDATE templates SET description = 'Adat Bali kuning keemasan dengan bunga kamboja dan gapura candi bentar.' WHERE id = 'bali-kuning' AND description = 'Adat Bali · Kuning · Kamboja';
UPDATE templates SET description = 'Syari hijau zamrud tanpa foto, berisi doa dan ornamen geometris.' WHERE id = 'syari-zamrud' AND description = 'Syari · Tanpa Foto · Hijau';
UPDATE templates SET description = 'Cat air ungu lembut dengan ilustrasi bunga dan polaroid.' WHERE id = 'lavender-air' AND description = 'Watercolor · Ungu · Ilustrasi';
UPDATE templates SET description = 'Minimalis putih bersih yang mengandalkan tipografi.' WHERE id = 'linen-putih' AND description = 'Minimalist · Putih · Tipografi';
UPDATE templates SET description = 'Gambar tangan di kertas krem, gaya buku tempel dengan coretan tinta.' WHERE id = 'sketsa-tangan' AND description = 'Hand Drawn · Cream · Line Art';
UPDATE templates SET description = 'Elegan hitam-emas dengan dedaunan dan kunang-kunang.' WHERE id = 'malam-rimba' AND description = 'Elegant · Hitam · Botanical';
UPDATE templates SET description = 'Ilustrasi datar pastel merah muda yang lucu dan ceria.' WHERE id = 'pastel-flat' AND description = 'Flat · Pink · Ilustrasi Lucu';
UPDATE templates SET description = 'Ala aplikasi ojek online: rute cinta, perjalanan, dan bintang untuk pengantin.' WHERE id = 'hijau-ojek' AND description = 'Undangan bergaya Hijau Ojek yang unik dan personal.';
UPDATE templates SET description = 'Ala aplikasi pesan-antar: menu acara, status pengiriman, dan voucher.' WHERE id = 'pesan-antar' AND description = 'Undangan bergaya Pesan-Antar yang unik dan personal.';
UPDATE templates SET description = 'Ala gim arena: pilih hero, rank pasangan, dan toko item hadiah.' WHERE id = 'arena-legenda' AND description = 'Undangan bergaya Arena Legenda yang unik dan personal.';
UPDATE templates SET description = 'Ala kanal video: episode kisah, tayangan premiere, dan kolom komentar.' WHERE id = 'kanal-video' AND description = 'Undangan bergaya Video yang unik dan personal.';
UPDATE templates SET description = 'Ala repositori kode: riwayat commit, kontribusi, dan diskusi.' WHERE id = 'repositori' AND description = 'Undangan bergaya Repositori yang unik dan personal.';
UPDATE templates SET description = 'Ala pemutar musik: daftar lagu acara, artis, dan pemutar mini.' WHERE id = 'pemutar-musik' AND description = 'Undangan bergaya Musik yang unik dan personal.';
UPDATE templates SET description = 'Ala playlist: antrean acara, kilas balik tahunan, dan pemutar mini.' WHERE id = 'playlist' AND description = 'Undangan bergaya Playlist yang unik dan personal.';
UPDATE templates SET description = 'Ala aplikasi chat: obrolan berdua, grup keluarga, dan ucapan tamu.' WHERE id = 'chat-hijau' AND description = 'Undangan bergaya Chat Hijau yang unik dan personal.';
UPDATE templates SET description = 'Ala feed foto: sorotan cerita, unggahan galeri, dan suka dari tamu.' WHERE id = 'feed-foto' AND description = 'Undangan bergaya Feed Foto yang unik dan personal.';
UPDATE templates SET description = 'Ala video vertikal: siaran premiere, hadiah, dan komentar tamu.' WHERE id = 'video-vertikal' AND description = 'Undangan bergaya Video Vertikal yang unik dan personal.';
UPDATE templates SET description = 'Ala aplikasi kencan: profil berdua, match, dan riwayat obrolan.' WHERE id = 'kencan' AND description = 'Undangan bergaya Kencan yang unik dan personal.';
UPDATE templates SET description = 'Ala aplikasi peta: titik lokasi, rute perjalanan, dan ulasan tamu.' WHERE id = 'peta-rute' AND description = 'Undangan bergaya Peta yang unik dan personal.';
UPDATE templates SET description = 'Ala kotak masuk surel: undangan sebagai email lengkap dengan lampiran.' WHERE id = 'surel' AND description = 'Undangan bergaya Surel yang unik dan personal.';
UPDATE templates SET description = 'Ala halaman dokumen: properti acara, daftar periksa, dan komentar.' WHERE id = 'dokumen' AND description = 'Undangan bergaya Dokumen yang unik dan personal.';
UPDATE templates SET description = 'Ala rapat video: ubin peserta, agenda, dan obrolan rapat.' WHERE id = 'rapat-video' AND description = 'Undangan bergaya Rapat Video yang unik dan personal.';
UPDATE templates SET description = 'Ala boarding pass: penerbangan cinta, gerbang, dan barcode tamu.' WHERE id = 'boarding-pass' AND description = 'Undangan bergaya Boarding Pass yang unik dan personal.';
UPDATE templates SET description = 'Ala tiket kereta: rute perjalanan, stasiun, dan jadwal keberangkatan.' WHERE id = 'tiket-kereta' AND description = 'Undangan bergaya Tiket Kereta yang unik dan personal.';
UPDATE templates SET description = 'Ala gim retro piksel: karakter, level, dan toko item.' WHERE id = 'game-retro' AND description = 'Undangan bergaya Game Retro yang unik dan personal.';
UPDATE templates SET description = 'Ala koran klasik: berita utama, kolom acara, dan iklan baris.' WHERE id = 'koran' AND description = 'Undangan bergaya Koran yang unik dan personal.';
UPDATE templates SET description = 'Ala dompet digital: saldo cinta, riwayat transaksi, dan struk.' WHERE id = 'dompet-digital' AND description = 'Undangan bergaya Dompet Digital yang unik dan personal.';
UPDATE templates SET description = 'Ala aplikasi bank: PIN masuk, transfer kasih, dan mutasi.' WHERE id = 'saku-biru' AND description = 'Undangan bergaya Saku Biru yang unik dan personal.';
UPDATE templates SET description = 'Ala aplikasi poin: misi, tukar poin, dan tingkat keanggotaan.' WHERE id = 'poin-ungu' AND description = 'Undangan bergaya Poin Ungu yang unik dan personal.';
UPDATE templates SET description = 'Ala kantong tabungan: target bersama, isi kantong, dan anggota.' WHERE id = 'kantong-oranye' AND description = 'Undangan bergaya Kantong Oranye yang unik dan personal.';
UPDATE templates SET description = 'Ala pemesanan kursi kereta: denah gerbong dan tiket tamu.' WHERE id = 'kursi-kereta' AND description = 'Undangan bergaya Kursi Kereta yang unik dan personal.';
UPDATE templates SET description = 'Ala paket liburan: rencana perjalanan, pesanan, dan voucher.' WHERE id = 'paket-liburan' AND description = 'Undangan bergaya Paket Liburan yang unik dan personal.';
UPDATE templates SET description = 'Ala aplikasi perjalanan: itinerary harian, penginapan, dan peta.' WHERE id = 'rencana-perjalanan' AND description = 'Undangan bergaya Rencana Perjalanan yang unik dan personal.';
UPDATE templates SET description = 'Undangan bergaya aplikasi belanja: paket cinta, lacak perjalanan, dan ulasan tamu.' WHERE id = 'marketplace' AND description = 'jawa';
UPDATE templates SET category = 'Gambar Tangan' WHERE category = 'Hand Drawn';
UPDATE templates SET category = 'Cat Air' WHERE category = 'Watercolor';
UPDATE templates SET category = 'Keuangan' WHERE category = 'Fintech';
`
