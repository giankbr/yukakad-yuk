import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nayla", groom: "Fikri",
    note: "Kami ingin cinta yang teduh seperti taman: tumbuh pelan, berakar dalam, dan selalu hijau.",
    brideFull: "Nayla Azzahra Rahmani, S.Farm.", groomFull: "Muhammad Fikri Ramadhan, S.Kom.",
    brideParents: "Putri pertama dari\nBapak Ahmad Rahmani & Ibu Siti Nurhaliza",
    groomParents: "Putra ketiga dari\nBapak Yusuf Hamdani & Ibu Aisyah Fitriani",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-04-24T08:30:00+07:00",
  place: "Taman Sari Garden Hall",
  address: "Jl. Raya Puncak Km. 82, Cisarua, Bogor",
  stories: [
    { date: "2020", title: "Relawan Hijau", body: "Bertemu di kegiatan menanam pohon di Kebun Raya. Fikri salah menanam bibit di petak milik Nayla." },
    { date: "2023", title: "Ta'aruf", body: "Setelah lama berteman, Fikri memberanikan diri berkenalan secara serius melalui keluarga." },
    { date: "2026", title: "Khitbah", body: "Lamaran sederhana di teras rumah Nayla, ditemani teh hangat dan rangkaian eukaliptus." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-24T08:30:00+07:00", time: "08.30 – 10.00 WIB", venue: "Masjid At-Taawun Puncak", address: "Jl. Raya Puncak, Tugu Utara, Cisarua, Bogor" },
    { name: "Garden Party", date: "2027-04-24T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Taman Sari Garden Hall", address: "Jl. Raya Puncak Km. 82, Cisarua, Bogor" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/a116.webp", "/themes/img/r75.webp", "/themes/img/r1.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Nayla Azzahra Rahmani" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0813 1122 3344", account_name: "Muhammad Fikri" },
    { id: "demo-kado", type: "address", address: "Perumahan Bukit Hijau Blok C2 No. 7, Ciawi, Bogor 16720" },
  ],
  guestName: "Bapak Rudi Hartono & Keluarga",
});
