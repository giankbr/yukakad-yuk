import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Vania", groom: "Kelvin",
    brideFull: "Vania Prameswari Wijaya, S.Sn.", groomFull: "Kelvin Dharmawan Tanoto, S.Kom.",
    brideParents: "Putri bungsu dari\nBapak Hendra Wijaya & Ibu Lili Susanto", groomParents: "Putra pertama dari\nBapak Rudy Tanoto & Ibu Mei Ling Halim",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
    note: "Dua warna tinta, satu lembar kertas. Kadang meleset sedikit, tapi justru di situ bagusnya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-09T10:00:00+07:00",
  place: "Gudang Sarinah Ekosistem",
  address: "Jl. Pancoran Timur II No. 4, Pancoran, Jakarta Selatan",
  stories: [
    { date: "2020", title: "Zine Fair Pertama", body: "Vania menjual zine cetak risograf, Kelvin membeli tiga eksemplar dan lupa membayar satu." },
    { date: "2023", title: "Studio Dua Warna", body: "Kami membuka studio cetak kecil di Blok M. Mesinnya bekas, tintanya merah muda dan biru." },
    { date: "2026", title: "Lamaran di Percetakan", body: "Kelvin mencetak satu lembar bertuliskan \"Mau?\" Registrasinya meleset, jawabannya tetap iya." },
  ],
  events: [
    { name: "Pemberkatan Pernikahan", date: "2027-10-09T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Vihara Ekayana Arama", address: "Jl. Mangga II No. 8, Duri Kepa, Kebon Jeruk, Jakarta Barat" },
    { name: "Resepsi", date: "2027-10-09T18:00:00+07:00", time: "18.00 – 21.30 WIB", venue: "Gudang Sarinah Ekosistem", address: "Jl. Pancoran Timur II No. 4, Pancoran, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/r9.webp", "/themes/img/r82.webp", "/themes/img/r23.webp", "/themes/img/r85.webp", "/themes/img/r19.webp", "/themes/img/r88.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "2881 0457 63", account_name: "Vania Prameswari Wijaya" },
    { id: "demo-jago", type: "bank", bank_name: "Jago", account_number: "1023 4455 6677", account_name: "Kelvin Dharmawan Tanoto" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0817 7788 9900", account_name: "Kelvin Dharmawan" },
  ],
  guestName: "Sdr. Bimo Prasetyo & Partner",
  guestTable: "Meja C-12",
  extras: {
    quote: { text: "Jika suami dan istri ingin selalu bersama dalam kehidupan ini dan kehidupan mendatang, keduanya hendaknya memiliki keyakinan, moralitas, kemurahan hati, dan kebijaksanaan yang sepadan.", source: "Samajivina Sutta, Anguttara Nikaya 4.55" },
    rundown: { items: [
      { time: "18.00", title: "Open gate & pameran cetak", note: "Hall A" },
      { time: "18.45", title: "Kedatangan pengantin" },
      { time: "19.15", title: "Makan malam & DJ set" },
      { time: "20.30", title: "Sesi foto booth risograf", note: "Cetak langsung, bawa pulang" },
    ] },
    dressCode: { note: "Bebas rapi dengan aksen merah muda atau biru. Sneakers sangat dipersilakan.", colors: ["#ff48b0", "#0078bf", "#1d2a7a", "#f6f1e7"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendra Wijaya", "Kel. Besar Bpk. Rudy Tanoto"] },
    faq: { items: [
      { q: "Boleh membawa anak?", a: "Boleh, tersedia pojok mewarnai untuk anak-anak." },
      { q: "Apakah ada parkir?", a: "Parkir tersedia di area Gudang Sarinah, kapasitas terbatas. Disarankan naik transportasi daring." },
    ] },
  },
});
