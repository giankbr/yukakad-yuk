import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Arka", groom: "",
    brideFull: "Arkana Bintang Pradipta",
    brideParents: "Putra pertama dari Bapak Yudha Pradipta & Ibu Sekar Ayuningtyas",
    note: "Hitung mundur dimulai! Arka sudah enam tahun dan mengajak teman-teman terbang bersama ke luar angkasa.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-08-15T15:00:00+07:00",
  place: "Rumah Main Galaksi",
  address: "Jl. Kemang Raya No. 18, Bangka, Mampang Prapatan, Jakarta Selatan",
  story: { title: "Jejak Arka", body: "" },
  stories: [
    { date: "2021", title: "Peluncuran pertama", body: "Arka lahir di malam berbintang bulan Agustus, saat hujan meteor Perseid sedang ramai di langit." },
    { date: "2023", title: "Kata pertama: bulan", body: "Setiap malam menunjuk ke jendela dan berkata \"bulan!\" sebelum tidur." },
    { date: "2025", title: "Kunjungan ke planetarium", body: "Duduk paling depan, matanya tidak berkedip melihat cincin Saturnus di kubah." },
    { date: "2027", title: "Enam tahun, siap meluncur!", body: "Kini hafal urutan delapan planet dan bercita-cita menjadi astronaut." },
  ],
  events: [
    { name: "Pesta Misi Antariksa", date: "2027-08-15T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Rumah Main Galaksi", address: "Jl. Kemang Raya No. 18, Bangka, Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0812 3345 66", account_name: "Sekar Ayuningtyas" },
    { id: "demo-kado", type: "address", address: "Jl. Bangka XI No. 7, Mampang Prapatan, Jakarta Selatan 12720" },
  ],
  guestName: "Adik Raka & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Arkana Bintang Pradipta", nickname: "Arka", birthDate: "2021-08-14T21:40:00+07:00", parents: "Putra pertama dari Bapak Yudha Pradipta & Ibu Sekar Ayuningtyas" },
    quote: { text: "Teruslah melihat ke bintang-bintang, dan jangan berhenti bertanya. Dunia selalu punya keajaiban untuk anak yang penasaran.", source: "Ayah & Bunda" },
    rundown: { items: [
      { time: "15.00", title: "Check-in kru & ambil helm astronaut", note: "Meja pendaftaran di pintu masuk" },
      { time: "15.30", title: "Membuat roket kertas" },
      { time: "16.15", title: "Tiup lilin kue planet", note: "Nyanyi bersama" },
      { time: "16.45", title: "Pertunjukan bintang mini & bagi bingkisan" },
    ] },
    dressCode: { note: "Kostum astronaut, alien yang ramah, atau baju warna langit malam dan bintang.", colors: ["#1b2452", "#e8573f", "#f7c95a", "#4fb8b0"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Pradipta", "Opa & Oma Ayuningtyas"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Arka.", items: [
      { id: "w1", name: "Teleskop mainan anak", price: "± Rp250.000" },
      { id: "w2", name: "Buku cerita tata surya", price: "± Rp85.000", claimed_by: "Tante Dewi" },
      { id: "w3", name: "Lampu proyektor bintang", price: "± Rp120.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada ruang tunggu dengan kopi dan camilan untuk Ayah & Bunda." },
      { q: "Perlu membawa kostum?", a: "Tidak wajib. Helm astronaut kertas disediakan untuk semua kru cilik." },
    ] },
  },
});
