import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Arkan", groom: "",
    brideFull: "Muhammad Arkan Al-Fatih",
    brideParents: "Putra pertama dari Bapak Fajar Ramadhan & Ibu Siti Aisyah Putri",
    note: "Pangeran kecil kami siap melangkah menjadi anak saleh yang gagah dan berani dalam kebaikan.",
  },
  eventLabel: "Khitanan",
  date: "2027-06-27T09:00:00+07:00",
  place: "Kediaman Bapak Fajar Ramadhan",
  address: "Jl. Merpati Raya No. 14, Pancoran Mas, Kota Depok",
  story: { title: "", body: "" },
  stories: [
    { date: "2020", title: "Pangeran kecil lahir", body: "Arkan lahir di pagi Jumat yang cerah, disambut azan dari ayahnya." },
    { date: "2024", title: "Hafal surat pendek", body: "Setiap habis Magrib Arkan setor hafalan pada Umi, dari Al-Fatihah sampai An-Nas." },
    { date: "2027", title: "Tujuh tahun & berani", body: "Sekarang Arkan sudah kelas satu SD, rajin salat berjamaah, dan siap dikhitan." },
  ],
  events: [
    { name: "Pengajian & Doa Bersama", date: "2027-06-26T19:30:00+07:00", time: "Ba'da Isya · 19.30 WIB", venue: "Musala Al-Ikhlas", address: "Jl. Merpati Raya No. 2, Pancoran Mas, Kota Depok" },
    { name: "Tasyakuran Khitanan Arkan", date: "2027-06-27T09:00:00+07:00", time: "09.00 – 13.00 WIB", venue: "Kediaman Bapak Fajar Ramadhan", address: "Jl. Merpati Raya No. 14, Pancoran Mas, Kota Depok" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7140 2288 51", account_name: "Siti Aisyah Putri" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0857 1122 3344", account_name: "Fajar Ramadhan" },
  ],
  guestName: "Om Rizal & Keluarga",
  guestTable: "",
  extras: {
    child: {
      name: "Muhammad Arkan Al-Fatih",
      nickname: "Arkan",
      birthDate: "2020-03-13",
      meaning: "Arkan berarti tiang yang kokoh, Al-Fatih berarti sang pembuka kebaikan. Semoga Arkan tumbuh kokoh imannya dan menjadi pembuka jalan kebaikan bagi banyak orang.",
      parents: "Putra pertama dari Bapak Fajar Ramadhan & Ibu Siti Aisyah Putri",
    },
    quote: { text: "Ya Allah, jadikanlah anak kami anak yang saleh, berbakti kepada kedua orang tua, cinta kepada Al-Qur'an, dan bermanfaat bagi sesama.", source: "Doa ayah & bunda" },
    rundown: { items: [
      { time: "09.00", title: "Pembukaan & tilawah Al-Qur'an" },
      { time: "09.30", title: "Tausiyah singkat & doa untuk Arkan" },
      { time: "10.30", title: "Makan bersama", note: "Nasi kebuli & es buah" },
      { time: "11.30", title: "Panggung dongeng & lomba anak", note: "Hadiah mahkota untuk teman-teman Arkan" },
    ] },
    dressCode: { note: "Nuansa kerajaan: biru, emas, dan putih. Teman-teman boleh memakai mahkota atau kopiah terbaiknya!", colors: ["#2f5cc4", "#d9a93f", "#fbf1dc", "#163584"] },
    guestPass: {},
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Ramadhan", "Kakek & Nenek Hasanuddin", "Adik Kayla (adik Arkan)"] },
    wishlist: { note: "Doa teman-teman adalah hadiah terbaik untuk Arkan. Kalau ingin memberi, ini kesukaannya.", items: [
      { id: "w1", name: "Buku kisah para nabi bergambar", price: "± Rp85.000" },
      { id: "w2", name: "Sarung & kopiah anak", price: "± Rp120.000", claimed_by: "Tante Nisa" },
      { id: "w3", name: "Set lego istana", price: "± Rp250.000" },
    ] },
    faq: { items: [
      { q: "Apakah Arkan bisa ditemui?", a: "Insyaallah Arkan menyapa tamu dari kursi pangerannya sambil beristirahat." },
      { q: "Ada acara untuk anak-anak?", a: "Ada panggung dongeng dan lomba mewarnai istana mulai pukul 11.30." },
    ] },
  },
});
