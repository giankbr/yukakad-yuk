import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Fikri",
    brideFull: "Nadia Syafitri, S.Pd.", groomFull: "Ahmad Fikri Ramadhan, S.T.",
    brideParents: "Putri sulung dari\nBapak H. Zulkifli Hasan & Ibu Hj. Siti Mariam", groomParents: "Putra ketiga dari\nBapak Rusli Effendi & Ibu Nurlela",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Seperti bata-bata Muaro Jambi yang tersusun rapi berabad-abad di tepi Batanghari, semoga rumah tangga kami kokoh, sabar, dan diberkahi.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-07-10T08:00:00+07:00",
  place: "Ratu Convention Center",
  address: "Jl. Ir. H. Juanda No. 148, Simpang III Sipin, Kec. Kota Baru, Kota Jambi",
  stories: [
    { date: "2020", title: "Kuliah lapangan di candi", body: "Nadia mahasiswi pendidikan sejarah, Fikri relawan pemetaan situs. Kami berkenalan di antara Candi Gumpung dan Candi Tinggi, sambil berteduh dari hujan." },
    { date: "2024", title: "Perahu di Batanghari", body: "Pulang dari Desa Muara Jambi naik ketek menyusuri sungai. Di tengah perjalanan Fikri bertanya, apakah Nadia mau menua bersamanya." },
    { date: "2026", title: "Antar tando", body: "Keluarga Fikri datang membawa tando dan sirih pinang. Adat diisi, lembaga dituang, dan kedua keluarga bersepakat dengan restu para tetua." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-10T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Kediaman Mempelai Wanita", address: "Desa Muara Jambi RT 04, Kec. Maro Sebo, Kab. Muaro Jambi" },
    { name: "Resepsi", date: "2027-07-10T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Ratu Convention Center", address: "Jl. Ir. H. Juanda No. 148, Simpang III Sipin, Kec. Kota Baru, Kota Jambi" },
  ],
  gallery: ["/themes/img/a50.webp", "/themes/img/a72.webp", "/themes/img/a63.webp", "/themes/img/a38.webp"],
  gifts: [
    { id: "demo-jambi", type: "bank", bank_name: "Bank Jambi Syariah", account_number: "1102 3345 81", account_name: "Nadia Syafitri" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7180 2260 47", account_name: "Ahmad Fikri Ramadhan" },
    { id: "demo-kado", type: "address", address: "Desa Muara Jambi RT 04, Kec. Maro Sebo, Kab. Muaro Jambi, Jambi 36382" },
  ],
  guestName: "Bapak H. Darmawan & Keluarga",
  guestTable: "Meja Batanghari 3",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Arak-arakan pengantin", note: "Diiringi kompangan dan pencak silat" },
      { time: "11.30", title: "Tari Sekapur Sirih", note: "Penyambutan tamu kehormatan" },
      { time: "12.00", title: "Makan bersamo", note: "Gulai ikan patin & tempoyak" },
      { time: "13.30", title: "Doa dan foto keluarga" },
    ] },
    dressCode: { note: "Busana muslim atau batik Jambi. Merah bata, biru nila, dan kuning kunyit dipersilakan.", colors: ["#b4532f", "#23305a", "#d9a441", "#f6ead6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Zulkifli Hasan", "Kel. Besar Rusli Effendi"] },
  },
});
