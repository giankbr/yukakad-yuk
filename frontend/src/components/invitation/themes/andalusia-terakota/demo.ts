import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salsabila", groom: "Ihsan",
    brideFull: "Salsabila Khairunnisa, M.Hum.", groomFull: "Muhammad Ihsan Al-Ghifari, Lc.",
    brideParents: "Putri bungsu dari\nBapak Dr. H. Ahmad Syafi'i & Ibu Hj. Nur Azizah",
    groomParents: "Putra sulung dari\nBapak H. Muhammad Yusran & Ibu Hj. Halimah Tusa'diyah",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Di bawah lengkung-lengkung yang dibangun dengan sabar, kami ingin membangun rumah tangga yang teduh dan penuh berkah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-08-28T09:00:00+07:00",
  place: "Masjid Al-Akbar Surabaya",
  address: "Jl. Masjid Al-Akbar Timur No. 1, Pagesangan, Jambangan, Surabaya",
  stories: [
    { date: "2019", title: "Perpustakaan Kampus", body: "Salsabila meneliti naskah-naskah Andalusia, Ihsan baru pulang menimba ilmu. Kami berkenalan di rak buku sejarah." },
    { date: "2025", title: "Ta'aruf", body: "Didampingi keluarga, kami saling mengenal visi dan cita-cita, lalu memantapkan hati dengan istikharah." },
    { date: "April 2027", title: "Khitbah", body: "Keluarga Ihsan datang meminang dengan tradisi Jawa Timur yang hangat dan sederhana." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-28T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Al-Akbar Surabaya", address: "Jl. Masjid Al-Akbar Timur No. 1, Pagesangan, Jambangan, Surabaya" },
    { name: "Walimah", date: "2027-08-28T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Graha Sawunggaling", address: "Jl. Jimerto No. 25–27, Ketabang, Genteng, Surabaya" },
  ],
  gallery: ["/themes/img/a31.webp", "/themes/img/a43.webp", "/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/a18.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-muamalat", type: "bank", bank_name: "Bank Muamalat", account_number: "1420 0098 7654", account_name: "Salsabila Khairunnisa" },
    { id: "demo-kado", type: "address", address: "Jl. Darmo Permai III No. 12, Pradahkalikendal, Dukuh Pakis, Surabaya 60226" },
  ],
  guestName: "Ibu Hj. Maryam Syarifah & Keluarga",
  guestTable: "Meja Granada 2",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "09.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "10.00", title: "Doa bersama & nasihat pernikahan" },
      { time: "18.30", title: "Walimah dibuka" },
      { time: "19.30", title: "Ramah tamah & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim formal. Terakota, biru kobalt, dan krem batu dipersilakan.", colors: ["#a4472a", "#23418f", "#e9d9bd", "#c08a3e"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-28T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Dr. H. Ahmad Syafi'i", "Kel. Besar H. Muhammad Yusran"] },
  },
});
