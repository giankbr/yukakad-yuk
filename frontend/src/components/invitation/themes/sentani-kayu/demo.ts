import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Retha", groom: "Yohan",
    brideFull: "Margaretha Ohee, S.Sos.", groomFull: "Yohanis Pepuho, S.T.",
    brideParents: "Putri pertama dari\nBapak Agus Ohee & Ibu Martha Monim", groomParents: "Putra ketiga dari\nBapak Kornelis Pepuho & Ibu Yuliana Yoku",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti ikan dan air di Danau Sentani, kami dipertemukan Tuhan untuk saling menghidupi.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T10:00:00+09:00",
  place: "Pantai Khalkote",
  address: "Kampung Harapan, Distrik Sentani Timur, Kabupaten Jayapura, Papua",
  stories: [
    { date: "2020", title: "Festival Danau Sentani", body: "Retha menari di atas perahu, Yohan mendokumentasikan festival untuk kantor distrik. Satu foto yang terlambat dikirim membuka percakapan panjang." },
    { date: "2023", title: "Belajar di Asei", body: "Kami belajar melukis kulit kayu bersama mama-mama di Pulau Asei. Di sana Yohan meminta izin keluarga untuk melamar Retha." },
    { date: "2027", title: "Pulang ke Danau", body: "Dengan restu ondofolo, keluarga besar, dan berkat Tuhan, kami siap membangun rumah di tepi danau tempat kami dibesarkan." },
  ],
  events: [
    { name: "Ibadah Pemberkatan Nikah", date: "2027-09-18T10:00:00+09:00", time: "10.00 – 12.00 WIT", venue: "Gereja GKI Betania Asei Besar", address: "Pulau Asei Besar, Distrik Sentani Timur, Kabupaten Jayapura" },
    { name: "Resepsi & Makan Bersama", date: "2027-09-18T16:00:00+09:00", time: "16.00 – 21.00 WIT", venue: "Pantai Khalkote", address: "Kampung Harapan, Distrik Sentani Timur, Kabupaten Jayapura" },
  ],
  gallery: ["/themes/img/r108.webp", "/themes/img/r15.webp", "/themes/img/r16.webp", "/themes/img/r13.webp", "/themes/img/r12.webp", "/themes/img/r10.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank Papua", account_number: "1504 0227 8810", account_name: "Margaretha Ohee" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "154 00 1188 2741", account_name: "Yohanis Pepuho" },
    { id: "demo-kado", type: "address", address: "Jl. Raya Sentani–Abepura, Kampung Harapan, Sentani Timur, Kabupaten Jayapura 99352" },
  ],
  guestName: "Bapak Daniel Wally & Keluarga",
  guestTable: "Meja Asei",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "16.00", title: "Penyambutan dengan tifa", note: "Tari isosolo dari perahu" },
      { time: "17.00", title: "Ibadah syukur keluarga" },
      { time: "18.00", title: "Makan bersama", note: "Papeda, ikan kuah kuning & sayur ganemo" },
      { time: "19.30", title: "Yospan bersama di pantai" },
    ] },
    dressCode: { note: "Busana rapi bernuansa tanah: cokelat kulit kayu, krem, merah oker, dan hitam. Motif khas Papua sangat dianjurkan.", colors: ["#8a5a34", "#eee3cf", "#a9472b", "#1d1612"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Ohee – Monim", "Kel. Besar Pepuho – Yoku", "Jemaat GKI Betania Asei Besar"] },
    travel: { note: "Penyeberangan ke Pulau Asei tersedia dari dermaga Khalkote.", items: [
      { name: "Longboat keluarga", detail: "Berangkat tiap 20 menit mulai 09.00 WIT dari dermaga Khalkote" },
      { name: "Dari Bandara Sentani", detail: "± 25 menit berkendara ke Kampung Harapan" },
    ] },
  },
});
