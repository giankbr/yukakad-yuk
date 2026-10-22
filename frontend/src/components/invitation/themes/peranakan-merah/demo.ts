import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Lian", groom: "Kevin",
    brideFull: "Lian Kartika Tjoa, S.Ds.", groomFull: "Kevin Adiputra Oey, S.T.",
    brideParents: "Putri kedua dari\nBapak Hendra Tjoa & Ibu Lanny Wijaya", groomParents: "Putra sulung dari\nBapak Johan Oey & Ibu Meliana Lim",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Kasih itu sabar; kasih itu murah hati. Ia menutupi segala sesuatu, percaya segala sesuatu, mengharapkan segala sesuatu.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-22T10:00:00+07:00",
  place: "Gedung Monod Diephuis",
  address: "Jl. Kepodang No. 11, Purwodinatan, Semarang Tengah, Kota Semarang",
  stories: [
    { date: "2018", title: "Pecinan Semarang", body: "Kami berkenalan di Pasar Semawis, berebut kursi terakhir di depan penjual lumpia pada suatu malam Sabtu." },
    { date: "2022", title: "Pulang ke Lasem", body: "Lian mengajak Kevin ke rumah keluarga di Lasem. Di beranda bertegel tua itu, ia belajar menyeduh teh untuk para tetua." },
    { date: "2026", title: "Lamaran", body: "Keluarga Oey dari Tangerang datang membawa seserahan dan nampan merah. Kedua keluarga sepakat menautkan dua rumah." },
    { date: "2027", title: "Hari Bahagia", body: "Dengan berkat Tuhan dan restu orang tua, kami mengikat janji di Semarang." },
  ],
  events: [
    { name: "Upacara Teh (Tea Pai)", date: "2027-05-21T16:00:00+07:00", time: "16.00 – 18.00 WIB", venue: "Rumah Keluarga Tjoa", address: "Jl. Karangturi Gg. 4, Soditan, Lasem, Kabupaten Rembang" },
    { name: "Pemberkatan Nikah", date: "2027-05-22T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "GPIB Immanuel (Gereja Blenduk)", address: "Jl. Letjen Suprapto No. 32, Tanjung Mas, Semarang Utara, Kota Semarang" },
    { name: "Resepsi", date: "2027-05-22T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Gedung Monod Diephuis", address: "Jl. Kepodang No. 11, Purwodinatan, Semarang Tengah, Kota Semarang" },
  ],
  gallery: ["/themes/img/a31.webp", "/themes/img/a27.webp", "/themes/img/a28.webp", "/themes/img/a29.webp", "/themes/img/a25.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0095 7788 12", account_name: "Lian Kartika Tjoa" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "135 00 1122 334 5", account_name: "Kevin Adiputra Oey" },
    { id: "demo-kado", type: "address", address: "Jl. Gang Pinggir No. 28, Kranggan, Semarang Tengah, Kota Semarang 50137" },
  ],
  guestName: "Bapak Budi Hartanto & Keluarga",
  guestTable: "Meja Peoni 3",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "18.30", title: "Kedatangan tamu", note: "Diiringi gambang kromong" },
      { time: "19.00", title: "Masuknya kedua mempelai" },
      { time: "19.30", title: "Doa & potong kue", note: "Jamuan nyonya: lontong cap go meh & bakmi" },
      { time: "20.15", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Batik pesisiran atau kebaya encim. Merah, emas, hijau giok, dan merah muda dipersilakan.", colors: ["#a8161f", "#d5a948", "#2f8a6c", "#e47d8f"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-05-22T10:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Tjoa (Lasem)", "Kel. Besar Oey (Tangerang)", "Kel. Wijaya", "Kel. Lim"] },
  },
});
