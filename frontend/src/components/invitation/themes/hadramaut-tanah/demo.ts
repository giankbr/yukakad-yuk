import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Fathimah", groom: "Umar",
    brideFull: "Fathimah Zahra Baraqbah, S.Farm.", groomFull: "Umar Faruq Bawazier, S.E.",
    brideParents: "Putri ketiga dari\nBapak H. Hasan Ali Baraqbah & Ibu Hj. Khadijah Assegaf",
    groomParents: "Putra kedua dari\nBapak H. Salim Abdullah Bawazier & Ibu Hj. Nur Laila",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/a113.webp",
    note: "Seperti rumah tanah yang berdiri ratusan tahun, semoga ikatan kami kokoh karena dibangun dengan sabar, doa, dan restu keluarga.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-08-21T19:00:00+07:00",
  place: "Gedung Serbaguna Ampel Suci",
  address: "Jl. Ampel Suci No. 12, Ampel, Semampir, Surabaya",
  stories: [
    { date: "2021", title: "Haul di Kampung Ampel", body: "Keluarga kami bertetangga lama. Kami saling melihat di dapur umum saat persiapan haul, membagi gulai kambing dan teh susu." },
    { date: "2025", title: "Ta'aruf", body: "Atas perantaraan bibi Fathimah, kami bertukar kabar dengan niat baik dan saling mengenal didampingi keluarga." },
    { date: "Mei 2027", title: "Khitbah", body: "Keluarga Bawazier datang membawa seserahan dan diiringi marawis; lamaran diterima dengan penuh syukur." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-21T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Agung Sunan Ampel", address: "Jl. Ampel Masjid No. 53, Ampel, Semampir, Surabaya" },
    { name: "Walimah", date: "2027-08-21T19:00:00+07:00", time: "19.00 – 22.00 WIB", venue: "Gedung Serbaguna Ampel Suci", address: "Jl. Ampel Suci No. 12, Ampel, Semampir, Surabaya" },
  ],
  gallery: ["/themes/img/r64.webp", "/themes/img/a31.webp", "/themes/img/a123.webp", "/themes/img/a30.webp", "/themes/img/r89.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7155 2093 41", account_name: "Fathimah Zahra Baraqbah" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0881 4426 70", account_name: "Umar Faruq Bawazier" },
    { id: "demo-kado", type: "address", address: "Jl. Nyamplungan Gg. 3 No. 8, Ampel, Semampir, Surabaya 60151", account_name: "Keluarga H. Hasan Ali Baraqbah" },
  ],
  guestName: "Bapak H. Abdurrahman Bin Thalib & Keluarga",
  guestTable: "Meja Tarim 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "19.00", title: "Penyambutan tamu", note: "Gahwa & kurma" },
      { time: "19.30", title: "Pembacaan maulid & doa" },
      { time: "20.15", title: "Santap malam", note: "Nasi kebuli & gulai kambing" },
      { time: "21.00", title: "Marawis & gambus" },
    ] },
    dressCode: { note: "Busana muslim bernuansa tanah: cokelat bata, krem kapur, pasir, dan biru senja.", colors: ["#b27a4a", "#f4ede0", "#e8c79a", "#3c4f74"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Hasan Ali Baraqbah", "Kel. Besar H. Salim Abdullah Bawazier"] },
  },
});
