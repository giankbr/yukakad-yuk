import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Clarissa", groom: "Raditya",
    brideFull: "Clarissa Ayu Hartanto, S.Ds.", groomFull: "Raditya Bayu Wibisono, S.T.",
    brideParents: "Putri pertama dari\nBapak Yohanes Hartanto & Ibu Maria Kristina", groomParents: "Putra kedua dari\nBapak Antonius Wibisono & Ibu Lidia Susanti",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Seperti baris-baris lavender yang tumbuh searah, kami ingin terus berjalan menuju rumah yang sama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T10:00:00+07:00",
  place: "Rumah Batu Arunika",
  address: "Jl. Kolonel Masturi Km. 8, Cikole, Lembang, Kabupaten Bandung Barat",
  stories: [
    { date: "2021", title: "Kelas Melukis", body: "Kami duduk bersebelahan di kelas melukis gouache akhir pekan. Raditya selalu kehabisan warna ungu dan meminjam milik Clarissa." },
    { date: "2024", title: "Musim Panas yang Panjang", body: "Perjalanan pertama berdua menyusuri kebun bunga di Lembang, dengan bekal roti, keju, dan sebotol teh dingin." },
    { date: "2026", title: "Di Antara Baris Ungu", body: "Di ujung jalan setapak menuju rumah batu, Raditya berlutut dan bertanya. Jawabannya: ya." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-07-10T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Gereja Santo Laurentius", address: "Jl. Sukajadi No. 223, Sukagalih, Sukajadi, Kota Bandung" },
    { name: "Resepsi Taman", date: "2027-07-10T16:00:00+07:00", time: "16.00 – 20.00 WIB", venue: "Rumah Batu Arunika", address: "Jl. Kolonel Masturi Km. 8, Cikole, Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: ["/themes/img/r16.webp", "/themes/img/r104.webp", "/themes/img/r8.webp", "/themes/img/a111.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "2830 5521 07", account_name: "Clarissa Ayu Hartanto" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1300 0187 4422 9", account_name: "Raditya Bayu Wibisono" },
    { id: "demo-kado", type: "address", address: "Jl. Setiabudi No. 186, Hegarmanah, Cidadap, Kota Bandung 40141", account_name: "Clarissa & Raditya" },
  ],
  guestName: "Bapak Stefanus Gunawan & Keluarga",
  guestTable: "Meja Lavande 3",
  extras: {
    rundown: { items: [
      { time: "16.00", title: "Welcome drink di kebun", note: "Limun lavender & teh dingin" },
      { time: "17.00", title: "Makan malam di meja panjang" },
      { time: "18.15", title: "Dansa pertama saat matahari terbenam" },
      { time: "19.30", title: "Lampu taman & foto bersama" },
    ] },
    dressCode: { note: "Garden formal. Lilac, krem, sage, atau putih gading. Sepatu nyaman untuk rumput.", colors: ["#8a73bf", "#efe3cc", "#8f9b63", "#f8f3ea"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Yohanes Hartanto", "Kel. Besar Antonius Wibisono"] },
  },
});
