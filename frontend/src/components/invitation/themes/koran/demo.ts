import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ayu", groom: "Teguh",
    brideFull: "Ayu Lestari", groomFull: "Teguh Prabowo",
    brideParents: "Putri Bpk. Lesmana & Ibu Harni. Dikenal sebagai redaktur rubrik kuliner.",
    groomParents: "Putra Bpk. Prabowo & Ibu Siti. Fotografer lapangan harian ini.",
    bridePhoto: "/themes/img/r53.webp", groomPhoto: "/themes/img/r52.webp",
  },
  eventLabel: "Pernikahan",
  date: "2028-01-16T08:00:00+07:00",
  place: "Gedung Marabunta",
  address: "Kota Lama, Semarang",
  stories: [
    { title: "Dua Jurnalis Muda Saling Lirik di Ruang Redaksi", date: "2020", body: "rubrik gosip kantor" },
    { title: "Resmi! Liputan Berdua Berujung Jadian", date: "2023", body: "headline minggu itu" },
    { title: "Teguh Berlutut di Simpang Lima", date: "2027", body: "tiras terjual habis" },
  ],
  events: [
    { name: "Akad Nikah", date: "2028-01-16T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Agung Jawa Tengah" },
    { name: "Resepsi", date: "2028-01-16T11:30:00+07:00", time: "11.30 – 14.30 WIB", venue: "Gedung Marabunta", address: "Kota Lama" },
  ],
  gallery: ["/themes/img/r51.webp", "/themes/img/r54.webp", "/themes/img/r55.webp", "/themes/img/r56.webp"],
  gifts: [{ id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "1601 2028 55", account_name: "Ayu Lestari" }],
  guestName: "Bapak Bambang Wijaya & Keluarga",
});
