import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Gibran", groom: "",
    brideFull: "Muhammad Gibran Pratama",
    brideParents: "Putra pertama dari Bapak Reza Pratama & Ibu Annisa Kartika",
    note: "Panggilan darurat! Tim pemadam cilik dibutuhkan untuk menyemprot air, naik tangga, dan tiup lilin bersama Gibran.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-03-13T15:30:00+07:00",
  place: "Kenari Kids Space",
  address: "Jl. Bintaro Utama 3A No. 10, Pondok Karya, Pondok Aren, Tangerang Selatan",
  story: { title: "Cerita Gibran", body: "" },
  stories: [
    { date: "2022", title: "Sirene pertama", body: "Gibran lahir di bulan Maret. Tangisnya kencang sekali, kata Ayah seperti sirene truk merah." },
    { date: "2025", title: "Mobil kesayangan", body: "Truk pemadam mainan jadi teman tidur, teman mandi, dan teman makan. Selalu dibawa ke mana-mana." },
    { date: "2027", title: "Lima tahun!", body: "Sekarang Gibran sudah hafal semua alat pemadam dan ingin merayakannya bersama teman-teman." },
  ],
  events: [
    { name: "Pesta Pemadam Gibran", date: "2027-03-13T15:30:00+07:00", time: "15.30 – 18.00 WIB", venue: "Kenari Kids Space", address: "Jl. Bintaro Utama 3A No. 10, Pondok Karya, Pondok Aren, Tangerang Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "5271 0313 22", account_name: "Annisa Kartika" },
    { id: "demo-kado", type: "address", address: "Jl. Kasuari IV Blok HD No. 7, Bintaro Jaya Sektor 9, Tangerang Selatan 15229" },
  ],
  guestName: "Adik Kirana & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Muhammad Gibran Pratama", nickname: "Gibran", birthDate: "2022-03-11T07:20:00+07:00", parents: "Putra pertama dari Bapak Reza Pratama & Ibu Annisa Kartika" },
    rundown: { items: [
      { time: "15.30", title: "Apel pagi pemadam cilik", note: "Setiap anak dapat helm merah dan lencana bintang" },
      { time: "16.00", title: "Latihan semprot air ke sasaran", note: "Pakai pistol air, siapkan baju ganti" },
      { time: "16.40", title: "Kenalan dengan truk pemadam & naik tangga mini" },
      { time: "17.20", title: "Tiup lilin, potong kue & bagi bingkisan" },
    ] },
    dressCode: { note: "Kaus merah, kuning, atau biru. Boleh pakai kostum pemadam!", colors: ["#e0352b", "#ffc93c", "#5bbbea", "#1f2a44"] },
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Pratama", "Opa & Oma Kartika", "Adik Alesha"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini yang sedang Gibran impikan.", items: [
      { id: "w1", name: "Buku cerita bergambar tentang pemadam", price: "± Rp85.000" },
      { id: "w2", name: "Set balok susun pos pemadam", price: "± Rp210.000", claimed_by: "Om Dika" },
      { id: "w3", name: "Kostum pemadam anak", price: "± Rp150.000" },
    ] },
    faq: { items: [
      { q: "Apakah ada permainan air?", a: "Ada, semprot air ke sasaran di halaman. Bawa baju ganti dan handuk kecil ya." },
      { q: "Apakah orang tua boleh menemani?", a: "Tentu, ada area duduk dan minuman untuk orang tua di dalam aula." },
    ] },
  },
});
