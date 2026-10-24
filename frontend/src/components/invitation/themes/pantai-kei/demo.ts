import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Tesa", groom: "Frans",
    brideFull: "Theresia Ngabalin, S.Pd.", groomFull: "Fransiskus Rahanra, S.T.",
    brideParents: "Putri kedua dari\nBapak Yohanes Ngabalin & Ibu Maria Renyaan", groomParents: "Putra sulung dari\nBapak Petrus Rahanra & Ibu Agustina Ohoitimur",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Ain ni ain: kita semua satu. Dua keluarga, satu meja, satu doa di tanah Evav.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T10:00:00+09:00",
  place: "Gereja Katolik Langgur",
  address: "Jl. Jenderal Sudirman, Langgur, Kei Kecil, Kabupaten Maluku Tenggara, Maluku",
  stories: [
    { date: "2019", title: "Pagi di Ngurbloat", body: "Tesa mengajar anak-anak ohoi berenang di pasir putih Ngurbloat, Frans datang memperbaiki perahu ayahnya. Satu pagi, banyak cerita." },
    { date: "2023", title: "Pulang ke Tual", body: "Setelah bertahun-tahun bekerja di Ambon, Frans memilih pulang. Setiap sore kami berjalan di dermaga Tual sambil menunggu kapal masuk." },
    { date: "2026", title: "Kedua Keluarga Duduk Bersama", body: "Dengan adat dan doa, keluarga Rahanra datang ke rumah keluarga Ngabalin. Kami disatukan dalam semangat ain ni ain." },
  ],
  events: [
    { name: "Sakramen Perkawinan", date: "2027-07-10T10:00:00+09:00", time: "10.00 – 11.30 WIT", venue: "Gereja Katolik Langgur", address: "Jl. Jenderal Sudirman, Langgur, Kei Kecil, Kabupaten Maluku Tenggara" },
    { name: "Resepsi & Makan Patita", date: "2027-07-10T17:00:00+09:00", time: "17.00 – 21.00 WIT", venue: "Gedung Serbaguna Tual", address: "Jl. Pattimura, Kota Tual, Maluku" },
  ],
  gallery: ["/themes/img/r15.webp", "/themes/img/r9.webp", "/themes/img/r11.webp", "/themes/img/r103.webp", "/themes/img/r5.webp", "/themes/img/r110.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank Maluku", account_number: "0312 0419 2275", account_name: "Theresia Ngabalin" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "2140 0100 8837 506", account_name: "Fransiskus Rahanra" },
    { id: "demo-kado", type: "address", address: "Jl. Ohoijang No. 12, Langgur, Kei Kecil, Maluku Tenggara 97611" },
  ],
  guestName: "Bapak Paulus Rettob & Keluarga",
  guestTable: "Meja Ngurbloat",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "17.00", title: "Penyambutan tamu", note: "Tarian sawat dan tifa" },
      { time: "17.45", title: "Doa syukur keluarga" },
      { time: "18.30", title: "Makan patita bersama", note: "Ikan bakar, enbal, dan sayur santan" },
      { time: "20.00", title: "Dansa bersama keluarga" },
    ] },
    dressCode: { note: "Putih pasir dan biru laut. Kain tenun Kei sangat dipersilakan.", colors: ["#fbf8f1", "#3cbfb9", "#0f5f6e", "#b1442e"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Ngabalin – Renyaan", "Kel. Besar Rahanra – Ohoitimur", "Umat Paroki Langgur"] },
  },
});
