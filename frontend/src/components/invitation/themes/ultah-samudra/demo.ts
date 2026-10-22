import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Arka", groom: "",
    brideFull: "Arka Samudra Wijaya",
    brideParents: "Putra pertama dari Bapak Hendra Wijaya & Ibu Laras Pratiwi",
    note: "Kapal selam kuning sudah siap menyelam! Kapten Arka menunggu teman-temannya di dasar laut.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-05-22T15:30:00+08:00",
  place: "Ruang Pesta Lumba-Lumba",
  address: "Jl. Jenderal Sudirman No. 47, Klandasan Ilir, Balikpapan Kota, Balikpapan",
  story: { title: "", body: "" },
  stories: [
    { date: "2021", title: "Kapten kecil lahir", body: "Arka lahir di bulan Mei, saat Ayah pulang berlayar membawa boneka paus biru." },
    { date: "2024", title: "Pertama melihat laut", body: "Di Pantai Manggar, Arka berlari mengejar ombak dan menamai semua kepiting yang ia temukan." },
    { date: "2027", title: "Enam tahun!", body: "Sekarang Arka hafal nama dua puluh jenis ikan dan bercita-cita menjadi penjelajah samudra." },
  ],
  events: [
    { name: "Pesta Bawah Laut Arka", date: "2027-05-22T15:30:00+08:00", time: "15.30 – 18.00 WITA", venue: "Ruang Pesta Lumba-Lumba", address: "Jl. Jenderal Sudirman No. 47, Klandasan Ilir, Balikpapan Kota, Balikpapan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0712 5583 09", account_name: "Laras Pratiwi" },
    { id: "demo-kado", type: "address", address: "Perumahan Balikpapan Baru Blok D3 No. 12, Damai Baru, Balikpapan Selatan 76114" },
  ],
  guestName: "Kak Kirana & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Arka Samudra Wijaya", nickname: "Arka", birthDate: "2021-05-22T07:40:00+08:00", parents: "Putra pertama dari Bapak Hendra Wijaya & Ibu Laras Pratiwi" },
    rundown: { items: [
      { time: "15.30", title: "Naik kapal selam", note: "Ambil topi kapten & teropong kertas" },
      { time: "16.00", title: "Dongeng gurita & tebak nama ikan" },
      { time: "16.45", title: "Tiup lilin & potong kue samudra", note: "Nyanyi bersama" },
      { time: "17.15", title: "Berburu harta karun di pasir" },
    ] },
    dressCode: { note: "Warna laut dan matahari: biru, kuning, oranye, atau toska. Kostum ikan, gurita, atau penyelam boleh banget!", colors: ["#2a7d92", "#f8c93c", "#f58b2e", "#64c3cf"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Wijaya", "Opa & Oma Pratiwi", "Adik Naya (adik Arka)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini kesukaan Arka.", items: [
      { id: "w1", name: "Ensiklopedia hewan laut anak", price: "± Rp120.000" },
      { id: "w2", name: "Mainan kapal selam untuk mandi", price: "± Rp85.000", claimed_by: "Tante Dewi" },
      { id: "w3", name: "Kacamata renang anak", price: "± Rp60.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada meja kopi dan camilan untuk Ayah & Bunda di dek atas." },
      { q: "Perlu membawa baju ganti?", a: "Boleh dibawa, karena ada permainan gelembung sabun yang bisa sedikit basah." },
    ] },
  },
});
