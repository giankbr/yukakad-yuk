import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Amanda", groom: "Rizki",
    brideFull: "Amanda Puspita", groomFull: "Rizki Ananda",
    brideParents: "Putri Bapak Pupung & Ibu Sinta", groomParents: "Putra Bapak Anang & Ibu Yuli",
  },
  eventLabel: "Pernikahan",
  date: "2027-04-17T08:00:00+07:00",
  place: "Birawa Ballroom",
  address: "Jakarta",
  stories: [
    { title: "Scan pertama", date: "2019", body: "Bayar bareng di kantin — QRIS jadi mak comblang" },
    { title: "Saldo masuk", date: "2022", body: "Resmi pacaran, saling top up semangat" },
    { title: "Pembelian terbesar", date: "2026", body: "Cincin lamaran · cicilan lunas lebih cepat" },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-17T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Agung Sunda Kelapa" },
    { name: "Resepsi", date: "2027-04-17T11:30:00+07:00", time: "11.30 – 14.00 WIB", venue: "Birawa Ballroom", address: "Jakarta" },
  ],
  gallery: [
    "/themes/img/a22.webp",
    "/themes/img/a23.webp",
    "/themes/img/a25.webp",
  ],
  gifts: [{ id: "demo-qris", type: "ewallet", ewallet_provider: "QRIS", ewallet_number: "0812 1704 2027", account_name: "Amanda Puspita" }],
  guestName: "Bapak Hendri Saputra & Keluarga",
});
