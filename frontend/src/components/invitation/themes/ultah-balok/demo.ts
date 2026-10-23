import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Arsya", groom: "",
    brideFull: "Arsya Danendra Pratama",
    brideParents: "Putra pertama dari Bapak Yoga Pratama & Ibu Citra Maharani",
    note: "Arsya genap empat tahun! Ayo datang, kita bangun kota balok paling tinggi bersama, lalu tiup lilin dan makan kue.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-03-13T15:30:00+07:00",
  place: "Balai Warga Taman Melati",
  address: "Jl. Melati Raya Blok C No. 2, Perumahan Taman Melati, Kec. Sukmajaya, Kota Depok",
  story: { title: "Cerita Arsya", body: "" },
  stories: [
    { date: "2023", title: "Halo dunia!", body: "Arsya lahir di awal musim hujan. Mainan pertamanya adalah tiga balok kayu dari Kakek." },
    { date: "2025", title: "Menara pertama", body: "Arsya menyusun lima balok tanpa jatuh, lalu bertepuk tangan sendiri sambil tertawa keras." },
    { date: "2027", title: "Empat tahun!", body: "Sekarang Arsya sudah bisa membangun jembatan, rumah beratap segitiga, dan kota kecil di karpet ruang tamu." },
  ],
  events: [
    { name: "Pesta Kota Balok", date: "2027-03-13T15:30:00+07:00", time: "15.30 – 17.30 WIB", venue: "Balai Warga Taman Melati", address: "Jl. Melati Raya Blok C No. 2, Perumahan Taman Melati, Kec. Sukmajaya, Kota Depok" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0662 4471 30", account_name: "Citra Maharani" },
    { id: "demo-kado", type: "address", address: "Jl. Melati Raya Blok C No. 14, Perumahan Taman Melati, Kec. Sukmajaya, Kota Depok 16412" },
  ],
  guestName: "Adik Nayla & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Arsya Danendra Pratama", nickname: "Arsya", birthDate: "2023-03-10T07:20:00+07:00", parents: "Putra pertama dari Bapak Yoga Pratama & Ibu Citra Maharani" },
    rundown: { items: [
      { time: "15.30", title: "Datang & ambil tanda nama balok", note: "Setiap anak dapat satu balok huruf untuk dibawa pulang" },
      { time: "15.45", title: "Lomba menara balok tertinggi" },
      { time: "16.30", title: "Membangun kota bersama" },
      { time: "17.00", title: "Tiup lilin & potong kue" },
    ] },
    dressCode: { note: "Baju warna-warni seperti balok mainan: merah, kuning, biru, atau hijau.", colors: ["#e2412f", "#f6b928", "#2f6fd0", "#3aa25a"] },
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Pratama", "Opa & Oma Maharani"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini yang sedang Arsya sukai.", items: [
      { id: "w1", name: "Set balok kayu 100 keping", price: "± Rp250.000" },
      { id: "w2", name: "Buku cerita bergambar kota", price: "± Rp85.000", claimed_by: "Tante Rani" },
      { id: "w3", name: "Mobil-mobilan kayu", price: "± Rp120.000" },
    ] },
  },
});
