import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Damar",
    note: "Dengan penuh rasa syukur, kami memohon doa restu di usia tujuh bulan kandungan anak pertama kami.",
    brideFull: "Sekar Ayuningtyas, S.Pd.", groomFull: "Damar Wicaksono, S.T.",
    brideParents: "Putri dari Bapak Suryo Hadi & Ibu Sri Wahyuni",
    groomParents: "Putra dari Bapak Bambang Sutejo & Ibu Endah Purwani",
  },
  eventLabel: "Syukuran Tujuh Bulanan",
  date: "2027-05-16T09:00:00+07:00",
  place: "Ndalem Keluarga Bapak Suryo Hadi",
  address: "Jl. Mondorakan No. 21, Prenggan, Kotagede, Yogyakarta",
  story: { title: "Menanti buah hati", body: "" },
  stories: [
    { date: "Juni 2025", title: "Ijab kabul", body: "Kami memulai hidup baru di Kotagede, di rumah kecil dekat pasar." },
    { date: "Oktober 2026", title: "Kabar bahagia", body: "Dua garis yang membuat kami menangis haru. Bapak dan Ibu langsung sujud syukur." },
    { date: "Mei 2027", title: "Tujuh bulan", body: "Si kecil makin aktif menendang setiap kali mendengar suara ayahnya mengaji." },
  ],
  events: [
    { name: "Pengajian & Doa Bersama", date: "2027-05-16T09:00:00+07:00", time: "09.00 – 10.15 WIB", venue: "Ndalem Keluarga Bapak Suryo Hadi", address: "Jl. Mondorakan No. 21, Prenggan, Kotagede, Yogyakarta" },
    { name: "Siraman & Brojolan", date: "2027-05-16T10:30:00+07:00", time: "10.30 – 12.30 WIB", venue: "Pendapa & taman belakang", address: "Jl. Mondorakan No. 21, Prenggan, Kotagede, Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0812 3456 78", account_name: "Sekar Ayuningtyas" },
    { id: "demo-kado", type: "address", address: "Jl. Mondorakan No. 21, Prenggan, Kotagede, Yogyakarta 55172" },
  ],
  guestName: "Ibu Hj. Siti Aminah & Keluarga",
  guestTable: "",
  extras: {
    rundown: { items: [
      { time: "09.00", title: "Pembukaan & tilawah", note: "QS. Maryam & QS. Yusuf" },
      { time: "09.30", title: "Tausiyah & doa untuk ibu dan bayi" },
      { time: "10.30", title: "Siraman oleh tujuh sesepuh" },
      { time: "11.30", title: "Brojolan, ganti busana & dodol rujak" },
    ] },
    dressCode: { note: "Kebaya atau batik bernuansa pastel.", colors: ["#f4e1dc", "#c8707a", "#b8c26a", "#fbf6ee"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut mengundang", names: ["Keluarga Besar Bapak Suryo Hadi", "Keluarga Besar Bapak Bambang Sutejo", "Ibu-ibu pengajian Al-Hidayah Prenggan"] },
    faq: { items: [
      { q: "Apakah tamu pria boleh mengikuti siraman?", a: "Siraman dilakukan oleh sesepuh perempuan. Tamu pria dipersilakan menunggu di pendapa sambil menikmati hidangan." },
      { q: "Apa itu dodol rujak?", a: "Calon ibu ‘berjualan’ rujak dan dawet yang dibayar dengan kreweng, sebagai harapan rezeki yang lancar." },
    ] },
  },
});
