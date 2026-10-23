import { makeDemo } from "../demo-base";

// Peringatan Isra Mi'raj oleh Panitia PHBI DKM & majelis taklim: penceramah dan pembaca doa di data mempelai, tema
// tausiyah di catatan, sesi di daftar acara, susunan acara malam itu di cerita. Malam 27 Rajab 1449 H jatuh pada
// Sabtu malam, 25 Desember 2027 (perkiraan kalender; panitia menyesuaikan dengan ketetapan setempat).
export const demo = makeDemo({
  couple: {
    bride: "KH. Ahmad Zainul Muttaqin", groom: "Ustadz Hilman Fauzi",
    brideFull: "KH. Ahmad Zainul Muttaqin, Lc., M.Ag.",
    groomFull: "Ustadz Hilman Fauzi, S.Pd.I., Al-Hafizh",
    brideParents: "Pengasuh Pondok Pesantren Nurul Huda, Tasikmalaya",
    groomParents: "Imam Masjid Agung Baiturrahman",
    note: "Shalat, Hadiah Terindah dari Langit",
  },
  eventLabel: "Peringatan Isra Mi'raj Nabi Muhammad SAW 1449 H",
  date: "2027-12-25T19:30:00+07:00",
  place: "Masjid Agung Baiturrahman",
  address: "Jl. Ahmad Yani No. 112, Kel. Cicadas, Kec. Cibeunying Kidul, Kota Bandung",
  story: { title: "", body: "" },
  stories: [
    { date: "18.00 WIB", title: "Shalat Maghrib Berjamaah", body: "Jamaah berkumpul di ruang utama, dilanjutkan tadarus singkat menunggu waktu Isya." },
    { date: "19.00 WIB", title: "Shalat Isya Berjamaah", body: "Diimami oleh Ustadz Hilman Fauzi, Al-Hafizh." },
    { date: "19.30 WIB", title: "Pembukaan & Tilawah Al-Qur'an", body: "Pembacaan QS. Al-Isra' ayat 1 dan sambutan Ketua DKM Masjid Agung Baiturrahman." },
    { date: "20.00 WIB", title: "Tausiyah Isra Mi'raj", body: "\"Shalat, Hadiah Terindah dari Langit\" bersama KH. Ahmad Zainul Muttaqin, dilanjutkan tanya jawab." },
    { date: "21.30 WIB", title: "Doa Bersama & Ramah Tamah", body: "Doa penutup, santunan anak yatim, dan hidangan sederhana di serambi masjid." },
  ],
  events: [
    { name: "Tausiyah Peringatan Isra Mi'raj", date: "2027-12-25T19:30:00+07:00", time: "19.30 – 21.30 WIB (ba'da Isya)", venue: "Ruang Utama Masjid Agung Baiturrahman", address: "Jl. Ahmad Yani No. 112, Cicadas, Cibeunying Kidul, Kota Bandung" },
    { name: "Santunan Yatim & Ramah Tamah", date: "2027-12-25T21:30:00+07:00", time: "21.30 – 22.15 WIB", venue: "Serambi Masjid Agung Baiturrahman", address: "Jl. Ahmad Yani No. 112, Cicadas, Cibeunying Kidul, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-infaq", type: "bank", bank_name: "BSI", account_number: "7145 2027 99", account_name: "DKM Masjid Agung Baiturrahman" },
    { id: "demo-yatim", type: "bank", bank_name: "Bank BJB Syariah", account_number: "0510 1027 4411", account_name: "Santunan Yatim Baiturrahman" },
  ],
  guestName: "Bapak H. Dadang Suherman & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Mahasuci (Allah) yang telah memperjalankan hamba-Nya (Nabi Muhammad) pada malam hari dari Masjidilharam ke Masjidilaqsa yang telah Kami berkahi sekelilingnya agar Kami perlihatkan kepadanya sebagian tanda-tanda (kebesaran) Kami. Sesungguhnya Dia Maha Mendengar lagi Maha Melihat.", source: "QS. Al-Isra': 1" },
    dressCode: { note: "Busana muslim dan muslimah yang rapi dan sopan. Bawalah sajadah kecil bila memungkinkan.", colors: ["#ffffff", "#26296a", "#c9a35a", "#e6e1f0"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-12-25T19:30:00+07:00" },
    family: { title: "Penyelenggara", names: ["Panitia PHBI DKM Masjid Agung Baiturrahman", "Majelis Taklim Al-Mubarak", "Ikatan Remaja Masjid Baiturrahman"] },
    faq: { items: [
      { q: "Apakah tersedia tempat untuk jamaah muslimah?", a: "Ya, jamaah muslimah menempati lantai dua dengan layar dan pengeras suara." },
      { q: "Di mana tempat parkir?", a: "Parkir motor di halaman samping masjid, parkir mobil di lapangan RW 05 sekitar 100 meter dari masjid." },
      { q: "Bolehkah membawa anak-anak?", a: "Boleh dan dianjurkan. Mohon didampingi agar majelis tetap khidmat." },
    ] },
  },
});
