import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zulfa", groom: "Hilmi",
    brideFull: "Zulfa Nur Aini Mubarokah", groomFull: "Muhammad Hilmi Fuadi, S.Pd.",
    brideParents: "Putri ketiga dari\nBapak K.H. Masyhudi Ahmad & Ibu Nyai Hj. Muthmainnah", groomParents: "Putra sulung dari\nBapak H. Sholihin & Ibu Siti Rofi'ah",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r4.webp",
    note: "Kami belajar di bawah pohon kamboja yang sama. Semoga rumah kami kelak seteduh serambi surau: sederhana, terbuka, dan selalu penuh doa.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-08-14T08:00:00+07:00",
  place: "Halaman Pondok Pesantren Darussalam",
  address: "Dusun Krajan, Desa Blokagung, Kec. Tegalsari, Banyuwangi, Jawa Timur",
  stories: [
    { date: "2018", title: "Santri Baru", body: "Kami mondok di pesantren yang sama, di asrama putra dan putri yang dipisah halaman berpasir. Hanya saling tahu nama dari daftar setoran hafalan." },
    { date: "2025", title: "Kembali Mengabdi", body: "Selepas kuliah, kami sama-sama pulang mengajar di madrasah pondok. Bu Nyai yang pertama kali menanyakan kesediaan kami." },
    { date: "2027", title: "Akad di Serambi", body: "Insyaallah akad kami digelar di serambi surau tempat kami dulu mengaji, disaksikan para guru." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.00 WIB", venue: "Surau Pondok Pesantren Darussalam", address: "Dusun Krajan, Desa Blokagung, Kec. Tegalsari, Banyuwangi" },
    { name: "Walimatul 'Ursy", date: "2027-08-14T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Halaman Pondok Pesantren Darussalam", address: "Dusun Krajan, Desa Blokagung, Kec. Tegalsari, Banyuwangi" },
  ],
  gallery: ["/themes/img/r1.webp", "/themes/img/r13.webp", "/themes/img/a64.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0045 0110 2233 509", account_name: "Zulfa Nur Aini Mubarokah" },
    { id: "demo-kado", type: "address", address: "Ndalem Pondok Pesantren Darussalam, Blokagung, Tegalsari, Banyuwangi 68491" },
  ],
  guestName: "Bapak Ustadz Mahfudz & Keluarga",
  guestTable: "Serambi Timur",
  extras: {
    quote: { text: "Dan nikahkanlah orang-orang yang masih membujang di antara kamu. Jika mereka miskin, Allah akan memberi kemampuan kepada mereka dengan karunia-Nya.", source: "QS. An-Nur: 32" },
    rundown: { items: [
      { time: "10.00", title: "Pembacaan shalawat", note: "Grup hadrah santri" },
      { time: "10.45", title: "Mauidhoh hasanah", note: "K.H. Masyhudi Ahmad" },
      { time: "11.30", title: "Makan bersama", note: "Nasi berkat & tumpeng" },
    ] },
    dressCode: { note: "Sarung, koko, dan gamis sederhana. Warna tanah, hijau daun, dan putih.", colors: ["#5e3b20", "#4f6b3a", "#c0643a", "#fbf4e6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Pondok Pesantren Darussalam", "Kel. Besar H. Sholihin"] },
  },
});
