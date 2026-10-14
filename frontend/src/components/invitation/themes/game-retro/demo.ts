import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Dina", groom: "Rama",
    brideFull: "Dina Puspita", groomFull: "Rama Wicaksono",
    brideParents: "Putri Bpk. Santoso & Ibu Erna", groomParents: "Putra Bpk. Wawan & Ibu Tutik",
    bridePhoto: "/themes/img/r46.webp", groomPhoto: "/themes/img/r47.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-12-05T08:00:00+07:00",
  place: "Graha Cakrawala",
  address: "Malang",
  stories: [
    { title: "Warnet Dekat Kampus", date: "2018", body: "pertemuan pertama, rebutan PC gaming" },
    { title: "CO-OP MODE", date: "2021", body: "resmi jadi duo permanen" },
    { title: "BOSS: RESTU ORTU", date: "2025", body: "CLEARED! dengan skor sempurna" },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-12-05T08:00:00+07:00", time: "08.00 WIB", venue: "Masjid Jami Malang" },
    { name: "Resepsi", date: "2027-12-05T18:00:00+07:00", time: "18.00 WIB", venue: "Graha Cakrawala", address: "Malang" },
  ],
  gallery: ["/themes/img/r49.webp", "/themes/img/r50.webp", "/themes/img/r48.webp"],
  gifts: [{ id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0512 2027 99", account_name: "Dina Puspita" }],
  guestName: "Keluarga Bapak Hari Santoso",
});
