import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Danang",
    brideFull: "Sekar Arum Wulandari, S.E.", groomFull: "Danang Setyo Aji, S.H.",
    brideParents: "Putri ketiga dari\nBapak H. Mulyono & Ibu Hj. Sumarni", groomParents: "Putra pertama dari\nBapak Slamet Riyadi & Ibu Tutik Handayani",
    bridePhoto: "/themes/img/a36.webp", groomPhoto: "/themes/img/a35.webp",
    note: "Kawula namung saderma, mugi Gusti paring margi — kami hanya berusaha, semoga Tuhan memberi jalan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T10:00:00+07:00",
  place: "Pendopo Rumah Joglo Kotagede",
  address: "Jl. Mondorakan No. 28, Prenggan, Kotagede, Yogyakarta",
  stories: [
    { date: "2017", title: "Satu Kampung", body: "Tumbuh di gang yang sama di Kotagede, kami baru benar-benar saling mengenal saat reuni sekolah." },
    { date: "2021", title: "Merintis Bersama", body: "Danang membuka kantor kecil, Sekar mengelola usaha perak keluarga. Kami belajar saling menopang." },
    { date: "2026", title: "Peningsetan", body: "Keluarga Danang datang membawa peningset, tanda ikatan yang kami jaga sampai hari ini." },
  ],
  events: [
    { name: "Ijab Kabul", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.00 WIB", venue: "Masjid Gedhe Mataram Kotagede", address: "Jl. Watu Gilang, Jagalan, Banguntapan, Bantul" },
    { name: "Panggih & Resepsi", date: "2027-08-14T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Pendopo Rumah Joglo Kotagede", address: "Jl. Mondorakan No. 28, Prenggan, Kotagede, Yogyakarta" },
  ],
  gallery: ["/themes/img/a46.webp", "/themes/img/a24.webp", "/themes/img/a36.webp", "/themes/img/a35.webp", "/themes/img/a34.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0029 0101 2345 507", account_name: "Sekar Arum Wulandari" },
    { id: "demo-kado", type: "address", address: "Jl. Mondorakan No. 28, Prenggan, Kotagede, Yogyakarta 55172" },
  ],
  guestName: "Bapak Wahyu Nugroho & Keluarga",
  extras: {
    rundown: { items: [
      { time: "10.00", title: "Kirab & panggih", note: "Balangan gantal, ngidak tigan, kacar-kucur" },
      { time: "11.00", title: "Sungkeman" },
      { time: "11.30", title: "Resepsi & kembul bujana" },
    ] },
    dressCode: { note: "Nuansa sogan, krem, dan emas tembaga. Batik parang atau sidomukti dipersilakan.", colors: ["#7a5230", "#f5eee2", "#b88a4a", "#4a2f19"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. H. Mulyono", "Kel. Besar Bpk. Slamet Riyadi", "Paguyuban Perajin Perak Kotagede"] },
  },
});
