import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laila", groom: "Fadli",
    brideFull: "Baiq Laila Wardani, S.Pd.", groomFull: "Lalu Muhammad Fadli, S.T.",
    brideParents: "Putri kedua dari\nBapak Lalu H. Sudirman & Ibu Baiq Hj. Rohani", groomParents: "Putra pertama dari\nBapak H. Lalu Abdul Hakim & Ibu Hj. Nurhasanah",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti padi yang disimpan di lumbung, semoga cinta kami terjaga, cukup, dan berkah sepanjang musim.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-12T08:00:00+08:00",
  place: "Dusun Rembitan, Lombok Tengah",
  address: "Desa Rembitan, Kec. Pujut, Kabupaten Lombok Tengah, NTB",
  stories: [
    { date: "2020", title: "Pantai Kuta Mandalika", body: "Kami bertemu saat kegiatan bersih pantai bersama komunitas pemuda Lombok Tengah. Laila membawa kantong sampah paling banyak." },
    { date: "2025", title: "Selabar", body: "Keluarga Fadli datang dengan adat selabar untuk bermusyawarah bersama keluarga Laila. Semua dimudahkan dengan doa para tetua." },
    { date: "2027", title: "Begawe", body: "Dengan izin Allah, kami menikah di Mataram dan merayakannya bersama keluarga di kampung halaman Laila di Rembitan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-12T08:00:00+08:00", time: "08.00 – 09.30 WITA", venue: "Masjid Hubbul Wathan Islamic Center", address: "Jl. Udayana No. 1, Gomong, Selaparang, Kota Mataram, NTB" },
    { name: "Nyongkolan & Resepsi", date: "2027-06-13T13:00:00+08:00", time: "13.00 – 17.00 WITA", venue: "Kediaman Keluarga Mempelai Wanita", address: "Dusun Rembitan, Desa Rembitan, Kec. Pujut, Lombok Tengah, NTB" },
  ],
  gallery: ["/themes/img/r15.webp", "/themes/img/r105.webp", "/themes/img/r110.webp", "/themes/img/r104.webp", "/themes/img/r10.webp"],
  gifts: [
    { id: "demo-ntb", type: "bank", bank_name: "Bank NTB Syariah", account_number: "001 02 11 223344 5", account_name: "Baiq Laila Wardani" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7212 3344 55", account_name: "Lalu Muhammad Fadli" },
  ],
  guestName: "Bapak H. Lalu Ahmad Zaini & Keluarga",
  guestTable: "Berugaq 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "13.00", title: "Nyongkolan", note: "Arak-arakan diiringi gendang beleq" },
      { time: "14.30", title: "Sorong serah aji krama", note: "Penyerahan adat oleh pembayun" },
      { time: "15.30", title: "Ramah tamah", note: "Ayam taliwang & plecing kangkung" },
    ] },
    dressCode: { note: "Busana muslim atau pakaian adat Sasak. Hitam, merah bata, dan emas dipersilakan.", colors: ["#16100c", "#9a2620", "#c99a3a", "#efe4cc"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Lalu H. Sudirman", "Kel. Besar H. Lalu Abdul Hakim"] },
  },
});
