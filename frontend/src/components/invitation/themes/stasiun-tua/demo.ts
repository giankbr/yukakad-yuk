import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Arga",
    brideFull: "Sekar Ayu Larasati, S.Hum.", groomFull: "Argadinata Putra Wibisono, S.T.",
    brideParents: "Putri tunggal dari\nBapak Hendro Wicaksono & Ibu Ratna Pertiwi", groomParents: "Putra kedua dari\nBapak Bambang Sutrisno & Ibu Lilik Handayani",
    bridePhoto: "/themes/img/r40.webp", groomPhoto: "/themes/img/r41.webp",
    note: "Kami bertemu di peron yang sama, dan memutuskan untuk naik kereta yang sama sampai stasiun terakhir.",
  },
  eventLabel: "Pernikahan",
  date: "2027-11-13T10:00:00+07:00",
  place: "Lawang Sewu",
  address: "Jl. Pemuda No. 160, Sekayu, Semarang Tengah, Kota Semarang",
  stories: [
    { date: "Maret 2020", title: "Peron 2, Semarang Tawang", body: "Kereta pagi ke Yogyakarta terlambat dua puluh menit. Sekar meminjam pulpen untuk mengisi buku sketsanya, Arga tak pernah meminta pulpen itu kembali." },
    { date: "2022", title: "Perjalanan-perjalanan kecil", body: "Setiap akhir pekan kami memilih satu stasiun tua untuk dikunjungi: Ambarawa, Willem I, Jakarta Kota. Kami mengoleksi karcis cetaknya." },
    { date: "Juni 2027", title: "Karcis sekali jalan", body: "Di museum kereta, Arga menyerahkan karcis karton bertuliskan satu pertanyaan. Sekar menjawabnya dengan anggukan." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-11-13T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Lawang Sewu, Gedung A", address: "Jl. Pemuda No. 160, Sekayu, Semarang Tengah, Kota Semarang" },
    { name: "Resepsi Senja", date: "2027-11-13T17:30:00+07:00", time: "17.30 – 21.00 WIB", venue: "Halaman Lawang Sewu", address: "Jl. Pemuda No. 160, Sekayu, Semarang Tengah, Kota Semarang" },
  ],
  gallery: ["/themes/img/r61.webp", "/themes/img/r42.webp", "/themes/img/r40.webp", "/themes/img/r41.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0095 6627 381", account_name: "Sekar Ayu Larasati" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1350 0188 4426 1", account_name: "Argadinata Putra Wibisono" },
    { id: "demo-kado", type: "address", address: "Jl. Kepodang No. 21, Purwodinatan, Semarang Tengah, Kota Semarang 50137" },
  ],
  guestName: "Bapak Yohanes Setiadi & Keluarga",
  guestTable: "Gerbong 4",
  extras: {
    quote: { text: "Cinta tidak saling memandang, tetapi bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "17.30", title: "Peron dibuka", note: "Penyambutan tamu dan foto di lorong seribu pintu" },
      { time: "18.00", title: "Kedatangan pengantin", note: "Diiringi orkes keroncong" },
      { time: "18.30", title: "Jamuan makan malam" },
      { time: "20.00", title: "Dansa & lempar buket" },
    ] },
    dressCode: { note: "Vintage formal: kemeja, batik, atau gaun klasik. Nuansa sepia, teal, dan kuningan.", colors: ["#2f6563", "#c49445", "#7a4a28", "#efe2c8"] },
    guestPass: { note: "Tunjukkan karcis ini kepada petugas peron saat tiba di lokasi." },
    family: { names: ["Kel. Besar Hendro Wicaksono (Semarang)", "Kel. Besar Bambang Sutrisno (Ambarawa)"] },
  },
});
