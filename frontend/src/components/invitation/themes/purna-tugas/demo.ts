import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Pak Bambang", groom: "",
    brideFull: "Drs. Bambang Sutejo, M.Pd.",
    brideParents: "Bersama keluarga: Ibu Endang Wahyuni (istri), Rizky & Anindita",
    note: "Tiga puluh tujuh tahun di depan papan tulis. Kini kapur itu diletakkan dengan syukur, dan kami ingin merayakannya bersama orang-orang yang menemani perjalanannya.",
  },
  eventLabel: "Syukuran Purna Tugas",
  date: "2027-08-28T18:30:00+07:00",
  place: "Pendapa Griya Sutejo",
  address: "Jl. Bondowoso No. 12, Gading Kasri, Klojen, Kota Malang",
  story: { title: "Perjalanan Karier", body: "" },
  stories: [
    { date: "1990", title: "Guru muda di Bululawang", body: "Mengawali tugas sebagai guru SD Inpres di Bululawang, bersepeda 12 kilometer setiap pagi." },
    { date: "1996", title: "Mengajar Matematika", body: "Pindah ke SMP negeri di Kota Malang. Ribuan murid kemudian mengenalnya sebagai guru yang sabar menjelaskan pecahan." },
    { date: "2009", title: "Wakil kepala sekolah", body: "Merintis klub olimpiade sains dan perpustakaan kelas yang masih berjalan sampai hari ini." },
    { date: "2016", title: "Kepala sekolah", body: "Memimpin sekolah selama sebelas tahun, dengan pintu ruang kepala sekolah yang hampir tak pernah ditutup." },
    { date: "2027", title: "Purna tugas", body: "Pensiun dengan hormat setelah 37 tahun mengabdi di dunia pendidikan." },
  ],
  events: [
    { name: "Syukuran & Makan Malam", date: "2027-08-28T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Pendapa Griya Sutejo", address: "Jl. Bondowoso No. 12, Gading Kasri, Klojen, Kota Malang" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BRI", account_number: "0045 0110 2233 509", account_name: "Endang Wahyuni" },
  ],
  guestName: "Ibu Sulastri & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Drs. Bambang Sutejo, M.Pd.", nickname: "Pak Bambang", parents: "Bersama keluarga: Ibu Endang Wahyuni (istri), Rizky & Anindita" },
    quote: { text: "Tugas boleh selesai, tetapi ilmu yang ditanam akan terus tumbuh di tangan murid-muridnya." },
    rundown: { items: [
      { time: "18.30", title: "Ramah tamah & makan malam" },
      { time: "19.15", title: "Doa syukur bersama" },
      { time: "19.30", title: "Kesan & pesan rekan guru dan murid" },
      { time: "20.15", title: "Pemutaran album kenangan" },
      { time: "20.40", title: "Foto bersama" },
    ] },
    dressCode: { note: "Batik atau kemeja rapi, nuansa biru tua dan krem.", colors: ["#22345a", "#3b5384", "#f6eedd", "#c4923f"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut mengundang", names: ["Rizky Sutejo & Maya", "Anindita Sutejo & Arief", "Keluarga besar Sutejo, Blitar"] },
    faq: { items: [
      { q: "Bolehkah membawa kenang-kenangan tulisan?", a: "Sangat boleh. Kami menyiapkan buku kenangan di meja tamu untuk pesan dan foto lama." },
      { q: "Apakah ada parkir?", a: "Parkir mobil di sepanjang Jl. Bondowoso, dibantu petugas." },
    ] },
  },
});
