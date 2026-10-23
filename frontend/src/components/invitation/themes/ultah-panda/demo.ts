import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alya", groom: "",
    brideFull: "Alya Putri Ramadhani",
    brideParents: "Putri pertama dari Bapak Reza Pratama & Ibu Dinda Larasati",
    note: "Alya genap empat tahun! Ayo datang ke hutan bambu, kita makan kue, bermain, dan berpelukan seperti panda.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-04-17T15:00:00+07:00",
  place: "Saung Bambu Lembah Pajajaran",
  address: "Jl. Pajajaran No. 41, Baranangsiang, Kec. Bogor Timur, Kota Bogor",
  story: { title: "Cerita Alya", body: "" },
  stories: [
    { date: "2023", title: "Panda kecil lahir", body: "Alya lahir di pagi yang gerimis. Boneka panda dari Nenek langsung jadi teman tidur pertamanya." },
    { date: "2025", title: "Suka bambu", body: "Setiap ke taman, Alya selalu berhenti di rumpun bambu dan mendengarkan daunnya berbisik tertiup angin." },
    { date: "2027", title: "Empat tahun!", body: "Sekarang Alya sudah bisa bercerita panjang tentang panda, dan ingin merayakannya bersama teman-teman." },
  ],
  events: [
    { name: "Pesta Panda Alya", date: "2027-04-17T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Saung Bambu Lembah Pajajaran", address: "Jl. Pajajaran No. 41, Baranangsiang, Kec. Bogor Timur, Kota Bogor" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4210 8877 21", account_name: "Dinda Larasati" },
    { id: "demo-kado", type: "address", address: "Perumahan Bogor Nirwana Residence, Cluster Bambu Kuning B2 No. 7, Kota Bogor 16132" },
  ],
  guestName: "Adik Kenzo & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Alya Putri Ramadhani", nickname: "Alya", birthDate: "2023-04-15T06:40:00+07:00", parents: "Putri pertama dari Bapak Reza Pratama & Ibu Dinda Larasati" },
    rundown: { items: [
      { time: "15.00", title: "Datang & pakai bando telinga panda", note: "Disediakan untuk semua anak" },
      { time: "15.30", title: "Dongeng panda dan permainan bambu" },
      { time: "16.20", title: "Lomba menghias kue mangkuk" },
      { time: "17.00", title: "Tiup lilin, potong kue & bagi bingkisan" },
    ] },
    dressCode: { note: "Pakai baju hitam-putih atau hijau bambu. Kostum panda boleh banget!", colors: ["#25262a", "#fbfaf4", "#7fbf5a", "#f3a7a4"] },
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Pratama", "Eyang Kakung & Eyang Putri Larasati", "Om Bima & Tante Sekar"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini yang sedang Alya impikan.", items: [
      { id: "w1", name: "Buku cerita bergambar tentang panda", price: "± Rp95.000" },
      { id: "w2", name: "Set krayon dan buku mewarnai hutan", price: "± Rp60.000", claimed_by: "Tante Sekar" },
      { id: "w3", name: "Tas punggung bentuk panda", price: "± Rp140.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu, ada saung teduh untuk orang tua di samping area bermain." },
      { q: "Bagaimana jika hujan?", a: "Acara tetap berjalan di saung besar yang beratap, jadi tidak perlu khawatir." },
    ] },
  },
});
