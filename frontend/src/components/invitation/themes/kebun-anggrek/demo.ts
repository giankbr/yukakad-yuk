import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Raka",
    brideFull: "Nadia Kusumawardani, S.Si.", groomFull: "Raka Pradipta Nugraha, S.P.",
    brideParents: "Putri bungsu dari\nBapak H. Asep Kusnadi & Ibu Hj. Euis Rohaeni", groomParents: "Putra kedua dari\nBapak Dedi Supriatna & Ibu Neneng Haryati",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r4.webp",
    note: "Seperti anggrek yang tumbuh perlahan di udara lembap, cinta kami tumbuh dengan sabar.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-11T08:00:00+07:00",
  place: "Rumah Kaca Anggrek Ciapus",
  address: "Jl. Raya Ciapus No. 77, Tamansari, Kabupaten Bogor",
  stories: [
    { date: "Agustus 2022", title: "Pameran Anggrek Bogor", body: "Raka menjaga stan anggrek bulan milik kebun keluarganya. Nadia datang untuk meneliti dendrobium dan pulang membawa nomor teleponnya." },
    { date: "2024", title: "Rumah Kaca Pertama", body: "Kami menyewa rumah kaca kecil di Ciapus. Setiap pagi embun menempel di kaca, dan setiap sore kami menyiram bersama." },
    { date: "Februari 2027", title: "Lamaran di Musim Mekar", body: "Keluarga Raka datang melamar saat vanda biru pertama kami berbunga. Bismillah, kami mantap melangkah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-11T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Bogor", address: "Jl. Raya Pajajaran No. 10, Baranangsiang, Bogor Timur, Kota Bogor" },
    { name: "Resepsi di Rumah Kaca", date: "2027-09-11T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Rumah Kaca Anggrek Ciapus", address: "Jl. Raya Ciapus No. 77, Tamansari, Kabupaten Bogor" },
  ],
  gallery: ["/themes/img/a87.webp", "/themes/img/r1.webp", "/themes/img/a85.webp", "/themes/img/a86.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7211 0459 33", account_name: "Nadia Kusumawardani" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0412 0100 8823 507", account_name: "Raka Pradipta Nugraha" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0812 8820 4417", account_name: "Nadia Kusumawardani" },
  ],
  guestName: "Bapak Hendra Gunawan & Keluarga",
  guestTable: "Meja Vanda 2",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu di lorong anggrek", note: "Minuman jahe sereh hangat" },
      { time: "11.30", title: "Kirab kedua mempelai" },
      { time: "12.00", title: "Ramah tamah & santap siang" },
      { time: "13.15", title: "Bibit anggrek untuk setiap tamu", note: "Dibawa pulang dalam pot kecil" },
    ] },
    dressCode: { note: "Nuansa rumah kaca: hijau daun, putih, ungu anggrek, dan biru vanda. Hindari hak tinggi karena lantai batu basah.", colors: ["#2f6a4f", "#f4f1ea", "#a64d9c", "#7c7fd6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Asep Kusnadi", "Kel. Besar Bpk. Dedi Supriatna", "Paguyuban Pecinta Anggrek Bogor"] },
    travel: { note: "Ciapus berada di kaki Gunung Salak. Udara sejuk dan sering gerimis siang hari.", items: [
      { name: "Shuttle dari Stasiun Bogor", detail: "Berangkat pukul 10.00 dan 10.30 WIB" },
      { name: "Parkir", detail: "Lapangan desa Tamansari, 200 m dari rumah kaca" },
    ] },
  },
});
