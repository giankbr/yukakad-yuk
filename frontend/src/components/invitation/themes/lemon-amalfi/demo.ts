import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Gabriela", groom: "Rafael",
    brideFull: "Gabriela Maria Djogo, S.Par.", groomFull: "Rafael Adrian Mamahit, S.Kom.",
    brideParents: "Putri sulung dari\nBapak Yohanes Djogo & Ibu Maria Goreti Seda", groomParents: "Putra ketiga dari\nBapak Fransiskus Mamahit & Ibu Theresia Lumentut",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/a96.webp",
    note: "Matahari, laut, dan sekeranjang lemon segar. Kami menanti Anda di tepi tebing.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-11T09:00:00+08:00",
  place: "Taman Lemon Batu Cermin",
  address: "Jl. Batu Cermin No. 5, Wae Kelambu, Komodo, Manggarai Barat, NTT",
  stories: [
    { date: "Juli 2022", title: "Satu Kapal Wisata", body: "Gabriela memandu tur pulau-pulau Labuan Bajo. Rafael, wisatawan dari Manado, lupa membawa topi dan dipinjami topi jerami miliknya." },
    { date: "2024", title: "Limun di Pelabuhan", body: "Setiap sore kami berbagi segelas limun lemon di warung pelabuhan sambil menunggu matahari tenggelam." },
    { date: "Maret 2027", title: "Lamaran di Atas Perahu", body: "Rafael menyembunyikan cincin di dalam keranjang lemon. Gabriela menemukannya setelah membelah buah ketiga." },
  ],
  events: [
    { name: "Sakramen Perkawinan", date: "2027-09-11T09:00:00+08:00", time: "09.00 – 11.00 WITA", venue: "Gereja Stella Maris Labuan Bajo", address: "Jl. Soekarno-Hatta No. 21, Labuan Bajo, Komodo, Manggarai Barat, NTT" },
    { name: "Resepsi di Tebing", date: "2027-09-11T16:00:00+08:00", time: "16.00 – 20.00 WITA", venue: "Taman Lemon Batu Cermin", address: "Jl. Batu Cermin No. 5, Wae Kelambu, Komodo, Manggarai Barat, NTT" },
  ],
  gallery: ["/themes/img/r11.webp", "/themes/img/r65.webp", "/themes/img/r105.webp", "/themes/img/r15.webp", "/themes/img/r38.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "4521 0100 3387 506", account_name: "Gabriela Maria Djogo" },
    { id: "demo-mandiri", type: "bank", bank_name: "Bank Mandiri", account_number: "150 00 2266 8841", account_name: "Rafael Adrian Mamahit" },
    { id: "demo-kado", type: "address", address: "Jl. Pantai Pede No. 3, Gorontalo, Komodo, Manggarai Barat, NTT 86754" },
  ],
  guestName: "Bapak Agustinus Bere & Keluarga",
  guestTable: "Meja Limone 6",
  extras: {
    quote: { text: "Air yang banyak tidak dapat memadamkan cinta, sungai-sungai tidak dapat menghanyutkannya.", source: "Kidung Agung 8:7" },
    rundown: { items: [
      { time: "16.00", title: "Limun selamat datang & musik akustik", note: "Taman lemon" },
      { time: "16.45", title: "Kedua mempelai tiba di tebing" },
      { time: "17.30", title: "Bersulang menjelang matahari terbenam" },
      { time: "18.15", title: "Makan malam keluarga & dansa" },
    ] },
    dressCode: { note: "Cerah dan segar seperti siang di tepi laut: kuning lemon, biru kobalt, hijau daun, dan putih. Alas kaki datar untuk rumput.", colors: ["#f5cf2e", "#1f4f9c", "#5d8a3c", "#fbf8ef"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Yohanes Djogo", "Kel. Besar Bpk. Fransiskus Mamahit"] },
    travel: { note: "Penerbangan ke Bandara Komodo (LBJ) tersedia setiap hari dari Jakarta dan Denpasar.", items: [
      { name: "Antar-jemput", detail: "Shuttle dari bandara & hotel tepi pelabuhan pukul 15.00" },
      { name: "Menginap", detail: "Hotel di sekitar Pantai Pede, kode tamu LIMONE" },
    ] },
  },
});
