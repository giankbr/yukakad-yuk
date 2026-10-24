import { makeDemo } from "../demo-base";

// Pernikahan di Samarinda: sarung tenun gedokan dari Kampung Tenun Samarinda Seberang dan Sungai Mahakam yang lebar.
export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Fahri",
    brideFull: "Nadia Rahmadani, S.Pd.", groomFull: "Fahri Muhammad Akbar, S.H.",
    brideParents: "Putri bungsu dari\nBapak H. Syahrani & Ibu Hj. Norhayati", groomParents: "Putra kedua dari\nBapak Ir. H. Masrani & Ibu Hj. Rusmiati",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Benang lungsin dan pakan sarung Samarinda saling silang ribuan kali sebelum menjadi kotak-kotak yang utuh. Begitu juga kami.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-25T09:00:00+08:00",
  place: "Hotel Mesra Samarinda",
  address: "Jl. Pahlawan No. 1, Dadi Mulya, Samarinda Ulu, Kota Samarinda, Kalimantan Timur",
  stories: [
    { date: "2020", title: "Di Tepian Mahakam", body: "Kami berkenalan saat sama-sama menunggu senja di Tepian Mahakam, menonton kapal tongkang lewat pelan di bawah langit oranye." },
    { date: "2023", title: "Rumah Nenek Penenun", body: "Fahri pertama kali menyeberang ke Samarinda Seberang untuk bertemu nenek Nadia, yang masih menenun sarung di gedokan setiap pagi." },
    { date: "2027", title: "Sarung yang Sama", body: "Nenek menenun dua helai sarung bercorak sama untuk kami. Dengan restu keluarga, kami memakainya di hari akad." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-25T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Islamic Center Samarinda", address: "Jl. Slamet Riyadi, Karang Asam Ulu, Sungai Kunjang, Kota Samarinda" },
    { name: "Resepsi", date: "2027-09-25T19:00:00+08:00", time: "19.00 – 21.30 WITA", venue: "Hotel Mesra Samarinda", address: "Jl. Pahlawan No. 1, Dadi Mulya, Samarinda Ulu, Kota Samarinda" },
  ],
  gallery: ["/themes/img/a26.webp", "/themes/img/a22.webp", "/themes/img/a30.webp", "/themes/img/a21.webp", "/themes/img/r38.webp"],
  gifts: [
    { id: "demo-bankaltimtara", type: "bank", bank_name: "Bankaltimtara", account_number: "0021 4570 9925", account_name: "Nadia Rahmadani" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7250 9270 12", account_name: "Fahri Muhammad Akbar" },
    { id: "demo-kado", type: "address", address: "Jl. Pangeran Bendahara Gg. Tenun No. 8, Tenun, Samarinda Seberang, Kota Samarinda 75131" },
  ],
  guestName: "Bapak H. Rusdiansyah & Keluarga",
  guestTable: "Meja Mahakam 4",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat kebesaran Allah.", source: "QS. Az-Zariyat: 49" },
    rundown: { items: [
      { time: "19.00", title: "Kedatangan pengantin", note: "Diiringi hadrah dan tingkilan" },
      { time: "19.30", title: "Doa & sambutan keluarga" },
      { time: "20.00", title: "Ramah tamah", note: "Nasi kuning, gence ruan, dan amplang" },
    ] },
    dressCode: { note: "Bersarung atau bertenun Samarinda dipersilakan. Merah tua, hitam, dan emas.", colors: ["#5a1420", "#16100f", "#c8973a", "#1e5f5e"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bapak H. Syahrani", "Kel. Besar Bapak Ir. H. Masrani"] },
  },
});
