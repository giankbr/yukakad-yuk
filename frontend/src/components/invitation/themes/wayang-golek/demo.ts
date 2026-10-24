import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Resti", groom: "Gilang",
    brideFull: "Resti Ayu Nurfitriani, S.Sn.", groomFull: "Gilang Permana Sudrajat, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Engkos Kosasih & Ibu Hj. Iis Rohaeti", groomParents: "Putra sulung dari\nBapak Dede Suryana & Ibu Nining Kurniasih",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Dua lalakon yang akhirnya dipentaskan dalam satu panggung.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T08:00:00+07:00",
  place: "Gedung Kesenian Sunan Ambu",
  address: "Jl. Buah Batu No. 212, Cijagra, Lengkong, Kota Bandung",
  stories: [
    { date: "2019", title: "Di Hareupeun Kelir", body: "Kami pertama bertemu di pagelaran wayang golek semalam suntuk di Purwakarta. Resti menabuh saron, Gilang menonton dari barisan paling depan." },
    { date: "2023", title: "Lalakon Panjang", body: "Seperti dalang yang sabar menuntun lakon, kami belajar saling menunggu dan saling menguatkan, bolak-balik Bandung dan Purwakarta." },
    { date: "2026", title: "Neundeun Omong", body: "Keluarga Gilang datang menyampaikan maksud baik. Dua keluarga sepakat memilih hari yang berkah untuk kami." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Agung Baing Yusuf", address: "Jl. Mayor Ishak Djuarsa, Nagri Kidul, Kec. Purwakarta, Kabupaten Purwakarta" },
    { name: "Resepsi & Pagelaran Golek", date: "2027-08-15T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Gedung Kesenian Sunan Ambu", address: "Jl. Buah Batu No. 212, Cijagra, Lengkong, Kota Bandung" },
  ],
  gallery: ["/themes/img/a64.webp", "/themes/img/a28.webp", "/themes/img/a29.webp", "/themes/img/a40.webp"],
  gifts: [
    { id: "demo-bjb", type: "bank", bank_name: "BJB", account_number: "0098 1234 5670 1", account_name: "Resti Ayu Nurfitriani" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7208 4411 93", account_name: "Gilang Permana Sudrajat" },
    { id: "demo-kado", type: "address", address: "Jl. Veteran No. 37, Nagri Tengah, Kec. Purwakarta, Kabupaten Purwakarta" },
  ],
  guestName: "Bapak Ujang Suhendar & Keluarga",
  guestTable: "Saung Degung",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Ngabagéakeun tamu", note: "Diiringi gamelan degung" },
      { time: "11.30", title: "Mapag panganten" },
      { time: "12.30", title: "Pagelaran wayang golek", note: "Lakon pendek, ± 60 menit" },
      { time: "14.00", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Kebaya atau batik bernuansa merah bata, hijau kelir, dan emas.", colors: ["#9c2a22", "#1f5a55", "#cf9d3c", "#f3e6c8"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Engkos Kosasih", "Kel. Besar Dede Suryana", "Sanggar Degung Pakuan Purwakarta"] },
  },
});
