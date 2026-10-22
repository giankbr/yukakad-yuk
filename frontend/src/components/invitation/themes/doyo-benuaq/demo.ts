import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Lusi", groom: "Dodi",
    brideFull: "Maria Lusiana Nyurang, S.Pd.", groomFull: "Kristianus Dodi Aleng, S.Hut.",
    brideParents: "Putri ketiga dari\nBapak Yohanes Lerang & Ibu Martina Inen", groomParents: "Putra sulung dari\nBapak Paulus Asang & Ibu Veronika Uyang",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r29.webp",
    note: "Serat doyo dipintal helai demi helai sampai kuat menjadi kain. Begitu juga kami, ingin saling menguatkan setiap hari.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T10:00:00+08:00",
  place: "Lamin Adat Eheng",
  address: "Kampung Eheng, Kec. Barong Tongkok, Kabupaten Kutai Barat, Kalimantan Timur",
  stories: [
    { date: "2018", title: "Di Tepi Mahakam", body: "Kami bertemu saat kegiatan penanaman pohon di hulu Mahakam. Dodi membawa bibit, Lusi membawa catatan." },
    { date: "2023", title: "Belajar Menenun", body: "Lusi mengajak Dodi menemui neneknya yang masih menenun ulap doyo. Dari sana ia belajar arti kesabaran." },
    { date: "2027", title: "Satu Lamin", body: "Dengan restu kedua keluarga, kami melangkah ke pelaminan dan pulang ke satu rumah." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-08-14T10:00:00+08:00", time: "10.00 – 11.30 WITA", venue: "Gereja Paroki Barong Tongkok", address: "Jl. Sendawar Raya, Barong Tongkok, Kutai Barat, Kalimantan Timur" },
    { name: "Resepsi di Lamin", date: "2027-08-14T16:00:00+08:00", time: "16.00 – 20.00 WITA", venue: "Lamin Adat Eheng", address: "Kampung Eheng, Kec. Barong Tongkok, Kutai Barat, Kalimantan Timur" },
  ],
  gallery: ["/themes/img/r108.webp", "/themes/img/r27.webp", "/themes/img/r29.webp", "/themes/img/a26.webp", "/themes/img/r81.webp"],
  gifts: [
    { id: "demo-bankaltim", type: "bank", bank_name: "Bankaltimtara", account_number: "0071 2345 678", account_name: "Maria Lusiana Nyurang" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0571 01 012345 50 9", account_name: "Kristianus Dodi Aleng" },
    { id: "demo-kado", type: "address", address: "Jl. Kampung Eheng RT 03, Barong Tongkok, Kutai Barat, Kalimantan Timur 75776" },
  ],
  guestName: "Bapak Fransiskus Ngayoq & Keluarga",
  guestTable: "Meja Ulin 4",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "16.00", title: "Penyambutan tamu di lamin", note: "Diiringi petikan sampeq" },
      { time: "17.00", title: "Doa & sambutan keluarga" },
      { time: "18.00", title: "Makan bersama", note: "Hidangan khas Kutai Barat" },
      { time: "19.00", title: "Tari gantar bersama" },
    ] },
    dressCode: { note: "Busana adat atau batik. Warna serat alam, merah, dan hitam dipersilakan.", colors: ["#c4a97c", "#2a1d15", "#8b2b1d", "#3e5a48"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T10:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Yohanes Lerang", "Kel. Besar Paulus Asang", "Warga Kampung Eheng"] },
  },
});
