import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laras", groom: "Gilang",
    brideFull: "Larasati Ayu Pramesti", groomFull: "Gilang Mahendra Putra",
    brideParents: "Putri dari\nBapak Hendro Wibisono & Ibu Ratna Kusuma",
    groomParents: "Putra dari\nBapak Agus Santoso & Ibu Dewi Lestari",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Episode terbaru dari kisah yang dimulai di rak komik bekas: kali ini dengan akhir yang bahagia.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-25T15:00:00+07:00",
  place: "Studio Lantai Lima",
  address: "Jl. Cikini Raya No. 73, Menteng, Jakarta Pusat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Edisi #1 · 2019", title: "Rebutan Komik Terakhir", body: "Di lapak buku bekas Kwitang, kami meraih jilid yang sama. Gilang mengalah, Laras mentraktir es teh sebagai gantinya." },
    { date: "Edisi #12 · 2022", title: "Satu Tim, Satu Zine", body: "Kami menggambar dan menulis zine kecil berdua. Edisi pertamanya habis dalam sehari di pasar kreatif." },
    { date: "Edisi Spesial · 2026", title: "Panel Terakhir", body: "Gilang menyelipkan halaman komik buatannya sendiri: panel terakhir berisi satu pertanyaan, dan jawabannya \"iya!\"." },
  ],
  events: [
    { name: "Pengucapan Janji", date: "2027-09-25T15:00:00+07:00", time: "15.00 – 16.00 WIB", venue: "Studio Lantai Lima", address: "Jl. Cikini Raya No. 73, Menteng, Jakarta Pusat" },
    { name: "Pesta Resepsi", date: "2027-09-25T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Atap Studio Lantai Lima", address: "Jl. Cikini Raya No. 73, Menteng, Jakarta Pusat" },
  ],
  gallery: ["/themes/img/a122.webp", "/themes/img/a131.webp", "/themes/img/a123.webp", "/themes/img/a130.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "5271 0938 44", account_name: "Larasati Ayu Pramesti" },
    { id: "demo-ewallet", type: "ewallet", ewallet_provider: "GoPay", ewallet_number: "0812 9034 5521", account_name: "Gilang Mahendra Putra" },
  ],
  guestName: "Kak Nadia & Partner",
  guestTable: "",
  extras: {
    rundown: { items: [
      { time: "15.00", title: "Pengucapan janji", note: "Keluarga & sahabat dekat" },
      { time: "16.00", title: "Sesi foto ala sampul komik" },
      { time: "18.30", title: "Pesta dibuka", note: "Makan malam & live band" },
      { time: "20.30", title: "Lempar buket & dansa" },
    ] },
    dressCode: { note: "Tampil berani! Pilih satu warna primer: merah, kuning, atau biru. Motif polkadot sangat dianjurkan.", colors: ["#e5322a", "#ffd21f", "#1d5fc4", "#15121a"] },
    guestPass: {},
    rsvpDietary: {},
    faq: { items: [
      { q: "Boleh datang dengan kostum?", a: "Boleh sekali, asal tetap nyaman dan sopan. Ada hadiah kecil untuk kostum paling niat." },
      { q: "Parkirnya di mana?", a: "Parkir tersedia di gedung sebelah. Disarankan naik KRL ke Stasiun Cikini, lalu jalan kaki lima menit." },
    ] },
  },
});
