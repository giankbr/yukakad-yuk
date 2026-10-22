import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hadi Prasetyo", groom: "Rahmawati",
    brideFull: "H. Hadi Prasetyo, S.E.", groomFull: "Hj. Rahmawati Sukardi",
    brideParents: "Bersama putra-putri: Dimas, Laras & Fajar", groomParents: "Bersama menantu dan cucu-cucu tercinta",
    note: "Selepas sebulan berpuasa, mari kita bertemu, bersalaman dan saling memaafkan sambil menikmati ketupat opor buatan Ibu.",
  },
  eventLabel: "Halal Bihalal",
  date: "2027-03-21T10:00:00+07:00",
  place: "Kediaman Keluarga Bapak H. Hadi Prasetyo",
  address: "Jl. Sompok Lama No. 27, Lamper Kidul, Semarang Selatan, Kota Semarang",
  story: { title: "Kabar Keluarga", body: "" },
  stories: [
    { date: "Juli 2026", title: "Laras diwisuda", body: "Laras menyelesaikan kuliah keperawatannya di Undip dan kini bertugas di RSUP Kariadi." },
    { date: "Oktober 2026", title: "Fajar menikah", body: "Keluarga bertambah: Fajar dan Annisa melangsungkan akad nikah di Kudus." },
    { date: "Januari 2027", title: "Cucu kedua lahir", body: "Alhamdulillah, Dimas dan Mira dikaruniai putri kecil bernama Khaira." },
  ],
  events: [
    { name: "Halal Bihalal & Silaturahmi", date: "2027-03-21T10:00:00+07:00", time: "10.00 – 12.00 WIB", venue: "Kediaman Keluarga Bapak H. Hadi Prasetyo", address: "Jl. Sompok Lama No. 27, Lamper Kidul, Semarang Selatan, Kota Semarang" },
    { name: "Makan Ketupat Bersama", date: "2027-03-21T12:00:00+07:00", time: "12.00 – 14.00 WIB", venue: "Halaman Belakang Rumah", address: "Jl. Sompok Lama No. 27, Lamper Kidul, Semarang Selatan, Kota Semarang" },
  ],
  gallery: [],
  gifts: [],
  guestName: "Keluarga Om Bambang & Tante Sari",
  guestTable: "",
  extras: {
    quote: { text: "(Yaitu) orang yang berinfak, baik di waktu lapang maupun sempit, dan orang-orang yang menahan amarahnya dan memaafkan (kesalahan) orang lain. Dan Allah mencintai orang yang berbuat kebaikan.", source: "QS. Ali 'Imran: 134" },
    rundown: { items: [
      { time: "10.00", title: "Pembukaan & sambutan tuan rumah" },
      { time: "10.20", title: "Tausiyah halal bihalal", note: "Ustaz H. Mahfud" },
      { time: "11.00", title: "Saling bersalaman & bermaafan" },
      { time: "12.00", title: "Makan ketupat, opor & sambal goreng ati" },
      { time: "13.15", title: "Foto keluarga besar" },
    ] },
    dressCode: { note: "Baju koko atau gamis bernuansa hijau daun dan kuning janur.", colors: ["#2f6b3a", "#7fae5a", "#f2c14e", "#fbf5e2"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut mengundang", names: ["Keluarga Dimas & Mira", "Laras Prasetyo", "Keluarga Fajar & Annisa"] },
    faq: { items: [
      { q: "Apakah ada tempat parkir?", a: "Parkir mobil di lapangan RT 05, sekitar 50 meter dari rumah. Motor bisa di halaman depan." },
      { q: "Boleh membawa anak-anak?", a: "Tentu, justru ramai. Ada sudut bermain kecil di teras samping." },
    ] },
  },
});
