import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alya", groom: "Bima",
    brideFull: "Alya Maharani Putri", groomFull: "Bima Arditya Wibowo",
    brideParents: "Putri dari\nBapak Hendra Gunawan & Ibu Ratih Kusuma", groomParents: "Putra dari\nBapak Agus Wibowo & Ibu Lina Marlina",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Lingkaran, segitiga, persegi: bentuk sederhana yang, bila disusun dengan sengaja, menjadi utuh. Begitu juga kami.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-17T16:00:00+07:00",
  place: "Galeri Ruang Rupa Bidang",
  address: "Jl. Kemang Timur No. 41, Bangka, Mampang Prapatan, Jakarta Selatan",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2018", title: "Kelas Tipografi", body: "Kami duduk bersebelahan di kelas desain grafis. Alya menyukai huruf tanpa kait, Bima tidak. Debat itu tidak pernah selesai." },
    { date: "2022", title: "Studio Bersama", body: "Kami membuka studio kecil di Kemang: satu meja panjang, dua kursi, dan dinding penuh poster cetak saring." },
    { date: "2026", title: "Lamaran", body: "Bima melamar dengan sebuah poster buatannya sendiri: lingkaran merah, segitiga kuning, dan satu pertanyaan." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-07-17T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Galeri Ruang Rupa Bidang", address: "Jl. Kemang Timur No. 41, Bangka, Mampang Prapatan, Jakarta Selatan" },
    { name: "Resepsi", date: "2027-07-17T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Atap Galeri Ruang Rupa Bidang", address: "Jl. Kemang Timur No. 41, Bangka, Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/r88.webp", "/themes/img/a78.webp", "/themes/img/r55.webp", "/themes/img/r8.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0388 19", account_name: "Alya Maharani Putri" },
    { id: "demo-jago", type: "bank", bank_name: "Jago", account_number: "1002 7731 4450", account_name: "Bima Arditya Wibowo" },
    { id: "demo-kado", type: "address", address: "Jl. Kemang Selatan VIII No. 3, Bangka, Jakarta Selatan 12730" },
  ],
  guestName: "Saudari Prita Anindya",
  guestTable: "Meja B4",
  extras: {
    quote: { text: "Bentuk mengikuti fungsi; dan cinta, kami kira, mengikuti kesediaan untuk terus menyusunnya bersama.", source: "Alya & Bima" },
    rundown: { items: [
      { time: "16.00", title: "Upacara pernikahan", note: "Ruang pamer utama" },
      { time: "17.00", title: "Foto bersama keluarga" },
      { time: "18.30", title: "Resepsi di atap", note: "Musik akustik & hidangan" },
      { time: "20.30", title: "Potong kue & dansa pertama" },
    ] },
    dressCode: { note: "Warna primer atau monokrom. Satu blok warna berani sangat kami sukai.", colors: ["#d8402b", "#f1bb1f", "#1f4fa0", "#1b1a19"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Hendra Gunawan", "Kel. Agus Wibowo"] },
  },
});
