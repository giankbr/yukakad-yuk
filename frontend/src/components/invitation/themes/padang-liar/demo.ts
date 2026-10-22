import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kezia", groom: "Samuel",
    brideFull: "Kezia Anindita Putri, S.P.", groomFull: "Samuel Adiwangsa Hartanto, S.T.",
    brideParents: "Putri kedua dari\nBapak Yohanes Widodo & Ibu Maria Sulistyowati", groomParents: "Putra sulung dari\nBapak Daniel Hartanto & Ibu Ruth Kusumaningrum",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r26.webp",
    note: "Kasih itu sabar; kasih itu murah hati. Ia tidak cemburu, tidak memegahkan diri dan tidak sombong. (1 Korintus 13:4)",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T09:00:00+07:00",
  place: "Taman Bunga Selecta",
  address: "Jl. Raya Selecta No. 1, Tulungrejo, Bumiaji, Kota Batu, Jawa Timur",
  stories: [
    { date: "2019", title: "Bibit Pertama", body: "Kami berkenalan di kebun pembibitan kampus pertanian di Malang. Kezia menanam cosmos, Samuel sibuk memperbaiki pompa air." },
    { date: "2022", title: "Musim Berbunga", body: "Setiap akhir pekan kami bersepeda ke ladang bunga di Batu, pulang membawa seikat bunga liar dan cerita baru." },
    { date: "2026", title: "Di Tengah Padang", body: "Di antara bunga matahari yang sedang mekar, Samuel berlutut dan bertanya. Jawabannya, tentu saja, ya." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-05-15T09:00:00+07:00", time: "09.00 – 11.00 WIB", venue: "GKJW Jemaat Batu", address: "Jl. Diponegoro No. 7, Sisir, Kota Batu, Jawa Timur" },
    { name: "Resepsi di Taman", date: "2027-05-15T16:00:00+07:00", time: "16.00 – 19.00 WIB", venue: "Taman Bunga Selecta", address: "Jl. Raya Selecta No. 1, Tulungrejo, Bumiaji, Kota Batu, Jawa Timur" },
  ],
  gallery: ["/themes/img/r8.webp", "/themes/img/a111.webp", "/themes/img/r1.webp", "/themes/img/a22.webp", "/themes/img/r27.webp", "/themes/img/a116.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "3150 2277 81", account_name: "Kezia Anindita Putri" },
    { id: "demo-kado", type: "address", address: "Jl. Bukit Berbunga No. 22, Sidomulyo, Kota Batu, Jawa Timur 65317" },
  ],
  guestName: "Ibu Lidya Rahardjo & Keluarga",
  guestTable: "Meja Cosmos 3",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "16.00", title: "Penyambutan tamu", note: "Teh bunga & limun di gerbang taman" },
      { time: "16.30", title: "Doa syukur & pemotongan kue" },
      { time: "17.15", title: "Makan malam di rumput" },
      { time: "18.15", title: "Lempar buket & foto bersama" },
    ] },
    dressCode: { note: "Busana pesta kebun warna lembut. Sepatu datar disarankan karena acara di atas rumput.", colors: ["#f2a9c4", "#fbf3dc", "#8fa8e8", "#a4c06a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-05-15T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Yohanes Widodo", "Kel. Besar Bpk. Daniel Hartanto", "Persekutuan Pemuda GKJW Batu"] },
    faq: { items: [
      { q: "Acaranya di luar ruangan?", a: "Resepsi di taman terbuka. Tersedia tenda bila hujan, dan udara Batu cukup sejuk menjelang malam." },
      { q: "Apakah ada parkir?", a: "Parkir tersedia di area Selecta, berjalan kaki 3 menit ke taman." },
    ] },
  },
});
