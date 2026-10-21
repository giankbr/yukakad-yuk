import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Yasmin", groom: "Daffa",
    brideFull: "Yasmin Khairiyah Putri, S.Psi.", groomFull: "Daffa Rasyid Ramadhan, M.Sc.",
    brideParents: "Putri sulung dari\nBapak H. Fadhil Abdullah & Ibu Hj. Rahmawati Sukma",
    groomParents: "Putra pertama dari\nBapak Dr. H. Hasbullah Thalib & Ibu Hj. Zahratul Jannah",
    note: "Semoga rumah kami kelak seperti taman: teduh oleh doa, mengalir oleh syukur, dan berbuah kebaikan.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-10-09T09:00:00+07:00",
  place: "Masjid Raya Sheikh Zayed Solo",
  address: "Jl. Ahmad Yani No. 128, Gilingan, Banjarsari, Surakarta",
  stories: [
    { date: "2022", title: "Majelis Ilmu", body: "Kami sama-sama mengikuti kajian tafsir pekanan, saling mengenal lewat diskusi yang hangat." },
    { date: "2025", title: "Ta'aruf", body: "Dengan perantara ustazah pembimbing, kami berta'aruf bersama keluarga dan memohon petunjuk-Nya." },
    { date: "Juni 2027", title: "Khitbah", body: "Keluarga Daffa datang meminang; dua keluarga menyatukan niat untuk hari yang diberkahi." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-09T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Raya Sheikh Zayed Solo", address: "Jl. Ahmad Yani No. 128, Gilingan, Banjarsari, Surakarta" },
    { name: "Walimah", date: "2027-10-09T11:30:00+07:00", time: "11.30 – 14.00 WIB", venue: "Pendapi Gede Balai Kota", address: "Jl. Jend. Sudirman No. 2, Kp. Baru, Pasar Kliwon, Surakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7230 1122 33", account_name: "Yasmin Khairiyah Putri" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "081225566778", account_name: "Daffa Rasyid Ramadhan" },
  ],
  guestName: "Ustadz H. Abdurrahman Hasyim & Keluarga",
  guestTable: "Meja Delima 5",
  extras: {
    quote: { text: "Mereka (istri-istrimu) adalah pakaian bagimu, dan kamu adalah pakaian bagi mereka.", source: "QS. Al-Baqarah: 187" },
    rundown: { items: [
      { time: "09.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "10.00", title: "Khutbah nikah & doa" },
      { time: "11.30", title: "Walimah dibuka" },
      { time: "13.00", title: "Ramah tamah" },
    ] },
    dressCode: { note: "Busana muslim santun. Biru lapis, hijau cemara, dan krem emas dipersilakan.", colors: ["#1f3a8a", "#1f4a35", "#f2e7cf", "#c9a24a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-09T09:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Fadhil Abdullah", "Kel. Besar Dr. H. Hasbullah Thalib"] },
  },
});
