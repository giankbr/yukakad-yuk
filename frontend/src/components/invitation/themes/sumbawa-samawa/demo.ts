import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aini", groom: "Arif",
    brideFull: "Nurul Aini Ramadhani, S.Pd.", groomFull: "Arif Rahman Hakim, S.P.",
    brideParents: "Putri pertama dari\nBapak H. Abdul Muis & Ibu Hj. Siti Hajar", groomParents: "Putra ketiga dari\nBapak Syamsuddin & Ibu Maryam",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/a96.webp",
    note: "Seperti benang emas kre alang yang ditenun helai demi helai, kami merajut janji dengan sabar untuk saling menjaga seumur hidup.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T08:00:00+08:00",
  place: "Gedung Serbaguna Samawa",
  address: "Jl. Garuda No. 8, Brang Bara, Sumbawa, Kabupaten Sumbawa",
  stories: [
    { date: "2019", title: "Barapan Kebo", body: "Kami bertemu di tepi sawah saat lomba barapan kebo. Arif ikut menjadi joki, Aini sibuk memotret lumpur yang beterbangan." },
    { date: "2023", title: "Perahu ke Pulau Moyo", body: "Satu perjalanan ke air terjun Mata Jitu membuat kami yakin: kami ingin menempuh perjalanan yang lebih panjang bersama." },
    { date: "2026", title: "Bakatoan & Basaputis", body: "Keluarga Arif datang bakatoan, lalu dua keluarga basaputis menyepakati hari baik dengan doa dan mufakat." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+08:00", time: "08.00 – 09.30 WITA", venue: "Masjid Agung Nurul Huda", address: "Jl. Masjid, Bugis, Sumbawa, Kabupaten Sumbawa" },
    { name: "Resepsi", date: "2027-08-14T11:00:00+08:00", time: "11.00 – 15.00 WITA", venue: "Gedung Serbaguna Samawa", address: "Jl. Garuda No. 8, Brang Bara, Sumbawa, Kabupaten Sumbawa" },
  ],
  gallery: ["/themes/img/r104.webp", "/themes/img/a99.webp", "/themes/img/a96.webp", "/themes/img/r81.webp", "/themes/img/r102.webp", "/themes/img/r80.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7244 0187 65", account_name: "Nurul Aini Ramadhani" },
    { id: "demo-ntb", type: "bank", bank_name: "Bank NTB Syariah", account_number: "0210 1123 4567 8", account_name: "Arif Rahman Hakim" },
    { id: "demo-kado", type: "address", address: "Jl. Hasanuddin No. 41, Seketeng, Sumbawa, Kabupaten Sumbawa 84312" },
  ],
  guestName: "Bapak H. Lukman Hakim & Keluarga",
  guestTable: "Meja Moyo 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan pengantin", note: "Diiringi ratib rabana ode" },
      { time: "11.45", title: "Sambutan keluarga & doa" },
      { time: "12.30", title: "Ramah tamah & sakeco", note: "Singang, sepat, dan gecok khas Samawa" },
    ] },
    dressCode: { note: "Busana muslim atau kain kre alang. Marun, emas, dan hitam dipersilakan.", colors: ["#6e1424", "#d4a640", "#24090d", "#efe2c4"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T08:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Muis (Sumbawa Besar)", "Kel. Besar Syamsuddin (Alas, Sumbawa)"] },
  },
});
