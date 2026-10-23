import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Anindita", groom: "Baskara",
    brideFull: "Anindita Larasati Wibisono", groomFull: "Yosef Baskara Adiwangsa",
    brideParents: "Putri pertama dari\nBapak Hendro Wibisono & Ibu Lucia Sri Rahayu", groomParents: "Putra ketiga dari\nBapak Fransiskus Adiwangsa & Ibu Theresia Kurniawati",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Disusun huruf demi huruf, dicetak dengan sabar, dan kini kami bagikan kepada Anda.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-11T10:00:00+07:00",
  place: "Rumah Cetak Braga",
  address: "Jl. Braga No. 37, Sumur Bandung, Kota Bandung, Jawa Barat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2020", title: "Lokakarya Cetak Tangan", body: "Kami bertemu di sebuah lokakarya letterpress di Bandung. Anindita menyusun huruf terlalu rapat, Baskara meminjamkan spasinya." },
    { date: "2023", title: "Mesin Tua di Garasi", body: "Kami membeli dan memperbaiki sebuah mesin cetak tua bersama. Kartu pertama yang kami cetak berbunyi: terima kasih." },
    { date: "2027", title: "Satu Lembar Lagi", body: "Undangan ini kami susun sendiri, sebagai lembar pertama dari cerita panjang yang akan kami tulis berdua." },
  ],
  events: [
    { name: "Janji Pernikahan", date: "2027-09-11T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Taman Belakang Rumah Cetak Braga", address: "Jl. Braga No. 37, Sumur Bandung, Kota Bandung" },
    { name: "Resepsi", date: "2027-09-11T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Rumah Cetak Braga", address: "Jl. Braga No. 37, Sumur Bandung, Kota Bandung" },
  ],
  gallery: ["/themes/img/a74.webp", "/themes/img/r88.webp", "/themes/img/r56.webp", "/themes/img/a77.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0712 4490 18", account_name: "Anindita Larasati Wibisono" },
    { id: "demo-kado", type: "address", address: "Jl. Cihampelas No. 120, Cipaganti, Coblong, Kota Bandung 40131" },
  ],
  guestName: "Ibu Margaretha Tanudjaja",
  guestTable: "7",
  extras: {
    quote: { text: "Kata-kata yang dicetak dengan sabar akan bertahan lebih lama daripada yang diucapkan terburu-buru. Begitu pula janji.", source: "Catatan dari meja cetak" },
    rundown: { items: [
      { time: "18.30", title: "Ramah tamah & pameran cetak", note: "Tamu dapat mencetak kartu kenangan sendiri" },
      { time: "19.15", title: "Sambutan keluarga" },
      { time: "19.30", title: "Makan malam" },
      { time: "20.30", title: "Dansa pertama" },
    ] },
    dressCode: { note: "Formal sederhana. Gading, hitam, dan merah marun.", colors: ["#f3eee4", "#1f1a17", "#6e1a24", "#b9ab98"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-11T10:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendro Wibisono", "Kel. Besar Bpk. Fransiskus Adiwangsa"] },
  },
});
