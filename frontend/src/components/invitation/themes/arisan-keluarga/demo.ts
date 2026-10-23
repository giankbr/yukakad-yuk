import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Keluarga Susanto", groom: "",
    brideFull: "Bapak Hendra Susanto & Ibu Rini Wulandari",
    brideParents: "Tuan rumah arisan bulan Oktober,\nbersama Alya, Bima, dan Eyang Putri Sumarni",
    note: "Sebulan sekali kita pulang ke satu ruang tamu: teh manis, kue basah, cerita yang tidak habis-habis, dan satu nama yang keluar dari gelas kocokan.",
  },
  eventLabel: "Arisan Keluarga",
  date: "2027-10-17T10:00:00+07:00",
  place: "Kediaman Keluarga Susanto",
  address: "Perum Griya Sari Blok C-12, Jl. Kaliurang Km 7, Sinduharjo, Ngaglik, Sleman, DI Yogyakarta",
  story: { title: "Cerita Arisan Kita", body: "" },
  stories: [
    { date: "2009", title: "Arisan pertama di rumah Eyang", body: "Delapan keluarga, satu tikar pandan, dan iuran sepuluh ribu rupiah. Eyang Kakung sendiri yang mengocok gelas pertama." },
    { date: "2016", title: "Makin ramai, makin seru", body: "Cucu-cucu ikut datang, kue dibagi giliran, dan grup keluarga mulai dipakai untuk mengingatkan jadwal dan iuran." },
    { date: "2027", title: "Putaran ke-7, giliran kami", body: "Bulan ini Keluarga Susanto menjadi tuan rumah. Siapkan perut untuk klepon buatan Eyang Putri dan risoles Bu Rini." },
  ],
  events: [
    { name: "Kumpul & Makan Siang", date: "2027-10-17T10:00:00+07:00", time: "10.00 – 12.00 WIB", venue: "Kediaman Keluarga Susanto", address: "Perum Griya Sari Blok C-12, Jl. Kaliurang Km 7, Sinduharjo, Ngaglik, Sleman, DI Yogyakarta" },
    { name: "Kocokan Arisan Putaran ke-7", date: "2027-10-17T12:30:00+07:00", time: "12.30 – 13.30 WIB", venue: "Ruang tamu Keluarga Susanto", address: "Perum Griya Sari Blok C-12, Jl. Kaliurang Km 7, Sinduharjo, Ngaglik, Sleman, DI Yogyakarta" },
  ],
  gallery: ["/themes/img/r74.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BRI", account_number: "0029 0103 4477 508", account_name: "Rini Wulandari (Bendahara Arisan)" },
  ],
  guestName: "Keluarga Om Bambang & Tante Wati",
  guestTable: "",
  extras: {
    rundown: { items: [
      { time: "10.00", title: "Datang, salaman, dan teh manis" },
      { time: "10.30", title: "Kabar keluarga dan pengumuman", note: "Termasuk kabar cucu yang baru wisuda" },
      { time: "11.15", title: "Makan siang bersama", note: "Soto ayam dan kue-kue tradisional" },
      { time: "12.30", title: "Setor iuran dan kocokan", note: "Pemenang jadi tuan rumah bulan depan" },
    ] },
    dressCode: { note: "Santai dan nyaman. Kalau mau kompak, pakai batik atau atasan warna hijau mint.", colors: ["#9fd3bd", "#d0643c", "#f3c74e", "#ef9bb0"] },
    guestPass: {},
    rsvpDietary: {},
    faq: { items: [
      { q: "Berapa iuran bulan ini?", a: "Rp200.000 per keluarga, sama seperti putaran sebelumnya. Bisa dibayar di tempat atau ditransfer ke bendahara." },
      { q: "Boleh membawa makanan?", a: "Boleh sekali. Kabari di grup supaya menunya tidak kembar, ya." },
      { q: "Parkirnya di mana?", a: "Mobil bisa parkir di sepanjang jalan blok C. Motor masuk ke halaman rumah." },
    ] },
  },
});
