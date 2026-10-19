import { makeDemo } from "../demo-base";

// Batak Toba (Kristen): martumpol → pemberkatan nikah di gereja → ulaon unjuk (pesta adat) di gedung.
export const demo = makeDemo({
  couple: {
    bride: "Rotua", groom: "Daniel",
    brideFull: "Rotua Grace br. Simanjuntak, S.E.", groomFull: "Daniel Parulian Sitorus, S.Kom.",
    brideParents: "Putri dari\nBapak St. Jonggi Simanjuntak & Ibu Rosmawati br. Hutabarat", groomParents: "Putra dari\nBapak Marihot Sitorus & Ibu Tiurma br. Siregar",
    note: "Dua marga, satu ikatan dalam kasih Tuhan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T09:00:00+07:00",
  place: "Gedung Sopo Godang Pardamean",
  address: "Jl. Sisingamangaraja No. 112, Medan Amplas, Kota Medan",
  stories: [
    { date: "2018", title: "Jumpa di Koor Naposo", body: "Bertemu di paduan suara Naposobulung gereja. Rotua di suara sopran, Daniel di tenor yang selalu salah masuk." },
    { date: "2021", title: "Martandang", body: "Daniel memberanikan diri bertandang ke rumah keluarga Simanjuntak, membawa kue lapet buatan inangnya." },
    { date: "2026", title: "Marhusip & Marhata Sinamot", body: "Kedua keluarga besar duduk bersama dalam Dalihan Na Tolu, bermusyawarah hingga sepakat melangkah ke pesta." },
  ],
  events: [
    { name: "Martumpol", date: "2027-06-26T10:00:00+07:00", time: "10.00 – 12.00 WIB", venue: "Gereja HKBP Pardamean", address: "Jl. Sisingamangaraja No. 88, Medan Amplas, Kota Medan" },
    { name: "Pemberkatan Nikah", date: "2027-07-10T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Gereja HKBP Pardamean", address: "Jl. Sisingamangaraja No. 88, Medan Amplas, Kota Medan" },
    { name: "Ulaon Unjuk (Pesta Adat)", date: "2027-07-10T11:30:00+07:00", time: "11.30 WIB – selesai", venue: "Gedung Sopo Godang Pardamean", address: "Jl. Sisingamangaraja No. 112, Medan Amplas, Kota Medan" },
  ],
  gallery: ["/themes/img/a33.webp", "/themes/img/r81.webp", "/themes/img/a125.webp", "/themes/img/a116.webp", "/themes/img/r1.webp", "/themes/img/a111.webp", "/themes/img/r8.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0812 3456 78", account_name: "Rotua Grace Simanjuntak" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "8420 1199 33", account_name: "Daniel Parulian Sitorus" },
    { id: "demo-kado", type: "address", address: "Jl. Karya Wisata No. 21, Medan Johor, Kota Medan 20144" },
  ],
  guestName: "Bapak J. Hutagalung & Keluarga",
  guestTable: "Meja Hula-hula",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "11.30", title: "Kedatangan rombongan", note: "Hula-hula, dongan tubu & boru" },
      { time: "12.30", title: "Makan bersama", note: "Pembagian jambar menurut adat" },
      { time: "14.00", title: "Mangulosi", note: "Penyerahan ulos kepada pengantin" },
      { time: "16.30", title: "Tortor & doa penutup" },
    ] },
    dressCode: { note: "Nuansa merah, hitam, dan putih. Silakan mengenakan ulos atau sortali.", colors: ["#b3261e", "#15100e", "#f4efe6", "#7a1616"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-10T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Keluarga Besar Simanjuntak", "Keluarga Besar Sitorus", "Hula-hula Hutabarat & Siregar", "Punguan Naposobulung HKBP Pardamean"] },
    travel: { note: "Untuk keluarga dari luar kota, berikut pilihan terdekat dari gedung.", items: [
      { name: "Hotel Grand Kanaya", detail: "± 3 km dari gedung" },
      { name: "Parkir gedung", detail: "Tersedia untuk ± 150 mobil, ada petugas parkir" },
    ] },
    faq: { items: [
      { q: "Apakah tamu wajib membawa ulos?", a: "Tidak wajib. Ulos dibawa oleh pihak hula-hula sesuai adat; tamu umum cukup hadir dan memberi doa restu." },
      { q: "Jam berapa sebaiknya datang ke ulaon unjuk?", a: "Rombongan keluarga diharapkan hadir pukul 11.30 WIB agar dapat mengikuti seluruh rangkaian adat." },
    ] },
  },
});
