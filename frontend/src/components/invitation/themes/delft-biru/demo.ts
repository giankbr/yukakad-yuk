import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Natalia", groom: "Yosua",
    brideFull: "Natalia Kusuma Dewi, S.Ds.", groomFull: "Gabriel Yosua Santoso, S.T.",
    brideParents: "Putri sulung dari\nBapak Robertus Hadi Kusuma & Ibu Elisabeth Sri Rahayu",
    groomParents: "Putra kedua dari\nBapak Daniel Santoso & Ibu Yohana Lestari",
    note: "Seperti ubin yang dipasang satu per satu, kami ingin menyusun rumah tangga dengan sabar, rapi, dan penuh warna kasih.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-22T10:00:00+07:00",
  place: "Gereja Blenduk (GPIB Immanuel Semarang)",
  address: "Jl. Letjen Suprapto No. 32, Tanjung Mas, Semarang Utara, Kota Semarang",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2019", title: "Ubin yang Retak", body: "Natalia sedang memotret ubin tua di sebuah rumah Kota Lama ketika Yosua, arsitek pemugaran, menegurnya agar tidak menginjak ubin yang retak." },
    { date: "2022", title: "Proyek Pemugaran", body: "Dua tahun bekerja di proyek yang sama: ia menggambar ulang motif ubin, ia memastikan dindingnya berdiri tegak." },
    { date: "Desember 2026", title: "Lamaran", body: "Di teras rumah keluarga, Yosua memberikan sebuah ubin biru yang ia lukis sendiri, dengan tulisan kecil di baliknya." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-05-22T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Gereja Blenduk (GPIB Immanuel Semarang)", address: "Jl. Letjen Suprapto No. 32, Tanjung Mas, Semarang Utara, Kota Semarang" },
    { name: "Resepsi", date: "2027-05-22T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Gedung Oudetrap Kota Lama", address: "Jl. Letjen Suprapto No. 34, Tanjung Mas, Semarang Utara, Kota Semarang" },
  ],
  gallery: ["/themes/img/a31.webp", "/themes/img/a116.webp", "/themes/img/a22.webp", "/themes/img/a18.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0093 4512 77", account_name: "Natalia Kusuma Dewi" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0124 0100 8876 501", account_name: "Gabriel Yosua Santoso" },
    { id: "demo-kado", type: "address", address: "Jl. Kepodang No. 21, Purwodinatan, Semarang Tengah, Kota Semarang 50137" },
  ],
  guestName: "Bapak Stefanus Wijaya & Keluarga",
  guestTable: "Meja Kincir 4",
  extras: {
    quote: { text: "Dan di atas semuanya itu: kenakanlah kasih, sebagai pengikat yang mempersatukan dan menyempurnakan.", source: "Kolose 3:14" },
    rundown: { items: [
      { time: "18.30", title: "Penyambutan tamu", note: "Lobi bergaya Indis, minuman selamat datang" },
      { time: "19.00", title: "Kirab pengantin & doa syukur" },
      { time: "19.30", title: "Makan malam", note: "Hidangan peranakan & Belanda-Indis" },
      { time: "20.30", title: "Foto bersama keluarga & sahabat" },
    ] },
    dressCode: { note: "Nuansa biru Delft dan putih gading. Kebaya, batik, atau jas dipersilakan.", colors: ["#13368a", "#5a7cc6", "#f7f6f0", "#d9dfeb"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-05-22T10:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Robertus Hadi Kusuma", "Kel. Besar Bpk. Daniel Santoso"] },
    travel: { note: "Untuk tamu dari luar kota, berikut pilihan menginap di sekitar Kota Lama.", items: [
      { name: "Penginapan di kawasan Kota Lama", detail: "± 500 m dari gereja, bisa berjalan kaki" },
      { name: "Parkir", detail: "Parkir Taman Srigunting, di samping Gereja Blenduk" },
    ] },
    wishlist: { items: [
      { id: "w1", name: "Set cangkir teh keramik", price: "± Rp650.000" },
      { id: "w2", name: "Lampu gantung bergaya Indis", price: "± Rp1.400.000", claimed_by: "Tante Maria" },
      { id: "w3", name: "Tabungan rumah pertama", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Boleh membawa anak?", a: "Tentu, anak-anak sangat diterima. Mohon didampingi selama ibadah pemberkatan." },
      { q: "Apakah tersedia parkir?", a: "Parkir tersedia di Taman Srigunting dan sekitar Kota Lama." },
    ] },
  },
});
