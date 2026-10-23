import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laras", groom: "Dion",
    brideFull: "Larasati Kusumawardhani", groomFull: "Dionisius Arya Wibisana",
    brideParents: "Putri sulung dari\nBapak Hendro Kusumo & Ibu Maria Sulistyowati",
    groomParents: "Putra kedua dari\nBapak Stefanus Wibisana & Ibu Lenny Hartati",
    bridePhoto: "/themes/img/r28.webp", groomPhoto: "/themes/img/r26.webp",
    note: "Hujan pertama kami jatuh di halte Jalan Braga. Sejak itu, setiap gerimis terasa seperti undangan untuk pulang bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-11-20T16:00:00+07:00",
  place: "Gedung Serbaguna Braga Sembilan",
  address: "Jl. Braga No. 9, Braga, Kec. Sumur Bandung, Kota Bandung",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "Nov 2021", title: "Satu Payung di Halte", body: "Hujan deras, bus terlambat, dan hanya Dion yang membawa payung. Laras menumpang sampai ujung jalan, lalu kami lupa berpamitan." },
    { date: "2022", title: "Kopi Setiap Kamis", body: "Ternyata kantor kami bersebelahan. Kamis sore jadi jadwal tetap: kopi, obrolan panjang, dan menunggu reda bersama." },
    { date: "Mar 2027", title: "Lamaran di Bawah Gerimis", body: "Di trotoar yang sama, Dion membuka payung kuning dan bertanya. Jawabannya: iya, tentu saja." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-11-20T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Gedung Serbaguna Braga Sembilan", address: "Jl. Braga No. 9, Braga, Kec. Sumur Bandung, Kota Bandung" },
    { name: "Resepsi Malam", date: "2027-11-20T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Teras Atap Braga Sembilan", address: "Lantai 5, Jl. Braga No. 9, Kota Bandung" },
  ],
  gallery: ["/themes/img/a122.webp", "/themes/img/r7.webp", "/themes/img/a140.webp", "/themes/img/r83.webp", "/themes/img/a39.webp", "/themes/img/r56.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4380 211 977", account_name: "Larasati Kusumawardhani" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 2044 7319", account_name: "Dionisius Arya Wibisana" },
  ],
  guestName: "Bapak Rudy Halim & Keluarga",
  guestTable: "Meja Payung 4",
  extras: {
    quote: { text: "Kita tidak menunggu badai berlalu. Kita belajar berjalan berdua di bawah hujan.", source: "Laras & Dion" },
    rundown: { items: [
      { time: "16.00", title: "Upacara pernikahan", note: "Keluarga & sahabat dekat" },
      { time: "18.30", title: "Resepsi dibuka" },
      { time: "19.30", title: "Makan malam & musik akustik" },
      { time: "21.00", title: "Foto bersama di bawah payung" },
    ] },
    dressCode: { note: "Semi formal malam hari: navy, abu, dan sentuhan kuning hangat. Payung disediakan di pintu masuk.", colors: ["#1d2738", "#5d6675", "#e9b46e", "#b9533c"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendro Kusumo", "Kel. Besar Bpk. Stefanus Wibisana"] },
    travel: { note: "Bandung sedang musim hujan. Berikut pilihan dekat lokasi untuk tamu dari luar kota.", items: [
      { name: "Stasiun Bandung", detail: "± 10 menit berkendara" },
      { name: "Parkir", detail: "Gedung parkir Braga, payung antar-jemput dari pintu parkir" },
    ] },
  },
});
