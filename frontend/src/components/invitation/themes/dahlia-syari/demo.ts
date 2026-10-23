import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salsabila", groom: "Umar",
    brideFull: "Salsabila Khairunnisa, S.Gz.", groomFull: "Umar Al-Faruq Hidayat, S.Kom.",
    brideParents: "Putri kedua dari\nBapak H. Dedi Supriadi & Ibu Hj. Rina Marlina", groomParents: "Putra sulung dari\nBapak Ir. Asep Hidayat & Ibu Euis Rohmah",
    note: "Seperti dahlia yang mekar perlahan lapis demi lapis, semoga kasih kami tumbuh dalam sabar dan syukur.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-15T08:00:00+07:00",
  place: "Masjid Pusdai Jawa Barat",
  address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung",
  stories: [
    { date: "2022", title: "Kajian Pekanan", body: "Kami sama-sama menjadi panitia kajian muslimah dan pemuda di masjid kampus, hanya bertegur sapa soal jadwal dan konsumsi." },
    { date: "2026", title: "Ta'aruf", body: "Melalui guru ngaji keluarga, biodata kami dipertukarkan. Pertemuan pertama berlangsung di ruang tamu rumah, ditemani teh hangat." },
    { date: "Januari 2027", title: "Khitbah", body: "Keluarga Umar datang ke Antapani membawa doa dan serangkai dahlia dari kebun neneknya di Lembang." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
    { name: "Walimatul 'Ursy", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Aula Serbaguna Pusdai", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7291 0438 5527", account_name: "Salsabila Khairunnisa" },
    { id: "demo-bjbs", type: "bank", bank_name: "Bank BJB Syariah", account_number: "5200 1094 7713", account_name: "Umar Al-Faruq Hidayat" },
    { id: "demo-kado", type: "address", address: "Jl. Terusan Jakarta No. 112, Antapani Tengah, Kota Bandung 40291", account_name: "Keluarga H. Dedi Supriadi" },
  ],
  guestName: "Ibu Hj. Nurhasanah & Keluarga",
  guestTable: "Meja Dahlia 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu merasa tenteram kepadanya.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Area tamu putra & putri terpisah" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim santun bernuansa hangat: terakota, merah muda pudar, dan krem.", colors: ["#b55a3a", "#e8a99a", "#f4e6d2", "#7d8a58"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Dedi Supriadi", "Kel. Besar Ir. Asep Hidayat"] },
    faq: { items: [
      { q: "Apakah area tamu putra dan putri dipisah?", a: "Ya, aula walimah dibagi dua dengan tirai untuk tamu putra dan putri." },
      { q: "Apakah tersedia parkir?", a: "Tersedia parkir di halaman Pusdai dan Lapangan Gasibu di seberangnya." },
    ] },
  },
});
