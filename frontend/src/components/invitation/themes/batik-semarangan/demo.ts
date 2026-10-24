import { makeDemo } from "../demo-base";

// Pernikahan di Semarang: batik Semarangan bermotif asem arang dan kuntul, Kota Lama, dan pesisir utara Jawa.
export const demo = makeDemo({
  couple: {
    bride: "Kinasih", groom: "Rizal",
    brideFull: "Kinasih Ayuningtyas, S.Sn.", groomFull: "Muhammad Rizal Hakim, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Bambang Sutejo & Ibu Hj. Endang Wahyuni", groomParents: "Putra pertama dari\nBapak Drs. Agus Salim & Ibu Siti Maemunah",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti pohon asem di tepi jalan Semarang: akarnya dalam, daunnya rindang, dan selalu ada tempat bagi burung kuntul pulang.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T08:00:00+07:00",
  place: "Gedung Monod Diephuis, Kota Lama",
  address: "Jl. Kepodang No. 11–13, Purwodinatan, Semarang Tengah, Kota Semarang",
  stories: [
    { date: "2021", title: "Canting Pertama", body: "Rizal ikut kelas membatik di Kampung Batik Bubakan karena tugas kantor. Kinasih yang mengajar, dan malam pertamanya menetes ke mana-mana." },
    { date: "2024", title: "Sore di Kota Lama", body: "Kami mulai rutin berjalan sore dari Gereja Blenduk ke Pasar Johar, mencari lumpia dan cerita lama tentang kota ini." },
    { date: "2027", title: "Satu Kain, Dua Nama", body: "Dengan restu kedua keluarga, kami menorehkan malam di kain yang sama, motif asem dan kuntul, untuk dipakai di hari bahagia." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Jawa Tengah", address: "Jl. Gajah Raya, Sambirejo, Kec. Gayamsari, Kota Semarang" },
    { name: "Resepsi", date: "2027-08-14T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Gedung Monod Diephuis, Kota Lama", address: "Jl. Kepodang No. 11–13, Purwodinatan, Semarang Tengah, Kota Semarang" },
  ],
  gallery: ["/themes/img/a27.webp", "/themes/img/a49.webp", "/themes/img/a26.webp", "/themes/img/a43.webp", "/themes/img/a50.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0095 1408 2027", account_name: "Kinasih Ayuningtyas" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7214 0827 15", account_name: "Muhammad Rizal Hakim" },
    { id: "demo-kado", type: "address", address: "Jl. Pandanaran II No. 24, Mugassari, Semarang Selatan, Kota Semarang 50249" },
  ],
  guestName: "Bapak Hendra Gunawan & Keluarga",
  guestTable: "Meja Asem 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "18.30", title: "Kirab pengantin", note: "Diiringi gambang Semarang" },
      { time: "19.00", title: "Doa & sambutan keluarga" },
      { time: "19.30", title: "Ramah tamah", note: "Lumpia, tahu gimbal, dan wedang tahu" },
    ] },
    dressCode: { note: "Berbatik pesisir dipersilakan. Merah soga, nila, dan krem.", colors: ["#b03a2b", "#1d2a52", "#f1e5c8", "#d29a3e"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bapak H. Bambang Sutejo", "Kel. Besar Bapak Drs. Agus Salim", "Paguyuban Pembatik Bubakan"] },
  },
});
