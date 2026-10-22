import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadhira", groom: "Fikri",
    brideFull: "Nadhira Salsabila Rahmani, S.Farm.", groomFull: "Muhammad Fikri Al-Ghifari, S.Si.",
    brideParents: "Putri kedua dari\nBapak H. Ridwan Kamaludin & Ibu Hj. Euis Nurhayati", groomParents: "Putra pertama dari\nBapak Drs. Hasan Basri & Ibu Siti Maryam",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Seperti hortensia yang warnanya mengikuti tanah tempat ia tumbuh, semoga kami saling menumbuhkan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T08:00:00+07:00",
  place: "Taman Hortensia Cikole",
  address: "Jl. Raya Tangkuban Perahu Km. 22, Cikole, Lembang, Bandung Barat",
  stories: [
    { date: "2018", title: "Praktikum Botani", body: "Satu meja di laboratorium ITB. Fikri salah memberi label daun, Nadhira yang membetulkannya." },
    { date: "2023", title: "Kebun di Lembang", body: "Kami merawat petak hortensia milik keluarga, belajar bahwa tanah yang asam membuat bunganya biru." },
    { date: "2026", title: "Khitbah", body: "Keluarga Fikri datang bersilaturahmi ke rumah di Cimahi, disambut teh hangat dan doa." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Bandung" },
    { name: "Walimatul 'Ursy", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Taman Hortensia Cikole", address: "Jl. Raya Tangkuban Perahu Km. 22, Cikole, Lembang, Bandung Barat" },
  ],
  gallery: ["/themes/img/a18.webp", "/themes/img/r75.webp", "/themes/img/r84.webp", "/themes/img/r79.webp", "/themes/img/r83.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4560 98", account_name: "Nadhira Salsabila Rahmani" },
    { id: "demo-bjb", type: "bank", bank_name: "bjb", account_number: "0098 1122 3344 100", account_name: "Muhammad Fikri Al-Ghifari" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0812 2233 4455", account_name: "Nadhira Salsabila" },
  ],
  guestName: "Ibu Hj. Ratna Komalasari & Keluarga",
  guestTable: "Meja Biru 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan tamu", note: "Teh & kudapan di taman" },
      { time: "11.30", title: "Kirab pengantin" },
      { time: "12.00", title: "Ramah tamah & santap siang" },
      { time: "13.00", title: "Foto bersama", note: "Di lorong hortensia" },
    ] },
    dressCode: { note: "Biru, lavender, dan putih. Tamu wanita dipersilakan berhijab nuansa pastel.", colors: ["#4a57a3", "#8c96d6", "#c3c4ec", "#f4f6fa"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. H. Ridwan Kamaludin", "Kel. Besar Bpk. Drs. Hasan Basri"] },
    travel: { note: "Lembang cukup sejuk, siapkan pakaian hangat. Berikut pilihan terdekat dari lokasi.", items: [
      { name: "Parkir & shuttle", detail: "Parkir di Terminal Cikole, shuttle tiap 15 menit" },
      { name: "Stasiun Bandung", detail: "± 50 menit berkendara ke Lembang" },
    ] },
  },
});
