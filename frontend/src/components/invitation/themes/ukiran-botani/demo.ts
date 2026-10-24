import { makeDemo } from "../demo-base";

// Vintage, pasangan netral: pecinta tanaman yang bertemu di perpustakaan botani; upacara dan resepsi taman di Bogor.
export const demo = makeDemo({
  couple: {
    bride: "Livia", groom: "Bastian",
    brideFull: "Livia Anggraeni Wardhana, M.Si.", groomFull: "Bastian Raditya Pranoto, S.Hut.",
    brideParents: "Putri sulung dari\nBapak Hendra Wardhana & Ibu Lestari Wulandari", groomParents: "Putra kedua dari\nBapak Teguh Pranoto & Ibu Ratna Kumalasari",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Seperti pakis yang tumbuh perlahan dan tak pernah berhenti membuka daun baru.",
  },
  eventLabel: "Pernikahan",
  date: "2027-11-27T15:00:00+07:00",
  place: "Rumah Kaca Paku Haji",
  address: "Jl. Pajajaran Indah V No. 12, Baranangsiang, Bogor Timur, Kota Bogor",
  stories: [
    { date: "2019", title: "Fig. 1 — Perpustakaan", body: "Kami berebut satu-satunya salinan buku ilustrasi botani tua di perpustakaan kampus. Akhirnya membacanya bersama." },
    { date: "2022", title: "Fig. 2 — Herbarium", body: "Akhir pekan kami habiskan menggambar daun dan pakis, mengisi buku sketsa yang kini sudah tiga jilid." },
    { date: "2027", title: "Fig. 3 — Satu Spesimen", body: "Di bawah atap kaca yang dipenuhi tanaman, kami memutuskan untuk tumbuh bersama." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-11-27T15:00:00+07:00", time: "15.00 – 16.00 WIB", venue: "Rumah Kaca Paku Haji", address: "Jl. Pajajaran Indah V No. 12, Baranangsiang, Bogor Timur, Kota Bogor" },
    { name: "Resepsi Taman", date: "2027-11-27T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Taman Seribu Pakis", address: "Jl. Pajajaran Indah V No. 12, Baranangsiang, Bogor Timur, Kota Bogor" },
  ],
  gallery: ["/themes/img/r89.webp", "/themes/img/a77.webp", "/themes/img/a76.webp", "/themes/img/r42.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "6045 1127 90", account_name: "Livia Anggraeni Wardhana" },
    { id: "demo-kado", type: "address", address: "Jl. Bangbarung Raya No. 7, Tegal Gundil, Bogor Utara, Kota Bogor 16152" },
  ],
  guestName: "Bapak Antonius Setiadi & Keluarga",
  guestTable: "Meja Filix 4",
  extras: {
    quote: { text: "Cinta tidak tumbuh dalam semalam. Ia disiram setiap pagi, dijaga dari musim ke musim, lalu suatu hari mekar tanpa diminta.", source: "Dari buku sketsa kami" },
    rundown: { items: [
      { time: "18.30", title: "Sambutan di taman pakis", note: "Musik gesek dan lampu taman" },
      { time: "19.00", title: "Makan malam bersama" },
      { time: "20.00", title: "Pemotongan kue & dansa pertama" },
    ] },
    dressCode: { note: "Busana resmi vintage: hitam, krem kertas tua, dan hijau pakis.", colors: ["#1e1a16", "#efe5cf", "#5f6b4e", "#8a7b62"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Hendra Wardhana", "Kel. Besar Teguh Pranoto"] },
  },
});
