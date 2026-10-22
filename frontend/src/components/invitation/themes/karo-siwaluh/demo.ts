import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ruth", groom: "Andreas",
    brideFull: "Ruth Natalia br Tarigan, S.P.", groomFull: "Andreas Sembiring Meliala, S.T.",
    brideParents: "Putri sulung dari\nBapak Rudi Tarigan & Ibu Saripah br Sitepu", groomParents: "Putra kedua dari\nBapak Jhonson Sembiring & Ibu Rosmawati br Ginting",
    bridePhoto: "/themes/img/r28.webp", groomPhoto: "/themes/img/r26.webp",
    note: "Seperti delapan keluarga yang hidup rukun di bawah satu atap siwaluh jabu, kami ingin membangun rumah yang hangat bagi semua.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T09:00:00+07:00",
  place: "Jambur Taman Mejuah-juah",
  address: "Jl. Jamin Ginting, Gundaling I, Berastagi, Kabupaten Karo, Sumatera Utara",
  stories: [
    { date: "2019", title: "Pasar Buah Berastagi", body: "Ruth sedang meneliti jeruk Karo untuk skripsinya, Andreas membantu ladang keluarganya. Kami berkenalan di antara tumpukan jeruk dan markisa." },
    { date: "2023", title: "Mendaki Sibayak", body: "Menunggu matahari terbit di puncak Sibayak, dengan Sinabung di kejauhan, Andreas bertanya apakah Ruth mau berjalan bersamanya seumur hidup." },
    { date: "2027", title: "Erdemu Bayu", body: "Dengan restu sangkep nggeluh kedua keluarga, kalimbubu, senina, dan anak beru, kami dipersatukan dalam kasih Tuhan." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-06-19T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "GBKP Runggun Berastagi Kota", address: "Jl. Veteran No. 12, Berastagi, Kabupaten Karo" },
    { name: "Pesta Adat Erdemu Bayu", date: "2027-06-19T11:30:00+07:00", time: "11.30 – selesai", venue: "Jambur Taman Mejuah-juah", address: "Jl. Jamin Ginting, Gundaling I, Berastagi, Kabupaten Karo" },
  ],
  gallery: ["/themes/img/r104.webp", "/themes/img/a116.webp", "/themes/img/a22.webp", "/themes/img/r16.webp", "/themes/img/r28.webp", "/themes/img/r26.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BRI", account_number: "3392 0102 7745 508", account_name: "Ruth Natalia br Tarigan" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "106 00 1477 2093", account_name: "Andreas Sembiring Meliala" },
    { id: "demo-kado", type: "address", address: "Jl. Udara Gg. Mawar No. 5, Berastagi, Kabupaten Karo 22152" },
  ],
  guestName: "Bapak Edison Perangin-angin & Keluarga",
  guestTable: "Kalimbubu 3",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "11.30", title: "Kedatangan kalimbubu & sangkep nggeluh" },
      { time: "12.30", title: "Landek bersama", note: "Diiringi gendang lima sendalanen" },
      { time: "13.30", title: "Makan bersama", note: "Cipera, babi panggang Karo & arsik" },
      { time: "14.30", title: "Ngerana & pemberian uis" },
    ] },
    dressCode: { note: "Uis Karo atau busana formal bernuansa merah hati, hitam, dan emas.", colors: ["#a3201d", "#1b1514", "#d7a43c", "#f4ead6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Tarigan – Sitepu", "Kel. Besar Sembiring Meliala – Ginting", "Jemaat GBKP Runggun Berastagi Kota"] },
  },
});
