import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Syila", groom: "",
    brideFull: "Arsyila Putri Ramadhani",
    brideParents: "Putri kedua dari Bapak dr. Yoga Pradipta & Ibu Larasati",
    note: "Dokter Syila sudah lima tahun dan siap memeriksa semua tamu: resepnya kue, balon, dan banyak tawa!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-07-17T15:00:00+07:00",
  place: "Rumah Main Ceria",
  address: "Jl. Pandanaran No. 88, Pekunden, Semarang Tengah, Kota Semarang",
  stories: [
    { date: "2022", title: "Pasien pertama", body: "Syila lahir di bulan Juli, tangisnya paling nyaring di ruang bayi, katanya sudah siap jadi dokter." },
    { date: "2024", title: "Stetoskop mainan", body: "Hadiah ulang tahun ke-2 yang tidak pernah lepas: semua boneka di rumah sudah pernah diperiksa." },
    { date: "2026", title: "Klinik boneka", body: "Syila membuka 'klinik' di ruang tamu, lengkap dengan plester gambar dan resep coretan." },
    { date: "2027", title: "Dokter lima tahun", body: "Sekarang sudah hafal cara cuci tangan yang benar dan selalu mengingatkan Ayah minum air putih." },
  ],
  events: [
    { name: "Pesta Dokter Cilik", date: "2027-07-17T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Rumah Main Ceria", address: "Jl. Pandanaran No. 88, Pekunden, Semarang Tengah, Kota Semarang" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "0095 7712 34", account_name: "Larasati" },
    { id: "demo-kado", type: "address", address: "Jl. Gajahmungkur Selatan No. 14, Gajahmungkur, Kota Semarang 50232" },
  ],
  guestName: "Dek Kenzo & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Arsyila Putri Ramadhani", nickname: "Syila", birthDate: "2022-07-17T06:40:00+07:00", parents: "Putri kedua dari Bapak dr. Yoga Pradipta & Ibu Larasati" },
    quote: { text: "Tumbuhlah sehat, kuat, dan baik hati. Semoga tanganmu kelak selalu senang menolong.", source: "Ayah & Bunda" },
    rundown: { items: [
      { time: "15.00", title: "Pakai jas dokter & stetoskop", note: "Disediakan untuk semua dokter cilik" },
      { time: "15.30", title: "Klinik boneka: periksa & pasang plester" },
      { time: "16.15", title: "Tiup lilin & potong kue", note: "Nyanyi bersama" },
      { time: "16.45", title: "Bagi bingkisan 'obat' permen" },
    ] },
    dressCode: { note: "Baju nyaman, boleh pakai jas dokter atau seragam perawat. Warna merah, biru muda, dan putih.", colors: ["#e5483b", "#8fc9ea", "#fffaf3", "#f2c48d"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Pradipta", "Kakek & Nenek Larasati"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Syila.", items: [
      { id: "w1", name: "Set mainan dokter lengkap", price: "± Rp250.000" },
      { id: "w2", name: "Buku cerita tubuh manusia", price: "± Rp90.000", claimed_by: "Tante Wulan" },
      { id: "w3", name: "Boneka beruang pasien", price: "± Rp150.000" },
    ] },
    faq: { items: [
      { q: "Perlu membawa boneka?", a: "Boleh sekali! Bawa boneka kesayangan untuk diperiksa di klinik boneka." },
      { q: "Apakah ada area untuk orang tua?", a: "Ada, tersedia ruang duduk dan minuman untuk Ayah dan Bunda." },
    ] },
  },
});
