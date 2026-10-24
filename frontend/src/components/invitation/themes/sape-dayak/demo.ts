import { makeDemo } from "../demo-base";

// Pernikahan Kristen keluarga Dayak Kenyah dari hulu Mahakam: pemberkatan di gereja dan resepsi adat di lamin,
// diiringi petikan sape.
export const demo = makeDemo({
  couple: {
    bride: "Lusiana", groom: "Daniel",
    brideFull: "Lusiana Ping Lawing, S.Kep.", groomFull: "Daniel Ajang Bilung, S.Hut.",
    brideParents: "Putri kedua dari\nBapak Yohanes Lawing Usat & Ibu Maria Ubung", groomParents: "Putra sulung dari\nBapak Petrus Bilung Ngau & Ibu Ester Lahang",
    note: "Seperti dua dawai sape yang dipetik bersama, kiranya hidup kami menjadi satu lagu syukur bagi Tuhan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T10:00:00+08:00",
  place: "Lamin Adat Pemung Tawai",
  address: "Desa Budaya Pampang, Sungai Siring, Kec. Samarinda Utara, Samarinda, Kalimantan Timur",
  stories: [
    { date: "2019", title: "Bertemu di Hulu Mahakam", body: "Lusi bertugas di puskesmas Long Bagun, Daniel datang bersama tim kehutanan. Perkenalan kami dimulai dari antrean longboat yang tertunda kabut pagi." },
    { date: "2022", title: "Petikan Sape Pertama", body: "Di teras rumah keluarga, Daniel memainkan sape untuk Lusi. Lagunya sederhana, tetapi sejak malam itu kami tahu ingin berjalan bersama." },
    { date: "2026", title: "Restu Dua Keluarga", body: "Keluarga Daniel datang ke Long Bagun menyampaikan maksud baik. Dengan doa para tetua dan pendeta, kedua keluarga sepakat mengantar kami ke pelaminan." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-08-14T10:00:00+08:00", time: "10.00 – 11.30 WITA", venue: "GKII Jemaat Siloam Samarinda", address: "Jl. Pahlawan No. 21, Dadi Mulya, Kec. Samarinda Ulu, Samarinda" },
    { name: "Resepsi & Tari Adat", date: "2027-08-14T16:00:00+08:00", time: "16.00 – 20.00 WITA", venue: "Lamin Adat Pemung Tawai", address: "Desa Budaya Pampang, Sungai Siring, Kec. Samarinda Utara, Samarinda" },
  ],
  gallery: ["/themes/img/r89.webp", "/themes/img/a30.webp", "/themes/img/r104.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-kaltim", type: "bank", bank_name: "Bankaltimtara", account_number: "0071 2208 1427", account_name: "Lusiana Ping Lawing" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0612 0108 4471 502", account_name: "Daniel Ajang Bilung" },
    { id: "demo-kado", type: "address", address: "Jl. Juanda IV No. 18, Air Hitam, Kec. Samarinda Ulu, Samarinda 75124" },
  ],
  guestName: "Bapak Stefanus Ngau & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "16.00", title: "Penyambutan tamu", note: "Diiringi petikan sape dan tari kancet" },
      { time: "16.45", title: "Doa syukur & kata sambutan keluarga" },
      { time: "17.30", title: "Makan bersama", note: "Hidangan khas hulu Mahakam" },
      { time: "19.00", title: "Tari bersama di lamin" },
    ] },
    dressCode: { note: "Busana nuansa hutan dan sungai: hijau tua, krem, dan merah bata. Busana adat sangat dipersilakan.", colors: ["#1f3a30", "#f1e6cf", "#b0341f", "#8c4a25"] },
    rsvpDietary: {},
    family: { title: "Turut mengundang", names: ["Kel. Besar Lawing Usat, Long Bagun", "Kel. Besar Bilung Ngau, Samarinda", "Persekutuan Pemuda GKII Siloam"] },
    travel: { note: "Untuk keluarga dari hulu Mahakam dan luar kota:", items: [
      { name: "Bandara APT Pranoto", detail: "± 30 menit ke Desa Budaya Pampang" },
      { name: "Penginapan keluarga", detail: "Wisma di Jl. Juanda, hubungi panitia keluarga" },
    ] },
  },
});
