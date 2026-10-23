import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Yuliana", groom: "Frengky",
    brideFull: "Maria Yuliana Ndiwa, S.Pd.", groomFull: "Fransiskus Frengky Jehalu, S.T.",
    brideParents: "Putri kedua dari\nBapak Yohanes Ndiwa & Ibu Theresia Ndimut", groomParents: "Putra sulung dari\nBapak Gabriel Jehalu & Ibu Kristina Nggiri",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Gendang one, lingko peang — rumah adat di dalam, kebun di luar. Kami ingin membangun keduanya bersama: rumah yang hangat dan ladang yang memberi hidup.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T09:00:00+08:00",
  place: "Gereja Katedral Ruteng",
  address: "Jl. Katedral, Kelurahan Mbaumuku, Langke Rembong, Ruteng, Kabupaten Manggarai, NTT",
  stories: [
    { date: "2018", title: "Kabut di Golo Curu", body: "Kami berkenalan saat ziarah ke Bukit Golo Curu. Kabut pagi turun, dan kami berbagi satu payung sampai ke kota." },
    { date: "2022", title: "Melihat Lingko dari Atas", body: "Di bukit Cancar, Frengky menunjuk sawah jaring laba-laba dan bilang: semua petak bertemu di satu titik. Yuli tahu maksudnya." },
    { date: "2026", title: "Masuk Minta", body: "Keluarga datang membawa tuak dan ayam putih. Belis dibicarakan dengan hormat, restu diberikan di mbaru gendang." },
    { date: "2027", title: "Wagal & Sakramen", body: "Kami menerima Sakramen Perkawinan, lalu menutup rangkaian adat wagal bersama keluarga besar." },
  ],
  events: [
    { name: "Misa Sakramen Perkawinan", date: "2027-07-10T09:00:00+08:00", time: "09.00 – 11.00 WITA", venue: "Gereja Katedral Ruteng", address: "Jl. Katedral, Mbaumuku, Langke Rembong, Ruteng, Kabupaten Manggarai, NTT" },
    { name: "Wagal (Upacara Adat)", date: "2027-07-10T13:00:00+08:00", time: "13.00 – 15.30 WITA", venue: "Mbaru Gendang Ruteng Pu'u", address: "Kampung Adat Ruteng Pu'u, Golo Dukal, Langke Rembong, Ruteng" },
    { name: "Resepsi", date: "2027-07-10T18:00:00+08:00", time: "18.00 – 22.00 WITA", venue: "Aula Paroki Katedral Ruteng", address: "Jl. Katedral, Mbaumuku, Langke Rembong, Ruteng, Kabupaten Manggarai, NTT" },
  ],
  gallery: ["/themes/img/r104.webp", "/themes/img/a64.webp", "/themes/img/r89.webp", "/themes/img/r91.webp", "/themes/img/a30.webp"],
  gifts: [
    { id: "demo-bntt", type: "bank", bank_name: "Bank NTT", account_number: "053 02 01 778812 4", account_name: "Maria Yuliana Ndiwa" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "4231 01 009876 53 2", account_name: "Fransiskus Frengky Jehalu" },
    { id: "demo-kado", type: "address", address: "Jl. Ahmad Yani No. 21, Tenda, Langke Rembong, Ruteng 86511" },
  ],
  guestName: "Bapak Kornelis Dagur & Keluarga",
  guestTable: "Meja Lingko 3",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "18.00", title: "Penyambutan tamu", note: "Diiringi gong dan gendang" },
      { time: "18.30", title: "Tarian caci & danding" },
      { time: "19.30", title: "Makan bersama" },
      { time: "20.30", title: "Ja'i dan dansa keluarga" },
    ] },
    dressCode: { note: "Busana resmi atau kain songke. Hitam, merah, dan kuning dipersilakan.", colors: ["#16120e", "#c8432b", "#e8c547", "#3f8a4a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-10T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Ndiwa, Kampung Pu'u", "Kel. Besar Jehalu, Cancar"] },
  },
});
