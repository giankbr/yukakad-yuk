import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salma", groom: "Rizal",
    brideFull: "Salma Nurhasanah, S.Ds.", groomFull: "Rizal Maulana Yusuf",
    brideParents: "Putri kedua dari\nBapak H. Ujang Saepudin & Ibu Hj. Euis Kurniasih", groomParents: "Putra pertama dari\nBapak Dede Kusnadi & Ibu Neneng Rohayati",
    note: "Helai demi helai pandan dianyam sabar hingga menjadi tikar tempat keluarga berkumpul. Semoga begitu pula rumah tangga kami: rapat, hangat, dan penuh berkah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-22T08:00:00+07:00",
  place: "Kediaman Keluarga H. Ujang Saepudin",
  address: "Kp. Babakan Rajapolah RT 02/05, Kec. Rajapolah, Kab. Tasikmalaya",
  stories: [
    { date: "2021", title: "Bengkel anyaman", body: "Salma meneliti motif tikar untuk tugas akhirnya. Rizal pemuda yang mengajarinya membelah dan mewarnai daun pandan di bengkel milik pamannya." },
    { date: "2024", title: "Tikar pertama", body: "Rizal menganyam selembar tikar kecil bermotif belah ketupat, lalu menitipkannya pada ayah Salma bersama sebuah surat yang sopan." },
    { date: "2026", title: "Khitbah", body: "Dengan basmalah, keluarga Rizal datang meminang. Kedua keluarga bersepakat dan menetapkan hari baik." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Kota Tasikmalaya", address: "Jl. Otto Iskandardinata No. 2, Empangsari, Kec. Tawang, Kota Tasikmalaya" },
    { name: "Walimah", date: "2027-05-22T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Kediaman Keluarga H. Ujang Saepudin", address: "Kp. Babakan Rajapolah RT 02/05, Kec. Rajapolah, Kab. Tasikmalaya" },
  ],
  gallery: ["/themes/img/r5.webp", "/themes/img/r66.webp", "/themes/img/a52.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7212 0458 33", account_name: "Salma Nurhasanah" },
    { id: "demo-bjb", type: "bank", bank_name: "bank bjb syariah", account_number: "5120 1003 4471", account_name: "Rizal Maulana Yusuf" },
  ],
  guestName: "Ibu Hj. Ratna Sari & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu cenderung dan merasa tenteram kepadanya.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Gelaran tikar dan hidangan ringan" },
      { time: "11.30", title: "Tausiyah walimah" },
      { time: "12.00", title: "Ramah tamah & makan bersama", note: "Tamu putra dan putri dipisah dengan hijab" },
    ] },
    dressCode: { note: "Busana muslim yang sopan. Warna alam: krem pandan, hijau daun, dan merah saga.", colors: ["#d8bb80", "#2f6b4a", "#b02a48", "#f7efdc"] },
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ujang Saepudin", "Kel. Besar Dede Kusnadi"] },
  },
});
