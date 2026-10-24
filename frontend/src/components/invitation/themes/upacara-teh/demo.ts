import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Arya",
    brideFull: "Nadia Puspitasari, S.Ds.", groomFull: "Arya Wicaksana Putra, M.Ars.",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    brideParents: "Putri sulung dari\nBapak Bambang Sutrisno & Ibu Endang Sulistyowati", groomParents: "Putra kedua dari\nBapak Ir. Hendra Wicaksana & Ibu Maya Kartika",
    note: "Seperti semangkuk teh yang diseduh perlahan, kami belajar bahwa hal-hal baik tumbuh dari kesabaran dan perhatian.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-09T09:00:00+07:00",
  place: "Rumah Teh Sawarna",
  address: "Jl. Kemang Timur Raya No. 5, Bangka, Mampang Prapatan, Jakarta Selatan",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "Musim hujan 2020", title: "Kelas Sore", body: "Kami duduk bersebelahan di kelas upacara teh yang diadakan sebuah komunitas budaya Jepang di Jakarta. Arya terus salah memegang pengaduk." },
    { date: "2022", title: "Semangkuk Demi Semangkuk", body: "Setiap Sabtu kami berlatih menyeduh, lalu mengobrol lama tentang arsitektur, desain, dan rumah yang ingin kami bangun suatu hari." },
    { date: "2027", title: "Satu Pertemuan", body: "Di taman kecil berlantai batu, Arya menyajikan teh dengan mangkuk buatannya sendiri, lalu bertanya apakah kami bisa minum teh bersama seumur hidup." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-10-09T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Rumah Teh Sawarna", address: "Jl. Kemang Timur Raya No. 5, Bangka, Mampang Prapatan, Jakarta Selatan" },
    { name: "Jamuan Teh & Resepsi", date: "2027-10-09T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Taman Batu Rumah Teh Sawarna", address: "Jl. Kemang Timur Raya No. 5, Bangka, Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a75.webp", "/themes/img/a74.webp", "/themes/img/r88.webp"],
  gifts: [
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1270 0099 1009", account_name: "Nadia Puspitasari" },
    { id: "demo-kado", type: "address", address: "Jl. Bangka XI No. 3B, Pela Mampang, Mampang Prapatan, Jakarta Selatan 12720" },
  ],
  guestName: "Ibu Ratna Dewanti & Keluarga",
  guestTable: "Ruang Bambu",
  extras: {
    quote: { text: "Ichi-go ichi-e: satu waktu, satu pertemuan. Setiap perjumpaan hanya terjadi sekali, maka kami ingin menyambutnya dengan sepenuh hati.", source: "Ungkapan dalam tradisi upacara teh Jepang" },
    rundown: { items: [
      { time: "09.00", title: "Upacara pernikahan", note: "Keluarga inti & sahabat" },
      { time: "10.30", title: "Sesi foto keluarga" },
      { time: "11.00", title: "Jamuan teh dibuka", note: "Matcha dan wagashi di taman batu" },
      { time: "13.00", title: "Ramah tamah" },
    ] },
    dressCode: { note: "Tenang dan bersahaja: hijau matcha, krem kertas, abu batu, dan cokelat kayu. Mohon gunakan alas kaki yang mudah dilepas.", colors: ["#6b7f3a", "#f3eee2", "#8f8b80", "#7a5f40"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bambang Sutrisno", "Kel. Besar Ir. Hendra Wicaksana"] },
  },
});
