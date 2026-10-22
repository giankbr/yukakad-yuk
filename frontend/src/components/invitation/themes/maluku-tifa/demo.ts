import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Grace", groom: "Marvel",
    brideFull: "Grace Anastasya Latuheru, S.Kep.", groomFull: "Marvel Johanis Pattinama, S.H.",
    brideParents: "Putri bungsu dari\nBapak Johanis Latuheru & Ibu Maria Sahetapy", groomParents: "Putra kedua dari\nBapak Frans Pattinama & Ibu Yuliana Tuhumury",
    bridePhoto: "/themes/img/r28.webp", groomPhoto: "/themes/img/r4.webp",
    note: "Seperti tifa yang dipukul bersahut-sahutan, dua hati kami belajar seirama. Dangke, Tuhan, untuk kasih yang mempertemukan kami.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-16T10:00:00+09:00",
  place: "Hotel Santika Premiere Ambon",
  address: "Jl. Jend. Sudirman, Batu Merah, Sirimau, Kota Ambon",
  stories: [
    { date: "2018", title: "Rujak Natsepa", body: "Kami pertama bertemu di Pantai Natsepa, berebut porsi rujak terakhir. Marvel mengalah, Grace membagi setengahnya." },
    { date: "2022", title: "Paduan Suara Pemuda", body: "Bernyanyi di barisan yang sama setiap Minggu membuat kami saling mengenal lebih dalam, sampai hafal suara satu sama lain." },
    { date: "2026", title: "Masuk Minta", body: "Keluarga Pattinama datang masuk minta ke rumah Latuheru. Dua keluarga besar bersepakat, gandong pun bertambah." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-10-16T10:00:00+09:00", time: "10.00 – 12.00 WIT", venue: "Gereja Maranatha Ambon", address: "Jl. Raya Pattimura, Uritetu, Sirimau, Kota Ambon" },
    { name: "Resepsi", date: "2027-10-16T18:30:00+09:00", time: "18.30 – 22.00 WIT", venue: "Hotel Santika Premiere Ambon", address: "Jl. Jend. Sudirman, Batu Merah, Sirimau, Kota Ambon" },
  ],
  gallery: ["/themes/img/r110.webp", "/themes/img/r28.webp", "/themes/img/r4.webp", "/themes/img/r103.webp", "/themes/img/r107.webp", "/themes/img/a95.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0812 3344 56", account_name: "Grace Anastasya Latuheru" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1520 0098 7766 1", account_name: "Marvel Johanis Pattinama" },
    { id: "demo-kado", type: "address", address: "Jl. Dr. Kayadoe No. 27, Kudamati, Nusaniwe, Kota Ambon 97116" },
  ],
  guestName: "Bapak Pdt. Yance Leiwakabessy & Keluarga",
  guestTable: "Meja Cengkih 2",
  extras: {
    quote: { text: "Dan di atas semuanya itu: kenakanlah kasih, sebagai pengikat yang mempersatukan dan menyempurnakan.", source: "Kolose 3:14" },
    rundown: { items: [
      { time: "18.30", title: "Penyambutan tamu", note: "Diiringi totobuang dan suling bambu" },
      { time: "19.15", title: "Doa syukur & sambutan keluarga" },
      { time: "20.00", title: "Makan bersama & dansa lenso", note: "Papeda, ikan kuah kuning, dan sagu lempeng" },
    ] },
    dressCode: { note: "Kemeja atau kebaya dengan sentuhan tenun Maluku. Biru laut, merah tanah, dan krem dipersilakan.", colors: ["#1aa3a3", "#a8442a", "#4a1c17", "#ead9b6"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-16T10:00:00+09:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Latuheru – Sahetapy (Kudamati)", "Kel. Besar Pattinama – Tuhumury (Passo)"] },
  },
});
