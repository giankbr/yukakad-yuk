import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Anna", groom: "Yosef",
    brideFull: "Rambu Anna Kahi Ata, S.E.", groomFull: "Yosef Ndun, S.Kom.",
    brideParents: "Putri bungsu dari\nBapak Umbu Hina Kapita & Ibu Rambu Lika Ata", groomParents: "Putra kedua dari\nBapak Daniel Ndun & Ibu Agustina Bessie",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Benang demi benang ditenun dengan sabar; begitu pula kami ingin merajut rumah tangga yang kuat dan indah.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-11T10:00:00+08:00",
  place: "Gedung Serbaguna Matawai",
  address: "Jl. Ahmad Yani, Matawai, Kota Waingapu, Sumba Timur, NTT",
  stories: [
    { date: "2019", title: "Bertemu di Kupang", body: "Kami berkenalan saat kuliah di Kupang, sama-sama aktif di paduan suara kampus." },
    { date: "2024", title: "Pulang ke Sumba", body: "Yosef ikut Anna pulang ke Waingapu, belajar memahami adat dan disambut hangat keluarga besar." },
    { date: "2027", title: "Belis & Restu", body: "Setelah musyawarah dua keluarga, kami siap menerima pemberkatan nikah di tanah Sumba." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-09-11T10:00:00+08:00", time: "10.00 – 11.30 WITA", venue: "Gereja Kristen Sumba Payeti", address: "Jl. Prof. Dr. W.Z. Johannes, Payeti, Kota Waingapu" },
    { name: "Resepsi", date: "2027-09-11T18:00:00+08:00", time: "18.00 – 21.30 WITA", venue: "Gedung Serbaguna Matawai", address: "Jl. Ahmad Yani, Matawai, Kota Waingapu, Sumba Timur" },
  ],
  gallery: ["/themes/img/r104.webp", "/themes/img/r15.webp", "/themes/img/r105.webp", "/themes/img/r100.webp", "/themes/img/r101.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank NTT", account_number: "0350 1234 5678", account_name: "Rambu Anna Kahi Ata" },
    { id: "demo-kado", type: "address", address: "Jl. Kampung Raja Prailiu No. 5, Kambera, Sumba Timur 87112" },
  ],
  guestName: "Ibu Maria Ndolu & Keluarga",
  guestTable: "Meja 4",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "18.00", title: "Penyambutan tamu", note: "Kalungan selendang tenun bagi keluarga" },
      { time: "18.45", title: "Doa syukur & sambutan keluarga" },
      { time: "19.30", title: "Makan bersama" },
      { time: "20.30", title: "Ja'i & dansa bersama" },
    ] },
    dressCode: { note: "Kain tenun daerah sangat dipersilakan. Nuansa nila, karat, dan krem.", colors: ["#22305a", "#a8492a", "#efe4cf", "#c99a52"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-11T10:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Umbu Hina Kapita", "Kel. Besar Ndun – Bessie", "Jemaat GKS Payeti"] },
  },
});
