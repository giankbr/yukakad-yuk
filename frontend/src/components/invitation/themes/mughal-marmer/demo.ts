import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Shafira", groom: "Arkan",
    brideFull: "Shafira Kamila Az-Zahra, M.Psi.", groomFull: "Arkan Malik Ibrahim, S.Ked.",
    brideParents: "Putri pertama dari\nBapak Dr. H. Ridwan Hakim Hasibuan & Ibu Hj. Nadia Lubis",
    groomParents: "Putra ketiga dari\nBapak H. Ibrahim Siregar & Ibu Hj. Rosmawati Nasution",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Seperti batu-batu kecil yang ditatahkan satu per satu ke dalam marmer, semoga Allah menyusun kebaikan dalam hari-hari kami.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-18T08:00:00+07:00",
  place: "Masjid Agung Sunda Kelapa",
  address: "Jl. Taman Sunda Kelapa No. 16, Menteng, Jakarta Pusat",
  stories: [
    { date: "2020", title: "Ruang Baca Fakultas", body: "Kami sering duduk di meja yang sama di perpustakaan, tanpa pernah benar-benar saling menyapa." },
    { date: "2025", title: "Ta'aruf", body: "Seorang sahabat mempertemukan kami. Kami saling bertanya dengan jujur, lalu menyerahkan jawabannya kepada Allah." },
    { date: "Juni 2027", title: "Khitbah", body: "Keluarga Arkan datang dari Medan, meminang dengan adat yang hangat dan doa yang panjang." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Sunda Kelapa", address: "Jl. Taman Sunda Kelapa No. 16, Menteng, Jakarta Pusat" },
    { name: "Walimah", date: "2027-09-18T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Balai Kartini, Ruang Kartika", address: "Jl. Gatot Subroto Kav. 37, Kuningan, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a116.webp", "/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/a18.webp", "/themes/img/a64.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7301 2299 84", account_name: "Shafira Kamila Az-Zahra" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5480 771 203", account_name: "Arkan Malik Ibrahim" },
  ],
  guestName: "Ibu Hj. Fadhilah Rangkuti & Keluarga",
  guestTable: "Meja Lapis 2",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Jamuan & ramah tamah" },
      { time: "13.00", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim santun. Putih gading, emas lembut, dan biru lapis dipersilakan.", colors: ["#f6f1e6", "#b8955a", "#29467f", "#b24a2c"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Dr. H. Ridwan Hakim Hasibuan", "Kel. Besar H. Ibrahim Siregar"] },
  },
});
