import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ana", groom: "Yosua",
    brideFull: "Rambu Ana Kahi Ndapamuri, S.Pd.", groomFull: "Umbu Yosua Hina Lado, S.H.",
    brideParents: "Putri kedua dari\nBapak Umbu Ndjaka Pakareti & Ibu Rambu Margaretha Lunggi", groomParents: "Putra sulung dari\nBapak Pdt. Daniel Lado Bili & Ibu Yuliana Mete",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r29.webp",
    note: "Seperti benang lungsin dan pakan pada sehelai hinggi, kami ditenun menjadi satu oleh kasih-Nya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T10:00:00+08:00",
  place: "GKS Payeti",
  address: "Jl. Adam Malik, Kambajawa, Kota Waingapu, Sumba Timur",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2019", title: "Bertemu di Waingapu", body: "Kami berkenalan dalam pelayanan pemuda gereja menjelang Natal di Waingapu." },
    { date: "2022", title: "Melintasi Sabana", body: "Perjalanan Waikabubak–Waingapu jadi rute rutin, menyusuri bukit-bukit sabana yang menguning." },
    { date: "2027", title: "Satu Rumah", body: "Dengan restu kedua keluarga dan berkat Tuhan, kami melangkah ke dalam pernikahan kudus." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-09-18T10:00:00+08:00", time: "10.00 – 12.00 WITA", venue: "GKS Payeti", address: "Jl. Adam Malik, Kambajawa, Kota Waingapu, Sumba Timur" },
    { name: "Resepsi & Syukuran Keluarga", date: "2027-09-18T17:00:00+08:00", time: "17.00 – 21.00 WITA", venue: "Halaman Kediaman Keluarga Ndapamuri", address: "Kampung Prailiu, Kambera, Kabupaten Sumba Timur" },
  ],
  gallery: ["/themes/img/r104.webp", "/themes/img/r27.webp", "/themes/img/r29.webp", "/themes/img/r105.webp"],
  gifts: [
    { id: "demo-ntt", type: "bank", bank_name: "Bank NTT", account_number: "0342 0101 2345 67", account_name: "Rambu Ana Kahi Ndapamuri" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "4021 0100 7788 509", account_name: "Umbu Yosua Hina Lado" },
  ],
  guestName: "Bapak Yohanis Umbu Djama & Keluarga",
  guestTable: "Meja Kuda 3",
  extras: {
    quote: { text: "Dan di atas semuanya itu: kenakanlah kasih, sebagai pengikat yang mempersatukan dan menyempurnakan.", source: "Kolose 3:14" },
    rundown: { items: [
      { time: "17.00", title: "Penyambutan tamu", note: "Diiringi gong dan tarian penyambutan" },
      { time: "17.45", title: "Ibadah syukur keluarga" },
      { time: "18.30", title: "Ramah tamah & makan malam" },
      { time: "19.30", title: "Tarian bersama" },
    ] },
    dressCode: { note: "Kain tenun ikat sangat dipersilakan. Nuansa merah kombu, biru nila, dan krem.", colors: ["#7d2f1e", "#28324d", "#c99a3e", "#ecdcbc"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T10:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Umbu Ndjaka Pakareti (Waingapu)", "Kel. Besar Pdt. Daniel Lado Bili (Waikabubak)"] },
    travel: { note: "Untuk tamu dari luar Sumba, berikut beberapa info perjalanan.", items: [
      { name: "Bandara Umbu Mehang Kunda", detail: "± 10 menit berkendara ke GKS Payeti" },
      { name: "Dari Waikabubak", detail: "± 3,5 jam perjalanan darat melalui jalur sabana" },
    ] },
  },
});
