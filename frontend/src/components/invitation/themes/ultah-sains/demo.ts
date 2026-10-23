import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kayla", groom: "",
    brideFull: "Kayla Putri Anindita",
    brideParents: "Putri pertama dari Bapak Rizky Pratama & Ibu Dwi Anindita",
    note: "Kayla sudah tujuh tahun dan siap melakukan eksperimen paling seru: pesta ulang tahun bersama teman-teman!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-09-12T15:00:00+07:00",
  place: "Lab Main Sains Ceria",
  address: "Jl. Ir. H. Juanda No. 214, Dago, Coblong, Kota Bandung",
  story: { title: "Catatan Lab Kayla", body: "" },
  stories: [
    { date: "2020", title: "Penemuan terbesar", body: "Kayla lahir di pagi yang cerah bulan September, dan langsung menggenggam jari Ayah erat-erat." },
    { date: "2023", title: "Kenapa langit biru?", body: "Pertanyaan pertama yang membuat Ayah dan Bunda membuka buku ensiklopedia bersama." },
    { date: "2025", title: "Gunung meletus di dapur", body: "Eksperimen soda kue dan cuka pertama. Busanya tumpah ke mana-mana, tawanya juga." },
    { date: "2027", title: "Ilmuwan tujuh tahun", body: "Sekarang punya mikroskop mainan dan buku catatan penuh gambar daun, serangga, dan bintang." },
  ],
  events: [
    { name: "Pesta Ilmuwan Cilik", date: "2027-09-12T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Lab Main Sains Ceria", address: "Jl. Ir. H. Juanda No. 214, Dago, Coblong, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "1300 0177 2245 9", account_name: "Dwi Anindita" },
    { id: "demo-kado", type: "address", address: "Jl. Cisitu Lama No. 9, Dago, Coblong, Kota Bandung 40135" },
  ],
  guestName: "Kak Bima & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Kayla Putri Anindita", nickname: "Kayla", birthDate: "2020-09-12T07:20:00+07:00", parents: "Putri pertama dari Bapak Rizky Pratama & Ibu Dwi Anindita" },
    quote: { text: "Jangan pernah berhenti bertanya \"kenapa?\". Setiap pertanyaan adalah awal dari sebuah penemuan.", source: "Ayah & Bunda" },
    rundown: { items: [
      { time: "15.00", title: "Pakai jas lab & kacamata pelindung", note: "Disediakan untuk semua ilmuwan cilik" },
      { time: "15.30", title: "Eksperimen gunung meletus" },
      { time: "16.15", title: "Tiup lilin kue tabung reaksi", note: "Nyanyi bersama" },
      { time: "16.45", title: "Peluncuran roket botol & bagi bingkisan" },
    ] },
    dressCode: { note: "Baju nyaman yang boleh kena busa! Warna putih, hijau mint, atau biru laboratorium.", colors: ["#fbfcfd", "#bfe8dc", "#2f8f9d", "#24406e"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Pratama", "Opa & Oma Anindita"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Kayla.", items: [
      { id: "w1", name: "Mikroskop anak", price: "± Rp300.000" },
      { id: "w2", name: "Buku eksperimen sains di rumah", price: "± Rp95.000", claimed_by: "Tante Rani" },
      { id: "w3", name: "Kit kristal warna-warni", price: "± Rp150.000" },
    ] },
    faq: { items: [
      { q: "Apakah eksperimennya aman?", a: "Aman! Semua bahan dari dapur (soda kue, cuka, pewarna makanan) dan didampingi kakak pemandu." },
      { q: "Perlu membawa baju ganti?", a: "Boleh, untuk berjaga-jaga kalau busanya meluber." },
    ] },
  },
});
