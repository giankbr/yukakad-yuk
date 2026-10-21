import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Bima", groom: "",
    brideFull: "Bima Arsenio Pratama",
    brideParents: "Putra kedua dari Bapak Arif Pratama & Ibu Nadia Kusumawardani",
    note: "Rawrr! Bima sudah lima tahun. Ayo ikut berpetualang ke lembah dinosaurus dan tiup lilin gunung api bersama!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-06-20T15:30:00+07:00",
  place: "Kebun Bermain Rimba Kecil",
  address: "Jl. Cempaka Putih Raya No. 41, Cempaka Putih, Jakarta Pusat",
  story: { title: "Jejak Bima", body: "" },
  stories: [
    { date: "2022", title: "Telur pertama menetas", body: "Bima lahir di suatu pagi bulan Juni, tangisnya paling nyaring satu lorong rumah sakit." },
    { date: "2023", title: "Langkah kecil", body: "Langkah pertamanya menuju rak buku, mengambil buku bergambar dinosaurus milik kakak." },
    { date: "2025", title: "Penjelajah taman", body: "Tiap sore menggali pasir di taman, mencari fosil bersama Ayah." },
    { date: "2027", title: "Lima tahun, rawrr!", body: "Sekarang hafal nama dua puluh dinosaurus dan ingin jadi ahli fosil kalau besar nanti." },
  ],
  events: [
    { name: "Pesta Petualangan Dino", date: "2027-06-20T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Kebun Bermain Rimba Kecil", address: "Jl. Cempaka Putih Raya No. 41, Cempaka Putih, Jakarta Pusat" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "1270 0098 7712", account_name: "Nadia Kusumawardani" },
    { id: "demo-kado", type: "address", address: "Jl. Percetakan Negara VII No. 18, Rawasari, Jakarta Pusat 10570" },
  ],
  guestName: "Adik Kirana & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Bima Arsenio Pratama", nickname: "Bima", birthDate: "2022-06-20T06:10:00+07:00", parents: "Putra kedua dari Bapak Arif Pratama & Ibu Nadia Kusumawardani" },
    rundown: { items: [
      { time: "15.30", title: "Datang & ambil topi dino", note: "Meja penyambutan di gerbang kebun" },
      { time: "16.00", title: "Berburu fosil di bak pasir" },
      { time: "16.45", title: "Tiup lilin kue gunung api", note: "Nyanyi bersama" },
      { time: "17.15", title: "Dongeng & bagi bingkisan" },
    ] },
    dressCode: { note: "Baju warna hutan dan gunung api: hijau, oranye, kuning. Kostum dinosaurus sangat boleh!", colors: ["#7dbb5a", "#f0904a", "#f7c35c", "#8b6a46"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Pratama", "Kakek & Nenek Kusumawardani", "Kak Alya (kakak Bima)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Bima.", items: [
      { id: "w1", name: "Set penggali fosil mainan", price: "± Rp120.000" },
      { id: "w2", name: "Buku stiker dinosaurus", price: "± Rp65.000", claimed_by: "Tante Rini" },
      { id: "w3", name: "Senter kepala untuk berpetualang", price: "± Rp90.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada saung teduh dan camilan untuk Ayah & Bunda." },
      { q: "Acaranya di luar ruangan?", a: "Sebagian besar di kebun yang teduh. Ada aula kecil kalau hujan." },
    ] },
  },
});
