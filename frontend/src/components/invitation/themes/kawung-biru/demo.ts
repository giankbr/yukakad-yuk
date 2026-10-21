import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Anindya", groom: "Rakai",
    brideFull: "Anindya Kirana Putri, M.Ds.", groomFull: "Rakai Wisnu Pradipta, S.Kom.",
    brideParents: "Putri tunggal dari\nBapak Ir. Haryo Sasongko & Ibu Retno Palupi", groomParents: "Putra kedua dari\nBapak Bambang Wicaksono & Ibu Ratih Kusumastuti",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Seperti kawung yang tersusun rapi, semoga langkah kami selalu seimbang dan saling melengkapi.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-11T09:00:00+07:00",
  place: "Pendopo Agung Royal Ambarrukmo",
  address: "Jl. Laksda Adisucipto No. 81, Depok, Sleman, Yogyakarta",
  stories: [
    { date: "2019", title: "Satu Studio", body: "Bertemu di studio desain di Kotagede. Anindya menggambar motif, Rakai menyusun kodenya." },
    { date: "2023", title: "Pulang ke Jogja", body: "Setelah merantau, kami sama-sama memilih pulang dan membangun usaha kecil batik digital." },
    { date: "2026", title: "Lamaran", body: "Di bawah pendopo rumah Eyang, dua keluarga bersepakat menyatukan kami." },
  ],
  events: [
    { name: "Ijab Kabul", date: "2027-09-11T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Gedhe Kauman", address: "Jl. Kauman, Ngupasan, Gondomanan, Yogyakarta" },
    { name: "Upacara Panggih & Resepsi", date: "2027-09-11T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Pendopo Agung Royal Ambarrukmo", address: "Jl. Laksda Adisucipto No. 81, Depok, Sleman, Yogyakarta" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/a18.webp", "/themes/img/a31.webp", "/themes/img/a24.webp"],
  gifts: [
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "137 00 1234567 8", account_name: "Anindya Kirana Putri" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "ovo", ewallet_number: "0813 2900 1122", account_name: "Rakai Wisnu Pradipta" },
  ],
  guestName: "Ibu Dyah Ayu Lestari",
  extras: {
    dressCode: { note: "Nuansa biru, abu, dan putih. Batik kawung sangat dipersilakan.", colors: ["#2c3a5a", "#8fa0c6", "#eef2f6", "#56637a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Ir. Haryo Sasongko", "Kel. Besar Bpk. Bambang Wicaksono"] },
    travel: { note: "Untuk tamu dari luar kota, berikut beberapa pilihan terdekat dari lokasi.", items: [
      { name: "Bandara YIA", detail: "± 50 menit via tol / kereta bandara" },
      { name: "Stasiun Tugu", detail: "± 20 menit berkendara" },
    ] },
  },
});
