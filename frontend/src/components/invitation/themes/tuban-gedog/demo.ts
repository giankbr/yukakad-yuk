import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laila", groom: "Fadhil",
    brideFull: "Nur Laila Maghfiroh", groomFull: "Muhammad Fadhil Arrozaq",
    brideParents: "Putri dari Bapak H. Abdul Ghofur\n& Ibu Hj. Siti Masruroh", groomParents: "Putra dari Bapak Kasmuri\n& Ibu Sri Wahyuni",
    note: "Benang lungsin dari bukit Kerek, benang pakan dari pesisir Palang. Insyaallah kami ditenun menjadi satu kain, kuat dan hangat dipakai seumur hidup.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T08:00:00+07:00",
  place: "Masjid Agung Tuban",
  address: "Jl. Kartini No. 1, Kutorejo, Kec. Tuban, Kabupaten Tuban, Jawa Timur",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Mei 2022", title: "Di Pameran Tenun", body: "Laila menjaga stan tenun gedog keluarganya di alun-alun Tuban. Fadhil datang mencari kain untuk ibunya dan pulang membawa dua lembar, satu lagi sebagai alasan untuk kembali." },
    { date: "2024", title: "Dari Kerek ke Palang", body: "Setiap Ahad Fadhil mengantar ikan dari TPI Palang, lalu mampir ke Kerek mendengar suara gedog alat tenun di teras rumah Laila." },
    { date: "Februari 2027", title: "Lamaran", body: "Keluarga Fadhil datang membawa seserahan dan sehelai kain gedog biru tua. Kedua keluarga bersepakat dengan penuh syukur." },
    { date: "September 2027", title: "Akad Nikah", body: "Bismillah, kami menyempurnakan separuh agama di Masjid Agung Tuban." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Tuban", address: "Jl. Kartini No. 1, Kutorejo, Kec. Tuban, Kabupaten Tuban" },
    { name: "Resepsi", date: "2027-09-18T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Serbaguna Kerek", address: "Jl. Raya Kerek–Merakurak, Desa Kedungrejo, Kec. Kerek, Kabupaten Tuban" },
    { name: "Ngunduh Mantu", date: "2027-09-25T19:00:00+07:00", time: "19.00 WIB – selesai", venue: "Kediaman Bapak Kasmuri", address: "Dusun Pesisir RT 02, Desa Palang, Kec. Palang, Kabupaten Tuban" },
  ],
  gallery: ["/themes/img/a21.webp", "/themes/img/r109.webp", "/themes/img/r103.webp", "/themes/img/a23.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7180 2027 918", account_name: "Nur Laila Maghfiroh" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4120 918 027", account_name: "Muhammad Fadhil Arrozaq" },
    { id: "demo-kado", type: "address", address: "Desa Kedungrejo RT 03 RW 01, Kec. Kerek, Kabupaten Tuban, Jawa Timur 62356" },
  ],
  guestName: "Bapak Imam Syafi'i & Keluarga",
  guestTable: "Meja Gedog 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin dan sambutan keluarga" },
      { time: "11.30", title: "Doa bersama dan ramah tamah" },
      { time: "12.00", title: "Santap siang: ikan bakar pesisir dan nasi ampok" },
      { time: "13.00", title: "Pameran kecil tenun gedog keluarga Kerek" },
    ] },
    dressCode: { note: "Batik atau tenun gedog dipersilakan. Nuansa biru indigo dan putih alam.", colors: ["#22395c", "#e7dcc3", "#9c3b2a", "#2e5560"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar H. Abdul Ghofur", "Keluarga Besar Kasmuri", "Paguyuban Penenun Kedungrejo"] },
    faq: { items: [
      { q: "Apakah tersedia tempat salat?", a: "Tersedia musala di Gedung Serbaguna Kerek, dan Masjid Agung Tuban untuk akad." },
      { q: "Berapa jauh Kerek dari kota Tuban?", a: "Sekitar 30 menit ke arah barat daya lewat jalan raya Merakurak." },
    ] },
  },
});
