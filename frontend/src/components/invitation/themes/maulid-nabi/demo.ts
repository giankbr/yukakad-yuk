import { makeDemo } from "../demo-base";

// Peringatan Maulid Nabi Muhammad SAW oleh DKM & majelis taklim: pengisi acara di data mempelai (penceramah + grup
// shalawat), tema tausiyah di catatan, sesi acara di daftar acara, rangkaian kegiatan menyambut Maulid di cerita.
export const demo = makeDemo({
  couple: {
    bride: "Ustadz H. Faiz Rabbani", groom: "Hadrah Al-Mahabbah",
    brideFull: "Ustadz H. Muhammad Faiz Rabbani, Lc., M.A.",
    groomFull: "Grup Hadrah & Shalawat Al-Mahabbah",
    brideParents: "Pengasuh Majelis Taklim Raudhatul Muhibbin, Bekasi",
    groomParents: "Remaja Masjid Jami' Nurul Iman",
    note: "Meneladani Akhlak Rasulullah di Tengah Keluarga",
  },
  eventLabel: "Peringatan Maulid Nabi Muhammad SAW",
  date: "2027-08-15T08:00:00+07:00",
  place: "Masjid Jami' Nurul Iman",
  address: "Jl. Pondok Kelapa Raya No. 27, Kel. Pondok Kelapa, Kec. Duren Sawit, Jakarta Timur",
  story: { title: "", body: "" },
  stories: [
    { date: "1 Rabiul Awal", title: "Pembukaan Bulan Maulid", body: "Pembacaan maulid dan shalawat bersama jamaah setiap malam Jumat di serambi masjid." },
    { date: "8 Agustus 2027", title: "Lomba Anak-anak", body: "Lomba adzan, hafalan surat pendek, dan mewarnai untuk santri TPQ Nurul Iman." },
    { date: "Sepekan sebelumnya", title: "Penggalangan Infaq & Sembako", body: "Panitia menerima infaq dan paket sembako untuk santunan anak yatim dan dhuafa di lingkungan masjid." },
    { date: "12 Rabiul Awal 1449 H", title: "Puncak Peringatan", body: "Tausiyah Maulid, lantunan shalawat, dan santunan anak yatim bersama seluruh jamaah." },
  ],
  events: [
    { name: "Pembukaan, Tilawah & Shalawat", date: "2027-08-15T08:00:00+07:00", time: "08.00 – 08.45 WIB", venue: "Ruang Utama Masjid Jami' Nurul Iman", address: "Jl. Pondok Kelapa Raya No. 27, Duren Sawit, Jakarta Timur" },
    { name: "Tausiyah Maulid Nabi", date: "2027-08-15T08:45:00+07:00", time: "08.45 – 10.15 WIB", venue: "Ruang Utama Masjid Jami' Nurul Iman", address: "Jl. Pondok Kelapa Raya No. 27, Duren Sawit, Jakarta Timur" },
    { name: "Santunan Anak Yatim & Doa Bersama", date: "2027-08-15T10:15:00+07:00", time: "10.15 – 11.30 WIB", venue: "Pelataran Masjid Jami' Nurul Iman", address: "Jl. Pondok Kelapa Raya No. 27, Duren Sawit, Jakarta Timur" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-infaq", type: "bank", bank_name: "BSI", account_number: "7230 1455 18", account_name: "DKM Masjid Jami' Nurul Iman" },
    { id: "demo-yatim", type: "bank", bank_name: "Bank Muamalat", account_number: "3410 0098 77", account_name: "Santunan Yatim Nurul Iman" },
    { id: "demo-sembako", type: "address", address: "Sekretariat DKM, Jl. Pondok Kelapa Raya No. 27, Duren Sawit, Jakarta Timur 13450", account_name: "Panitia Maulid Nurul Iman" },
  ],
  guestName: "Bapak H. Rahmat Hidayat & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Sungguh, telah ada pada (diri) Rasulullah itu suri teladan yang baik bagimu, (yaitu) bagi orang yang mengharap (rahmat) Allah dan (kedatangan) hari Kiamat dan yang banyak mengingat Allah.", source: "QS. Al-Ahzab: 21" },
    dressCode: { note: "Busana muslim dan muslimah yang rapi dan sopan. Nuansa putih atau hijau dipersilakan.", colors: ["#ffffff", "#1f6b4e", "#c79a45", "#efe6cf"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-15T08:45:00+07:00" },
    guestPass: {},
    family: { title: "Penyelenggara", names: ["DKM Masjid Jami' Nurul Iman", "Majelis Taklim Raudhatul Muhibbin", "Ikatan Remaja Masjid Nurul Iman"] },
    faq: { items: [
      { q: "Apakah tersedia tempat untuk jamaah muslimah?", a: "Ya, jamaah muslimah menempati lantai dua dengan layar dan pengeras suara." },
      { q: "Bagaimana menyalurkan paket sembako?", a: "Paket sembako dapat diantar ke sekretariat DKM paling lambat H-3, setiap hari pukul 09.00 – 16.00 WIB." },
      { q: "Apakah anak-anak boleh ikut?", a: "Boleh, dan sangat dianjurkan. Mohon didampingi agar majelis tetap khidmat." },
    ] },
  },
});
