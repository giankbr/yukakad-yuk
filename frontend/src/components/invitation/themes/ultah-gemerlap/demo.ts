import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "",
    note: "Tiga puluh tahun penuh syukur. Malam ini, mari rayakan bersama orang-orang tersayang.",
    brideFull: "Nadia Putri Maharani",
    brideParents: "Putri dari Bapak Surya Maharani & Ibu Lestari",
    bridePhoto: "/themes/img/r27.webp",
  },
  eventLabel: "Ulang Tahun ke-30",
  date: "2027-07-17T19:00:00+07:00",
  place: "Langit Rooftop Lounge",
  address: "Jl. Senopati No. 88, Lt. 21, Kebayoran Baru, Jakarta Selatan",
  story: { title: "", body: "" },
  stories: [
    { date: "1997", title: "Bintang kecil lahir", body: "Lahir di Yogyakarta pada suatu malam berbintang di bulan Juli." },
    { date: "2015", title: "Merantau ke Jakarta", body: "Kuliah, kos pertama, dan pertemanan yang masih bertahan sampai hari ini." },
    { date: "2027", title: "Kepala tiga", body: "Lebih tenang, lebih berani, dan semakin bersyukur atas setiap orang yang hadir di hidupnya." },
  ],
  events: [
    { name: "Makan Malam Bersama", date: "2027-07-17T19:00:00+07:00", time: "19.00 – 21.00 WIB", venue: "Langit Rooftop Lounge", address: "Jl. Senopati No. 88, Lt. 21, Kebayoran Baru, Jakarta Selatan" },
    { name: "Gemerlap After Party", date: "2027-07-17T21:00:00+07:00", time: "21.00 – 23.30 WIB", venue: "Langit Rooftop Lounge · Sky Deck", address: "Jl. Senopati No. 88, Lt. 22, Kebayoran Baru, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/r19.webp", "/themes/img/r27.webp", "/themes/img/r2.webp", "/themes/img/r24.webp", "/themes/img/r20.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5530 221 987", account_name: "Nadia Putri Maharani" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "ovo", ewallet_number: "0811 9090 3030", account_name: "Nadia Putri" },
  ],
  guestName: "Kak Rendra & Partner",
  guestTable: "VIP 3",
  extras: {
    quote: { text: "Bertambah usia bukan soal berapa lama kita hidup, tetapi seberapa dalam kita mensyukurinya.", source: "Catatan Nadia" },
    rundown: { items: [
      { time: "19.00", title: "Welcome drink & foto", note: "Photo booth emas di pintu masuk" },
      { time: "19.30", title: "Makan malam" },
      { time: "20.45", title: "Tiup lilin & potong kue" },
      { time: "21.00", title: "After party", note: "DJ & live acoustic" },
    ] },
    dressCode: { note: "Black & gold glam. Sentuhan payet atau metalik sangat dianjurkan.", colors: ["#0d0b1e", "#d9b45a", "#f3dc9b", "#2a2350"] },
    guestPass: {},
    rsvpDietary: {},
    faq: { items: [
      { q: "Boleh membawa pasangan?", a: "Boleh. Cantumkan jumlah tamu saat konfirmasi agar kursimu disiapkan." },
      { q: "Ada area parkir?", a: "Parkir basement tersedia, akses lift langsung ke lantai 21." },
    ] },
  },
});
