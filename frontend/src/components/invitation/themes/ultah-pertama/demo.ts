import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aruna", groom: "",
    brideFull: "Aruna Zahra Kirana",
    brideParents: "Putri pertama dari Bapak Dimas Wicaksono & Ibu Laras Ayuningtyas",
    note: "Setahun lalu ia datang membawa terang. Kini Aruna sudah bisa melangkah kecil, dan kami ingin merayakannya bersama orang-orang yang menyayanginya.",
  },
  eventLabel: "Ulang Tahun Pertama",
  date: "2027-05-23T10:00:00+07:00",
  place: "Kebun Teras Sari",
  address: "Jl. Kaliurang Km 8,5 No. 21, Sleman, Daerah Istimewa Yogyakarta",
  story: { title: "Setahun Aruna", body: "" },
  stories: [
    { date: "Mei 2026", title: "Selamat datang, Aruna", body: "Lahir pukul 06.40 pagi dengan berat 3,1 kg, tangisnya membuat seisi rumah menangis bahagia." },
    { date: "Agustus 2026", title: "Senyum pertama", body: "Tawa kecilnya pecah setiap kali Ayah pura-pura bersin. Sejak itu Ayah rajin bersin." },
    { date: "November 2026", title: "Duduk sendiri", body: "Aruna mulai duduk tegak dan sibuk menyusun balok kayu pemberian Eyang." },
    { date: "Mei 2027", title: "Langkah pertama", body: "Tiga langkah kecil menuju pelukan Ibu, tepat beberapa hari sebelum ulang tahunnya." },
  ],
  events: [
    { name: "Syukuran & Tiup Lilin Pertama", date: "2027-05-23T10:00:00+07:00", time: "10.00 – 12.30 WIB", venue: "Kebun Teras Sari", address: "Jl. Kaliurang Km 8,5 No. 21, Sleman, Daerah Istimewa Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0812 4471 90", account_name: "Laras Ayuningtyas" },
    { id: "demo-kado", type: "address", address: "Perum Griya Kaliurang Asri Blok B-7, Ngaglik, Sleman 55581" },
  ],
  guestName: "Ibu Wulan & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Aruna Zahra Kirana", nickname: "Aruna", birthDate: "2026-05-21T06:40:00+07:00", parents: "Putri pertama dari Bapak Dimas Wicaksono & Ibu Laras Ayuningtyas", meaning: "Aruna berarti cahaya fajar, Zahra bunga yang mekar, Kirana yang cantik berseri." },
    rundown: { items: [
      { time: "10.00", title: "Penyambutan tamu", note: "Teh hangat dan camilan di teras kebun" },
      { time: "10.30", title: "Doa syukur bersama", note: "Dipimpin Eyang Kakung" },
      { time: "11.00", title: "Tiup lilin & smash cake", note: "Siapkan kamera, pasti berantakan!" },
      { time: "11.30", title: "Makan siang & foto keluarga" },
    ] },
    dressCode: { note: "Nuansa lembut: krem, hijau sage, atau merah muda pucat. Si kecil boleh datang dengan baju paling nyaman.", colors: ["#f3ebe0", "#9fb29a", "#e7bcab", "#e6cf98"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi atau pantangan makanan? (opsional)" },
    family: { title: "Turut berbahagia", names: ["Eyang Kakung & Eyang Putri Wicaksono", "Opa & Oma Ayuningtyas", "Om Raka & Tante Sinta"] },
    wishlist: { note: "Doa dan kehadiran Anda sudah lebih dari cukup. Bila ingin memberi, ini beberapa kebutuhan Aruna.", items: [
      { id: "w1", name: "Buku kain bergambar", price: "± Rp95.000" },
      { id: "w2", name: "Balok kayu susun", price: "± Rp180.000", claimed_by: "Om Raka" },
      { id: "w3", name: "Sepatu jalan pertama", price: "± Rp150.000" },
    ] },
    faq: { items: [
      { q: "Apakah ada ruang menyusui?", a: "Ada ruang tenang di dalam rumah kebun, lengkap dengan sofa dan meja ganti popok." },
      { q: "Boleh membawa kereta bayi?", a: "Boleh, jalur kebun sudah rata dan ramah kereta dorong." },
    ] },
  },
});
