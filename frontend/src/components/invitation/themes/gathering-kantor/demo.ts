import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Arunika Family", groom: "",
    brideFull: "PT Arunika Cipta Logistik",
    brideParents: "Diselenggarakan oleh Divisi Human Capital\nbersama Panitia Family Gathering 2027",
    note: "Setahun penuh kita mengejar target bersama. Satu hari ini, ajak keluarga di rumah untuk berkenalan dengan keluarga di kantor.",
  },
  eventLabel: "Family Gathering",
  date: "2027-07-17T07:00:00+07:00",
  place: "Taman Wisata Danau Pinus Cikole",
  address: "Jl. Raya Tangkuban Parahu Km 9, Cikole, Kec. Lembang, Kab. Bandung Barat",
  story: { title: "Jejak Gathering Kita", body: "" },
  stories: [
    { date: "2019", title: "Gathering pertama di Ciater", body: "Baru 60 karyawan, satu bus, dan satu lomba tarik tambang yang dimenangkan tim gudang. Ceritanya masih dibahas sampai sekarang." },
    { date: "2023", title: "Berkemah di Pangalengan", body: "Keluarga mulai ikut. Anak-anak belajar memasang tenda, para orang tua belajar kalah di lomba estafet kelereng." },
    { date: "2027", title: "Tepi danau di Lembang", body: "Tahun ini 240 peserta dari kantor pusat dan tiga cabang. Ada outbound keluarga, barbeku, dan doorprize utama sepeda listrik." },
  ],
  events: [
    { name: "Kumpul & Senam Pagi", date: "2027-07-17T07:00:00+07:00", time: "07.00 – 08.30 WIB", venue: "Lapangan Utama Danau Pinus", address: "Jl. Raya Tangkuban Parahu Km 9, Cikole, Kec. Lembang, Kab. Bandung Barat" },
    { name: "Outbound & Lomba Keluarga", date: "2027-07-17T09:00:00+07:00", time: "09.00 – 12.00 WIB", venue: "Padang Rumput Tepi Danau", address: "Area outbound Taman Wisata Danau Pinus, Cikole, Lembang" },
    { name: "Barbeku & Doorprize", date: "2027-07-17T12:30:00+07:00", time: "12.30 – 15.30 WIB", venue: "Area Tenda Panitia", address: "Area perkemahan Taman Wisata Danau Pinus, Cikole, Lembang" },
  ],
  gallery: ["/themes/img/r77.webp", "/themes/img/r103.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "1300 0277 1707 7", account_name: "Panitia Gathering Arunika" },
    { id: "demo-address", type: "address", address: "Sekretariat Panitia, Lt. 2 Gedung Arunika, Jl. Soekarno-Hatta No. 590, Bandung 40286", account_name: "Ibu Dewi Anggraini (Panitia)" },
  ],
  guestName: "Bapak Hendra Saputra & Keluarga",
  guestTable: "Tim Elang",
  extras: {
    rundown: { items: [
      { time: "05.30", title: "Bus berangkat dari kantor pusat", note: "Jl. Soekarno-Hatta, Bandung" },
      { time: "07.00", title: "Registrasi, sarapan, senam pagi" },
      { time: "09.00", title: "Outbound per kelompok", note: "Tarik tambang, estafet air, balap karung keluarga" },
      { time: "12.30", title: "Barbeku di tepi danau" },
      { time: "14.30", title: "Pembagian doorprize & foto bersama" },
      { time: "16.00", title: "Bus kembali ke Bandung" },
    ] },
    dressCode: { note: "Kaos gathering yang dibagikan panitia, celana olahraga, dan sepatu kets. Bawa jaket, udara Lembang dingin di pagi hari.", colors: ["#f28c38", "#2bb3a3", "#f6c945", "#2f6b4f"] },
    guestPass: {},
    rsvpDietary: {},
    faq: { items: [
      { q: "Siapa saja yang boleh ikut?", a: "Karyawan beserta pasangan dan anak. Isi jumlah tamu sesuai anggota keluarga yang ikut agar kursi bus dan kaos cukup." },
      { q: "Apakah ada transportasi?", a: "Ada bus dari kantor pusat pukul 05.30. Peserta yang membawa kendaraan sendiri bisa parkir di area utama." },
      { q: "Perlu membawa apa?", a: "Baju ganti, topi, botol minum, dan obat pribadi. Makan pagi dan siang disediakan panitia." },
    ] },
  },
});
