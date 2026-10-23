import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hana", groom: "Andre",
    brideFull: "Yohana Lestari Dohong, S.Pd.", groomFull: "Andreas Mantikei Saman, S.T.",
    brideParents: "Putri sulung dari\nBapak Simson Dohong & Ibu Rina Lambung",
    groomParents: "Putra ketiga dari\nBapak Daniel Saman & Ibu Elisabet Bungai",
    note: "Seperti batang garing yang berakar di bumi dan bertunas ke langit, kiranya rumah tangga kami tumbuh di dalam kasih-Nya.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-18T09:00:00+07:00",
  place: "Betang Hapakat",
  address: "Jl. RTA Milono Km. 1,5, Menteng, Kec. Jekan Raya, Palangka Raya, Kalimantan Tengah",
  stories: [
    { date: "2019", title: "Satu Perahu di Kahayan", body: "Kami bertemu dalam susur sungai Kahayan bersama pemuda gereja. Andre mendayung, Hana memotret, dan perahunya hampir terbalik karena kami terlalu banyak tertawa." },
    { date: "2023", title: "Tumbuh Bersama", body: "Hana mengajar di Kuala Kurun, Andre bekerja di Palangka Raya. Jarak empat jam perjalanan justru mengajarkan kami setia pada hal-hal kecil." },
    { date: "2026", title: "Hakumbang Auh", body: "Keluarga Andre datang menyampaikan maksud baik kepada keluarga Hana, dan kedua keluarga sepakat menuntun kami ke pelaminan." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-09-18T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "GKE Jemaat Imanuel Palangka Raya", address: "Jl. Jend. Sudirman No. 17, Langkai, Kec. Pahandut, Palangka Raya" },
    { name: "Upacara Adat & Resepsi", date: "2027-09-18T15:00:00+07:00", time: "15.00 – 20.00 WIB", venue: "Betang Hapakat", address: "Jl. RTA Milono Km. 1,5, Menteng, Kec. Jekan Raya, Palangka Raya" },
  ],
  gallery: ["/themes/img/r108.webp", "/themes/img/a116.webp", "/themes/img/r110.webp"],
  gifts: [
    { id: "demo-kalteng", type: "bank", bank_name: "Bank Kalteng", account_number: "0203 4411 7820", account_name: "Yohana Lestari Dohong" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0451 0102 3399 507", account_name: "Andreas Mantikei Saman" },
    { id: "demo-kado", type: "address", address: "Jl. G. Obos XII No. 28, Menteng, Kec. Jekan Raya, Palangka Raya 73112" },
  ],
  guestName: "Bapak Yulianus Nyahu & Keluarga",
  guestTable: "Meja Garing 3",
  extras: {
    quote: { text: "Ia akan seperti pohon, yang ditanam di tepi aliran air, yang menghasilkan buahnya pada musimnya, dan yang tidak layu daunnya.", source: "Mazmur 1:3" },
    rundown: { items: [
      { time: "15.00", title: "Penyambutan rombongan mempelai pria", note: "Diiringi tabuhan gandang dan kecapi" },
      { time: "15.45", title: "Prosesi adat & doa para tetua" },
      { time: "16.30", title: "Ramah tamah & makan bersama", note: "Juhu umbut rotan dan ikan baung bakar" },
      { time: "18.30", title: "Resepsi & tari bersama" },
    ] },
    dressCode: { note: "Busana rapi bernuansa merah, kuning kunyit, atau hitam. Busana adat Dayak sangat dipersilakan.", colors: ["#a3302a", "#d99a2b", "#1c1612", "#efe3c8"] },
    rsvpDietary: {},
    family: { names: ["Kel. Besar Dohong – Lambung", "Kel. Besar Saman – Bungai"] },
    travel: { note: "Untuk tamu dari luar kota:", items: [
      { name: "Bandara Tjilik Riwut", detail: "± 10 menit berkendara ke Betang Hapakat" },
      { name: "Taman Pasuk Kameloh", detail: "Tepian Kahayan, tempat bagus untuk menunggu senja" },
    ] },
    faq: { items: [
      { q: "Apakah tamu boleh menyaksikan prosesi adat?", a: "Tentu. Seluruh tamu dipersilakan hadir sejak pukul 15.00." },
      { q: "Apakah tersedia parkir?", a: "Tersedia parkir luas di halaman Betang Hapakat." },
    ] },
  },
});
