import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Raka",
    brideFull: "Sekar Ayudia Prameswari, M.Ars.", groomFull: "Raka Pradipta Wiratama, S.Si.",
    brideParents: "Putri tunggal dari\nBapak Ir. Bambang Sutejo & Ibu Dian Kartika", groomParents: "Putra kedua dari\nBapak Agus Wiratama & Ibu Lestari Handayani",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Seperti telaga di kaki gunung: tenang di permukaan, dalam di dasarnya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T09:00:00+07:00",
  place: "Dermaga Kayu Situ Patenggang",
  address: "Kawasan Wisata Situ Patenggang, Patengan, Rancabali, Kabupaten Bandung",
  stories: [
    { date: "2018", title: "Pendakian Pertama", body: "Kami berkenalan di jalur pendakian Papandayan, tersesat di kabut pagi dan menemukan jalan pulang bersama." },
    { date: "2022", title: "Pagi-Pagi Berkabut", body: "Setiap libur panjang kami berburu telaga: Sarangan, Dieng, lalu kembali lagi ke Patenggang." },
    { date: "2027", title: "Di Tepi Telaga", body: "Di dermaga yang sama tempat Raka melamar, kami mengikat janji di hadapan keluarga." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-08-21T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Dermaga Kayu Situ Patenggang", address: "Kawasan Wisata Situ Patenggang, Patengan, Rancabali, Kabupaten Bandung" },
    { name: "Resepsi Tepi Telaga", date: "2027-08-21T12:00:00+07:00", time: "12.00 – 15.00 WIB", venue: "Paviliun Kebun Teh Rancabali", address: "Jl. Raya Ciwidey – Rancabali Km. 39, Kabupaten Bandung" },
  ],
  gallery: ["/themes/img/a30.webp", "/themes/img/a116.webp", "/themes/img/a33.webp", "/themes/img/r102.webp", "/themes/img/a77.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "1320 0456 7788", account_name: "Sekar Ayudia Prameswari" },
    { id: "demo-kado", type: "address", address: "Jl. Dago Pakar Timur No. 12, Cimenyan, Kabupaten Bandung 40198" },
  ],
  guestName: "Bapak Herman Susanto & Keluarga",
  guestTable: "Meja 9",
  extras: {
    quote: { text: "Mencintai bukan berarti saling memandang, melainkan bersama-sama memandang ke arah yang sama.", source: "Antoine de Saint-Exupéry" },
    rundown: { items: [
      { time: "12.00", title: "Teh hangat & sambutan", note: "Di paviliun menghadap kebun teh" },
      { time: "12.30", title: "Jamuan siang" },
      { time: "13.30", title: "Akustik tepi telaga" },
      { time: "14.30", title: "Foto bersama di dermaga" },
    ] },
    dressCode: { note: "Udara Rancabali sejuk (± 18°C). Nuansa sage, abu kebiruan, dan krem; bawa jaket tipis.", colors: ["#8fa094", "#6f8290", "#e9ecea", "#3f5560"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-21T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    travel: { note: "Perjalanan dari Bandung kota ± 2 jam. Jalan berkelok, mohon berangkat lebih pagi.", items: [
      { name: "Shuttle tamu", detail: "Berangkat 07.00 dari Jl. Dago, kembali 16.00" },
      { name: "Penginapan", detail: "Glamping & vila di sekitar Rancabali" },
    ] },
    family: { names: ["Kel. Besar Bpk. Ir. Bambang Sutejo", "Kel. Besar Bpk. Agus Wiratama"] },
  },
});
