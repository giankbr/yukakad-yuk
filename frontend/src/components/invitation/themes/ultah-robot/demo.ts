import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Gibran", groom: "",
    brideFull: "Muhammad Gibran Alfarizi",
    brideParents: "Putra pertama dari Bapak Yoga Pratama & Ibu Dewi Anggraini",
    note: "Bip bup! Sistem pesta sudah menyala. Ayo datang, rakit robot kardus, joget robot bersama, dan tiup lilin kue robot!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-09-19T15:00:00+07:00",
  place: "Ruang Main Kayu Kecil",
  address: "Jl. Kemang Pratama Raya Blok AN No. 9, Bojong Rawalumbu, Kota Bekasi",
  story: { title: "Cerita Gibran", body: "" },
  stories: [
    { date: "2020", title: "Sistem menyala!", body: "Gibran lahir di suatu pagi yang cerah, tangisnya kencang seperti alarm robot." },
    { date: "2023", title: "Insinyur cilik", body: "Remote TV, jam weker, dan mobil-mobilan pernah dibongkar Gibran hanya untuk melihat isinya." },
    { date: "2025", title: "Robot kardus pertama", body: "Bersama Ayah, Gibran membuat robot dari kardus bekas dan tutup botol. Namanya Bip." },
    { date: "2027", title: "Tujuh tahun!", body: "Sekarang Gibran ingin jadi pembuat robot yang bisa membantu menanam pohon." },
  ],
  events: [
    { name: "Pesta Robot Gibran", date: "2027-09-19T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Ruang Main Kayu Kecil", address: "Jl. Kemang Pratama Raya Blok AN No. 9, Bojong Rawalumbu, Kota Bekasi" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "1670 0081 2245 9", account_name: "Dewi Anggraini" },
    { id: "demo-kado", type: "address", address: "Perum Taman Galaxy Blok C3 No. 12, Pekayon Jaya, Bekasi Selatan, Kota Bekasi 17148" },
  ],
  guestName: "Adik Nadia & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Muhammad Gibran Alfarizi", nickname: "Gibran", birthDate: "2020-09-19T07:40:00+07:00", parents: "Putra pertama dari Bapak Yoga Pratama & Ibu Dewi Anggraini" },
    rundown: { items: [
      { time: "15.00", title: "Datang & ambil kartu identitas robot", note: "Meja registrasi di pintu masuk" },
      { time: "15.30", title: "Bengkel robot kardus", note: "Semua bahan sudah disiapkan" },
      { time: "16.15", title: "Lomba joget robot" },
      { time: "16.45", title: "Tiup lilin kue robot & bagi bingkisan" },
    ] },
    dressCode: { note: "Baju warna cerah: oranye, toska, kuning, atau biru tua. Kostum robot buatan sendiri sangat boleh!", colors: ["#f28a4a", "#38b2a6", "#f7c948", "#2c3a5e"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Pratama", "Opa & Oma Anggraini", "Tante Laras & Om Bayu"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Gibran.", items: [
      { id: "w1", name: "Set balok rakit warna-warni", price: "± Rp150.000" },
      { id: "w2", name: "Buku sains bergambar untuk anak", price: "± Rp85.000", claimed_by: "Tante Laras" },
      { id: "w3", name: "Kit robot sederhana tenaga baterai", price: "± Rp120.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada kopi, teh, dan camilan untuk Ayah & Bunda di area tunggu." },
      { q: "Perlu membawa bahan untuk robot kardus?", a: "Tidak perlu, semua bahan sudah kami siapkan. Cukup bawa semangat!" },
    ] },
  },
});
