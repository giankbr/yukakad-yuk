import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Syafiqah", groom: "Hafizh",
    brideFull: "Tengku Nur Syafiqah", groomFull: "Muhammad Hafizh Azhari, S.T.",
    brideParents: "Putri dari Bapak Tengku Said Abdurrahman\n& Ibu Hj. Wan Mardiah", groomParents: "Putra dari Bapak H. Zulkarnain Azhari\n& Ibu Hj. Siti Rahmah",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Sungai Siak airnya tenang,\nTempat sampan berlabuh di tepian;\nDua hati sudah dipertemukan,\nMohon doa agar kekal berpanjangan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T08:00:00+07:00",
  place: "Masjid Raya Syahabuddin",
  address: "Jl. Sultan Syarif Kasim, Kampung Dalam, Kec. Siak, Kabupaten Siak, Riau",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2021", title: "Tepian Sungai Siak", body: "Pertama berjumpa di Festival Siak Bermadah. Syafiqah menari zapin, Hafizh mengatur pengeras suara yang tak mau berbunyi." },
    { date: "2023", title: "Jembatan Tengku Agung", body: "Sepulang kerja di Pekanbaru, kami kerap singgah memandang lampu jembatan menyala di atas sungai." },
    { date: "Jan 2027", title: "Merisik & Meminang", body: "Keluarga Hafizh datang membawa tepak sirih. Kedua keluarga bermufakat dan menetapkan hari baik." },
    { date: "Juni 2027", title: "Bersanding", body: "Insyaallah kami bernikah di Masjid Syahabuddin dan bersanding di kota pusaka tempat kami bertemu." },
  ],
  events: [
    { name: "Malam Berinai", date: "2027-06-11T19:30:00+07:00", time: "19.30 WIB – selesai", venue: "Kediaman Keluarga Tengku Said", address: "Jl. Sultan Ismail No. 21, Kampung Dalam, Siak Sri Indrapura" },
    { name: "Akad Nikah", date: "2027-06-12T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Syahabuddin", address: "Jl. Sultan Syarif Kasim, Kampung Dalam, Kec. Siak, Kabupaten Siak, Riau" },
    { name: "Kenduri & Bersanding", date: "2027-06-12T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Balai Kerapatan Tinggi", address: "Jl. Sultan Syarif Hasyim, Kampung Dalam, Siak Sri Indrapura, Riau" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a72.webp", "/themes/img/a63.webp", "/themes/img/a27.webp"],
  gifts: [
    { id: "demo-brk", type: "bank", bank_name: "BRK Syariah", account_number: "8120 6127 0612", account_name: "Tengku Nur Syafiqah" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7306 1220 27", account_name: "Muhammad Hafizh Azhari" },
    { id: "demo-kado", type: "address", address: "Jl. Sultan Ismail No. 21, Kampung Dalam, Siak Sri Indrapura, Riau 28773" },
  ],
  guestName: "Bapak Datuk H. Syamsuar & Keluarga",
  guestTable: "Hamparan Songket 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Arak-arakan pengantin dengan kompang" },
      { time: "11.30", title: "Tepuk tepung tawar", note: "Oleh keluarga dan pemangku adat" },
      { time: "12.00", title: "Bersanding di pelaminan songket" },
      { time: "12.30", title: "Makan bersila hidangan Melayu" },
    ] },
    dressCode: { note: "Baju kurung, kebaya labuh, atau teluk belanga bersamping songket. Ungu, merah hati, dan emas dipersilakan.", colors: ["#3b1534", "#6d1b3a", "#d6a74a", "#f6ead8"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar Tengku Said Abdurrahman", "Keluarga Besar H. Zulkarnain Azhari", "Lembaga Adat Melayu Riau Kabupaten Siak"] },
    travel: { note: "Menuju Siak Sri Indrapura.", items: [
      { name: "Dari Pekanbaru", detail: "± 2 jam berkendara lewat Jalan Lintas Pekanbaru – Siak" },
      { name: "Parkir tamu", detail: "Lapangan Tugu Siak, 3 menit berjalan kaki ke Balai Kerapatan" },
    ] },
  },
});
