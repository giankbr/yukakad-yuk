import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laras", groom: "Bayu",
    brideFull: "Larasati Wulandari, S.Pd.", groomFull: "Bayu Aji Prasetyo, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Darsono & Ibu Hj. Tuminah", groomParents: "Putra sulung dari\nBapak Slamet Riyadi & Ibu Kasmiyati",
    bridePhoto: "/themes/img/a36.webp", groomPhoto: "/themes/img/a35.webp",
    note: "Cablaka, apa anane: kami berjanji saling jujur, seperti air Serayu yang jernih mengalir dari lereng Slamet.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-07T08:00:00+07:00",
  place: "Pendapa Si Panji",
  address: "Kompleks Alun-alun Purwokerto, Jl. Masjid, Sokanegara, Purwokerto Timur, Banyumas",
  stories: [
    { date: "2020", title: "KKN di Lereng Slamet", body: "Kami satu kelompok KKN di Desa Ketenger, Baturraden. Bayu sibuk memperbaiki pipa air, Laras mengajar mengaji anak-anak desa." },
    { date: "2023", title: "Mendoan & Tempe Kemul", body: "Setelah lulus, kami sering bertemu di warung mendoan dekat alun-alun. Obrolan sederhana, tapi tak pernah ingin cepat selesai." },
    { date: "2026", title: "Lamaran", body: "Keluarga Bayu datang melamar dengan seserahan batik Banyumasan buatan perajin Sokaraja." },
    { date: "2027", title: "Loro Dadi Siji", body: "Dengan restu kedua keluarga, kami melangkah bersama di kota kelahiran kami, Purwokerto." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-07T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Baitussalam", address: "Jl. Masjid No. 1, Sokanegara, Purwokerto Timur, Banyumas" },
    { name: "Resepsi", date: "2027-08-07T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendapa Si Panji", address: "Kompleks Alun-alun Purwokerto, Jl. Masjid, Sokanegara, Purwokerto Timur, Banyumas" },
  ],
  gallery: ["/themes/img/a64.webp", "/themes/img/a33.webp", "/themes/img/a36.webp", "/themes/img/r102.webp", "/themes/img/a35.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0071 0102 3456 507", account_name: "Larasati Wulandari" },
    { id: "demo-kado", type: "address", address: "Jl. Gerilya Timur No. 27, Tanjung, Purwokerto Selatan, Banyumas 53144" },
  ],
  guestName: "Bapak Ahmad Tohari & Keluarga",
  guestTable: "Meja Serayu",
  extras: {
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin", note: "Diiringi calung Banyumasan" },
      { time: "11.30", title: "Sambutan keluarga & doa" },
      { time: "12.00", title: "Ramah tamah", note: "Mendoan hangat, sroto Sokaraja, dan getuk goreng" },
      { time: "13.00", title: "Tari lengger & foto bersama" },
    ] },
    dressCode: { note: "Batik Banyumasan atau busana muslim. Warna sogan, hitam, dan krem dipersilakan.", colors: ["#7a4a24", "#1c1612", "#efe3c8", "#7d8a4e"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Darsono (Sokaraja)", "Kel. Besar Slamet Riyadi (Baturraden)"] },
  },
});
