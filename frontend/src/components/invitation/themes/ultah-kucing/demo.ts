import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "",
    brideFull: "Kirana Ayu Lestari",
    brideParents: "Putri pertama dari Bapak Galih Pramudito & Ibu Sekar Larasati",
    note: "Meong! Kirana sudah enam tahun. Ayo datang, main bola benang, sembunyi di kardus, dan tiup lilin kue ikan bersama!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-04-17T15:00:00+07:00",
  place: "Rumah Eyang Kirana",
  address: "Jl. Kaliurang Km 7,5, Gg. Wiroto No. 12, Sinduadi, Mlati, Sleman",
  story: { title: "Cerita Kirana", body: "" },
  stories: [
    { date: "2021", title: "Halo, dunia!", body: "Kirana lahir di suatu sore yang hujan, ditemani Oyen, kucing oranye milik Eyang." },
    { date: "2023", title: "Kata pertama: meong", body: "Sebelum bisa bilang 'mama', Kirana sudah pintar menirukan suara kucing." },
    { date: "2025", title: "Sahabat berbulu", body: "Mochi si kucing abu datang ke rumah dan langsung jadi teman tidur siang Kirana." },
    { date: "2027", title: "Enam tahun!", body: "Sekarang Kirana ingin jadi dokter hewan supaya bisa merawat semua kucing di kampung." },
  ],
  events: [
    { name: "Pesta Kucing Kirana", date: "2027-04-17T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Rumah Eyang Kirana", address: "Jl. Kaliurang Km 7,5, Gg. Wiroto No. 12, Sinduadi, Mlati, Sleman" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "0373 5512 908", account_name: "Sekar Larasati" },
    { id: "demo-kado", type: "address", address: "Jl. Kaliurang Km 7,5, Gg. Wiroto No. 12, Sinduadi, Mlati, Sleman 55284" },
  ],
  guestName: "Adik Raka & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Kirana Ayu Lestari", nickname: "Kirana", birthDate: "2021-04-17T16:20:00+07:00", parents: "Putri pertama dari Bapak Galih Pramudito & Ibu Sekar Larasati" },
    rundown: { items: [
      { time: "15.00", title: "Datang & pakai bando telinga kucing", note: "Meja penyambutan di teras" },
      { time: "15.30", title: "Lomba menggulung bola benang" },
      { time: "16.15", title: "Tiup lilin kue ikan", note: "Nyanyi bersama" },
      { time: "16.45", title: "Mewarnai kardus rumah kucing & bagi bingkisan" },
    ] },
    dressCode: { note: "Baju warna ceria: oranye, abu-abu, toska, atau merah muda. Kostum kucing sangat boleh!", colors: ["#f3a04a", "#a9adb8", "#3aa6a0", "#f59ab0"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Pramudito", "Kakek & Nenek Larasati", "Oyen & Mochi (kucing kesayangan)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Kirana.", items: [
      { id: "w1", name: "Buku cerita bergambar kucing", price: "± Rp75.000" },
      { id: "w2", name: "Set krayon & buku mewarnai", price: "± Rp60.000", claimed_by: "Tante Wulan" },
      { id: "w3", name: "Boneka kucing kecil", price: "± Rp90.000" },
    ] },
    faq: { items: [
      { q: "Apakah ada kucing sungguhan di pesta?", a: "Oyen dan Mochi akan ada di kamar sendiri. Teman yang alergi bulu kucing tetap aman di area pesta." },
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada teh hangat dan camilan untuk Ayah & Bunda di teras." },
    ] },
  },
});
