import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Arkan", groom: "",
    brideFull: "Muhammad Arkan Wicaksono",
    brideParents: "Putra pertama dari Bapak Galih Wicaksono & Ibu Ratna Dewi Anggraini",
    note: "Mesin sudah panas, jalan sudah diratakan! Arkan genap empat tahun dan mengajak teman-teman membangun pesta paling seru.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-09-18T15:30:00+07:00",
  place: "Rumah Pasir Playground",
  address: "Jl. Raya Darmo Permai III No. 12, Pradahkalikendal, Dukuh Pakis, Surabaya",
  story: { title: "Cerita Arkan", body: "" },
  stories: [
    { date: "2023", title: "Si kecil datang", body: "Arkan lahir di pagi yang ramai, ditemani suara molen tetangga yang sedang membangun rumah." },
    { date: "2025", title: "Kata pertama: truk!", body: "Setiap lewat proyek jalan, Arkan berhenti dan melambai ke ekskavator kuning sampai operatornya membalas." },
    { date: "2026", title: "Masuk KB", body: "Di hari pertama sekolah, Arkan membawa truk mainan kesayangan dan langsung punya teman main pasir." },
    { date: "2027", title: "Empat tahun!", body: "Sekarang Arkan hafal nama semua alat berat dan bercita-cita membangun jembatan paling panjang." },
  ],
  events: [
    { name: "Pesta Proyek Ulang Tahun Arkan", date: "2027-09-18T15:30:00+07:00", time: "15.30 – 17.30 WIB", venue: "Rumah Pasir Playground", address: "Jl. Raya Darmo Permai III No. 12, Pradahkalikendal, Dukuh Pakis, Surabaya" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0812 4471 90", account_name: "Ratna Dewi Anggraini" },
    { id: "demo-kado", type: "address", address: "Jl. Bukit Darmo Golf Blok C2 No. 7, Dukuh Pakis, Surabaya 60226" },
  ],
  guestName: "Adik Kenzo & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Muhammad Arkan Wicaksono", nickname: "Arkan", birthDate: "2023-09-18T07:10:00+07:00", parents: "Putra pertama dari Bapak Galih Wicaksono & Ibu Ratna Dewi Anggraini" },
    rundown: { items: [
      { time: "15.30", title: "Absen pekerja cilik", note: "Ambil helm proyek & rompi" },
      { time: "15.50", title: "Gali harta karun di bak pasir" },
      { time: "16.30", title: "Lomba dorong truk & menyusun balok" },
      { time: "17.00", title: "Tiup lilin, potong kue & bagi bingkisan" },
    ] },
    dressCode: { note: "Kostum pekerja proyek! Kaos kuning, oranye, atau overall. Helm & rompi kami sediakan.", colors: ["#f5b819", "#f07c22", "#3a3b42", "#3b7fc4"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Uti Wicaksono", "Opa & Oma Anggraini", "Kak Naura (sepupu Arkan)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah paling seru. Kalau ingin memberi, ini yang sedang Arkan impikan.", items: [
      { id: "w1", name: "Set balok kayu konstruksi", price: "± Rp180.000" },
      { id: "w2", name: "Buku stiker alat berat", price: "± Rp60.000", claimed_by: "Tante Sinta" },
      { id: "w3", name: "Ekskavator remote control", price: "± Rp250.000" },
    ] },
    faq: { items: [
      { q: "Apakah anak boleh main pasir?", a: "Boleh sekali! Bawa baju ganti, ada area cuci tangan dan kaki." },
      { q: "Ada parkir?", a: "Parkir mobil tersedia di halaman Rumah Pasir dan sepanjang Darmo Permai III." },
    ] },
  },
});
