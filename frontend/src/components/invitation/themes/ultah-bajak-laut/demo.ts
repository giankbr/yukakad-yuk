import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Raka", groom: "",
    brideFull: "Raka Bayu Aditya",
    brideParents: "Putra pertama dari Bapak Aditya Nugroho & Ibu Sekar Ayuningtyas",
    note: "Peta harta karun sudah digambar, kapal sudah siap. Kapten Raka menunggu kru terbaiknya untuk berlayar ke Pulau Rahasia!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-10-09T15:00:00+07:00",
  place: "Kafe Anak Pelabuhan Ceria",
  address: "Jl. Raya Darmo Permai III No. 18, Pradahkalikendal, Dukuhpakis, Surabaya",
  story: { title: "", body: "" },
  stories: [
    { date: "2020", title: "Kapten kecil lahir", body: "Raka lahir di bulan Oktober, saat hujan pertama turun di Surabaya. Tangisnya kencang seperti terompet kapal." },
    { date: "2024", title: "Peta pertama", body: "Di TK, Raka menggambar peta harta karun pertamanya: rumah, taman, dan sebuah X besar di bawah pohon mangga." },
    { date: "2027", title: "Tujuh tahun!", body: "Sekarang Raka bisa membaca kompas, hafal nama tujuh benua, dan ingin berlayar keliling dunia bersama teman-temannya." },
  ],
  events: [
    { name: "Pesta Bajak Laut Raka", date: "2027-10-09T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Kafe Anak Pelabuhan Ceria", address: "Jl. Raya Darmo Permai III No. 18, Pradahkalikendal, Dukuhpakis, Surabaya" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0882 7713 40", account_name: "Sekar Ayuningtyas" },
    { id: "demo-kado", type: "address", address: "Perumahan Darmo Harapan Blok F2 No. 9, Tanjungsari, Sukomanunggal, Surabaya 60187" },
  ],
  guestName: "Adik Kinan & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Raka Bayu Aditya", nickname: "Raka", birthDate: "2020-10-09T06:20:00+07:00", parents: "Putra pertama dari Bapak Aditya Nugroho & Ibu Sekar Ayuningtyas" },
    rundown: { items: [
      { time: "15.00", title: "Naik kapal & ambil topi kapten", note: "Setiap kru dapat peta dan teropong kertas" },
      { time: "15.30", title: "Berburu harta karun", note: "Ikuti jejak titik-titik sampai tanda X" },
      { time: "16.30", title: "Tiup lilin & potong kue kapal" },
      { time: "17.00", title: "Foto kru bersama Kapten Raka" },
    ] },
    dressCode: { note: "Kostum bajak laut atau pelaut: garis-garis, bandana, topi kapten. Warna merah, biru laut, dan kuning emas!", colors: ["#d4473a", "#2f9aa6", "#e8b33c", "#263247"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Nugroho", "Eyang Kakung & Eyang Putri Ayuningtyas", "Adik Laras (adik Raka)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi harta karun terindah. Kalau ingin memberi, ini kesukaan Raka.", items: [
      { id: "w1", name: "Buku atlas dunia bergambar", price: "± Rp150.000" },
      { id: "w2", name: "Kompas & teropong mainan", price: "± Rp95.000", claimed_by: "Om Fajar" },
      { id: "w3", name: "Lego kapal layar", price: "± Rp250.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada pojok kopi dan camilan untuk Ayah & Bunda di dek belakang." },
      { q: "Wajib pakai kostum?", a: "Tidak wajib, tapi topi dan bandana bajak laut akan dibagikan di pintu masuk." },
    ] },
  },
});
