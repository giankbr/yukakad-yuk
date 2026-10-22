import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aini", groom: "Fikri",
    brideFull: "Tengku Nurul Aini, S.H.", groomFull: "Muhammad Fikri Azhar, S.E.",
    brideParents: "Putri sulung dari\nBapak Tengku H. Syahril Amri & Ibu Hj. Siti Rahmah", groomParents: "Putra ketiga dari\nBapak H. Zulkarnain Nasution & Ibu Hj. Rosmawati Lubis",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Adat bersendikan syarak, syarak bersendikan Kitabullah. Semoga rumah tangga kami berdiri di atas sendi yang kokoh.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-09T09:00:00+07:00",
  place: "Tiara Convention Center",
  address: "Jl. Cut Mutia No. 1, Gg. Buntu, Medan Timur, Kota Medan",
  stories: [
    { date: "2020", title: "Kota Lama Medan", body: "Kami bertemu dalam lomba berbalas pantun Melayu di Medan. Fikri kalah satu bait, Aini menang satu senyum." },
    { date: "2025", title: "Merisik", body: "Keluarga Fikri datang merisik dengan tepak sirih. Keluarga Aini menyambutnya dengan pantun dan doa." },
    { date: "2027", title: "Bersanding", body: "Dengan izin Allah, kami bersanding di pelaminan sebagai raja dan ratu sehari." },
  ],
  events: [
    { name: "Tepung Tawar & Berinai", date: "2027-10-08T19:30:00+07:00", time: "19.30 – 21.30 WIB", venue: "Kediaman Keluarga Mempelai Wanita", address: "Jl. Brigjend Katamso No. 45, Kampung Baru, Medan Maimun, Kota Medan" },
    { name: "Akad Nikah", date: "2027-10-09T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Raya Al-Mashun", address: "Jl. Sisingamangaraja No. 61, Mesjid, Medan Kota, Kota Medan" },
    { name: "Resepsi Bersanding", date: "2027-10-09T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Tiara Convention Center", address: "Jl. Cut Mutia No. 1, Gg. Buntu, Medan Timur, Kota Medan" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a99.webp", "/themes/img/a63.webp", "/themes/img/a49.webp", "/themes/img/a40.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7300 1122 33", account_name: "Tengku Nurul Aini" },
    { id: "demo-sumut", type: "bank", bank_name: "Bank Sumut", account_number: "210 01 04 556677 8", account_name: "Muhammad Fikri Azhar" },
  ],
  guestName: "Bapak Datuk H. Mahmud Lubis & Keluarga",
  guestTable: "Meja Seri 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Arak-arakan pengantin", note: "Diiringi kompang & silat pengantin" },
      { time: "11.30", title: "Bersanding di pelaminan" },
      { time: "12.00", title: "Jamuan makan", note: "Nasi minyak & gulai kambing" },
      { time: "13.30", title: "Bergambar bersama keluarga" },
    ] },
    dressCode: { note: "Baju kurung atau teluk belanga. Kuning, emas, dan hijau tua dipersilakan.", colors: ["#e6b62a", "#c99a3c", "#2d5a46", "#fbf1d2"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-09T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Tengku H. Syahril Amri", "Kel. Besar H. Zulkarnain Nasution"] },
  },
});
