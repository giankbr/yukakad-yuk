import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hasnah", groom: "Ardi",
    brideFull: "Sitti Hasnah Lamaridi", groomFull: "Ardiansyah Kasim, S.Pi.",
    brideParents: "Putri bungsu dari\nBapak H. Lamaridi & Ibu Hadijah", groomParents: "Putra kedua dari\nBapak Kasim & Ibu Nursia",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/a96.webp",
    note: "Laut tidak pernah memisahkan orang Bajo. Ia justru jalan pulang. Semoga rumah tangga kami seperti lepa: kokoh di atas ombak dan selalu tahu arah ke rumah.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-22T09:00:00+08:00",
  place: "Kampung Bajo Mola, Wakatobi",
  address: "Kel. Mola Selatan, Wangi-Wangi Selatan, Kabupaten Wakatobi, Sulawesi Tenggara",
  stories: [
    { date: "2019", title: "Satu Perahu ke Kaledupa", body: "Kami pertama bertemu di perahu penumpang dari Wanci ke Kaledupa. Ombak tinggi, tapi Ardi sibuk menenangkan kambing orang di sebelahnya." },
    { date: "2023", title: "Menjaga Karang", body: "Sama-sama menjadi relawan transplantasi karang di perairan Mola. Di antara rumah panggung, kami mulai sering pulang bersama." },
    { date: "2026", title: "Lamaran di Atas Air", body: "Keluarga Ardi datang dengan lepa yang dihias, membawa seserahan menyeberang ke rumah keluarga Hasnah." },
    { date: "2027", title: "Akad & Pesta Kampung", body: "Insyaallah kami menikah, disaksikan keluarga besar dan tetangga sekampung di atas laut." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Al-Bahri Mola", address: "Kampung Bajo Mola Selatan, Wangi-Wangi Selatan, Wakatobi" },
    { name: "Resepsi", date: "2027-05-22T13:00:00+08:00", time: "13.00 – 17.00 WITA", venue: "Kediaman Mempelai Wanita", address: "Jl. Titian Mola Raya No. 8, Mola Selatan, Wangi-Wangi Selatan, Wakatobi" },
  ],
  gallery: ["/themes/img/r110.webp", "/themes/img/r105.webp", "/themes/img/r38.webp", "/themes/img/a99.webp", "/themes/img/r109.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "3301 01 004512 50 9", account_name: "Sitti Hasnah Lamaridi" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 456 789", account_name: "Ardiansyah Kasim" },
  ],
  guestName: "Bapak La Ode Hamiru & Keluarga",
  guestTable: "Titian 2",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu cenderung dan merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "13.00", title: "Penjemputan tamu dengan perahu", note: "Dermaga Mola, setiap 15 menit" },
      { time: "13.30", title: "Doa & sambutan keluarga" },
      { time: "14.00", title: "Makan bersama", note: "Kasuami dan ikan bakar" },
      { time: "15.30", title: "Hiburan & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim santai yang sejuk. Putih, tosca, dan krem pasir dipersilakan.", colors: ["#f6f1e4", "#3fb2b0", "#1f5f6e", "#e8673f"] },
    rsvpDietary: {},
    guestPass: {},
    family: { names: ["Kel. Besar H. Lamaridi", "Kel. Besar Kasim"] },
  },
});
