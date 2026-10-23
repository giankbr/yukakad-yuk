import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "H. Abdul Karim", groom: "",
    brideFull: "Almarhum H. Abdul Karim bin Sulaiman",
    brideParents: "Wafat Selasa, 14 Januari 2025\nbertepatan dengan 14 Rajab 1446 H, dalam usia 74 tahun",
    note: "Tiga tahun sudah Abah berpulang. Kami berkumpul kembali untuk membaca tahlil, mengirim doa, dan menyambung silaturahmi yang dulu selalu beliau rawat.",
  },
  eventLabel: "Haul ke-3 & Tahlil",
  date: "2027-12-11T19:30:00+07:00",
  place: "Kediaman Keluarga Almarhum",
  address: "Jl. Sunan Drajat No. 41, Desa Sumberwudi, Kec. Karanggeneng, Kabupaten Lamongan",
  story: { title: "Riwayat singkat", body: "" },
  stories: [
    { date: "1951", title: "Lahir di Lamongan", body: "Putra kedua dari pasangan Bapak Sulaiman dan Ibu Maimunah, tumbuh di kampung nelayan di tepi Bengawan Solo." },
    { date: "1976", title: "Membina keluarga", body: "Menikah dengan Hj. Siti Aminah dan dikaruniai empat putra-putri yang beliau didik dengan sabar dan sederhana." },
    { date: "1988", title: "Merintis majelis taklim", body: "Bersama warga mendirikan Majelis Taklim Nurul Huda di serambi rumah, yang hingga kini masih rutin mengaji setiap malam Jumat." },
    { date: "2025", title: "Berpulang", body: "Wafat dengan tenang di rumah, dikelilingi keluarga, pada 14 Rajab 1446 H. Semoga Allah menerima seluruh amal ibadah beliau." },
  ],
  events: [
    { name: "Khataman Al-Qur'an", date: "2027-12-11T08:00:00+07:00", time: "08.00 – 11.30 WIB", venue: "Masjid Nurul Huda Sumberwudi", address: "Jl. Sunan Drajat, Desa Sumberwudi, Kec. Karanggeneng, Kabupaten Lamongan" },
    { name: "Haul, Tahlil & Doa Bersama", date: "2027-12-11T19:30:00+07:00", time: "Ba'da Isya, 19.30 WIB – selesai", venue: "Kediaman Keluarga Almarhum", address: "Jl. Sunan Drajat No. 41, Desa Sumberwudi, Kec. Karanggeneng, Kabupaten Lamongan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7166 2051 90", account_name: "Ahmad Fauzi (Santunan Haul)" },
  ],
  guestName: "Bapak Kyai H. Mashuri & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Setiap yang bernyawa pasti akan merasakan mati. Dan hanya pada hari Kiamat sajalah diberikan dengan sempurna balasanmu.", source: "QS. Ali 'Imran: 185" },
    rundown: { items: [
      { time: "19.30", title: "Pembukaan & pembacaan Yasin" },
      { time: "20.00", title: "Tahlil bersama", note: "Dipimpin Kyai H. Mashuri" },
      { time: "20.45", title: "Mauidhoh hasanah" },
      { time: "21.15", title: "Doa penutup & ramah tamah" },
    ] },
    dressCode: { note: "Busana muslim yang sopan dengan warna teduh.", colors: ["#1f4a3a", "#f4eddc", "#b9975a", "#56625a"] },
    rsvpDietary: {},
    thankYou: { message: "Terima kasih atas doa dan kehadiran Bapak/Ibu/Saudara/i dalam majelis haul. Semoga menjadi amal kebaikan bagi kita semua dan cahaya bagi almarhum." },
    family: { title: "Kami yang mengundang", names: ["Hj. Siti Aminah (istri)", "Keluarga H. Ahmad Fauzi", "Keluarga Nur Hidayah", "Keluarga Muhammad Ridwan", "Keluarga Siti Rofiah"] },
    faq: { items: [
      { q: "Apakah jamaah perempuan disediakan tempat?", a: "Ya, jamaah perempuan bertempat di ruang tengah rumah dengan tabir." },
      { q: "Apakah ada parkir?", a: "Parkir tersedia di halaman Masjid Nurul Huda, sekitar 100 meter dari rumah." },
    ] },
  },
});
