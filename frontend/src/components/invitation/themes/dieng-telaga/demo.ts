import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Fajar",
    brideFull: "Nadia Ayu Rahmawati, S.P.", groomFull: "Fajar Nur Hidayat, S.T.",
    brideParents: "Putri sulung dari\nBapak H. Slamet Riyanto & Ibu Hj. Siti Khotimah", groomParents: "Putra kedua dari\nBapak Muhammad Darsono & Ibu Tri Wahyuningsih",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/a113.webp",
    note: "Seperti kabut pagi yang selalu pulang ke Telaga Warna, kami memilih untuk saling pulang, setiap hari.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T08:00:00+07:00",
  place: "Balai Desa Dieng Wetan",
  address: "Jl. Raya Dieng, Desa Dieng Wetan, Kec. Kejajar, Kabupaten Wonosobo, Jawa Tengah",
  stories: [
    { date: "2019", title: "Bertemu di Kebun", body: "Nadia sedang penelitian kentang untuk skripsinya, Fajar membantu pamannya di ladang sebelah. Obrolan pertama soal hama daun di tengah kabut pagi." },
    { date: "2023", title: "Festival Budaya Dieng", body: "Di antara lampion dan seruling, Fajar memberanikan diri mengenalkan Nadia kepada ibunya. Malam itu suhunya hampir nol derajat, tapi hati kami hangat." },
    { date: "2026", title: "Lamaran di Rumah", body: "Keluarga Fajar datang membawa seserahan dan sekeranjang carica. Kedua keluarga sepakat, Insyaallah tahun depan di musim kemarau." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Jami' Baiturrahman Dieng Wetan", address: "Dusun Dieng Wetan RT 02 RW 01, Kec. Kejajar, Kabupaten Wonosobo" },
    { name: "Resepsi & Syukuran", date: "2027-08-14T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Balai Desa Dieng Wetan", address: "Jl. Raya Dieng, Desa Dieng Wetan, Kec. Kejajar, Kabupaten Wonosobo" },
  ],
  gallery: ["/themes/img/r104.webp", "/themes/img/a22.webp", "/themes/img/r108.webp", "/themes/img/r89.webp", "/themes/img/r61.webp", "/themes/img/r42.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BRI", account_number: "3125 0102 7788 509", account_name: "Nadia Ayu Rahmawati" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7210 4455 81", account_name: "Fajar Nur Hidayat" },
    { id: "demo-kado", type: "address", address: "Dusun Dieng Wetan RT 02 RW 01, Kec. Kejajar, Kabupaten Wonosobo 56354" },
  ],
  guestName: "Bapak Kusnadi & Keluarga",
  guestTable: "Meja Telaga Warna",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kirab manten & penyambutan", note: "Diiringi rebana warga Dieng Wetan" },
      { time: "11.30", title: "Panggih & sungkeman" },
      { time: "12.15", title: "Ramah tamah", note: "Mie ongklok, tempe kemul & wedang purwaceng" },
      { time: "13.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Dieng sangat dingin di bulan Agustus (bisa 5–10°C pagi hari). Busana sopan bernuansa hijau telaga atau krem; jaket dan syal sangat dianjurkan.", colors: ["#1f5c5a", "#57b8ad", "#e39a32", "#efeee6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. H. Slamet Riyanto", "Kel. Besar Bpk. Muhammad Darsono", "Warga Desa Dieng Wetan"] },
    travel: { note: "Untuk tamu dari luar kota, berikut beberapa saran perjalanan dan menginap.", items: [
      { name: "Homestay di Dieng Wetan", detail: "Banyak pilihan ± 200–500 m dari balai desa, bisa dipesan lewat keluarga" },
      { name: "Dari Kota Wonosobo", detail: "± 1 jam berkendara lewat Kejajar; jalan menanjak, berangkat lebih pagi karena kabut" },
    ] },
  },
});
