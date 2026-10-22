import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Felicia", groom: "Ryan",
    brideFull: "Felicia Angelina Gunawan, S.Sn.", groomFull: "Ryan Pratama Halim, S.Ds.",
    brideParents: "Putri bungsu dari\nBapak Hendra Gunawan & Ibu Lily Setiawati", groomParents: "Putra pertama dari\nBapak Andi Halim & Ibu Susanti Tjandra",
    bridePhoto: "/themes/img/a127.webp", groomPhoto: "/themes/img/a126.webp",
    note: "Satu panggung kecil, satu lagu sumbang, lalu sepuluh tahun duet yang tidak pernah selesai.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-09T10:00:00+07:00",
  place: "Gudang Bata Kemang",
  address: "Jl. Kemang Raya No. 45B, Bangka, Mampang Prapatan, Jakarta Selatan",
  stories: [
    { date: "2017", title: "Malam Open Mic", body: "Felicia menyanyi di sebuah kafe kecil di Kemang, Ryan salah masuk kunci gitar. Penonton tertawa, mereka berdua juga." },
    { date: "2021", title: "Band Dua Orang", body: "Kami mulai manggung berdua tiap Jumat malam, di bawah papan neon yang lampunya kadang berkedip sendiri." },
    { date: "2026", title: "Lagu Terakhir Malam Itu", body: "Di akhir set, Ryan menyanyikan lagu ciptaannya sendiri, lalu mengeluarkan cincin dari saku jaket. Felicia menjawab dengan satu kata: iya." },
  ],
  events: [
    { name: "Pemberkatan Pernikahan", date: "2027-10-09T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Vihara Ekayana Arama", address: "Jl. Mangga II No. 8, Duri Kepa, Kebon Jeruk, Jakarta Barat" },
    { name: "Pesta Malam", date: "2027-10-09T19:00:00+07:00", time: "19.00 – 23.00 WIB", venue: "Gudang Bata Kemang", address: "Jl. Kemang Raya No. 45B, Bangka, Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/r23.webp", "/themes/img/a32.webp", "/themes/img/r63.webp", "/themes/img/r84.webp", "/themes/img/r24.webp", "/themes/img/a140.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "6803 1145 27", account_name: "Felicia Angelina Gunawan" },
    { id: "demo-ewallet", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 9001 2277", account_name: "Ryan Pratama Halim" },
  ],
  guestName: "Kak Nadia & Partner",
  guestTable: "Meja Neon 7",
  extras: {
    quote: { text: "Bila suami dan istri ingin bersama dalam kehidupan ini dan kehidupan mendatang, keduanya hendaknya memiliki keyakinan yang sama, moralitas yang sama, kedermawanan yang sama, dan kebijaksanaan yang sama.", source: "Anguttara Nikaya 4.55" },
    rundown: { items: [
      { time: "19.00", title: "Pintu dibuka & mocktail bar" },
      { time: "19.45", title: "Masuknya pengantin", note: "Lampu dimatikan sebentar" },
      { time: "20.15", title: "Makan malam & live band" },
      { time: "21.30", title: "Lantai dansa dibuka" },
    ] },
    dressCode: { note: "Gelap & berkilau: hitam, dengan aksen pink, toska, atau emas.", colors: ["#141015", "#ff4fa3", "#2fe0d0", "#ffb547"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendra Gunawan", "Kel. Besar Bpk. Andi Halim"] },
  },
});
