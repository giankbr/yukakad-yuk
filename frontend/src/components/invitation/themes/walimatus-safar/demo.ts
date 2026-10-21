import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Abdul Ghani", groom: "Siti Maimunah",
    brideFull: "Abdul Ghani Rasyid", groomFull: "Siti Maimunah",
    brideParents: "Calon jamaah haji Kloter SOC-27\nEmbarkasi Solo, Asrama Haji Donohudan", groomParents: "Istri tercinta, mendampingi dalam satu rombongan",
    note: "Semoga Allah memudahkan setiap langkah kami menuju Baitullah, dan memulangkan kami sebagai haji yang mabrur.",
  },
  eventLabel: "Walimatus Safar",
  date: "2027-04-17T09:00:00+07:00",
  place: "Kediaman Keluarga Bapak Abdul Ghani",
  address: "Jl. Kenanga No. 12, Laweyan, Kota Surakarta",
  stories: [
    { date: "2014", title: "Niat & Pendaftaran", body: "Menabung sedikit demi sedikit dari usaha batik, lalu mendaftar porsi haji di Kemenag Surakarta." },
    { date: "2026", title: "Panggilan Pelunasan", body: "Alhamdulillah, setelah dua belas tahun menanti, nama kami masuk daftar pelunasan." },
    { date: "2027", title: "Manasik Haji", body: "Mengikuti bimbingan manasik di KBIH bersama rombongan dari Laweyan." },
    { date: "2027", title: "Keberangkatan", body: "Insyaallah berangkat dari Embarkasi Solo menuju Madinah bersama Kloter SOC-27." },
  ],
  events: [
    { name: "Walimatus Safar & Doa Bersama", date: "2027-04-17T09:00:00+07:00", time: "09.00 – 12.00 WIB", venue: "Kediaman Keluarga Bapak Abdul Ghani", address: "Jl. Kenanga No. 12, Laweyan, Kota Surakarta" },
    { name: "Pelepasan Keberangkatan", date: "2027-04-24T13:00:00+07:00", time: "13.00 WIB", venue: "Asrama Haji Donohudan", address: "Jl. Embarkasi Haji, Donohudan, Ngemplak, Boyolali" },
  ],
  gallery: [],
  gifts: [],
  guestName: "Bapak Haryanto & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan (di antara) kewajiban manusia terhadap Allah adalah melaksanakan ibadah haji ke Baitullah, yaitu bagi orang-orang yang mampu mengadakan perjalanan ke sana.", source: "QS. Ali 'Imran: 97" },
    rundown: { items: [
      { time: "09.00", title: "Pembukaan & tilawah" },
      { time: "09.30", title: "Tausiyah manasik", note: "Ustaz H. Mahfudz Siddiq" },
      { time: "10.30", title: "Doa safar bersama" },
      { time: "11.00", title: "Ramah tamah & mohon maaf lahir batin" },
    ] },
    dressCode: { note: "Busana muslim rapi. Putih, hijau, atau krem dipersilakan.", colors: ["#f6f1e3", "#0f3b2e", "#c9a24e", "#d9c7a0"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar Rasyid", "Jamaah Masjid Al-Hikmah Laweyan"] },
    faq: { items: [
      { q: "Bolehkah menitipkan doa?", a: "Sangat boleh. Tuliskan di kolom doa, insyaallah kami bacakan di Tanah Suci." },
      { q: "Apakah ada parkir?", a: "Parkir tersedia di halaman Masjid Al-Hikmah, 50 meter dari rumah." },
    ] },
  },
});
