import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Faris",
    brideFull: "Aisyah Nur Halimah, S.Pd.", groomFull: "Muhammad Faris Al Habsyi, S.E.",
    brideParents: "Putri pertama dari\nBapak H. Abdullah Baraqbah & Ibu Hj. Maryam Assegaf", groomParents: "Putra kedua dari\nBapak H. Umar Al Habsyi & Ibu Hj. Fatimah Bin Syech",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti benang-benang sadu yang dirajut menjadi satu, semoga Allah menenun dua hati kami dalam sakinah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-16T09:00:00+07:00",
  place: "Gedung Al-Irsyad Al-Islamiyyah",
  address: "Jl. KH. Mas Mansyur No. 12, Nyamplungan, Pabean Cantikan, Surabaya",
  stories: [
    { date: "2022", title: "Majelis Taklim Ampel", body: "Kami pertama kali bertemu sebagai panitia kajian pekanan di kawasan Ampel, sama-sama sibuk mengatur konsumsi." },
    { date: "2025", title: "Ta'aruf", body: "Dengan perantara guru ngaji kami, Faris datang bersilaturahmi ke rumah keluarga Aisyah." },
    { date: "2027", title: "Menenun Bersama", body: "Alhamdulillah, dengan restu kedua keluarga kami melangkah menuju ikatan suci pernikahan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-16T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Sunan Ampel", address: "Jl. Ampel Masjid No. 53, Ampel, Semampir, Surabaya" },
    { name: "Walimatul 'Ursy", date: "2027-10-16T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Al-Irsyad Al-Islamiyyah", address: "Jl. KH. Mas Mansyur No. 12, Nyamplungan, Pabean Cantikan, Surabaya" },
  ],
  gallery: ["/themes/img/r57.webp", "/themes/img/r58.webp", "/themes/img/r3.webp", "/themes/img/r4.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7201 8845 31", account_name: "Aisyah Nur Halimah" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0882 4410 57", account_name: "Muhammad Faris Al Habsyi" },
    { id: "demo-kado", type: "address", address: "Jl. Sasak No. 27, Ampel, Semampir, Surabaya 60151" },
  ],
  guestName: "Ustadz Hasan Basri & Keluarga",
  guestTable: "Majelis 3",
  extras: {
    rundown: { items: [
      { time: "11.00", title: "Pembacaan ayat suci Al-Qur'an" },
      { time: "11.20", title: "Tausiyah pernikahan", note: "Oleh Habib Ali Alaydrus" },
      { time: "12.00", title: "Ramah tamah & hidangan kambing oven" },
    ] },
    dressCode: { note: "Busana muslim rapi. Nuansa merah marun, hitam, krem, atau kunyit.", colors: ["#9a2622", "#1d1512", "#ebe0c9", "#c4882c"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Baraqbah", "Kel. Besar Al Habsyi"] },
  },
});
