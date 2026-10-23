import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Rizal",
    brideFull: "Fatimah Azzahra, S.Farm.", groomFull: "Muhammad Rizal, S.H. (Sutan Mangkuto)",
    brideParents: "Putri dari\nBapak H. Zainal Abidin Chaniago & Ibu Hj. Nurhayati Koto", groomParents: "Putra dari\nBapak Ir. Syafrizal Piliang & Ibu Yusnimar Tanjung",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Dengan restu ninik mamak dan kedua orang tua, kami melangkah bersama menuju rumah tangga yang diridhai Allah.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T08:30:00+07:00",
  place: "Balai Sidang Bung Hatta",
  address: "Jl. Istana No. 1, Benteng Pasar Atas, Guguk Panjang, Kota Bukittinggi",
  stories: [
    { date: "2019", title: "Di Bawah Jam Gadang", body: "Kami pertama berkenalan saat sama-sama menjadi panitia festival budaya di pelataran Jam Gadang." },
    { date: "2022", title: "Merantau", body: "Rizal merantau ke Jakarta, Zahra melanjutkan pendidikan apoteker di Padang. Jarak justru membuat kami yakin." },
    { date: "2026", title: "Maminang", body: "Keluarga Zahra datang maminang ke rumah keluarga Rizal sesuai adat Minang, membawa sirih dalam carano." },
    { date: "2027", title: "Baralek", body: "Kini, dengan restu ninik mamak, kami basandiang di pelaminan Bukittinggi." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T08:30:00+07:00", time: "08.30 – 10.00 WIB", venue: "Masjid Raya Bukittinggi", address: "Jl. Minangkabau, Pasar Atas, Guguk Panjang, Kota Bukittinggi" },
    { name: "Baralek (Resepsi)", date: "2027-09-18T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Balai Sidang Bung Hatta", address: "Jl. Istana No. 1, Benteng Pasar Atas, Guguk Panjang, Kota Bukittinggi" },
  ],
  gallery: ["/themes/img/a66.webp", "/themes/img/a72.webp", "/themes/img/a70.webp", "/themes/img/a63.webp"],
  gifts: [
    { id: "demo-nagari", type: "bank", bank_name: "Bank Nagari", account_number: "1001 0210 0456 78", account_name: "Fatimah Azzahra" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Muhammad Rizal" },
  ],
  guestName: "Bapak H. Erwin Datuak Rajo Sampono & Keluarga",
  guestTable: "Meja Bajamba 3",
  extras: {
    rundown: { items: [
      { time: "11.00", title: "Manjapuik marapulai", note: "Rombongan marapulai disambut tari galombang" },
      { time: "11.30", title: "Basandiang di pelaminan" },
      { time: "12.15", title: "Makan bajamba bersama", note: "Rendang, gulai cubadak, dan samba lado tanak" },
      { time: "13.30", title: "Pituah ninik mamak & doa" },
    ] },
    dressCode: { note: "Busana muslim atau baju kuruang. Merah, emas, dan hitam sangat dipersilakan.", colors: ["#8e1018", "#d4a640", "#1a0f0c", "#f6ead2"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Chaniago (Bukittinggi)", "Kel. Besar Piliang (Padang Panjang)"] },
  },
});
