import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ester", groom: "Imanuel",
    brideFull: "Ester Naomi Nubatonis, S.Kep.", groomFull: "Imanuel Yohanis Boimau, S.T.",
    brideParents: "Putri sulung dari\nBapak Yakobus Nubatonis & Ibu Ruth Taneo", groomParents: "Putra kedua dari\nBapak Pdt. Markus Boimau, S.Th. & Ibu Agustina Benu",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti benang lungsin yang diikat dan dicelup sebelum ditenun, hidup kami dipersiapkan Tuhan untuk menjadi satu helai tais.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T10:00:00+08:00",
  place: "Gereja GMIT Kota Kupang",
  address: "Jl. Siliwangi, Lai Lai Bisi Kopan, Kota Lama, Kota Kupang",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2018", title: "Paduan Suara Pemuda", body: "Kami berkenalan di latihan paduan suara pemuda gereja menjelang Paskah di Kupang." },
    { date: "2022", title: "Jalan ke Soe", body: "Perjalanan Kupang–Soe menembus padang lontar menjadi rute kami setiap kali pulang menemui keluarga." },
    { date: "2027", title: "Satu Helai Tais", body: "Dengan restu kedua keluarga dan berkat Tuhan, kami melangkah ke pernikahan kudus." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-07-10T10:00:00+08:00", time: "10.00 – 12.00 WITA", venue: "Gereja GMIT Kota Kupang", address: "Jl. Siliwangi, Lai Lai Bisi Kopan, Kota Lama, Kota Kupang" },
    { name: "Resepsi Adat & Syukuran", date: "2027-07-11T16:00:00+08:00", time: "16.00 – 21.00 WITA", venue: "Halaman Kediaman Keluarga Nubatonis", address: "Jl. Gajah Mada, Karang Siri, Kota Soe, Timor Tengah Selatan" },
  ],
  gallery: ["/themes/img/r38.webp", "/themes/img/r81.webp", "/themes/img/r100.webp", "/themes/img/r101.webp"],
  gifts: [
    { id: "demo-ntt", type: "bank", bank_name: "Bank NTT", account_number: "0012 0102 7788 31", account_name: "Ester Naomi Nubatonis" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0451 0100 2234 508", account_name: "Imanuel Yohanis Boimau" },
  ],
  guestName: "Bapak Yeremias Tefa & Keluarga",
  guestTable: "Meja Lontar 2",
  extras: {
    quote: { text: "Dan bilamana seorang dapat dialahkan, dua orang akan dapat bertahan. Tali tiga lembar tak mudah diputuskan.", source: "Pengkhotbah 4:12" },
    rundown: { items: [
      { time: "16.00", title: "Penyambutan tamu", note: "Dengan natoni, tutur adat penyambutan" },
      { time: "16.45", title: "Pengalungan selendang tais" },
      { time: "17.30", title: "Ibadah syukur keluarga" },
      { time: "18.30", title: "Makan bersama & tarian bonet" },
    ] },
    dressCode: { note: "Tais, selendang, atau kemeja bermotif tenun sangat dipersilakan. Nuansa merah, hitam, dan jingga.", colors: ["#9b2319", "#1c1412", "#e0782a", "#efe3cc"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-10T10:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Yakobus Nubatonis (Soe)", "Kel. Besar Pdt. Markus Boimau (Kupang)"] },
    travel: { note: "Resepsi berlangsung di Soe, sekitar 110 km dari Kupang.", items: [
      { name: "Bandara El Tari, Kupang", detail: "± 20 menit ke Gereja GMIT Kota Kupang" },
      { name: "Kupang – Soe", detail: "± 2,5 jam perjalanan darat melalui jalur Trans Timor" },
    ] },
  },
});
