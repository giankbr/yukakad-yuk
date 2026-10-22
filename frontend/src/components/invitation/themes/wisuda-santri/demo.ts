import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Fauzan", groom: "",
    brideFull: "Ahmad Fauzan Hakim",
    brideParents: "Putra dari Bapak H. Syamsul Arifin & Ibu Hj. Siti Masruroh",
    note: "Enam tahun mondok, mengaji siang dan malam. Alhamdulillah, Fauzan telah menuntaskan hafalan 30 juz dan menamatkan pendidikan diniyah.",
  },
  eventLabel: "Wisuda & Khataman Santri",
  date: "2027-06-27T08:00:00+07:00",
  place: "Aula Pondok Pesantren Raudlatul Ilmi",
  address: "Jl. KH. Wahid Hasyim No. 7, Bandar Kidul, Mojoroto, Kediri",
  story: { title: "Perjalanan di pondok", body: "" },
  stories: [
    { date: "2021", title: "Pertama kali mondok", body: "Datang dengan satu lemari kecil dan sebuah sarung baru, menangis di malam pertama, lalu betah sampai lupa pulang." },
    { date: "2023", title: "Setengah perjalanan", body: "Menyetorkan hafalan 15 juz di depan pengasuh, sambil mulai mengaji kitab Jurumiyah dan Safinah." },
    { date: "2026", title: "Khatam 30 juz", body: "Menuntaskan setoran terakhir di bulan Ramadan, disambut tangis haru teman sekamar." },
    { date: "2027", title: "Wisuda", body: "Lulus Madrasah Diniyah Ulya dan diwisuda bersama 112 santri seangkatan." },
  ],
  events: [
    { name: "Wisuda & Khataman Akbar", date: "2027-06-27T08:00:00+07:00", time: "08.00 – 11.30 WIB", venue: "Aula Pondok Pesantren Raudlatul Ilmi", address: "Jl. KH. Wahid Hasyim No. 7, Bandar Kidul, Mojoroto, Kediri" },
    { name: "Tasyakuran Keluarga", date: "2027-06-27T13:00:00+07:00", time: "13.00 – 15.00 WIB", venue: "Kediaman Keluarga", address: "Jl. Pattimura Gg. III No. 18, Pesantren, Kediri" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BSI", account_number: "7192 0045 18", account_name: "Siti Masruroh" },
  ],
  guestName: "Bapak Ustadz Mahfudz & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Ahmad Fauzan Hakim, Al-Hafidz", nickname: "Fauzan", parents: "Putra dari Bapak H. Syamsul Arifin & Ibu Hj. Siti Masruroh" },
    quote: { text: "Sebaik-baik kalian adalah orang yang mempelajari Al-Qur'an dan mengajarkannya.", source: "HR. Bukhari" },
    rundown: { items: [
      { time: "08.00", title: "Pembukaan & pembacaan Al-Qur'an" },
      { time: "08.30", title: "Khataman bil ghaib", note: "Para hafidz membaca juz 30" },
      { time: "09.30", title: "Prosesi wisuda & penyerahan syahadah" },
      { time: "10.30", title: "Mauidhoh hasanah & doa khatmil Qur'an" },
    ] },
    dressCode: { note: "Busana muslim rapi bernuansa hijau atau putih. Bapak-bapak dipersilakan bersarung dan berpeci.", colors: ["#2f6b48", "#fbfbf6", "#a7c7a8", "#c9b26a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut berbahagia", names: ["KH. Abdul Ghofur (Pengasuh)", "Keluarga Besar Bani Arifin", "Keluarga Besar Bani Masruroh"] },
    faq: { items: [
      { q: "Apakah tamu putri dan putra dipisah?", a: "Ya. Tamu putra di aula utama, tamu putri di serambi aula sisi timur." },
      { q: "Di mana area parkir?", a: "Parkir tersedia di lapangan pondok, masuk dari gerbang utama." },
    ] },
  },
});
