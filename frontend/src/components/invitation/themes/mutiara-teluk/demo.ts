import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadhira", groom: "Fahmi",
    brideFull: "Nadhira Salsabila Al-Hamid, M.A.", groomFull: "Fahmi Rizqullah Baharun, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Al-Hamid & Ibu Hj. Syarifah Lubna", groomParents: "Putra sulung dari\nBapak H. Umar Baharun & Ibu Hj. Fatimah Assegaf",
    note: "Seperti mutiara yang tumbuh perlahan di dalam kerang, semoga cinta kami tumbuh dalam kesabaran dan menjadi berkah.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T09:00:00+07:00",
  place: "Masjid Agung Al-Azhar",
  address: "Jl. Sisingamangaraja No. 1, Selong, Kebayoran Baru, Jakarta Selatan",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2022", title: "Corniche Doha", body: "Kami bertemu di kajian pelajar Indonesia di Doha. Selepasnya, rombongan berjalan menyusuri corniche saat matahari tenggelam di teluk." },
    { date: "2024", title: "Rumah Batu Karang", body: "Nadhira meneliti rumah tradisional berpendingin menara angin, Fahmi bertanya tanpa henti. Dari situ obrolan kami tak pernah selesai." },
    { date: "Mar 2027", title: "Khitbah", body: "Kembali ke Jakarta, keluarga Fahmi datang melamar dengan sederhana. Kedua keluarga bermufakat menentukan hari baik." },
    { date: "Sep 2027", title: "Akad", body: "Insyaallah kami menyempurnakan separuh agama di Masjid Agung Al-Azhar, disaksikan keluarga dan sahabat." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Agung Al-Azhar", address: "Jl. Sisingamangaraja No. 1, Selong, Kebayoran Baru, Jakarta Selatan" },
    { name: "Walimatul 'Urs", date: "2027-09-18T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Balai Samudera", address: "Jl. Boulevard Bukit Gading Raya, Kelapa Gading, Jakarta Utara" },
  ],
  gallery: ["/themes/img/r105.webp", "/themes/img/a99.webp", "/themes/img/r38.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7180 9182 027", account_name: "Nadhira Salsabila Al-Hamid" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3310 0918 27", account_name: "Fahmi Rizqullah Baharun" },
  ],
  guestName: "Bapak Habib Hasan Alatas & Keluarga",
  guestTable: "Meja Lulu 6",
  extras: {
    quote: { text: "Dia membiarkan dua laut mengalir yang keduanya kemudian bertemu, di antara keduanya ada batas yang tidak dilampaui masing-masing. Dari keduanya keluar mutiara dan marjan.", source: "QS. Ar-Rahman: 19–22" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan tamu & jamuan kurma" },
      { time: "11.30", title: "Doa bersama dan nasihat pernikahan" },
      { time: "12.00", title: "Ramah tamah & santap siang" },
      { time: "13.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim formal. Warna pasir, emas senja, dan biru teluk dipersilakan.", colors: ["#14304a", "#e2a64b", "#efe3cf", "#f5efe4"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar H. Ahmad Al-Hamid", "Keluarga Besar H. Umar Baharun"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T09:00:00+07:00" },
  },
});
