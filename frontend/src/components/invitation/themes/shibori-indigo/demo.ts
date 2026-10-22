import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Liliana", groom: "Hendra",
    brideFull: "Liliana Wijaya, S.Ds.", groomFull: "Hendra Gunawan Tanoto, S.Kom.",
    brideParents: "Putri bungsu dari\nBapak Hartono Wijaya & Ibu Lily Susanti",
    groomParents: "Putra kedua dari\nBapak Wilson Tanoto & Ibu Meiliana Halim",
    note: "Seperti kain yang diikat lalu dicelup berulang kali, warna terindah lahir dari kesabaran. Kami memilih untuk terus belajar bersama, celup demi celup.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-25T09:00:00+07:00",
  place: "Aula Teratai Putih",
  address: "Jl. Diponegoro No. 18, Madras Hulu, Medan Polonia, Kota Medan",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2019", title: "Kelas Celup", body: "Liliana mengajar lokakarya shibori di sebuah ruang kreatif di Medan. Hendra datang menemani adiknya, lalu justru menjadi peserta yang paling tekun." },
    { date: "2022", title: "Kain Pertama", body: "Hendra menghadiahkan sehelai kain arashi buatannya sendiri. Lipatannya miring, warnanya belang, dan Liliana menyimpannya sampai hari ini." },
    { date: "Maret 2027", title: "Lamaran", body: "Kedua keluarga bertemu dalam jamuan teh sederhana dan bersepakat menyatukan dua rumah dalam satu doa." },
  ],
  events: [
    { name: "Pemberkatan Pernikahan", date: "2027-09-25T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Vihara Borobudur Medan", address: "Jl. Imam Bonjol No. 21, Jati, Medan Maimun, Kota Medan" },
    { name: "Resepsi", date: "2027-09-25T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Aula Teratai Putih", address: "Jl. Diponegoro No. 18, Madras Hulu, Medan Polonia, Kota Medan" },
  ],
  gallery: ["/themes/img/r82.webp", "/themes/img/a123.webp", "/themes/img/r83.webp", "/themes/img/a101.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "8205 1377 46", account_name: "Liliana Wijaya" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "106 00 1938 4421", account_name: "Hendra Gunawan Tanoto" },
  ],
  guestName: "Bapak Johan Setiawan & Keluarga",
  guestTable: "Meja Kumo 5",
  extras: {
    quote: { text: "Dengan lima cara seorang suami memperlakukan istrinya: dengan menghormatinya, dengan bersikap lemah lembut, dengan setia, dengan memercayakan urusan rumah tangga, dan dengan memberinya perhiasan. Dan istri yang diperlakukan demikian membalas kasihnya dengan sepenuh hati.", source: "Sigalovada Sutta, Digha Nikaya 31" },
    rundown: { items: [
      { time: "18.30", title: "Penyambutan tamu", note: "Teh melati di serambi" },
      { time: "19.00", title: "Masuknya kedua mempelai" },
      { time: "19.30", title: "Jamuan makan malam" },
      { time: "20.30", title: "Foto bersama keluarga & sahabat" },
    ] },
    dressCode: { note: "Nuansa indigo, biru tua, dan putih kapas. Busana rapi dan sederhana.", colors: ["#1c2f5e", "#5b74a6", "#c7d0e0", "#efede6"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-25T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hartono Wijaya", "Kel. Besar Bpk. Wilson Tanoto"] },
    travel: { note: "Untuk tamu dari luar kota, berikut pilihan menginap di sekitar lokasi.", items: [
      { name: "Hotel di kawasan Jl. Diponegoro", detail: "± 300 m dari aula, bisa berjalan kaki" },
      { name: "Dari Bandara Kualanamu", detail: "Kereta bandara ke Stasiun Medan, lalu ± 10 menit berkendara" },
    ] },
    wishlist: { items: [
      { id: "w1", name: "Set teko & cangkir keramik", price: "± Rp700.000" },
      { id: "w2", name: "Rak buku kayu jati", price: "± Rp1.800.000", claimed_by: "Ko Andi" },
      { id: "w3", name: "Tabungan rumah pertama", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Apakah tamu boleh mengikuti pemberkatan?", a: "Tentu. Mohon berpakaian sopan dan melepas alas kaki di dalam ruang Dhammasala." },
      { q: "Apakah tersedia parkir?", a: "Parkir tersedia di halaman aula dan gedung parkir sebelahnya." },
    ] },
  },
});
