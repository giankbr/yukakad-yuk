import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Anjani", groom: "Raditya",
    brideFull: "Anjani Kusumawardhani, S.Ds.", groomFull: "Raditya Wicaksana, M.Sc.",
    brideParents: "Putri sulung dari\nBapak Hendro Kusumo & Ibu Widyastuti", groomParents: "Putra ketiga dari\nBapak Iwan Wicaksana & Ibu Ratih Kurniasari",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
    note: "Kami bertemu di tepi kolam pada suatu pagi berkabut, dan sejak itu setiap pagi terasa seperti lukisan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-26T08:00:00+07:00",
  place: "Paviliun Telaga Seroja, Bogor",
  address: "Jl. Pajajaran Indah No. 23, Baranangsiang, Bogor Timur, Kota Bogor",
  stories: [
    { date: "Agustus 2020", title: "Kelas Melukis Pagi", body: "Anjani mengajar kelas melukis cat air di tepi kolam teratai. Raditya datang untuk memotret burung, lalu ikut duduk dan mencoba melukis untuk pertama kalinya." },
    { date: "2023", title: "Jembatan Kayu", body: "Kami membangun jembatan kayu kecil di halaman rumah keluarga, papan demi papan, setiap akhir pekan selama satu musim hujan." },
    { date: "Maret 2027", title: "Sekuntum Teratai", body: "Di jembatan itu, Raditya menyelipkan cincin di antara kelopak teratai yang baru mekar pagi itu." },
  ],
  events: [
    { name: "Janji Pernikahan", date: "2027-06-26T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Jembatan Kayu, Telaga Seroja", address: "Jl. Pajajaran Indah No. 23, Baranangsiang, Bogor Timur, Kota Bogor" },
    { name: "Jamuan Pagi & Resepsi", date: "2027-06-26T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Paviliun Telaga Seroja", address: "Jl. Pajajaran Indah No. 23, Baranangsiang, Bogor Timur, Kota Bogor" },
  ],
  gallery: ["/themes/img/a116.webp", "/themes/img/r16.webp", "/themes/img/r79.webp", "/themes/img/a22.webp", "/themes/img/r10.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4410 2287 30", account_name: "Anjani Kusumawardhani" },
    { id: "demo-permata", type: "bank", bank_name: "Permata", account_number: "9701 4433 1208", account_name: "Raditya Wicaksana" },
    { id: "demo-kado", type: "address", address: "Jl. Bangbarung Raya No. 7, Bantarjati, Bogor Utara, Kota Bogor 16153" },
  ],
  guestName: "Ibu Lucia Hendrawati & Keluarga",
  guestTable: "Meja Seroja 6",
  extras: {
    quote: { text: "Teratai tumbuh dari lumpur, tetapi mekar paling indah di bawah cahaya pagi. Begitulah kami ingin saling menumbuhkan.", source: "Anjani & Raditya" },
    rundown: { items: [
      { time: "10.00", title: "Jamuan pagi & teh melati", note: "Teras paviliun" },
      { time: "10.45", title: "Kedua mempelai menyeberangi jembatan" },
      { time: "11.15", title: "Ramah tamah & musik kecapi" },
      { time: "12.30", title: "Foto bersama di tepi kolam" },
    ] },
    dressCode: { note: "Pagi di tepi kolam: lilac lembut, biru air, merah muda teratai, dan hijau daun. Sepatu nyaman untuk jalan setapak berumput.", colors: ["#a69dc6", "#9fc0d6", "#f2b8c6", "#78a463", "#f4efe6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendro Kusumo", "Kel. Besar Bpk. Iwan Wicaksana"] },
    travel: { note: "Hindari jam padat Tol Jagorawi; berangkat lebih pagi atau gunakan KRL ke Stasiun Bogor.", items: [
      { name: "Parkir", detail: "Area parkir paviliun, ± 3 menit berjalan ke kolam" },
      { name: "Kereta", detail: "Stasiun Bogor, ± 15 menit berkendara" },
    ] },
  },
});
