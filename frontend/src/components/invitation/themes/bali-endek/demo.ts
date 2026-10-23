import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Saras", groom: "Wira",
    brideFull: "Ni Luh Putu Ayu Saraswati, S.Sn.", groomFull: "I Wayan Wiradharma, S.T.",
    brideParents: "Putri pertama dari\nBapak I Nyoman Sudarsana & Ibu Ni Made Sriani", groomParents: "Putra pertama dari\nBapak I Ketut Darmayasa & Ibu Ni Wayan Suartini",
    bridePhoto: "/themes/img/a62.webp", groomPhoto: "/themes/img/a60.webp",
    note: "Seperti sawah yang berundak menuruni lembah, kami ingin melangkah setahap demi setahap, saling mengairi dan bertumbuh bersama.",
  },
  eventLabel: "Pawiwahan",
  date: "2027-09-18T09:00:00+08:00",
  place: "Wantilan Desa Adat Peliatan",
  address: "Jl. Raya Peliatan, Peliatan, Kec. Ubud, Kabupaten Gianyar, Bali",
  stories: [
    { date: "2018", title: "Sanggar Tari", body: "Saras menari legong di sebuah sanggar di Peliatan, Wira menabuh gamelan di barisan belakang. Kami berkenalan selepas latihan sore." },
    { date: "2023", title: "Di Pematang Sawah", body: "Jalan sore menyusuri subak di Petulu menjadi kebiasaan kami, sambil membicarakan rumah dan keluarga yang ingin kami jaga." },
    { date: "2027", title: "Memadik", body: "Keluarga Wira datang memadik dengan tata adat Bali. Dengan restu kedua keluarga, dewasa ayu pun ditetapkan." },
  ],
  events: [
    { name: "Upacara Pawiwahan", date: "2027-09-18T09:00:00+08:00", time: "09.00 – 12.00 WITA", venue: "Griya Keluarga Mempelai Pria", address: "Banjar Petulu Gunung, Desa Petulu, Kec. Ubud, Kabupaten Gianyar, Bali" },
    { name: "Resepsi", date: "2027-09-18T18:30:00+08:00", time: "18.30 – 21.30 WITA", venue: "Wantilan Desa Adat Peliatan", address: "Jl. Raya Peliatan, Peliatan, Kec. Ubud, Kabupaten Gianyar, Bali" },
  ],
  gallery: ["/themes/img/a64.webp", "/themes/img/r108.webp", "/themes/img/a73.webp", "/themes/img/a71.webp", "/themes/img/a62.webp"],
  gifts: [
    { id: "demo-bpd", type: "bank", bank_name: "BPD Bali", account_number: "0200 2023 4567 8", account_name: "I Wayan Wiradharma" },
    { id: "demo-kado", type: "address", address: "Banjar Petulu Gunung No. 7, Desa Petulu, Kec. Ubud, Kabupaten Gianyar, Bali 80571" },
  ],
  guestName: "Bapak I Made Suarjana & Keluarga",
  guestTable: "Bale Subak 3",
  extras: {
    quote: { text: "Wahai pasangan pengantin, tetaplah kalian bersatu di sini, jangan terpisahkan. Nikmatilah hidup sepanjang umur, bergembira di rumah sendiri bersama anak dan cucu.", source: "Rgveda X.85.42" },
    rundown: { items: [
      { time: "18.30", title: "Penyambutan tamu", note: "Diiringi gamelan" },
      { time: "19.00", title: "Tari penyambutan" },
      { time: "19.30", title: "Ramah tamah & jamuan" },
      { time: "20.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana adat Bali madya atau kain endek. Hijau giok, magenta, dan kuning kunyit dipersilakan.", colors: ["#1d6b66", "#b2306a", "#e3a52e", "#f1e8d2"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar I Ketut Darmayasa", "Kel. Besar I Nyoman Sudarsana"] },
  },
});
