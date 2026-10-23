import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Naura", groom: "",
    brideFull: "Naura Elvina Safitri",
    brideParents: "Putri pertama dari Bapak Dimas Prasetya & Ibu Laras Ayuningtyas",
    note: "Ssst... kata Kiki si peri kecil, di hutan jamur akan ada pesta kunang-kunang. Naura ulang tahun kelima, ayo datang!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-05-22T15:30:00+07:00",
  place: "Taman Kupu-Kupu Cihanjuang",
  address: "Jl. Cihanjuang No. 71, Cibabat, Cimahi Utara, Kota Cimahi",
  story: { title: "Cerita Naura", body: "" },
  stories: [
    { date: "2022", title: "Bunga pertama mekar", body: "Naura lahir di suatu sore bulan Mei, saat hujan baru reda dan langit berwarna lembayung." },
    { date: "2024", title: "Penjelajah kebun", body: "Mulai suka jongkok lama di kebun, mengamati semut, kupu-kupu, dan jamur kecil sehabis hujan." },
    { date: "2027", title: "Lima tahun ajaib", body: "Sekarang pintar bercerita tentang peri yang tinggal di bawah jamur, dan ingin pesta di hutan." },
  ],
  events: [
    { name: "Pesta Hutan Peri", date: "2027-05-22T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Taman Kupu-Kupu Cihanjuang", address: "Jl. Cihanjuang No. 71, Cibabat, Cimahi Utara, Kota Cimahi" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "7810 4422 19", account_name: "Laras Ayuningtyas" },
    { id: "demo-kado", type: "address", address: "Jl. Melong Asih No. 9, Cijerah, Bandung Kulon, Kota Bandung 40213" },
  ],
  guestName: "Adik Raisa & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Naura Elvina Safitri", nickname: "Naura", birthDate: "2022-05-22T16:20:00+07:00", parents: "Putri pertama dari Bapak Dimas Prasetya & Ibu Laras Ayuningtyas" },
    rundown: { items: [
      { time: "15.30", title: "Datang & pakai sayap peri", note: "Meja sayap & mahkota bunga di gerbang taman" },
      { time: "16.00", title: "Berburu jamur ajaib", note: "Cari jamur kertas tersembunyi di taman" },
      { time: "16.45", title: "Tiup lilin kue jamur", note: "Nyanyi bersama" },
      { time: "17.20", title: "Lampion kunang-kunang & bingkisan" },
    ] },
    dressCode: { note: "Warna senja dan bunga: ungu, merah muda, hijau mint. Sayap dan mahkota bunga sangat boleh!", colors: ["#7d5bc4", "#f59ab9", "#9ad8c4", "#ffd98a"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Prasetya", "Eyang Kakung & Eyang Putri Ayuningtyas", "Om Bagas & Tante Mila"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini kesukaan Naura.", items: [
      { id: "w1", name: "Buku cerita bergambar peri hutan", price: "± Rp85.000" },
      { id: "w2", name: "Set cat air anak", price: "± Rp70.000", claimed_by: "Tante Rini" },
      { id: "w3", name: "Lampu tidur bentuk jamur", price: "± Rp110.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada gazebo teduh dan teh hangat untuk Ayah & Bunda." },
      { q: "Bagaimana kalau hujan?", a: "Pesta pindah ke aula kaca di tengah taman, tetap seru." },
    ] },
  },
});
