import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadhira", groom: "Ilham",
    brideFull: "Nadhira Kamila Putri, S.Farm.", groomFull: "Muhammad Ilham Fauzan, S.Kom.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Syarifuddin & Ibu Hj. Siti Rahmawati", groomParents: "Putra pertama dari\nBapak Drs. Fauzan Hidayat & Ibu Nurul Aini",
    note: "Seperti kenanga yang harumnya tetap tinggal meski bunganya telah gugur, semoga kebaikan rumah tangga kami terasa lama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T08:00:00+07:00",
  place: "Gedung Kenari Hall",
  address: "Jl. Pajajaran No. 88, Bantarjati, Bogor Utara, Kota Bogor",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2021", title: "Taaruf", body: "Dikenalkan oleh guru mengaji kami, dengan niat yang sama: mencari teman pulang ke surga." },
    { date: "2026", title: "Khitbah", body: "Keluarga Ilham datang bersilaturahmi dan melamar, disambut hangat oleh keluarga Nadhira." },
    { date: "2027", title: "Akad", body: "Insyaallah kami melangkah ke ikatan suci pernikahan dengan restu kedua orang tua." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Nurul Huda Cimanggu", address: "Jl. Cimanggu Kecil No. 2, Kedung Waringin, Tanah Sareal, Kota Bogor" },
    { name: "Walimatul 'Ursy", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Kenari Hall", address: "Jl. Pajajaran No. 88, Bantarjati, Bogor Utara, Kota Bogor" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Nadhira Kamila Putri" },
    { id: "demo-kado", type: "address", address: "Jl. Kenanga Raya No. 17, Bantarjati, Bogor Utara, Kota Bogor 16153" },
  ],
  guestName: "Ibu Hj. Maryam Lestari & Keluarga",
  guestTable: "Meja Kenanga 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "11.00", title: "Walimah dibuka", note: "Tilawah & doa" },
      { time: "11.30", title: "Ramah tamah & santap siang" },
      { time: "13.00", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim santun bernuansa krem, hijau zaitun, dan kuning lembut.", colors: ["#f6f1e3", "#5f6b34", "#c9c35a", "#a59a6e"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Syarifuddin", "Kel. Besar Drs. Fauzan Hidayat"] },
  },
});
