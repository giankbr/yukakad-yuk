import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Dimas",
    brideFull: "Kirana Larasati Putri", groomFull: "Dimas Aryo Wicaksono",
    brideParents: "Putri bungsu dari\nBapak Handoko Wibisono & Ibu Ratna Dewi", groomParents: "Putra kedua dari\nBapak Bambang Sutejo & Ibu Lestari Ningsih",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r26.webp",
    note: "Satu ikat mawar, dua gelas kopi, dan obrolan yang tidak pernah selesai sejak hari Sabtu itu.",
  },
  eventLabel: "Pernikahan",
  date: "2027-04-17T10:00:00+07:00",
  place: "Rumah Kebun Cipete",
  address: "Jl. Cipete Raya No. 41, Cilandak, Jakarta Selatan",
  stories: [
    { date: "2021", title: "Pagi di Rawa Belong", body: "Kirana mencari bunga untuk toko kecilnya, Dimas mencari buket untuk wisuda adiknya. Kami berebut ikatan mawar terakhir, lalu tertawa bersama." },
    { date: "2023", title: "Kios Kecil Kami", body: "Dimas ikut membantu setiap Sabtu pagi: mengangkat ember, menulis harga di papan kapur, dan belajar membedakan lisianthus dari mawar." },
    { date: "2026", title: "Buket yang Berbeda", body: "Suatu pagi Dimas membungkus buket sendiri, lengkap dengan kartu kecil bertuliskan satu pertanyaan. Jawabannya: iya." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-04-17T10:00:00+07:00", time: "10.00 – 11.00 WIB", venue: "Rumah Kebun Cipete", address: "Jl. Cipete Raya No. 41, Cilandak, Jakarta Selatan" },
    { name: "Resepsi Kebun", date: "2027-04-17T12:00:00+07:00", time: "12.00 – 15.00 WIB", venue: "Rumah Kebun Cipete", address: "Jl. Cipete Raya No. 41, Cilandak, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/r64.webp", "/themes/img/r75.webp", "/themes/img/r16.webp", "/themes/img/r27.webp", "/themes/img/r62.webp", "/themes/img/r79.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0388 91", account_name: "Kirana Larasati Putri" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0812 9034 5512", account_name: "Dimas Aryo Wicaksono" },
    { id: "demo-kado", type: "address", address: "Kios Bunga Kirana, Pasar Bunga Rawa Belong Blok B No. 7, Kebon Jeruk, Jakarta Barat 11530" },
  ],
  guestName: "Kak Anindya & Partner",
  guestTable: "Meja Tulip",
  extras: {
    rundown: { items: [
      { time: "10.00", title: "Upacara pernikahan", note: "Di bawah pergola mawar" },
      { time: "12.00", title: "Makan siang di kebun" },
      { time: "13.30", title: "Rangkai buket sendiri", note: "Setiap tamu pulang membawa satu ikat bunga" },
      { time: "14.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Warna-warna bunga yang ceria: merah muda, kuning mentega, lilac, dan hijau daun.", colors: ["#ef9fb2", "#f5cf5a", "#b49ad8", "#86a77a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Bapak Handoko Wibisono", "Kel. Bapak Bambang Sutejo", "Teman-teman Pasar Bunga Rawa Belong"] },
  },
});
