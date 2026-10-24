import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Fitriyah", groom: "Hasyim",
    brideFull: "Fitriyah Nur Aini, S.E.", groomFull: "Moh. Hasyim Fadholi, S.Kom.",
    brideParents: "Putri ketiga dari\nBapak H. Abd. Rahem & Ibu Hj. Maimunah", groomParents: "Putra kedua dari\nBapak Moh. Sholeh & Ibu Siti Aminah",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti kain gentongan yang direndam berbulan-bulan, semoga cinta kami makin dalam warnanya seiring waktu.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T09:00:00+07:00",
  place: "Gedung Serbaguna Tanjung Bumi",
  address: "Jl. Raya Tanjung Bumi, Kec. Tanjung Bumi, Kabupaten Bangkalan, Jawa Timur",
  stories: [
    { date: "2020", title: "Di Sanggar Batik", body: "Hasyim datang memotret para pembatik Tanjung Bumi untuk tugas kuliah. Fitriyah yang menjelaskan arti setiap motif." },
    { date: "2024", title: "Warna yang Meresap", body: "Pelan-pelan, seperti pewarna yang meresap ke serat kain, kami saling mengenal dan menguatkan." },
    { date: "2027", title: "Kain Satu Lembar", body: "Dengan restu kedua keluarga, kami menyatukan dua kisah menjadi satu lembar kain kehidupan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Kediaman Mempelai Putri", address: "Desa Telaga Biru, Kec. Tanjung Bumi, Kabupaten Bangkalan" },
    { name: "Resepsi", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Serbaguna Tanjung Bumi", address: "Jl. Raya Tanjung Bumi, Kec. Tanjung Bumi, Kabupaten Bangkalan, Jawa Timur" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a28.webp", "/themes/img/a29.webp", "/themes/img/a26.webp", "/themes/img/a30.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "6281 0102 4455 507", account_name: "Fitriyah Nur Aini" },
    { id: "demo-kado", type: "address", address: "Desa Telaga Biru RT 02 RW 01, Kec. Tanjung Bumi, Kabupaten Bangkalan 69156" },
  ],
  guestName: "Bapak H. Mat Sahri & Keluarga",
  guestTable: "Meja Gentong 4",
  extras: {
    quote: { text: "Mereka adalah pakaian bagimu, dan kamu pun adalah pakaian bagi mereka.", source: "QS. Al-Baqarah: 187" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan tamu & hiburan musik saronen" },
      { time: "11.30", title: "Kirab pengantin" },
      { time: "12.00", title: "Ramah tamah & doa bersama" },
    ] },
    dressCode: { note: "Batik atau busana muslim. Merah mengkudu, biru, dan cokelat soga dipersilakan.", colors: ["#8e1e17", "#1f2e57", "#8a5428", "#efe2c4"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abd. Rahem", "Kel. Besar Moh. Sholeh"] },
  },
});
