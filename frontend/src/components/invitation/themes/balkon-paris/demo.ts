import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Felicia", groom: "Jonathan",
    brideFull: "Felicia Anggraini Wijaya, B.A.", groomFull: "Jonathan Halim Santoso, M.M.",
    brideParents: "Putri kedua dari\nBapak Hendra Wijaya & Ibu Lily Tanoto", groomParents: "Putra sulung dari\nBapak Budi Santoso Halim & Ibu Meilani Kurnia",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Secangkir kopi di bawah jendela berbunga, lalu ribuan pagi yang ingin kami jalani bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-04-24T10:00:00+07:00",
  place: "Maison Lilas, Braga",
  address: "Jl. Braga No. 58, Braga, Sumur Bandung, Kota Bandung",
  stories: [
    { date: "Musim semi 2020", title: "Kafe di Sudut Braga", body: "Felicia sedang menggambar jendela-jendela tua Braga ketika Jonathan bertanya apakah kursi di depannya kosong. Kursi itu tidak pernah kosong lagi." },
    { date: "2023", title: "Kelas Bahasa Prancis", body: "Kami belajar mengucapkan je t'aime dengan benar. Hasilnya masih mengecewakan, tapi kami tetap lulus bersama." },
    { date: "Desember 2026", title: "Lamaran di Balkon", body: "Jonathan menggantung rangkaian wisteria di balkon rumah Felicia dan menunggu sampai ia membuka jendela." },
  ],
  events: [
    { name: "Pemberkatan Pernikahan", date: "2027-04-24T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Vihara Dhamma Sukha", address: "Jl. Kebon Jati No. 112, Kebon Jeruk, Andir, Kota Bandung" },
    { name: "Resepsi", date: "2027-04-24T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Maison Lilas, Braga", address: "Jl. Braga No. 58, Braga, Sumur Bandung, Kota Bandung" },
  ],
  gallery: ["/themes/img/a131.webp", "/themes/img/r86.webp", "/themes/img/r92.webp", "/themes/img/a132.webp", "/themes/img/r93.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0882 4410 57", account_name: "Felicia Anggraini Wijaya" },
    { id: "demo-ocbc", type: "bank", bank_name: "OCBC", account_number: "6930 0221 4785", account_name: "Jonathan Halim Santoso" },
    { id: "demo-kado", type: "address", address: "Jl. Cihampelas No. 220, Cipaganti, Coblong, Kota Bandung 40131" },
  ],
  guestName: "Ibu Susanti Gunawan & Keluarga",
  guestTable: "Meja Lilas 4",
  extras: {
    quote: { text: "Bila suami dan istri ingin terus bersama, tidak hanya dalam kehidupan ini tetapi juga di kehidupan mendatang, hendaknya keduanya memiliki keyakinan yang sama, moralitas yang sama, kemurahan hati yang sama, dan kebijaksanaan yang sama.", source: "Samajivina Sutta, Anguttara Nikaya 4.55" },
    rundown: { items: [
      { time: "18.30", title: "Apéritif & musik akordeon", note: "Teras depan" },
      { time: "19.00", title: "Kedua mempelai memasuki ruangan" },
      { time: "19.30", title: "Makan malam ala bistro" },
      { time: "20.30", title: "Dansa pertama & potong kue" },
    ] },
    dressCode: { note: "Musim semi di Paris: lilac, krem batu, biru jendela, dan sedikit hitam besi. Sepatu nyaman untuk berdansa.", colors: ["#c4a3dc", "#eadcc2", "#7f93a6", "#2a2830"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendra Wijaya", "Kel. Besar Bpk. Budi Santoso Halim"] },
    travel: { note: "Jalan Braga padat di malam Minggu. Parkir valet tersedia di depan Maison Lilas.", items: [
      { name: "Parkir", detail: "Valet di depan gedung, atau parkir Braga City Walk" },
      { name: "Menginap", detail: "Hotel di sekitar Asia Afrika, ± 5 menit berjalan kaki" },
    ] },
  },
});
