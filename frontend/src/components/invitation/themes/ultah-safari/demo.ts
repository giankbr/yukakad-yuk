import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alesha", groom: "",
    brideFull: "Alesha Putri Ramadhani",
    brideParents: "Putri pertama dari Bapak Yoga Ramadhani & Ibu Melati Kusumawardani",
    note: "Siapkan teropong dan topi petualang! Alesha genap lima tahun dan mengajak teman-teman berpetualang ke padang rumput.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-11-06T15:00:00+07:00",
  place: "Aula Bukit Sabana",
  address: "Jl. Pakuan Indah No. 5, Tegallega, Bogor Tengah, Kota Bogor",
  story: { title: "Cerita Alesha", body: "" },
  stories: [
    { date: "2022", title: "Anak singa kecil lahir", body: "Alesha lahir di sore yang hujan, tangisnya paling keras di seluruh ruangan, seperti auman anak singa." },
    { date: "2024", title: "Sahabat jerapah", body: "Boneka jerapah pemberian Nenek jadi teman tidur yang tidak pernah boleh tertinggal." },
    { date: "2026", title: "Hari pertama TK", body: "Alesha berani masuk kelas sendiri dan pulang dengan gambar gajah berwarna ungu." },
    { date: "2027", title: "Lima tahun!", body: "Sekarang Alesha hafal suara semua hewan dan bercita-cita jadi dokter hewan." },
  ],
  events: [
    { name: "Ekspedisi Ulang Tahun Alesha", date: "2027-11-06T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Aula Bukit Sabana", address: "Jl. Pakuan Indah No. 5, Tegallega, Bogor Tengah, Kota Bogor" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BRI", account_number: "0341 0110 2256 507", account_name: "Melati Kusumawardani" },
    { id: "demo-kado", type: "address", address: "Jl. Bangbarung Raya No. 18, Bantarjati, Bogor Utara, Kota Bogor 16153" },
  ],
  guestName: "Adik Naira & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Alesha Putri Ramadhani", nickname: "Alesha", birthDate: "2022-11-06T16:40:00+07:00", parents: "Putri pertama dari Bapak Yoga Ramadhani & Ibu Melati Kusumawardani" },
    rundown: { items: [
      { time: "15.00", title: "Daftar penjelajah", note: "Ambil topi petualang & paspor safari" },
      { time: "15.30", title: "Berburu stiker hewan di taman" },
      { time: "16.15", title: "Dongeng hewan & menari bersama" },
      { time: "16.45", title: "Tiup lilin, potong kue & bagi bingkisan" },
    ] },
    dressCode: { note: "Gaya penjelajah: warna krem, hijau zaitun, atau motif hewan favoritmu.", colors: ["#cdb46c", "#7d8a3c", "#e9a744", "#8a5a34"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Ramadhani", "Eyang Kusumawardani", "Kak Rafif (sepupu Alesha)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah paling seru. Kalau ingin memberi, ini yang sedang Alesha impikan.", items: [
      { id: "w1", name: "Ensiklopedia hewan anak", price: "± Rp150.000" },
      { id: "w2", name: "Teropong mainan", price: "± Rp90.000", claimed_by: "Tante Dewi" },
      { id: "w3", name: "Set boneka hewan savana", price: "± Rp200.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua ikut masuk?", a: "Tentu! Ada tempat duduk untuk Ayah & Bunda di sekeliling area bermain." },
      { q: "Ada parkir?", a: "Parkir tersedia di halaman Aula Bukit Sabana." },
    ] },
  },
});
