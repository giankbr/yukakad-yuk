import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salsabila", groom: "Rafi",
    brideFull: "Salsabila Putri Ardani, S.Ars.", groomFull: "Rafi Hanafi Siregar, S.T.",
    brideParents: "Putri pertama dari\nBapak Ir. Didik Ardani & Ibu Maryam Suhaila", groomParents: "Putra ketiga dari\nBapak H. Burhanuddin Siregar & Ibu Nurhayati",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Garis-garis yang berbeda, ditarik dari satu titik pusat yang sama. Begitulah kami ingin membangun rumah: tertata, saling menguatkan, dan kembali kepada-Nya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-11T08:30:00+07:00",
  place: "Galeri Nasional Indonesia, Gedung C",
  address: "Jl. Medan Merdeka Timur No. 14, Gambir, Jakarta Pusat",
  stories: [
    { date: "2019", title: "Studio Tingkat Akhir", body: "Satu meja gambar di studio arsitektur. Salsabila menggambar pola, Rafi menghitung strukturnya." },
    { date: "2025", title: "Proyek Masjid Desa", body: "Kami bertemu lagi saat merancang masjid kecil di Tapanuli. Di sana Rafi memberanikan diri bersilaturahmi ke keluarga." },
    { date: "2027", title: "Akad", body: "Bismillah, dua garis kini bertemu dalam satu pola." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-11T08:30:00+07:00", time: "08.30 – 09.30 WIB", venue: "Masjid Cut Meutia", address: "Jl. Cut Meutia No. 1, Menteng, Jakarta Pusat" },
    { name: "Walimatul 'Ursy", date: "2027-09-11T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Galeri Nasional Indonesia, Gedung C", address: "Jl. Medan Merdeka Timur No. 14, Gambir, Jakarta Pusat" },
  ],
  gallery: ["/themes/img/a74.webp", "/themes/img/r88.webp", "/themes/img/a75.webp", "/themes/img/r56.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7130 2219 45", account_name: "Salsabila Putri Ardani" },
    { id: "demo-kado", type: "address", address: "Jl. Tebet Barat Dalam X No. 21, Tebet, Jakarta Selatan 12810" },
  ],
  guestName: "Bapak Arif Wicaksono & Partner",
  guestTable: "Meja 08",
  extras: {
    quote: { text: "Dan Dia menciptakan segala sesuatu, lalu menetapkan ukuran-ukurannya dengan tepat.", source: "QS. Al-Furqan: 2" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan", note: "Pameran sketsa kami di lobi" },
      { time: "11.45", title: "Doa & tausiyah singkat" },
      { time: "12.15", title: "Santap siang", note: "Meja panjang, tanpa pelaminan" },
    ] },
    dressCode: { note: "Hitam, putih, dan abu-abu. Satu aksen merah bata dipersilakan.", colors: ["#141414", "#fbfaf7", "#9a9a9a", "#c4412b"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Ir. Didik Ardani", "Kel. Besar H. Burhanuddin Siregar"] },
  },
});
