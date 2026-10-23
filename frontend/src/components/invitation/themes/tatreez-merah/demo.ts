import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Faris",
    brideFull: "Nadia Salsabila Rahman, S.Ds.", groomFull: "Muhammad Faris Alhabsyi, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Abdul Rahman Siregar & Ibu Hj. Fatimah Lubis", groomParents: "Putra sulung dari\nBapak Husein Alhabsyi & Ibu Khadijah Assegaf",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti sulaman yang dikerjakan setusuk demi setusuk, kami ingin membangun rumah tangga dengan sabar, rapi, dan penuh doa.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-15T08:00:00+07:00",
  place: "Masjid Raya Bogor",
  address: "Jl. Raya Pajajaran No. 10, Baranangsiang, Kec. Bogor Timur, Kota Bogor",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2023", title: "Pameran Wastra", body: "Nadia menjaga stan sulaman di sebuah pameran amal. Faris datang membeli taplak bersulam untuk ibunya, lalu kembali keesokan harinya untuk bertanya cara merawatnya." },
    { date: "2025", title: "Ta'aruf", body: "Melalui perantara guru mengaji keluarga, kami bertukar biodata dan saling mendoakan dalam istikharah." },
    { date: "2026", title: "Khitbah", body: "Keluarga Alhabsyi datang ke Bogor dengan niat baik. Lamaran diterima dengan hangat oleh keluarga Rahman." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Bogor", address: "Jl. Raya Pajajaran No. 10, Baranangsiang, Kec. Bogor Timur, Kota Bogor" },
    { name: "Walimatul 'Ursy", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Graha Pancasila", address: "Jl. Pangrango No. 23, Babakan, Kec. Bogor Tengah, Kota Bogor" },
  ],
  gallery: ["/themes/img/r55.webp", "/themes/img/r57.webp", "/themes/img/r58.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7208 4415 63", account_name: "Nadia Salsabila Rahman" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3410 0287 9915", account_name: "Muhammad Faris Alhabsyi" },
    { id: "demo-kado", type: "address", address: "Jl. Pandu Raya Gg. Melati No. 7, Tegal Gundil, Kec. Bogor Utara, Kota Bogor 16152" },
  ],
  guestName: "Bapak Ustadz Ahmad Zaki & Keluarga",
  guestTable: "Meja Saru 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu cenderung dan merasa tenteram kepadanya.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Diiringi marawis Majelis Al-Ikhlas" },
      { time: "11.30", title: "Tilawah & tausiyah pernikahan", note: "Ustadz Hasan Basri, Lc." },
      { time: "12.15", title: "Ramah tamah & santap siang" },
      { time: "13.30", title: "Doa penutup & foto keluarga" },
    ] },
    dressCode: { note: "Busana muslim yang sopan. Nuansa merah tua, gading, dan hitam dipersilakan.", colors: ["#9b1c24", "#eee4cf", "#221c1b", "#2c5a3e"] },
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Rahman Siregar", "Kel. Besar Husein Alhabsyi", "Majelis Taklim Al-Ikhlas Bogor"] },
    faq: { items: [
      { q: "Apakah tempat tamu putra dan putri dipisah?", a: "Ya, area ramah tamah disusun terpisah dengan tirai, keluarga tetap bisa duduk berdekatan." },
      { q: "Di mana tempat parkir?", a: "Parkir tersedia di halaman Graha Pancasila dan di Jl. Pangrango, petugas akan membantu mengarahkan." },
    ] },
  },
});
