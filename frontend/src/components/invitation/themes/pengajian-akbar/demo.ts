import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ustadz Fauzan", groom: "Ustadz Ridwan",
    brideFull: "Ustadz H. Ahmad Fauzan Hakim, Lc., M.A.",
    groomFull: "Ustadz Muhammad Ridwan, S.Ag., Al-Hafizh",
    brideParents: "Pengasuh Pondok Pesantren Darul Falah, Bogor",
    groomParents: "Imam Masjid Jami' Al-Hidayah",
    note: "Menjaga Hati di Tengah Kesibukan Dunia",
  },
  eventLabel: "Pengajian Akbar",
  date: "2027-10-17T08:00:00+07:00",
  place: "Masjid Jami' Al-Hidayah",
  address: "Jl. Raya Pajajaran No. 88, Bantarjati, Kota Bogor, Jawa Barat",
  story: { title: "", body: "" },
  stories: [],
  events: [
    { name: "Pembukaan & Tilawah Al-Qur'an", date: "2027-10-17T08:00:00+07:00", time: "08.00 – 08.30 WIB", venue: "Ruang Utama Masjid Jami' Al-Hidayah", address: "Jl. Raya Pajajaran No. 88, Bantarjati, Kota Bogor" },
    { name: "Kajian Utama", date: "2027-10-17T08:30:00+07:00", time: "08.30 – 10.30 WIB", venue: "Ruang Utama Masjid Jami' Al-Hidayah", address: "Jl. Raya Pajajaran No. 88, Bantarjati, Kota Bogor" },
    { name: "Tanya Jawab & Doa Bersama", date: "2027-10-17T10:30:00+07:00", time: "10.30 – 11.30 WIB", venue: "Pelataran Masjid Jami' Al-Hidayah", address: "Jl. Raya Pajajaran No. 88, Bantarjati, Kota Bogor" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-infaq", type: "bank", bank_name: "BSI", account_number: "7123 4455 66", account_name: "DKM Masjid Jami' Al-Hidayah" },
  ],
  guestName: "Bapak H. Sulaiman & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "…niscaya Allah akan mengangkat (derajat) orang-orang yang beriman di antaramu dan orang-orang yang diberi ilmu beberapa derajat. Dan Allah Mahateliti apa yang kamu kerjakan.", source: "QS. Al-Mujadilah: 11" },
    dressCode: { note: "Busana muslim dan muslimah yang rapi dan sopan. Nuansa putih atau hijau dipersilakan.", colors: ["#ffffff", "#1f4d3f", "#c9a24a", "#e9e2cf"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-17T08:30:00+07:00" },
    guestPass: {},
    family: { title: "Penyelenggara", names: ["DKM Masjid Jami' Al-Hidayah", "Majelis Taklim Nurul Huda", "Ikatan Remaja Masjid Al-Hidayah"] },
    faq: { items: [
      { q: "Apakah tersedia tempat untuk jamaah muslimah?", a: "Ya, jamaah muslimah menempati lantai dua dengan layar dan pengeras suara." },
      { q: "Di mana tempat parkir?", a: "Parkir motor di halaman samping masjid, parkir mobil di lapangan SDN Bantarjati 3 (± 100 m)." },
      { q: "Apakah anak-anak boleh ikut?", a: "Boleh. Mohon didampingi agar majelis tetap khidmat." },
    ] },
  },
});
