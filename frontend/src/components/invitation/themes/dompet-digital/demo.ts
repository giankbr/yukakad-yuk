import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nisa", groom: "Fajar",
    brideFull: "Nisa Amalia", groomFull: "Fajar Nugraha",
    brideParents: "Putri Bapak Hasan & Ibu Lela", groomParents: "Putra Bapak Nug & Ibu Watik",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Aku transfer hatiku, saldonya tak akan habis",
  },
  eventLabel: "Pernikahan",
  date: "2028-02-20T08:00:00+07:00",
  place: "Dyandra Convention",
  address: "Surabaya",
  stories: [
    { title: "Transfer masuk", date: "2021", body: "Perkenalan di kajian kampus" },
    { title: "Top up komitmen", date: "2023", body: "Resmi serius, direstui dua keluarga" },
    { title: "Pembayaran mahar", date: "2027", body: "Lamaran diterima, cincin terpasang" },
  ],
  events: [
    { name: "Akad Nikah", date: "2028-02-20T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Al-Akbar", address: "Surabaya" },
    { name: "Resepsi", date: "2028-02-20T11:30:00+07:00", time: "11.30 – 14.30 WIB", venue: "Dyandra Convention", address: "Surabaya" },
  ],
  gallery: ["/themes/img/r59.webp", "/themes/img/r77.webp", "/themes/img/r74.webp"],
  gifts: [{ id: "demo-ewallet", type: "ewallet", ewallet_provider: "Dompet Cinta", ewallet_number: "0812 2002 2028", account_name: "Nisa Amalia" }],
  guestName: "Ibu Farida Hasan & Keluarga",
});
