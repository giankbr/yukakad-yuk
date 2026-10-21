import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salsabila", groom: "Fikri",
    brideFull: "Salsabila Putri Hanum", groomFull: "Muhammad Fikri Ramadhan",
    brideParents: "Putri dari Bapak Hendra Gunawan & Ibu Ratna Sari", groomParents: "Putra dari Bapak Agus Ramadhan & Ibu Siti Mardiyah",
    note: "Sebentar lagi rumah kami bertambah satu tawa kecil. Mari menyambutnya bersama, di antara awan dan doa.",
  },
  eventLabel: "Baby Shower",
  date: "2027-09-18T10:00:00+07:00",
  place: "Kafe Ladang Awan",
  address: "Jl. Bukit Dago Utara No. 22, Coblong, Bandung",
  story: { title: "Menanti Si Kecil", body: "" },
  stories: [
    { date: "Mei 2027", title: "Kabar paling manis", body: "Dua garis kecil di pagi hari, lalu pelukan panjang dan tangis bahagia." },
    { date: "Juni 2027", title: "Detak pertama", body: "Mendengar detak jantungnya untuk pertama kali di ruang dokter, secepat langkah kuda kecil." },
    { date: "Agustus 2027", title: "Tendangan kecil", body: "Si kecil mulai menendang setiap kali Ayah membacakan cerita sebelum tidur." },
    { date: "Desember 2027", title: "Sampai jumpa, Nak", body: "Insyaallah kami bertemu di akhir tahun. Kamarnya sudah dicat warna awan." },
  ],
  events: [
    { name: "Baby Shower & Syukuran", date: "2027-09-18T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Kafe Ladang Awan", address: "Jl. Bukit Dago Utara No. 22, Coblong, Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0812 4455 901", account_name: "Salsabila Putri Hanum" },
    { id: "demo-wallet", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 2345 6789", account_name: "Muhammad Fikri Ramadhan" },
    { id: "demo-kado", type: "address", address: "Jl. Taman Sari No. 56, Lebak Siliwangi, Bandung 40132" },
  ],
  guestName: "Teh Rania & Keluarga",
  guestTable: "",
  extras: {
    rundown: { items: [
      { time: "10.00", title: "Kedatangan & teh hangat", note: "Tulis harapan di kartu awan" },
      { time: "10.30", title: "Doa bersama untuk Bunda & si kecil" },
      { time: "11.00", title: "Tebak-tebakan seru", note: "Tebak berat & tanggal lahir" },
      { time: "12.00", title: "Makan siang & foto bersama" },
    ] },
    dressCode: { note: "Warna pastel lembut: mint, peach, atau lilac.", colors: ["#a8dcc8", "#f8c4a4", "#cdbbe6", "#f7dc8e"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut berbahagia", names: ["Kel. Bapak Hendra Gunawan", "Kel. Bapak Agus Ramadhan"] },
    wishlist: { note: "Kehadiran dan doa Anda sudah lebih dari cukup. Bila ingin memberi, berikut kebutuhan si kecil.", items: [
      { id: "w1", name: "Gendongan bayi ergonomis", price: "± Rp450.000" },
      { id: "w2", name: "Set baju bayi 0–3 bulan", price: "± Rp200.000", claimed_by: "Tante Wulan" },
      { id: "w3", name: "Lampu tidur bintang", price: "± Rp150.000" },
    ] },
    faq: { items: [
      { q: "Boleh membawa anak?", a: "Tentu, ada sudut bermain kecil di taman kafe." },
      { q: "Ada parkir?", a: "Parkir tersedia di halaman kafe dan di sepanjang Jl. Bukit Dago Utara." },
    ] },
  },
});
