import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Gerakan Tangan Hangat", groom: "Karang Taruna Sukamaju",
    brideFull: "Perkumpulan Gerakan Tangan Hangat", groomFull: "Karang Taruna RW 05 Sukamaju",
    brideParents: "Komunitas relawan lintas profesi di Cimahi sejak 2016. Rutin mengadakan donor darah, posyandu lansia, dan dapur umum.",
    groomParents: "Pemuda-pemudi RW 05 yang menyiapkan tempat, tenda, dan konsumsi, serta mengantar paket sembako ke rumah warga.",
    note: "Satu kantong darah bisa menolong hingga tiga orang. Satu paket sembako bisa meringankan satu keluarga.",
  },
  eventLabel: "Bakti Sosial & Donor Darah",
  date: "2027-09-12T07:30:00+07:00",
  place: "Balai Warga RW 05 Sukamaju",
  address: "Jl. Sukamaju Raya No. 21, Cigugur Tengah, Cimahi Tengah, Kota Cimahi, Jawa Barat",
  story: { title: "Program hari itu", body: "" },
  stories: [
    { date: "07.30", title: "Registrasi & Skrining", body: "Peserta mendaftar, mengisi formulir, lalu diperiksa tekanan darah dan kadar hemoglobin oleh petugas kesehatan." },
    { date: "08.00", title: "Donor Darah", body: "Bersama petugas unit donor darah setempat. Target kami 120 kantong untuk persediaan rumah sakit di Cimahi." },
    { date: "08.30", title: "Cek Kesehatan Gratis", body: "Cek gula darah, kolesterol, dan konsultasi dokter umum untuk warga lansia dan keluarga." },
    { date: "13.00", title: "Pembagian Sembako", body: "250 paket sembako dibagikan kepada warga yang sudah terdata. Relawan mengantar langsung bagi yang tidak bisa datang." },
  ],
  events: [
    { name: "Donor Darah & Cek Kesehatan", date: "2027-09-12T07:30:00+07:00", time: "07.30 – 12.00 WIB", venue: "Balai Warga RW 05 Sukamaju", address: "Jl. Sukamaju Raya No. 21, Cigugur Tengah, Cimahi Tengah, Kota Cimahi" },
    { name: "Pembagian Sembako", date: "2027-09-12T13:00:00+07:00", time: "13.00 – 15.00 WIB", venue: "Lapangan RW 05 Sukamaju", address: "Jl. Sukamaju Raya, samping Balai Warga, Cigugur Tengah, Kota Cimahi" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bjb", type: "bank", bank_name: "BJB", account_number: "0094 1127 8830 100", account_name: "Perkumpulan Gerakan Tangan Hangat" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "OVO", ewallet_number: "0857 2211 4093", account_name: "Bendahara Tangan Hangat" },
    { id: "demo-barang", type: "address", address: "Posko Tangan Hangat, Jl. Sukamaju Raya No. 21, Cimahi 40522 (beras, minyak goreng, susu, dan kebutuhan pokok lain)" },
  ],
  guestName: "Kak Rizky Ananda",
  guestTable: "Pos Sembako",
  extras: {
    quote: { text: "Tidak ada yang terlalu kecil untuk dibagikan, dan tidak ada yang terlalu besar untuk dikerjakan bersama.", source: "Relawan Tangan Hangat" },
    rundown: { items: [
      { time: "07.00", title: "Briefing relawan", note: "Pembagian rompi dan pos tugas" },
      { time: "07.30", title: "Registrasi peserta dibuka" },
      { time: "12.00", title: "Istirahat & makan siang bersama" },
      { time: "13.00", title: "Pembagian sembako" },
      { time: "15.00", title: "Foto bersama & beres-beres" },
    ] },
    dressCode: { note: "Pakaian nyaman berlengan pendek atau mudah digulung untuk pendonor. Relawan akan mendapat rompi di lokasi.", colors: ["#f08a3c", "#d94b3d", "#f6c445", "#5b8c3a"] },
    guestPass: { note: "Tunjukkan kode ini di meja registrasi untuk mengambil rompi relawan atau nomor antrean." },
    rsvpDietary: { label: "Golongan darah atau catatan kesehatan (opsional)" },
    family: { names: ["Unit Donor Darah Kota Cimahi", "Puskesmas Cigugur Tengah", "Karang Taruna RW 05"] },
    faq: { items: [
      { q: "Siapa yang boleh mendonorkan darah?", a: "Usia 17–60 tahun, berat badan minimal 45 kg, sehat, dan tidur cukup malam sebelumnya. Petugas akan melakukan skrining terlebih dahulu." },
      { q: "Apa yang perlu dibawa?", a: "KTP atau kartu identitas, dan kartu donor bila sudah punya. Sarapan dulu sebelum datang ya." },
      { q: "Bagaimana cara menjadi relawan?", a: "Pilih \"Relawan\" pada form pendaftaran di undangan ini. Panitia akan menghubungi untuk pembagian pos." },
    ] },
  },
});
