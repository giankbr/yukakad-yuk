import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Rasyid",
    brideFull: "Nadia Khairunnisa, S.Hum.", groomFull: "Rasyid Ilham Fadhlurrahman, M.A.",
    brideParents: "Putri ketiga dari\nBapak H. Syamsul Bahri & Ibu Hj. Rosmawati", groomParents: "Putra kedua dari\nBapak Dr. Ahmad Zaki & Ibu Laila Hanum",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti benang yang disulam satu demi satu, kami ingin merangkai hari-hari dengan sabar dan penuh warna.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-23T08:00:00+07:00",
  place: "Gedung Kemuning Gading",
  address: "Jl. Pangeran Sogiri No. 1, Tanah Baru, Bogor Utara, Kota Bogor",
  stories: [
    { date: "2022", title: "Bertemu di Bukhara", body: "Nadia meneliti naskah tua di Bukhara, Rasyid menuntaskan program bahasanya. Mereka berkenalan di pasar kain, di depan selembar suzani merah delima." },
    { date: "2025", title: "Khitbah", body: "Sepulang ke tanah air, setelah ta'aruf yang dijaga kedua keluarga, Rasyid datang bersama orang tuanya untuk mengkhitbah Nadia." },
    { date: "2027", title: "Menyulam Hari", body: "Dengan memohon ridha Allah, kami bersiap memulai babak baru: menyulam rumah tangga yang sakinah, mawaddah, wa rahmah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-23T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Raya Bogor", address: "Jl. Raya Pajajaran, Bantarjati, Bogor Utara, Kota Bogor" },
    { name: "Resepsi", date: "2027-10-23T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Kemuning Gading", address: "Jl. Pangeran Sogiri No. 1, Tanah Baru, Bogor Utara, Kota Bogor" },
  ],
  gallery: ["/themes/img/a40.webp", "/themes/img/r6.webp", "/themes/img/a118.webp", "/themes/img/r5.webp", "/themes/img/r62.webp", "/themes/img/r63.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7211 4590 33", account_name: "Nadia Khairunnisa" },
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0938 1172 45", account_name: "Rasyid Ilham Fadhlurrahman" },
    { id: "demo-kado", type: "address", address: "Jl. Kenari II No. 14, Tanah Baru, Bogor Utara, Kota Bogor 16154" },
  ],
  guestName: "Ibu Dr. Hj. Maryam Zahra & Keluarga",
  guestTable: "Meja Delima",
  extras: {
    quote: { text: "Mereka adalah pakaian bagimu, dan kamu adalah pakaian bagi mereka.", source: "QS. Al-Baqarah: 187" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Gambus & nasyid" },
      { time: "11.30", title: "Doa dan tausiyah singkat" },
      { time: "12.00", title: "Jamuan", note: "Plov nasi kebuli, samsa & teh rempah" },
      { time: "13.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim santun dengan sentuhan warna sulaman: merah delima, nila, kunyit, atau krem.", colors: ["#b0262c", "#262f69", "#e0a22a", "#f1e7d3"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Syamsul Bahri", "Kel. Besar Dr. Ahmad Zaki", "Alumni Pelajar Indonesia di Uzbekistan"] },
  },
});
