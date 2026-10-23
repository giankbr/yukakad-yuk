import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadhira", groom: "Ilham",
    brideFull: "Nadhira Khairunnisa, S.Ds.", groomFull: "Muhammad Ilham Fauzan, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Abdul Rozak & Ibu Hj. Siti Khotimah",
    groomParents: "Putra pertama dari\nBapak Slamet Riyadi & Ibu Nur Azizah",
    note: "Seperti dua helai kain yang ditenun bersama, semoga kami saling menguatkan dalam ridha-Nya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-19T08:00:00+07:00",
  place: "Masjid Agung Al-Jami' Pekalongan",
  address: "Jl. Kauman No. 1, Kauman, Kec. Pekalongan Timur, Kota Pekalongan",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2023", title: "Satu Rumah Batik", body: "Nadhira merancang motif untuk usaha batik keluarganya, Ilham datang membantu menata mesin cap yang baru." },
    { date: "2025", title: "Ta'aruf", body: "Lewat perantara ustadz di kajian Kamis malam, kami bertukar biodata dan bertemu didampingi keluarga." },
    { date: "Feb 2027", title: "Khitbah", body: "Keluarga Ilham datang ke Kauman membawa seserahan sederhana, dan dengan izin Allah lamaran diterima." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Al-Jami' Pekalongan", address: "Jl. Kauman No. 1, Kauman, Kec. Pekalongan Timur, Kota Pekalongan" },
    { name: "Walimah", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 13.30 WIB", venue: "Gedung Serbaguna Sapuro", address: "Jl. Dr. Wahidin No. 27, Sapuro Kebulen, Kec. Pekalongan Barat, Kota Pekalongan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7204 1188 63", account_name: "Nadhira Khairunnisa" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0071 0102 4455 507", account_name: "Muhammad Ilham Fauzan" },
    { id: "demo-address", type: "address", address: "Jl. Hayam Wuruk Gg. 3 No. 12, Kauman, Pekalongan Timur, Kota Pekalongan 51128", account_name: "Keluarga H. Abdul Rozak" },
  ],
  guestName: "Ibu Hj. Maryam & Keluarga",
  guestTable: "Meja Kawung 3",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat kebesaran Allah.", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah", note: "Area tamu putra & putri terpisah" },
      { time: "13.00", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim yang longgar dan sopan. Batik bernuansa sage, biru lembut, dan krem dipersilakan.", colors: ["#9db4a0", "#94abc0", "#f4eee2", "#46596a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Rozak", "Kel. Besar Slamet Riyadi"] },
  },
});
