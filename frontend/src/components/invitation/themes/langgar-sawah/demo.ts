import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Fitri", groom: "Asep",
    brideFull: "Fitri Rahmawati, S.Pd.", groomFull: "Asep Hidayatullah, S.P.",
    brideParents: "Putri kedua dari\nBapak H. Dadan Sudrajat & Ibu Hj. Iis Aisyah", groomParents: "Putra sulung dari\nBapak Ustaz Endang Kosasih & Ibu Imas Masitoh",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Kami tumbuh di kampung yang sama, mengaji di langgar kecil di tepi sawah yang sama. Insyaallah di sana pula kami mengikat janji, disaksikan para sesepuh dan suara bedug asar.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-07-10T09:00:00+07:00",
  place: "Langgar Al-Ikhlas Sukaresmi",
  address: "Kampung Sukaresmi, Desa Cigalontang, Kec. Cigalontang, Kabupaten Tasikmalaya",
  stories: [
    { date: "2008", title: "Mengaji di Langgar", body: "Setiap habis magrib kami mengaji di langgar panggung milik Abah. Fitri selalu duduk di saf depan, Asep selalu kebagian memukul bedug." },
    { date: "2024", title: "Pulang ke Kampung", body: "Selepas kuliah, Asep pulang mengurus sawah keluarga, Fitri mengajar di MI kampung. Kami bertemu lagi di pengajian ibu-ibu dan bapak-bapak." },
    { date: "Maret 2027", title: "Ngalamar", body: "Keluarga Asep datang membawa seserahan dan hasil panen pertama. Lamaran diterima dengan rengginang dan teh panas." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-10T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Langgar Al-Ikhlas Sukaresmi", address: "Kampung Sukaresmi, Desa Cigalontang, Kabupaten Tasikmalaya" },
    { name: "Walimatul 'Ursy", date: "2027-07-10T11:00:00+07:00", time: "11.00 – selesai", venue: "Kediaman Bapak H. Dadan Sudrajat", address: "Kampung Sukaresmi RT 02/RW 05, Desa Cigalontang, Kabupaten Tasikmalaya" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/r14.webp", "/themes/img/r16.webp", "/themes/img/r42.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "4120 0102 3398 507", account_name: "Fitri Rahmawati" },
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7155 2290 41", account_name: "Asep Hidayatullah" },
    { id: "demo-kado", type: "address", address: "Kampung Sukaresmi RT 02/RW 05, Desa Cigalontang, Kec. Cigalontang, Kabupaten Tasikmalaya 46463", account_name: "Keluarga H. Dadan Sudrajat" },
  ],
  guestName: "Bapak Ustaz Ma'mun & Keluarga",
  guestTable: "Saung Kulon",
  extras: {
    quote: { text: "Dan Dialah yang menurunkan air hujan dari langit, lalu Kami tumbuhkan dengan air itu segala macam tumbuh-tumbuhan, maka Kami keluarkan dari tumbuhan itu tanaman yang menghijau.", source: "QS. Al-An'am: 99" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Shalawatan grup marawis kampung" },
      { time: "11.30", title: "Tausiyah walimah", note: "Ustaz Endang Kosasih" },
      { time: "12.00", title: "Botram bersama", note: "Nasi liwet, ikan mas kolam, lalapan" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim sederhana bernuansa sawah: hijau padi, kuning gabah, cokelat kayu, dan putih.", colors: ["#3f6b2a", "#d39a2e", "#8a5a34", "#fbf5e6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Dadan Sudrajat", "Kel. Besar Ustaz Endang Kosasih"] },
  },
});
