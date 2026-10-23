import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Keluarga Siregar", groom: "Geng Cempaka",
    brideFull: "Bang Togar & Kak Rina Siregar", groomFull: "Warga Blok C, Kompleks Cempaka Asri",
    brideParents: "Tuan rumah, penjaga panggangan\nRumah No. 12, halaman belakang", groomParents: "Penyumbang arang, es batu,\nsambal kecap, dan playlist",
    note: "Arang sudah dibeli, lampu sudah dipasang. Tinggal kamu yang datang.",
  },
  eventLabel: "Pesta BBQ",
  date: "2027-07-17T16:00:00+07:00",
  place: "Halaman Belakang Rumah Siregar",
  address: "Jl. Cempaka Raya Blok C No. 12, Kompleks Cempaka Asri, Jatiasih, Kota Bekasi",
  stories: [
    { date: "16.00", title: "Kumpul & nyalakan arang", body: "Datang santai, bantu kipas-kipas arang sambil kenalan sama tetangga baru." },
    { date: "17.00", title: "Sate & jagung pertama", body: "Sate ayam, sate kambing, jagung bakar mentega. Yang datang duluan dapat paling hangat." },
    { date: "18.30", title: "Turnamen lempar karung", body: "Tim acak, hadiahnya sebotol sambal rahasia Kak Rina." },
    { date: "19.30", title: "Makan besar di bawah lampu", body: "Meja panjang, es jeruk, dan cerita-cerita sampai malam." },
  ],
  events: [
    { name: "Pesta BBQ Halaman Belakang", date: "2027-07-17T16:00:00+07:00", time: "16.00 – 21.00 WIB", venue: "Halaman Belakang Rumah Siregar", address: "Jl. Cempaka Raya Blok C No. 12, Kompleks Cempaka Asri, Jatiasih, Kota Bekasi" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-patungan", type: "ewallet", ewallet_provider: "GoPay", ewallet_number: "0812 9876 5432", account_name: "Rina Siregar" },
  ],
  guestName: "Mas Dimas & Mbak Sarah",
  guestTable: "Meja Kayu 2",
  extras: {
    dressCode: { note: "Santai saja: kaos, celana pendek, sandal. Siap kena asap!", colors: ["#d9452b", "#f2b632", "#5f9a4a", "#2f3a5a"] },
    rsvpDietary: {},
    faq: { items: [
      { q: "Perlu bawa apa?", a: "Cukup bawa diri dan selera makan. Kalau punya kursi lipat, boleh dibawa." },
      { q: "Ada menu tanpa daging?", a: "Ada jagung, tahu, jamur, dan sate sayur. Tulis saja di kolom pantangan makanan." },
      { q: "Boleh ajak anak?", a: "Boleh banget, ada sudut main dan es krim untuk anak-anak." },
    ] },
  },
});
