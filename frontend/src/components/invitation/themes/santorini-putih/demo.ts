import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ayu", groom: "Dewa",
    brideFull: "Ni Luh Putu Ayu Saraswati, S.Par.", groomFull: "I Dewa Gede Wiradharma, S.Kom.",
    brideParents: "Putri pertama dari\nBapak I Made Sudarsana & Ibu Ni Ketut Sri Wahyuni", groomParents: "Putra kedua dari\nBapak I Dewa Ketut Artawan & Ibu Desak Made Suarni",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Dua anak pesisir yang dipertemukan ombak, kini berlabuh di dermaga yang sama.",
  },
  eventLabel: "Pawiwahan",
  date: "2027-08-14T08:00:00+08:00",
  place: "Villa Batu Putih",
  address: "Jl. Pantai Suluban, Pecatu, Kuta Selatan, Badung, Bali",
  stories: [
    { date: "2019", title: "Kelas Selancar Pagi", body: "Dewa jatuh dari papan tiga kali di depan Ayu, pemandu baru di sekolah selancar Uluwatu. Ayu tertawa, lalu mengajarinya." },
    { date: "2023", title: "Rumah Putih di Tebing", body: "Kami sama-sama bekerja di sebuah vila bercat putih di atas laut, dan senja demi senja kami habiskan di teras yang sama." },
    { date: "2026", title: "Mapepadik", body: "Keluarga Dewa datang meminang dengan penuh adat. Di bawah bugenvil teras rumah, kedua keluarga sepakat menentukan hari baik." },
  ],
  events: [
    { name: "Upacara Pawiwahan", date: "2027-08-14T08:00:00+08:00", time: "08.00 – 11.00 WITA", venue: "Kediaman Mempelai Pria", address: "Jl. Tukad Badung No. 17, Renon, Denpasar Selatan, Denpasar" },
    { name: "Resepsi Senja di Tebing", date: "2027-08-14T17:00:00+08:00", time: "17.00 – 21.00 WITA", venue: "Villa Batu Putih", address: "Jl. Pantai Suluban, Pecatu, Kuta Selatan, Badung, Bali" },
  ],
  gallery: ["/themes/img/r10.webp", "/themes/img/a21.webp", "/themes/img/r105.webp", "/themes/img/r38.webp", "/themes/img/r9.webp", "/themes/img/r110.webp"],
  gifts: [
    { id: "demo-bpd", type: "bank", bank_name: "BPD Bali", account_number: "0180 2021 5566", account_name: "Ni Luh Putu Ayu Saraswati" },
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0631 4478 92", account_name: "I Dewa Gede Wiradharma" },
    { id: "demo-kado", type: "address", address: "Jl. Tukad Badung No. 17, Renon, Denpasar Selatan 80226" },
  ],
  guestName: "Bapak I Wayan Sutama & Keluarga",
  guestTable: "Meja Bugenvil 3",
  extras: {
    quote: { text: "Wahai pasangan suami-istri, semoga kalian tetap bersatu dan tidak pernah terpisahkan. Semoga kalian mencapai hidup penuh kebahagiaan, tinggal di rumah yang penuh kegembiraan bersama anak cucu.", source: "Rgveda X.85.42" },
    rundown: { items: [
      { time: "17.00", title: "Welcome drink di teras tebing" },
      { time: "17.45", title: "Matahari terbenam & foto bersama" },
      { time: "18.30", title: "Santap malam hidangan laut", note: "Taman bugenvil" },
      { time: "20.00", title: "Tari & musik akustik" },
    ] },
    dressCode: { note: "Putih bersih dengan aksen biru laut atau magenta bugenvil.", colors: ["#fbfaf5", "#1f4fa8", "#7fb2e5", "#c21f74"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. I Made Sudarsana", "Kel. Besar Bpk. I Dewa Ketut Artawan"] },
  },
});
