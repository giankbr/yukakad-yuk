import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rafa", groom: "",
    note: "Langkah kecil menjadi anak saleh yang mengikuti sunnah Nabi Ibrahim.",
    brideFull: "Muhammad Rafa Alfarizi",
    brideParents: "Putra kedua dari Bapak Hendra Gunawan & Ibu Sri Wahyuni",
  },
  eventLabel: "Khitanan",
  date: "2027-07-04T10:00:00+07:00",
  place: "Kediaman Bapak Hendra Gunawan",
  address: "Jl. Kenanga Raya No. 23, Bekasi Selatan, Kota Bekasi",
  story: { title: "", body: "" },
  events: [
    { name: "Pengajian & Doa Bersama", date: "2027-07-03T19:30:00+07:00", time: "Ba'da Isya · 19.30 WIB", venue: "Mushala Al-Barokah", address: "Jl. Kenanga Raya No. 2, Bekasi Selatan" },
    { name: "Tasyakuran Khitanan", date: "2027-07-04T10:00:00+07:00", time: "10.00 – 14.00 WIB", venue: "Kediaman Bapak Hendra Gunawan", address: "Jl. Kenanga Raya No. 23, Bekasi Selatan, Kota Bekasi" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank Mandiri", account_number: "167 000 8899 221", account_name: "Sri Wahyuni" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "ovo", ewallet_number: "0813 9988 7766", account_name: "Hendra Gunawan" },
  ],
  guestName: "Om Dimas & Keluarga",
  guestTable: "",
  extras: {
    child: {
      name: "Muhammad Rafa Alfarizi",
      nickname: "Rafa",
      birthDate: "2019-08-17",
      meaning: "Rafa berarti derajat yang tinggi, Alfarizi berarti sang penunggang kuda yang tangguh. Semoga Rafa tumbuh menjadi anak yang mulia akhlaknya dan berani dalam kebaikan.",
      parents: "Putra kedua dari Bapak Hendra Gunawan & Ibu Sri Wahyuni",
    },
    quote: { text: "Kemudian Kami wahyukan kepadamu (Muhammad), ‘Ikutilah agama Ibrahim yang lurus, dan dia bukanlah termasuk orang yang mempersekutukan Tuhan.’", source: "QS. An-Nahl: 123" },
    rundown: { items: [
      { time: "10.00", title: "Pembukaan & tilawah Al-Qur'an" },
      { time: "10.30", title: "Doa untuk Rafa" },
      { time: "11.00", title: "Makan siang bersama" },
      { time: "12.00", title: "Lomba & hiburan anak", note: "Ada hadiah untuk teman-teman Rafa" },
    ] },
    dressCode: { note: "Baju koko atau busana muslim warna cerah.", colors: ["#12a594", "#ffc93c", "#ff7a59", "#4cc3ff"] },
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bapak H. Sudirman", "Kel. Besar Bapak Wagiman", "Teman-teman TK Al-Hikmah"] },
    faq: { items: [
      { q: "Boleh membawa anak-anak?", a: "Boleh banget! Ada area bermain dan lomba seru untuk anak-anak." },
      { q: "Apakah tersedia parkir?", a: "Parkir motor di halaman, mobil di lapangan RW sebelah mushala." },
    ] },
  },
});
