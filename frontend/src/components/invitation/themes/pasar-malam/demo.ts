import { makeDemo } from "../demo-base";

// Pernikahan bertema pasar malam di Kota Lama Semarang: bianglala, komidi putar, gulali, dan lapak jajanan.
export const demo = makeDemo({
  couple: {
    bride: "Tari", groom: "Gilang",
    brideFull: "Lestari Ayu Wulandari", groomFull: "Gilang Prasetyo Nugroho",
    brideParents: "Putri pertama dari\nBapak Bambang Riyadi & Ibu Endang Lestari", groomParents: "Putra ketiga dari\nBapak Haryanto & Ibu Sri Mulyani",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
    note: "Bianglala itu macet tepat di puncak, tujuh menit lamanya. Cukup waktu untuk berkenalan, berbagi gulali, dan memutuskan untuk naik lagi bersama, seumur hidup.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-09T19:00:00+07:00",
  place: "Taman Srigunting, Kota Lama Semarang",
  address: "Jl. Letjen Suprapto, Tanjung Mas, Kec. Semarang Utara, Kota Semarang, Jawa Tengah",
  stories: [
    { date: "Agustus 2021", title: "Macet di Puncak Bianglala", body: "Malam tujuhbelasan di alun-alun. Kami kebetulan satu gondola dengan dua orang asing lain, lalu bianglalanya berhenti di puncak. Tari menawarkan gulali, Gilang menawarkan cerita." },
    { date: "2023", title: "Langganan Lapak Lumpia", body: "Setiap Jumat malam kami janjian di pasar malam Semawis: lumpia, wedang tahu, dan satu putaran komidi putar yang selalu Tari menangkan." },
    { date: "Juni 2027", title: "Lamaran di Lempar Gelang", body: "Gilang sengaja kalah di permainan lempar gelang, lalu menukar hadiahnya dengan sebuah cincin. Penjaga lapaknya ikut bertepuk tangan." },
  ],
  events: [
    { name: "Ikrar Pernikahan", date: "2027-10-09T15:00:00+07:00", time: "15.00 – 16.30 WIB", venue: "Gedung Oudetrap", address: "Jl. Letjen Suprapto No. 34, Tanjung Mas, Kec. Semarang Utara, Kota Semarang" },
    { name: "Resepsi Pasar Malam", date: "2027-10-09T19:00:00+07:00", time: "19.00 – 22.30 WIB", venue: "Taman Srigunting, Kota Lama", address: "Jl. Letjen Suprapto, Tanjung Mas, Kec. Semarang Utara, Kota Semarang, Jawa Tengah" },
  ],
  gallery: ["/themes/img/r85.webp", "/themes/img/a140.webp", "/themes/img/r0.webp", "/themes/img/r6.webp", "/themes/img/r72.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0094 2271 58", account_name: "Lestari Ayu Wulandari" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "135 00 1946 2207", account_name: "Gilang Prasetyo Nugroho" },
    { id: "demo-kado", type: "address", address: "Jl. Gajahmada No. 88, Kembangsari, Kec. Semarang Tengah, Kota Semarang 50133", account_name: "Tari & Gilang" },
  ],
  guestName: "Mas Bagus Wicaksono & Pasangan",
  guestTable: "Lapak 7",
  extras: {
    quote: { text: "Hidup itu seperti bianglala: kadang di atas, kadang di bawah. Yang penting, kita naik di gondola yang sama.", source: "Tari & Gilang" },
    rundown: { items: [
      { time: "19.00", title: "Lapak dibuka", note: "Lumpia, gulali, jagung bakar, dan wedang ronde gratis untuk tamu" },
      { time: "19.45", title: "Kedua mempelai naik komidi putar" },
      { time: "20.15", title: "Makan malam & hiburan orkes keroncong" },
      { time: "21.30", title: "Lempar gelang berhadiah & foto bersama di bianglala mini" },
    ] },
    dressCode: { note: "Santai rapi ala pasar malam: merah bata, kuning mustard, hijau mint, atau merah muda gulali.", colors: ["#e8553f", "#f2b632", "#6cc2a6", "#f39bb5"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Bapak Bambang Riyadi", "Kel. Bapak Haryanto"] },
  },
});
