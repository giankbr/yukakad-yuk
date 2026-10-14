import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Tami", groom: "Raka",
    note: "Dua repositori hidup, satu branch tujuan.\nSetelah 7 tahun development, siap untuk production.",
    brideFull: "Tami Lestari", groomFull: "Raka Wijaya",
    brideParents: "Putri Bapak Lesmana & Ibu Ani", groomParents: "Putra Bapak Wijaya & Ibu Sinta",
    bridePhoto: "/themes/img/a120.webp", groomPhoto: "/themes/img/a119.webp",
  },
  eventLabel: "Pernikahan",
  date: "2026-10-10T08:00:00+07:00",
  place: "The Hall, Senayan City",
  address: "Jl. Asia Afrika No. 19, Senayan, Jakarta",
  stories: [
    { title: "init: bertemu di bootcamp coding", date: "2019", body: "" },
    { title: "feat: resmi jadian setelah pair programming", date: "2021", body: "" },
    { title: "fix: LDR Jakarta–Singapura, uptime 100%", date: "2023", body: "" },
    { title: "feat!: lamaran diterima (breaking change)", date: "2025", body: "" },
  ],
  events: [
    { name: "Akad Nikah", date: "2026-10-10T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Sunda Kelapa", address: "Jl. Taman Sunda Kelapa No. 16, Menteng, Jakarta" },
    { name: "Resepsi", date: "2026-10-10T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "The Hall, Senayan City", address: "Jl. Asia Afrika No. 19, Senayan, Jakarta" },
  ],
  gallery: ["/themes/img/a121.webp", "/themes/img/a122.webp", "/themes/img/a124.webp", "/themes/img/a123.webp"],
  gifts: [{ id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1010 2026 77", account_name: "Tami Lestari" }],
  guestName: "Bapak Ir. Santoso & Keluarga",
});
