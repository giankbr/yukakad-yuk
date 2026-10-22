import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rini", groom: "Asep",
    brideFull: "Rini Nurhasanah, S.Pd.", groomFull: "Asep Saepul Rohman, S.T.",
    brideParents: "Putri bungsu dari\nBapak H. Dadang Suherman & Ibu Hj. Euis Kurniasih", groomParents: "Putra sulung dari\nBapak Ujang Rohmana & Ibu Iis Rosmiati",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r4.webp",
    note: "Sauyunan, sabilulungan: dua keluarga dipersatukan, saling menjaga dalam suka dan duka.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T08:00:00+07:00",
  place: "Gedung Sabilulungan",
  address: "Jl. Raya Soreang No. 17, Soreang, Kabupaten Bandung",
  story: { title: "Carita Urang", body: "" },
  stories: [
    { date: "2020", title: "Pinanggih di Garut", body: "Bertemu dalam kegiatan pengabdian masyarakat di sebuah desa di kaki Gunung Cikuray." },
    { date: "2023", title: "Ngalamar", body: "Diantar keluarga besar, Asep datang ke Tasikmalaya untuk meminang Rini secara adat." },
    { date: "2027", title: "Ngahiji", body: "Bismillah, kami memulai rumah tangga di tanah Priangan dengan doa restu para sesepuh." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Al-Fathu Soreang", address: "Jl. Alun-Alun Utara, Soreang, Kabupaten Bandung" },
    { name: "Upacara Adat & Sawer", date: "2027-08-14T10:00:00+07:00", time: "10.00 – 11.00 WIB", venue: "Gedung Sabilulungan", address: "Jl. Raya Soreang No. 17, Soreang, Kabupaten Bandung" },
    { name: "Resepsi", date: "2027-08-14T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Sabilulungan", address: "Jl. Raya Soreang No. 17, Soreang, Kabupaten Bandung" },
  ],
  gallery: ["/themes/img/a64.webp", "/themes/img/a116.webp", "/themes/img/r3.webp", "/themes/img/r4.webp", "/themes/img/r29.webp"],
  gifts: [
    { id: "demo-bjb", type: "bank", bank_name: "BJB", account_number: "0071 2345 6780", account_name: "Rini Nurhasanah" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4560 98", account_name: "Asep Saepul Rohman" },
    { id: "demo-kado", type: "address", address: "Kp. Babakan Sukamanah RT 03/05, Sukaresik, Kabupaten Tasikmalaya 46418" },
  ],
  guestName: "Bapak Ujang Suryana & Keluarga",
  guestTable: "Saung 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "10.00", title: "Mapag panganten", note: "Diiringi kacapi suling & tari payung" },
      { time: "10.20", title: "Sawer panganten", note: "Nasihat dalam tembang, taburan beras kuning & koin" },
      { time: "10.40", title: "Nincak endog & buka pintu" },
      { time: "11.00", title: "Resepsi & ramah tamah" },
    ] },
    dressCode: { note: "Kebaya atau batik bernuansa hangat: cokelat bambu, hijau sawah, dan kuning padi.", colors: ["#6b3f24", "#8fa53e", "#d9a944", "#efe2c4"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Dadang Suherman (Tasikmalaya)", "Kel. Besar Ujang Rohmana (Garut)"] },
    travel: { note: "Untuk tamu dari luar kota, berikut beberapa pilihan di sekitar Soreang.", items: [
      { name: "Penginapan di Soreang", detail: "± 1 km dari gedung, dekat gerbang Tol Soroja" },
      { name: "Parkir", detail: "Halaman gedung & lapangan sebelah, dijaga petugas" },
    ] },
  },
});
