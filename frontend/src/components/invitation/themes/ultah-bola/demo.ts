import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Arka", groom: "",
    brideFull: "Arkana Bima Pradipta",
    brideParents: "Putra pertama dari Bapak Yoga Pradipta & Ibu Larasati Wulandari",
    note: "Peluit sudah ditiup! Arka genap delapan tahun dan ingin merayakannya di lapangan bersama teman-teman. Jangan lupa bawa semangat juara!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-09-18T15:30:00+07:00",
  place: "Lapangan Mini Soccer Taman Cinere",
  address: "Jl. Cinere Raya No. 45, Cinere, Kota Depok, Jawa Barat",
  story: { title: "Cerita Arka", body: "" },
  stories: [
    { date: "2019", title: "Pemain baru lahir", body: "Arka lahir di suatu pagi bulan September, tepat saat Ayah sedang menonton pertandingan di televisi." },
    { date: "2021", title: "Tendangan pertama", body: "Bola plastik merah jadi mainan favorit. Setiap sore Arka mengejarnya keliling halaman sampai berkeringat." },
    { date: "2024", title: "Masuk sekolah sepak bola", body: "Arka bergabung dengan kelas sepak bola anak di kompleks dan mencetak gol pertamanya saat latih tanding." },
    { date: "2027", title: "Delapan tahun!", body: "Sekarang Arka kelas dua SD, rajin latihan menggiring bola, dan bercita-cita jadi kapten tim." },
  ],
  events: [
    { name: "Pesta Bola Arka", date: "2027-09-18T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Lapangan Mini Soccer Taman Cinere", address: "Jl. Cinere Raya No. 45, Cinere, Kota Depok, Jawa Barat" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "5271 0388 14", account_name: "Larasati Wulandari" },
    { id: "demo-kado", type: "address", address: "Jl. Pangkalan Jati Blok C4 No. 17, Cinere, Kota Depok 16514" },
  ],
  guestName: "Mas Kenzo & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Arkana Bima Pradipta", nickname: "Arka", birthDate: "2019-09-18T07:10:00+07:00", parents: "Putra pertama dari Bapak Yoga Pradipta & Ibu Larasati Wulandari" },
    rundown: { items: [
      { time: "15.30", title: "Registrasi & pembagian rompi tim", note: "Meja penyambutan di pinggir lapangan" },
      { time: "15.45", title: "Pemanasan & mini games bersama pelatih" },
      { time: "16.30", title: "Adu penalti seru", note: "Semua anak dapat giliran menendang" },
      { time: "17.15", title: "Tiup lilin, potong kue & bagi medali" },
    ] },
    dressCode: { note: "Kaus olahraga dan sepatu kets yang nyaman. Celana pendek boleh, bawa botol minum sendiri, ya!", colors: ["#e2452f", "#f4bb37", "#22336b", "#ffffff"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Pradipta", "Eyang Kakung & Eyang Putri Wulandari", "Dek Naura (adik Arka)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini yang sedang Arka inginkan.", items: [
      { id: "w1", name: "Bola latihan ukuran 4", price: "± Rp150.000" },
      { id: "w2", name: "Pelindung tulang kering anak", price: "± Rp85.000", claimed_by: "Om Dani" },
      { id: "w3", name: "Buku cerita tentang sepak bola", price: "± Rp75.000" },
    ] },
    faq: { items: [
      { q: "Perlu sepatu bola?", a: "Tidak perlu. Lapangannya rumput sintetis, sepatu kets biasa sudah cukup." },
      { q: "Apakah orang tua boleh ikut?", a: "Boleh sekali! Ada tribun teduh, teh hangat, dan camilan untuk Ayah & Bunda." },
    ] },
  },
});
