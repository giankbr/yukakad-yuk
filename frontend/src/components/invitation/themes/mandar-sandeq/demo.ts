import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Dhila", groom: "Arsyad",
    brideFull: "Fadhilah Ramadhani, S.Pd.", groomFull: "Muh. Arsyad Ridwan, S.Pi.",
    brideParents: "Putri pertama dari\nBapak H. Abd. Hamid & Ibu Hj. St. Aminah", groomParents: "Putra kedua dari\nBapak Ridwan Saleh & Ibu Hasnawati",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Siwaliparri: suami dan istri saling bahu-membahu, seperti layar dan cadik sandeq yang bersama-sama menjaga perahu tetap melaju.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T09:00:00+08:00",
  place: "Gedung Assamalewuang, Majene",
  address: "Jl. Jend. Sudirman No. 30, Banggae, Kabupaten Majene, Sulawesi Barat",
  stories: [
    { date: "2018", title: "Sandeq Race", body: "Arsyad ikut menjadi awak sandeq dalam lomba dari Mamuju; Dhila meliput untuk buletin kampus di Pantai Majene." },
    { date: "2022", title: "Senja di Pantai Dato", body: "Kami belajar saling mengerti sambil menunggu perahu nelayan pulang, ditemani jepa dan ikan bakar." },
    { date: "2026", title: "Massulekka", body: "Keluarga Arsyad datang dari Polewali untuk melamar. Dua keluarga besar bermufakat dan menentukan hari baik." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Agung Majene", address: "Jl. Ahmad Yani, Pangali-ali, Banggae, Majene" },
    { name: "Resepsi", date: "2027-09-18T11:30:00+08:00", time: "11.30 – 15.00 WITA", venue: "Gedung Assamalewuang", address: "Jl. Jend. Sudirman No. 30, Banggae, Majene" },
    { name: "Resepsi Keluarga Pria", date: "2027-09-25T11:00:00+08:00", time: "11.00 – 14.00 WITA", venue: "Gedung Serbaguna Polewali", address: "Jl. Ahmad Yani No. 12, Pekkabata, Polewali Mandar" },
  ],
  gallery: ["/themes/img/r15.webp", "/themes/img/r3.webp", "/themes/img/r58.webp", "/themes/img/r109.webp", "/themes/img/r105.webp", "/themes/img/r16.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7234 5678 90", account_name: "Fadhilah Ramadhani" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0533 0100 9876 501", account_name: "Muh. Arsyad Ridwan" },
    { id: "demo-kado", type: "address", address: "Jl. Pelabuhan Lama No. 5, Labuang, Banggae Timur, Majene 91412" },
  ],
  guestName: "Bapak H. Muh. Yusuf & Keluarga",
  guestTable: "Meja Cadik 3",
  extras: {
    rundown: { items: [
      { time: "11.30", title: "Kedatangan pengantin", note: "Diiringi rebana dan kalindaqdaq" },
      { time: "12.00", title: "Sambutan keluarga & doa" },
      { time: "12.30", title: "Ramah tamah", note: "Bau peapi, jepa, dan kue tetu" },
    ] },
    dressCode: { note: "Busana muslim atau sarung sutra Mandar. Biru laut, marun, dan emas dipersilakan.", colors: ["#1d557f", "#7d1f2b", "#c99a3c", "#f7f0e2"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-09-18T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abd. Hamid (Majene)", "Kel. Besar Ridwan Saleh (Polewali Mandar)"] },
  },
});
