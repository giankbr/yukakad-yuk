import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "PKK RW 07 Sukamaju", groom: "Dewan Juri",
    brideFull: "Tim Penggerak PKK RW 07 Kelurahan Sukamaju", groomFull: "Dewan Juri Lomba Masak Agustusan",
    brideParents: "Ibu-ibu PKK yang mengurus pendaftaran, kompor, tenda, dan konsumsi. Ketua panitia: Ibu Sri Wahyuni.",
    groomParents: "Chef Rudi (pemilik warung makan Rasa Bunda), Ibu Endang (ahli gizi Puskesmas), dan Pak RW Hadi Santoso.",
    note: "Satu jam, satu kompor, satu piring terbaik. Ayo tunjukkan masakan andalan keluargamu!",
  },
  eventLabel: "Lomba Masak Agustusan",
  date: "2027-08-21T08:00:00+07:00",
  place: "Lapangan Balai RW 07 Sukamaju",
  address: "Jl. Melati Raya No. 7, RW 07, Kelurahan Sukamaju",
  story: { title: "Aturan & jadwal", body: "" },
  stories: [
    { date: "07.00 – 07.45", title: "Daftar ulang & ambil celemek", body: "Setiap tim (maksimal 3 orang) mengambil nomor meja, celemek, dan satu paket bahan wajib dari panitia." },
    { date: "08.00 – 09.00", title: "Babak I: Nasi Goreng Kreasi", body: "Waktu memasak 60 menit. Bumbu dasar boleh dibawa dari rumah, semua bahan lain dimasak di tempat." },
    { date: "09.30 – 11.00", title: "Babak II: Tumpeng Mini Nusantara", body: "Tumpeng untuk 6 porsi dengan minimal 5 lauk. Tidak boleh memakai penyedap instan." },
    { date: "11.00 – 12.00", title: "Penjurian", body: "Dinilai dari rasa (40%), tampilan (30%), kreativitas (20%), dan kebersihan meja (10%)." },
    { date: "13.00", title: "Pengumuman juara & makan bersama", body: "Semua hidangan dicicipi bersama warga. Juara 1–3 mendapat piala, peralatan masak, dan voucher belanja." },
  ],
  events: [
    { name: "Technical Meeting Peserta", date: "2027-08-18T19:30:00+07:00", time: "19.30 – 21.00", venue: "Balai RW 07", address: "Jl. Melati Raya No. 7, RW 07, Kelurahan Sukamaju" },
    { name: "Hari Lomba", date: "2027-08-21T07:00:00+07:00", time: "07.00 – 14.00", venue: "Lapangan Balai RW 07", address: "Jl. Melati Raya No. 7, RW 07, Kelurahan Sukamaju (parkir di halaman masjid)" },
  ],
  gallery: ["/themes/img/r77.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0218 0100 4471 509", account_name: "Bendahara PKK RW 07" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "GoPay", ewallet_number: "0813 1420 6658", account_name: "Ibu Ratih (Bendahara)" },
    { id: "demo-hadiah", type: "address", address: "Rumah Ibu Sri Wahyuni, Jl. Melati III No. 12, RW 07 (sumbangan hadiah atau bahan masakan)" },
  ],
  guestName: "Ibu Wulan & Tim Dapur Melati",
  guestTable: "Meja Masak 5",
  extras: {
    rundown: { items: [
      { time: "07.00", title: "Daftar ulang", note: "Bawa bumbu dasar dan peralatan pribadi" },
      { time: "07.50", title: "Pembukaan oleh Ibu Lurah" },
      { time: "08.00", title: "Kompor dinyalakan!", note: "Babak I dimulai" },
      { time: "12.00", title: "Juri berkeliling meja" },
      { time: "13.00", title: "Pengumuman & makan bersama" },
    ] },
    guestPass: { note: "Tunjukkan kode ini di meja panitia untuk mengambil celemek dan nomor meja." },
    family: { title: "Didukung oleh", names: ["Karang Taruna RW 07", "Toko Sembako Berkah", "Warung Makan Rasa Bunda", "Puskesmas Kelurahan Sukamaju"] },
    faq: { items: [
      { q: "Siapa yang boleh ikut?", a: "Warga RW 07 dan sekitarnya, tim 2–3 orang. Boleh campur bapak-bapak, ibu-ibu, maupun remaja." },
      { q: "Apa yang disediakan panitia?", a: "Meja, kompor gas, wajan, panci, beras, telur, dan paket sayur. Bawa pisau, talenan, dan piring saji sendiri." },
      { q: "Penonton perlu daftar?", a: "Tidak perlu, gratis. Konfirmasi membantu panitia menyiapkan kursi dan porsi makan bersama." },
    ] },
  },
});
