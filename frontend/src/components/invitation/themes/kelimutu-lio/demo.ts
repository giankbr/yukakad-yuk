import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Yohana", groom: "Alfons",
    brideFull: "Yohana Maria Wangge, S.Pd.", groomFull: "Alfonsus Nong Rangga, S.T.",
    brideParents: "Putri kedua dari\nBapak Fransiskus Mbete Wangge & Ibu Theresia Ndona", groomParents: "Putra sulung dari\nBapak Yosef Rangga Pora & Ibu Agnes Wea",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti tiga danau yang berganti warna tetapi tetap satu gunung, kami ingin bertumbuh bersama dalam setiap musim.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-17T09:00:00+08:00",
  place: "Gereja Katedral Kristus Raja Ende",
  address: "Jl. Katedral No. 5, Kel. Potulando, Kec. Ende Tengah, Kabupaten Ende",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2019", title: "Satu Kelas di Uniflor", body: "Kami bertemu di Universitas Flores. Yohana meminjamkan catatan, Alfons membalasnya dengan kopi Bajawa setiap pagi." },
    { date: "2023", title: "Fajar di Kelimutu", body: "Kami mendaki dari Moni pukul tiga pagi untuk melihat matahari terbit di atas tiga danau. Di sana Alfons berkata ingin pulang ke rumah yang sama." },
    { date: "2026", title: "Masuk Minta", body: "Keluarga besar Rangga datang ke rumah keluarga Wangge membawa tanda adat. Belis dibicarakan dengan hangat dan penuh kekeluargaan." },
  ],
  events: [
    { name: "Sakramen Perkawinan", date: "2027-07-17T09:00:00+08:00", time: "09.00 – 11.00 WITA", venue: "Gereja Katedral Kristus Raja Ende", address: "Jl. Katedral No. 5, Kel. Potulando, Kec. Ende Tengah, Kabupaten Ende" },
    { name: "Resepsi Pernikahan", date: "2027-07-17T17:00:00+08:00", time: "17.00 – 21.00 WITA", venue: "Gedung Serbaguna Paroki Onekore", address: "Jl. Gatot Subroto, Kel. Onekore, Kec. Ende Tengah, Kabupaten Ende" },
    { name: "Syukuran Keluarga di Moni", date: "2027-07-18T10:00:00+08:00", time: "10.00 WITA – selesai", venue: "Rumah Keluarga Rangga", address: "Jl. Trans Flores, Desa Koanara, Kec. Kelimutu, Kabupaten Ende" },
  ],
  gallery: ["/themes/img/a110.webp", "/themes/img/r104.webp", "/themes/img/r109.webp", "/themes/img/r108.webp", "/themes/img/r100.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "4521 0102 8873 509", account_name: "Yohana Maria Wangge" },
    { id: "demo-ntt", type: "bank", bank_name: "Bank NTT", account_number: "012 03 11 778901", account_name: "Alfonsus Nong Rangga" },
    { id: "demo-kado", type: "address", address: "Jl. Kelimutu No. 21, Kel. Kelimutu, Kec. Ende Tengah, Kabupaten Ende 86318" },
  ],
  guestName: "Bapak Paulus Dhae & Keluarga",
  guestTable: "Meja Tiwu 3",
  extras: {
    quote: { text: "Air yang banyak tak dapat memadamkan cinta, sungai-sungai tak dapat menghanyutkannya.", source: "Kidung Agung 8:7" },
    rundown: { items: [
      { time: "17.00", title: "Penyambutan tamu", note: "Diiringi musik gong waning" },
      { time: "17.30", title: "Masuknya kedua mempelai", note: "Mengenakan lawo dan luka tenun ikat Lio" },
      { time: "18.00", title: "Doa dan makan malam bersama" },
      { time: "19.30", title: "Gawi bersama", note: "Tarian melingkar, semua tamu diajak bergabung" },
    ] },
    dressCode: { note: "Tenun ikat NTT sangat dianjurkan. Nuansa merah bata, kuning kunyit, dan hitam.", colors: ["#1d1512", "#a9381f", "#d39a3c", "#2fa79b"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-17T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Wangge – Ndona", "Kel. Besar Rangga – Pora", "Umat Paroki Kristus Raja Ende"] },
    travel: { note: "Untuk tamu dari luar Flores, Bandara H. Hasan Aroeboesman Ende melayani penerbangan dari Kupang dan Labuan Bajo.", items: [
      { name: "Penginapan di Ende", detail: "Banyak pilihan di sekitar Jl. Kelimutu, ± 5 menit dari katedral" },
      { name: "Perjalanan ke Moni", detail: "± 2 jam lewat Jl. Trans Flores, rombongan berangkat pukul 07.30" },
    ] },
    faq: { items: [
      { q: "Apakah tamu boleh ikut gawi?", a: "Tentu. Gawi adalah tarian kebersamaan, semua tamu sangat diharapkan bergabung." },
      { q: "Bisakah ikut ke Danau Kelimutu?", a: "Bagi tamu yang menginap di Moni, keluarga mengatur pendakian fajar pada Minggu pagi." },
    ] },
  },
});
