import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Shaka", groom: "",
    brideFull: "Shaka Abimanyu Prasetya",
    brideParents: "Putra pertama dari Bapak Dimas Prasetya & Ibu Anindya Larasati",
    note: "Dum-dum-tak! Shaka sudah enam tahun. Bawa suara terbaikmu, kita bikin konser kecil bersama!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-07-11T15:30:00+07:00",
  place: "Rumah Musik Tangga Nada",
  address: "Jl. Tebet Raya No. 52, Tebet Timur, Jakarta Selatan",
  story: { title: "Lagu Shaka", body: "" },
  stories: [
    { date: "2021", title: "Tangisan pertama", body: "Shaka lahir di bulan Juli, tangisnya nyaring seperti terompet kecil." },
    { date: "2023", title: "Panci jadi drum", body: "Semua panci di dapur Bunda pernah jadi drum. Sendok kayu jadi stiknya." },
    { date: "2025", title: "Gitar pertama", body: "Hadiah ulang tahun dari Kakek: gitar mungil oranye yang dibawa ke mana-mana." },
    { date: "2027", title: "Enam tahun, ayo bernyanyi!", body: "Sekarang Shaka hafal lima lagu anak dan ingin bikin band bersama teman-teman." },
  ],
  events: [
    { name: "Pesta Konser Mini", date: "2027-07-11T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Rumah Musik Tangga Nada", address: "Jl. Tebet Raya No. 52, Tebet Timur, Jakarta Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0451 2290 37", account_name: "Anindya Larasati" },
    { id: "demo-kado", type: "address", address: "Jl. Tebet Barat Dalam IV No. 9, Tebet, Jakarta Selatan 12810" },
  ],
  guestName: "Adik Keira & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Shaka Abimanyu Prasetya", nickname: "Shaka", birthDate: "2021-07-11T07:20:00+07:00", parents: "Putra pertama dari Bapak Dimas Prasetya & Ibu Anindya Larasati" },
    rundown: { items: [
      { time: "15.30", title: "Datang & pilih alat musik mainan", note: "Meja instrumen di depan panggung" },
      { time: "16.00", title: "Kelas drum dan ketipung mini" },
      { time: "16.45", title: "Tiup lilin & nyanyi bersama" },
      { time: "17.15", title: "Konser kecil teman-teman", note: "Semua boleh tampil!" },
    ] },
    dressCode: { note: "Baju warna-warni seperti xilofon: merah, oranye, kuning, hijau, biru, ungu. Topi pesta boleh!", colors: ["#ee4152", "#ff9a3c", "#ffd23f", "#2ec4b6", "#4d7cf3", "#8f5be8"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Prasetya", "Opa & Oma Larasati"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Shaka.", items: [
      { id: "w1", name: "Ketipung mainan", price: "± Rp95.000" },
      { id: "w2", name: "Buku lagu anak bergambar", price: "± Rp70.000", claimed_by: "Tante Sinta" },
      { id: "w3", name: "Mikrofon karaoke mini", price: "± Rp120.000" },
    ] },
  },
});
