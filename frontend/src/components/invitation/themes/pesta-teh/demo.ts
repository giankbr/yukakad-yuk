import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ratna", groom: "",
    brideFull: "Ratna Kusumawardani",
    brideParents: "Bersama suami, Bapak Hadi Santoso, putra-putri, dan para cucu",
    note: "Enam puluh tahun, ribuan cangkir teh, dan cerita yang selalu dimulai dengan kalimat: duduk dulu, tehnya masih hangat.",
  },
  eventLabel: "Ulang Tahun ke-60",
  date: "2027-05-16T15:30:00+07:00",
  place: "Taman Mawar Griya Santoso",
  address: "Jl. Taman Kebon Sirih No. 7, Menteng, Jakarta Pusat",
  story: { title: "Enam Dekade", body: "" },
  stories: [
    { date: "1967", title: "Lahir di Solo", body: "Putri kedua dari keluarga guru, tumbuh di rumah yang setiap sorenya beraroma teh melati." },
    { date: "1990", title: "Guru Piano", body: "Membuka kelas piano kecil di ruang tamu. Muridnya kini ada yang sudah menjadi guru juga." },
    { date: "1994", title: "Rumah di Menteng", body: "Menikah dengan Bapak Hadi dan menanam mawar pertama di halaman. Tiga anak, lima cucu, dan kebun yang terus bertambah." },
    { date: "2027", title: "Enam Puluh", body: "Masih menyeduh teh untuk siapa pun yang datang. Kali ini, giliran kami yang menyiapkan meja untuk Ibu." },
  ],
  events: [
    { name: "Pesta Teh Sore", date: "2027-05-16T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Taman Mawar Griya Santoso", address: "Jl. Taman Kebon Sirih No. 7, Menteng, Jakarta Pusat" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0613 2290 71", account_name: "Anindita Santoso" },
    { id: "demo-kado", type: "address", address: "Jl. Taman Kebon Sirih No. 7, Menteng, Jakarta Pusat 10340", account_name: "Keluarga Hadi Santoso" },
  ],
  guestName: "Ibu Lestari Handayani",
  guestTable: "Meja Earl Grey",
  extras: {
    child: { name: "Ratna Kusumawardani", nickname: "Ratna", birthDate: "1967-05-16", parents: "Bersama suami, Bapak Hadi Santoso, putra-putri, dan para cucu" },
    quote: { text: "Ada sedikit hal di dunia ini yang lebih menyenangkan daripada jam yang dipersembahkan untuk upacara minum teh sore hari.", source: "Henry James" },
    rundown: { items: [
      { time: "15.30", title: "Sambutan & teh pembuka", note: "Teh melati, earl grey, dan teh susu" },
      { time: "16.00", title: "Kenangan enam dekade", note: "Cerita dari anak, cucu, dan sahabat" },
      { time: "16.45", title: "Tiup lilin & potong kue" },
      { time: "17.15", title: "Ramah tamah di taman mawar" },
    ] },
    dressCode: { note: "Gaun atau batik sore yang ringan, bernuansa pastel: biru porselen, merah muda mawar, dan krem renda. Topi taman dipersilakan.", colors: ["#fbf6ef", "#dbe8e6", "#f3d3d3", "#2f569b", "#c4a15a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Dengan cinta dari", names: ["Anindita & Bayu", "Galih & Sekar", "Laras", "Kelima cucu"] },
    faq: { items: [
      { q: "Apakah boleh membawa kado?", a: "Kehadiran Anda sudah menjadi hadiah. Bila ingin memberi, Ibu Ratna senang menerima tanaman mawar atau buku resep." },
      { q: "Apakah acaranya di luar ruangan?", a: "Di taman yang beratap tenda, jadi tetap nyaman bila gerimis sore." },
    ] },
  },
});
