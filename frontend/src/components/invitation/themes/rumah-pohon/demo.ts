import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Dion",
    brideFull: "Sekar Ayu Maharani", groomFull: "Dionisius Adi Nugroho",
    brideParents: "Putri bungsu dari\nBapak Hendrik Wirawan & Ibu Maria Lestari", groomParents: "Putra pertama dari\nBapak Yohanes Nugroho & Ibu Theresia Wulan",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Kami sudah membangun rumah kecil di atas pohon. Tangganya sudah dipasang, lampunya sudah menyala, tinggal kamu yang datang.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T15:00:00+07:00",
  place: "Dusun Bambu",
  address: "Jl. Kolonel Masturi No. KM. 11, Kertawangi, Cisarua, Kabupaten Bandung Barat",
  stories: [
    { date: "2019", title: "Hujan di Perkemahan", body: "Kami bertemu di perkemahan pramuka alumni. Tenda Dion bocor, dan Sekar meminjamkan terpal cadangannya." },
    { date: "2022", title: "Rumah Pohon Pertama", body: "Bersama keponakan-keponakan, kami membangun rumah pohon kecil di halaman rumah nenek di Lembang." },
    { date: "2027", title: "Naik ke Atas Bersama", body: "Di bawah lampu-lampu kecil rumah pohon itu, Dion bertanya. Sekar menjawab ya sebelum ia selesai bicara." },
  ],
  events: [
    { name: "Janji Nikah", date: "2027-07-10T15:00:00+07:00", time: "15.00 – 16.00 WIB", venue: "Dusun Bambu · Taman Lembah", address: "Jl. Kolonel Masturi No. KM. 11, Kertawangi, Cisarua, Kabupaten Bandung Barat" },
    { name: "Resepsi Senja di Hutan", date: "2027-07-10T17:00:00+07:00", time: "17.00 – 20.30 WIB", venue: "Dusun Bambu · Lutung Kasarung", address: "Jl. Kolonel Masturi No. KM. 11, Kertawangi, Cisarua, Kabupaten Bandung Barat" },
  ],
  gallery: ["/themes/img/a30.webp", "/themes/img/r84.webp", "/themes/img/a18.webp", "/themes/img/a22.webp", "/themes/img/r100.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5210 7788 12", account_name: "Sekar Ayu Maharani" },
    { id: "demo-kado", type: "address", address: "Jl. Raya Lembang No. 118, Gudangkahuripan, Lembang, Bandung Barat 40391" },
  ],
  guestName: "Mas Raka & Mbak Tia",
  guestTable: "Meja Cemara 4",
  extras: {
    rundown: { items: [
      { time: "17.00", title: "Sambutan & bersulang" },
      { time: "17.40", title: "Makan malam di bawah lampu gantung" },
      { time: "19.00", title: "Dansa pertama & api unggun kecil", note: "Bawa jaket, udara Lembang dingin" },
    ] },
    dressCode: { note: "Nuansa hutan sore: hijau lumut, kayu, mustard, dan krem. Sepatu datar sangat disarankan.", colors: ["#4e7c3c", "#9a6638", "#e8b43a", "#f4e6c8"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Bapak Hendrik Wirawan", "Kel. Bapak Yohanes Nugroho"] },
  },
});
