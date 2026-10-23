import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Elsa", groom: "Yosua",
    brideFull: "Elsa Rante Pasang, S.Pd.", groomFull: "Yosua Dettumanan, S.Hut.",
    brideParents: "Putri bungsu dari\nBapak Yusuf Tandilangi & Ibu Marta Deppa", groomParents: "Putra kedua dari\nBapak Petrus Dettumanan & Ibu Ribka Salurante",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/a96.webp",
    note: "Dari lembah pinus yang sama kami belajar sabar menunggu musim panen, dan kini kami pulang ke satu banua.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-26T10:00:00+08:00",
  place: "Gereja Toraja Mamasa Jemaat Imanuel",
  address: "Jl. Poros Mamasa, Kelurahan Mamasa, Kec. Mamasa, Kab. Mamasa, Sulawesi Barat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2020", title: "Pagi berkabut di Tawalian", body: "Kami bertemu saat pelayanan pemuda gereja di Tawalian. Yosua menuntun rombongan menyusuri pematang, Elsa yang paling sering tertinggal memotret kabut." },
    { date: "2024", title: "Menanam bersama", body: "Kami ikut menanam bibit pinus di lereng Mambulilling. Di sana Yosua berjanji akan kembali menanam satu pohon setiap ulang tahun pernikahan." },
    { date: "2027", title: "Pemberkatan", body: "Dengan restu kedua keluarga, kami akan diteguhkan di hadapan Tuhan dan jemaat di Mamasa." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-06-26T10:00:00+08:00", time: "10.00 – 12.00 WITA", venue: "Gereja Toraja Mamasa Jemaat Imanuel", address: "Jl. Poros Mamasa, Kelurahan Mamasa, Kec. Mamasa, Kab. Mamasa" },
    { name: "Resepsi & Syukuran Keluarga", date: "2027-06-26T14:00:00+08:00", time: "14.00 – 18.00 WITA", venue: "Halaman Banua Keluarga Dettumanan", address: "Desa Tawalian, Kec. Tawalian, Kab. Mamasa, Sulawesi Barat" },
  ],
  gallery: ["/themes/img/a64.webp", "/themes/img/a22.webp", "/themes/img/r89.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "4512 0102 3388 509", account_name: "Elsa Rante Pasang" },
    { id: "demo-sulselbar", type: "bank", bank_name: "Bank Sulselbar", account_number: "160 202 000 4417 3", account_name: "Yosua Dettumanan" },
  ],
  guestName: "Bapak Pdt. Markus Lebang & Keluarga",
  guestTable: "Meja Pinus 2",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "14.00", title: "Penyambutan tamu", note: "Diiringi musik bambu" },
      { time: "14.30", title: "Doa syukur & sambutan keluarga" },
      { time: "15.00", title: "Santap bersama", note: "Masakan khas Mamasa" },
      { time: "16.30", title: "Foto bersama di depan banua" },
    ] },
    dressCode: { note: "Batik atau tenun. Merah, kuning, hitam, dan hijau pinus dipersilakan.", colors: ["#a8322a", "#e0aa3a", "#1f1a17", "#2f4a39"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Tandilangi", "Kel. Besar Dettumanan", "Jemaat GTM Imanuel Mamasa"] },
    faq: { items: [
      { q: "Berapa lama perjalanan ke Mamasa?", a: "Dari Polewali sekitar 3–4 jam perjalanan darat melalui jalur pegunungan. Berangkatlah pagi hari." },
      { q: "Apakah udara di Mamasa dingin?", a: "Ya, terutama sore hari. Kami sarankan membawa jaket atau selendang tenun." },
    ] },
  },
});
