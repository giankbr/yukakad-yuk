import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "",
    brideFull: "Kirana Ayu Lestari",
    brideParents: "Putri pertama dari Bapak Bagas Wicaksono & Ibu Laras Pramesti",
    note: "Kirana sudah enam tahun! Ayo datang membawa senyum, kita melukis bersama sampai tangan penuh warna.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-07-11T10:00:00+07:00",
  place: "Sanggar Lukis Pelangi Kecil",
  address: "Jl. Kemang Selatan VIII No. 23, Bangka, Mampang Prapatan, Jakarta Selatan",
  story: { title: "Kanvas Kirana", body: "" },
  stories: [
    { date: "2021", title: "Halo, Dunia!", body: "Kirana lahir di suatu pagi bulan Juli, dengan genggaman kecil yang kuat sekali." },
    { date: "2023", title: "Krayon Pertama", body: "Dinding kamar jadi kanvas pertamanya. Ayah dan Bunda pura-pura marah, lalu memotretnya." },
    { date: "2025", title: "Pelukis Cilik", body: "Setiap Minggu pagi Kirana melukis bunga dan kucing di sanggar dekat rumah." },
    { date: "2027", title: "Enam Tahun!", body: "Sekarang Kirana ingin merayakan ulang tahun dengan melukis bersama teman-temannya." },
  ],
  events: [
    { name: "Pesta Melukis Kirana", date: "2027-07-11T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Sanggar Lukis Pelangi Kecil", address: "Jl. Kemang Selatan VIII No. 23, Bangka, Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "5271 0388 14", account_name: "Laras Pramesti" },
    { id: "demo-kado", type: "address", address: "Jl. Bangka Raya No. 7B, Pela Mampang, Jakarta Selatan 12720" },
  ],
  guestName: "Adik Raka & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Kirana Ayu Lestari", nickname: "Kirana", birthDate: "2021-07-11T07:20:00+07:00", parents: "Putri pertama dari Bapak Bagas Wicaksono & Ibu Laras Pramesti" },
    rundown: { items: [
      { time: "10.00", title: "Datang & pakai celemek lukis", note: "Celemek dan kuas sudah disiapkan" },
      { time: "10.30", title: "Melukis kanvas mini bersama", note: "Tema: hewan kesayanganku" },
      { time: "11.45", title: "Tiup lilin & potong kue palet" },
      { time: "12.15", title: "Pameran kecil & bawa pulang lukisan" },
    ] },
    dressCode: { note: "Baju yang boleh kena cat ya! Warna-warni cerah sangat cocok.", colors: ["#e84a3c", "#f6c234", "#3a7bd5", "#4caf6a", "#ef6fa6"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Wicaksono", "Opa & Oma Pramesti"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Kirana.", items: [
      { id: "w1", name: "Set cat air 24 warna", price: "± Rp95.000" },
      { id: "w2", name: "Buku sketsa A4", price: "± Rp45.000", claimed_by: "Tante Dewi" },
      { id: "w3", name: "Celemek lukis anak", price: "± Rp70.000" },
    ] },
    faq: { items: [
      { q: "Apakah cat aman untuk anak?", a: "Tentu. Semua cat berbahan dasar air, tidak beracun, dan mudah dicuci." },
      { q: "Apakah orang tua boleh menemani?", a: "Boleh sekali! Ada kursi dan camilan untuk Ayah & Bunda." },
    ] },
  },
});
