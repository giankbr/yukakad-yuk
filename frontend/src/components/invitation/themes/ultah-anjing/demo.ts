import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Arka", groom: "",
    brideFull: "Arkana Bagas Wicaksono",
    brideParents: "Putra pertama dari Bapak Yudha Wicaksono & Ibu Anindya Putri",
    note: "Guk guk! Arka sudah lima tahun. Ayo datang, main lempar bola, berburu tulang mainan, dan tiup lilin bersama Cokelat dan Belang!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-07-10T15:30:00+07:00",
  place: "Halaman Rumah Arka",
  address: "Jl. Cigadung Raya Barat No. 21, Cigadung, Cibeunying Kaler, Bandung",
  story: { title: "Cerita Arka", body: "" },
  stories: [
    { date: "2022", title: "Halo, dunia!", body: "Arka lahir di pagi yang cerah. Cokelat, anjing keluarga, langsung setia berjaga di depan kamar." },
    { date: "2024", title: "Kata pertama: guk", body: "Kata pertama Arka bukan mama atau papa, tapi suara gonggongan menirukan Cokelat." },
    { date: "2026", title: "Teman baru", body: "Belang si anak anjing berbintik datang ke rumah dan langsung jadi teman main bola Arka." },
    { date: "2027", title: "Lima tahun!", body: "Sekarang Arka bercita-cita jadi dokter hewan supaya bisa merawat semua anjing di kompleks." },
  ],
  events: [
    { name: "Pesta Anak Anjing Arka", date: "2027-07-10T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Halaman Rumah Arka", address: "Jl. Cigadung Raya Barat No. 21, Cigadung, Cibeunying Kaler, Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0627 3318 54", account_name: "Anindya Putri" },
    { id: "demo-kado", type: "address", address: "Jl. Cigadung Raya Barat No. 21, Cigadung, Cibeunying Kaler, Bandung 40191" },
  ],
  guestName: "Adik Naura & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Arkana Bagas Wicaksono", nickname: "Arka", birthDate: "2022-07-10T07:10:00+07:00", parents: "Putra pertama dari Bapak Yudha Wicaksono & Ibu Anindya Putri" },
    rundown: { items: [
      { time: "15.30", title: "Datang & pakai bando telinga anjing", note: "Meja penyambutan di gerbang" },
      { time: "16.00", title: "Lomba lempar & tangkap bola" },
      { time: "16.30", title: "Berburu tulang mainan di halaman" },
      { time: "17.15", title: "Tiup lilin & bagi bingkisan" },
    ] },
    dressCode: { note: "Baju ceria: merah, kuning, biru langit, atau hijau rumput. Kostum anak anjing sangat boleh!", colors: ["#e05a3a", "#ffc93c", "#4a9fe0", "#7cc35a"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Wicaksono", "Opa & Oma Putri", "Cokelat & Belang (anjing kesayangan)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Arka.", items: [
      { id: "w1", name: "Buku cerita bergambar anjing", price: "± Rp75.000" },
      { id: "w2", name: "Bola sepak mini", price: "± Rp80.000", claimed_by: "Om Rizal" },
      { id: "w3", name: "Boneka anak anjing", price: "± Rp95.000" },
    ] },
    faq: { items: [
      { q: "Apakah ada anjing sungguhan di pesta?", a: "Cokelat dan Belang akan ada di kandangnya. Teman yang takut atau alergi tetap aman di area pesta." },
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada teh dan kopi hangat untuk Ayah & Bunda di teras." },
    ] },
  },
});
