import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Dimas",
    brideFull: "Kirana Maheswari", groomFull: "Dimas Arya Wicaksana",
    brideParents: "Putri dari\nBapak Hendra Gunawan & Ibu Lestari Wulandari", groomParents: "Putra dari\nBapak Bambang Wicaksono & Ibu Ratna Sari",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Hujan, lampu jalan, dan satu payung untuk berdua. Kisah kami dimulai seperti film lama, dan kami ingin kalian ada di adegan berikutnya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-23T16:00:00+07:00",
  place: "Gedung Arsip Nasional",
  address: "Jl. Gajah Mada No. 111, Krukut, Kec. Taman Sari, Jakarta Barat",
  stories: [
    { date: "Adegan I · 2020", title: "Hujan di Kota Tua", body: "Hujan turun deras di Kota Tua. Kirana berteduh di bawah tenda kedai, Dimas datang membawa payung yang terlalu kecil untuk berdua. Kami tetap berbagi." },
    { date: "Adegan II · 2023", title: "Bioskop Tengah Malam", body: "Setiap Jumat kami menonton film klasik di bioskop kecil di Cikini. Popcorn dibagi dua, komentar disimpan sampai lampu menyala." },
    { date: "Adegan III · 2027", title: "Satu Pertanyaan", body: "Di bawah lampu jalan yang sama, Dimas bertanya. Kirana menjawab sebelum hujan sempat reda." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-10-23T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Gedung Arsip Nasional", address: "Jl. Gajah Mada No. 111, Krukut, Kec. Taman Sari, Jakarta Barat" },
    { name: "Resepsi Malam", date: "2027-10-23T19:00:00+07:00", time: "19.00 – 22.00 WIB", venue: "Gedung Kesenian Jakarta", address: "Jl. Gedung Kesenian No. 1, Ps. Baru, Kecamatan Sawah Besar, Jakarta Pusat" },
  ],
  gallery: ["/themes/img/r56.webp", "/themes/img/a76.webp", "/themes/img/a77.webp", "/themes/img/r88.webp", "/themes/img/r55.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0398 44", account_name: "Kirana Maheswari" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1270 0091 8832 6", account_name: "Dimas Arya Wicaksana" },
    { id: "demo-kado", type: "address", address: "Jl. Cikini Raya No. 52, Menteng, Jakarta Pusat 10330", account_name: "Kirana & Dimas" },
  ],
  guestName: "Sdr. Rendy Pratama & Partner",
  guestTable: "Kursi Balkon B4",
  extras: {
    quote: { text: "Kota ini penuh lampu, tapi hanya satu yang membuat kami berhenti di tengah hujan dan memutuskan untuk pulang bersama.", source: "Kirana & Dimas" },
    rundown: { items: [
      { time: "19.00", title: "Karpet merah & foto hitam-putih", note: "Booth foto bergaya studio 1940-an" },
      { time: "19.45", title: "Pemutaran film pendek kisah kami" },
      { time: "20.15", title: "Jamuan malam & musik jazz" },
      { time: "21.30", title: "Dansa penutup" },
    ] },
    dressCode: { note: "Hitam, putih, dan abu-abu. Topi fedora dan sarung tangan sangat dipersilakan.", colors: ["#0e0e0f", "#4a4a4d", "#b9b7b2", "#efede7"] },
    guestPass: {},
    family: { names: ["Kel. Bapak Hendra Gunawan", "Kel. Bapak Bambang Wicaksono"] },
  },
});
