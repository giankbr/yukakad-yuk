import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Umar",
    note: "Menikah adalah ibadah terpanjang; kami memulainya dengan basmalah dan berharap Allah menuntun hingga akhir.",
    brideFull: "Aisyah Humaira", groomFull: "Umar Abdurrahman",
    brideParents: "Putri dari Bapak Ahmad Fauzi & Ibu Khairunnisa",
    groomParents: "Putra dari Bapak Abdul Karim & Ibu Maimunah",
  },
  eventLabel: "Pernikahan",
  date: "2027-03-27T08:00:00+07:00",
  place: "Masjid Jogokariyan",
  address: "Jl. Jogokaryan No. 36, Mantrijeron, Yogyakarta",
  stories: [
    { title: "Ta'aruf", date: "2025", body: "Dipertemukan melalui perantara ustadzah, berta'aruf dengan didampingi keluarga." },
    { title: "Khitbah", date: "2026", body: "Umar datang meminang bersama orang tuanya; kedua keluarga bersepakat dengan penuh syukur." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-03-27T08:00:00+07:00", time: "08.00 – 09.00 WIB", venue: "Masjid Jogokariyan", address: "Jl. Jogokaryan No. 36, Mantrijeron, Yogyakarta" },
    { name: "Walimah (terpisah ikhwan & akhwat)", date: "2027-03-27T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Aula Islamic Center Jogokariyan", address: "Jl. Jogokaryan No. 40, Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7209876543", account_name: "Umar Abdurrahman" },
    { id: "demo-kado", type: "address", address: "Jl. Parangtritis Km 3 No. 12, Sewon, Bantul" },
  ],
  guestName: "Bapak Ustadz Ridwan & Keluarga",
});
