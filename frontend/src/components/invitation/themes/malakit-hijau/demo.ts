import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Adrian",
    brideFull: "Kirana Maheswari Tanoto, M.B.A.", groomFull: "Adrian Wibisono Halim, S.T.",
    brideParents: "Putri kedua dari\nBapak Hendra Tanoto & Ibu Melinda Santoso", groomParents: "Putra sulung dari\nBapak Daniel Halim & Ibu Ratna Wibisono",
    bridePhoto: "/themes/img/a83.webp", groomPhoto: "/themes/img/a84.webp",
    note: "Seperti batu malakit yang tumbuh lapis demi lapis, kami ingin cinta ini terus bertambah, satu cincin setiap tahun.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T16:00:00+07:00",
  place: "Hotel Indonesia Kempinski",
  address: "Jl. M.H. Thamrin No. 1, Menteng, Jakarta Pusat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2018", title: "Galeri yang Sepi", body: "Sebuah pameran perhiasan di Kemang. Kami berdua berhenti di depan vitrin yang sama: liontin malakit tua berbingkai emas." },
    { date: "2022", title: "Dua Kota", body: "Kirana di Singapura, Adrian di Jakarta. Panggilan video setiap malam dan satu tiket pesawat setiap bulan." },
    { date: "2026", title: "Liontin Itu", body: "Adrian melamar dengan liontin malakit yang ia cari selama tiga tahun. Kirana menangis sebelum kotaknya terbuka." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-09-18T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "The Garden Terrace", address: "Hotel Indonesia Kempinski, Jl. M.H. Thamrin No. 1, Jakarta Pusat" },
    { name: "Resepsi", date: "2027-09-18T19:00:00+07:00", time: "19.00 – 22.00 WIB", venue: "Bali Room", address: "Hotel Indonesia Kempinski, Jl. M.H. Thamrin No. 1, Jakarta Pusat" },
  ],
  gallery: ["/themes/img/a86.webp", "/themes/img/a85.webp", "/themes/img/a87.webp", "/themes/img/a118.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0938 44", account_name: "Kirana Maheswari Tanoto" },
    { id: "demo-kado", type: "address", address: "Jl. Kertanegara No. 18, Kebayoran Baru, Jakarta Selatan 12110" },
  ],
  guestName: "Bapak Robert Gunawan & Partner",
  guestTable: "Meja Malakit 3",
  extras: {
    quote: { text: "Cinta tidak berarti saling memandang, melainkan bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupery" },
    rundown: { items: [
      { time: "19.00", title: "Cocktail & sambutan tamu", note: "Foyer Bali Room" },
      { time: "19.45", title: "Grand entrance" },
      { time: "20.15", title: "Makan malam & toast keluarga" },
      { time: "21.00", title: "Dansa pertama & pesta" },
    ] },
    dressCode: { note: "Black tie. Nuansa hijau zamrud, hitam, dan emas sangat dianjurkan.", colors: ["#0f4a30", "#0b0f0c", "#c9a04e", "#efe8da"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendra Tanoto", "Kel. Besar Bpk. Daniel Halim"] },
    faq: { items: [
      { q: "Apakah tersedia valet parking?", a: "Ya, valet tersedia di lobi utama hotel untuk seluruh tamu undangan." },
      { q: "Bolehkah membawa anak?", a: "Resepsi malam diperuntukkan bagi tamu dewasa. Terima kasih atas pengertiannya." },
    ] },
  },
});
