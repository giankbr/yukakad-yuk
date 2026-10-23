import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Tiara", groom: "Yosua",
    brideFull: "Tiara Maharani Kusuma, S.Ds.", groomFull: "Yosua Hendrawan Putra, S.Ars.",
    brideParents: "Putri pertama dari\nBapak Stefanus Kusuma & Ibu Lidia Kartika", groomParents: "Putra ketiga dari\nBapak Paulus Hendrawan & Ibu Ruth Anggraeni",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r4.webp",
    note: "Seperti selembar kertas yang digulung pelan-pelan, cinta kami tumbuh satu lilitan demi satu lilitan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-09T17:00:00+07:00",
  place: "Galeri Rumah Kertas",
  address: "Jl. Kepodang No. 18, Purwodinatan, Kota Lama, Semarang Tengah, Kota Semarang",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2019", title: "Lokakarya Hari Minggu", body: "Tiara mengajar kelas quilling di sebuah kedai kopi di Kota Lama. Yosua datang terlambat dan membuat bunga paling miring di kelas." },
    { date: "2022", title: "Satu Gulungan per Minggu", body: "Setiap minggu Yosua mengirim satu bunga kertas buatannya. Tiara menyimpannya di sebuah kotak, sampai kotaknya penuh." },
    { date: "2026", title: "Cincin di Tengah Bunga", body: "Di ulang tahun Tiara, kotak itu kembali dengan satu bunga baru. Di tengahnya, bukan gulungan kertas, melainkan cincin." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-10-09T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Taman Belakang Rumah Kertas", address: "Jl. Kepodang No. 18, Purwodinatan, Kota Lama, Semarang Tengah, Kota Semarang" },
    { name: "Resepsi", date: "2027-10-09T17:00:00+07:00", time: "17.00 – 20.00 WIB", venue: "Galeri Rumah Kertas", address: "Jl. Kepodang No. 18, Purwodinatan, Kota Lama, Semarang Tengah, Kota Semarang" },
  ],
  gallery: ["/themes/img/r92.webp", "/themes/img/a23.webp", "/themes/img/r5.webp", "/themes/img/r82.webp", "/themes/img/r13.webp", "/themes/img/a124.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0921 1009 27", account_name: "Tiara Maharani Kusuma" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0812 2910 0927", account_name: "Yosua Hendrawan Putra" },
    { id: "demo-kado", type: "address", address: "Jl. Pandanaran II No. 7, Mugassari, Semarang Selatan, Kota Semarang 50249" },
  ],
  guestName: "Ibu Lestari Wibisono & Keluarga",
  guestTable: "Melati 2",
  extras: {
    quote: { text: "Cinta bukan sekali jadi. Ia digulung pelan, dibentuk dengan sabar, lalu disatukan dengan hati-hati.", source: "Tiara & Yosua" },
    rundown: { items: [
      { time: "17.00", title: "Penyambutan tamu", note: "Pameran karya quilling kedua mempelai di lorong galeri" },
      { time: "17.45", title: "Kirab pengantin" },
      { time: "18.15", title: "Makan malam & hiburan akustik" },
      { time: "19.15", title: "Membuat bunga kertas bersama", note: "Bawa pulang hasil karyamu" },
    ] },
    dressCode: { note: "Warna pastel lembut: merah muda pudar, hijau sage, krem, dan sentuhan mustard.", colors: ["#cf6f80", "#8fae8b", "#f3e6c8", "#e0ac45"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Stefanus Kusuma", "Kel. Besar Bpk. Paulus Hendrawan", "Komunitas Quilling Semarang"] },
    faq: { items: [
      { q: "Apakah ada area parkir?", a: "Parkir tersedia di Taman Srigunting, sekitar 3 menit berjalan kaki ke galeri." },
      { q: "Boleh membawa anak?", a: "Tentu, ada meja kreasi kertas khusus untuk anak-anak." },
    ] },
  },
});
