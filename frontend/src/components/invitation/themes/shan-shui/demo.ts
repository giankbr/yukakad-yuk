import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Meilani", groom: "Hendra",
    brideFull: "Felicia Meilani Halim, B.Arch.", groomFull: "Hendrawan Wijaya Tanoto, S.Kom.",
    brideParents: "Putri kedua dari\nBapak Halim Gunawan & Ibu Lie Siu Lan",
    groomParents: "Putra sulung dari\nBapak Tjandra Wijaya & Ibu Tan Mei Hwa",
    note: "Seperti gunung dan kabut dalam lukisan lama: berbeda rupa, tetapi saling melengkapi dan tak pernah benar-benar terpisah.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T09:00:00+07:00",
  place: "Ballroom Taman Sari Semarang",
  address: "Jl. Pahlawan No. 8, Pleburan, Semarang Selatan, Kota Semarang, Jawa Tengah",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Juli 2021", title: "Kelas Kaligrafi Tinta", body: "Meilani datang untuk belajar melukis gunung, Hendra datang menemani neneknya. Kami berbagi satu batang tinta dan satu cerita yang tidak selesai sore itu." },
    { date: "2022 – 2026", title: "Mendaki Bersama", body: "Dari kabut pagi di Dieng sampai kebun teh Medini, kami belajar bahwa perjalanan yang pelan sering kali paling indah." },
    { date: "Februari 2027", title: "Sangjit & Lamaran", body: "Pada hari baik setelah Imlek, keluarga Hendra datang membawa seserahan sangjit. Kedua keluarga sepakat menyatukan dua cerita menjadi satu." },
  ],
  events: [
    { name: "Upacara Minum Teh (Tea Pai)", date: "2027-08-21T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Kediaman Keluarga Halim", address: "Jl. Gajahmada No. 112, Kembangsari, Semarang Tengah, Kota Semarang" },
    { name: "Pemberkatan Pernikahan Buddhis", date: "2027-08-21T11:00:00+07:00", time: "11.00 – 12.30 WIB", venue: "Vihara Buddhagaya Watugong", address: "Jl. Perintis Kemerdekaan, Pudakpayung, Banyumanik, Kota Semarang" },
    { name: "Resepsi", date: "2027-08-21T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Ballroom Taman Sari Semarang", address: "Jl. Pahlawan No. 8, Pleburan, Semarang Selatan, Kota Semarang, Jawa Tengah" },
  ],
  gallery: ["/themes/img/a116.webp", "/themes/img/a30.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0095 8812 46", account_name: "Felicia Meilani Halim" },
    { id: "demo-ocbc", type: "bank", bank_name: "OCBC", account_number: "6930 0517 7720", account_name: "Hendrawan Wijaya Tanoto" },
  ],
  guestName: "Bapak Liem Kok Siong & Keluarga",
  guestTable: "Meja Bambu 9",
  extras: {
    quote: { text: "Bila suami dan istri ingin bertemu kembali dalam kehidupan ini maupun kehidupan mendatang, hendaknya mereka memiliki keyakinan yang sama, sila yang sama, kemurahan hati yang sama, dan kebijaksanaan yang sama.", source: "Samajivina Sutta, Anguttara Nikaya 4.55" },
    rundown: { items: [
      { time: "18.30", title: "Penyambutan tamu", note: "Iringan guzheng & teh melati" },
      { time: "19.00", title: "Masuknya kedua mempelai & sambutan keluarga" },
      { time: "19.30", title: "Jamuan malam", note: "Hidangan Tionghoa peranakan, vegetarian tersedia" },
      { time: "20.30", title: "Bersulang & foto bersama" },
    ] },
    dressCode: { note: "Nuansa lukisan tinta: abu batu, hijau giok pucat, krem sutra, dengan sentuhan merah.", colors: ["#3a3834", "#86a39a", "#ece3cc", "#b8322a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-21T11:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Halim Gunawan", "Kel. Besar Tjandra Wijaya"] },
    faq: { items: [
      { q: "Apakah tamu boleh menghadiri pemberkatan di vihara?", a: "Boleh. Mohon berpakaian sopan dan melepas alas kaki di area dhammasala." },
      { q: "Apakah tersedia menu vegetarian?", a: "Ya, tersedia meja vegetarian khusus. Cantumkan di kolom pantangan makanan saat konfirmasi." },
    ] },
  },
});
