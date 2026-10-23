import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ance", groom: "Yermi",
    brideFull: "Ance Yuliana Ludji Kana, S.Pd.", groomFull: "Yeremias Riwu Hege, S.T.",
    brideParents: "Putri kedua dari\nBapak Daniel Ludji Kana & Ibu Martha Djara Wadu", groomParents: "Putra sulung dari\nBapak Paulus Riwu Hege & Ibu Ester Bire Lado",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Seperti benang lungsin dan pakan dalam selembar tenun Hawu, kami dipertemukan untuk saling menguatkan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-24T09:00:00+08:00",
  place: "Gereja GMIT Ebenhaezer Seba",
  address: "Jl. Trans Sabu, Kelurahan Mebba, Kec. Sabu Barat, Kab. Sabu Raijua, NTT",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2018", title: "Bertemu di Kupang", body: "Dua anak Rai Hawu bertemu di persekutuan mahasiswa Undana, jauh dari rumah tetapi dekat dalam bahasa dan doa." },
    { date: "2022", title: "Pulang ke Seba", body: "Ance mengajar di SMA Seba, Yermi membangun jaringan air bersih desa. Sore hari kami menyadap nira lontar bersama keluarga." },
    { date: "2027", title: "Satu Tenun", body: "Dengan restu kedua keluarga dan adat Hawu, kami melangkah ke pemberkatan nikah." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-07-24T09:00:00+08:00", time: "09.00 – 11.00 WITA", venue: "Gereja GMIT Ebenhaezer Seba", address: "Jl. Trans Sabu, Kelurahan Mebba, Kec. Sabu Barat, Kab. Sabu Raijua, NTT" },
    { name: "Resepsi & Tarian Pado'a", date: "2027-07-24T17:00:00+08:00", time: "17.00 – 22.00 WITA", venue: "Halaman Rumah Keluarga Ludji Kana", address: "Desa Raeloro, Kec. Sabu Barat, Kab. Sabu Raijua, NTT" },
  ],
  gallery: ["/themes/img/r109.webp", "/themes/img/r107.webp", "/themes/img/r106.webp", "/themes/img/r105.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "4612 0101 8834 507", account_name: "Ance Yuliana Ludji Kana" },
    { id: "demo-bank-ntt", type: "bank", bank_name: "NTT", account_number: "063 02 11 004821", account_name: "Yeremias Riwu Hege" },
    { id: "demo-kado", type: "address", address: "Rumah Keluarga Ludji Kana, Desa Raeloro, Kec. Sabu Barat, Kab. Sabu Raijua, NTT 85391" },
  ],
  guestName: "Bapak Pdt. Markus Bunga & Keluarga",
  guestTable: "Meja Lontar 3",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "17.00", title: "Penyambutan tamu", note: "Diiringi gong dan tambur" },
      { time: "18.00", title: "Ibadah syukur keluarga" },
      { time: "19.00", title: "Makan malam bersama" },
      { time: "20.00", title: "Tarian Pado'a bersama", note: "Semua tamu dipersilakan ikut menari" },
    ] },
    dressCode: { note: "Busana tenun ikat Sabu, atau kemeja dan kebaya bernuansa gelap. Merah dan putih dipersilakan.", colors: ["#1e1b2a", "#4a2c1e", "#b0322a", "#efe6d2"] },
    guestPass: {},
    rsvpDietary: {},
    travel: { note: "Seba dapat dicapai dengan kapal cepat atau pesawat dari Kupang.", items: [
      { name: "Kapal cepat Kupang – Seba", detail: "± 4 jam, berangkat pagi dari Pelabuhan Tenau" },
      { name: "Bandara Tardamu", detail: "± 15 menit dari gereja, penerbangan harian dari Kupang" },
    ] },
    family: { names: ["Kel. Besar Ludji Kana", "Kel. Besar Riwu Hege", "Kel. Besar Djara Wadu", "Kel. Besar Bire Lado"] },
  },
});
