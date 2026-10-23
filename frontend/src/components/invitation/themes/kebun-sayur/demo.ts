import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Wulan", groom: "Bima",
    brideFull: "Wulan Sekar Arum, S.P.", groomFull: "Bima Aditya Nugraha, S.TP.",
    brideParents: "Putri bungsu dari\nBapak Slamet Riyadi & Ibu Endang Lestari", groomParents: "Putra pertama dari\nBapak Haryo Prasetyo & Ibu Dewi Anggraini",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
    note: "Yang ditanam dengan sabar akan dipanen dengan gembira. Kami menanam ini bersama, dan ingin memanennya bersama kalian.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T09:00:00+07:00",
  place: "Kebun Tumbuh Bersama",
  address: "Jl. Raya Selecta No. 12, Tulungrejo, Bumiaji, Kota Batu, Jawa Timur",
  stories: [
    { date: "Musim tanam 2022", title: "Satu Petak Kebun Kampus", body: "Kami kebagian petak bersebelahan di kebun percobaan. Wulan menanam bayam, Bima menanam tomat yang selalu dimakan burung." },
    { date: "2024", title: "Pasar Tani Minggu Pagi", body: "Berdua membuka lapak sayur organik di pasar tani Kota Batu. Pelanggan pertama kami: ibu-ibu senam pagi." },
    { date: "Panen 2027", title: "Ladang Sendiri", body: "Kami menyewa sepetak lahan di lereng Selecta, membangun bedeng, dan memutuskan untuk berkeluarga di tengahnya." },
  ],
  events: [
    { name: "Ikrar Pernikahan", date: "2027-08-21T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Rumah Keluarga Wulan", address: "Jl. Dewi Sartika Gg. 4 No. 9, Temas, Batu, Kota Batu" },
    { name: "Pesta Kebun & Makan Siang", date: "2027-08-21T11:30:00+07:00", time: "11.30 – 15.00 WIB", venue: "Kebun Tumbuh Bersama", address: "Jl. Raya Selecta No. 12, Tulungrejo, Bumiaji, Kota Batu, Jawa Timur" },
  ],
  gallery: ["/themes/img/r79.webp", "/themes/img/r25.webp", "/themes/img/r75.webp", "/themes/img/a26.webp", "/themes/img/r77.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0071 0102 4455 507", account_name: "Wulan Sekar Arum" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "GoPay", ewallet_number: "0812 3366 9014", account_name: "Bima Aditya Nugraha" },
    { id: "demo-kado", type: "address", address: "Jl. Raya Selecta No. 12, Tulungrejo, Bumiaji, Kota Batu 65336", account_name: "Wulan & Bima" },
  ],
  guestName: "Mbak Retno & Mas Agus",
  guestTable: "Meja Wortel 2",
  extras: {
    rundown: { items: [
      { time: "11.30", title: "Tur kebun singkat", note: "Petik sendiri selada dan tomat ceri" },
      { time: "12.00", title: "Makan siang di meja panjang", note: "Menu dari kebun dan petani tetangga" },
      { time: "13.30", title: "Lomba tebak berat labu" },
      { time: "14.30", title: "Bibit untuk dibawa pulang" },
    ] },
    dressCode: { note: "Santai rapi dan nyaman untuk rumput: hijau daun, krem, terakota, atau kuning jagung.", colors: ["#5f8f3a", "#efe2c4", "#c7704a", "#f1b62e"] },
    guestPass: {},
    rsvpDietary: { label: "Pantangan makanan / vegetarian (opsional)" },
    family: { names: ["Kel. Besar Slamet Riyadi", "Kel. Besar Haryo Prasetyo"] },
  },
});
