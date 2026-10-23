import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Raka", groom: "",
    brideFull: "Rakha Aditya Pratama",
    brideParents: "Putra pertama dari Bapak Dimas Pratama & Ibu Laras Ayuningtyas",
    note: "Misi rahasia: datang, main lempar bintang busa, dan tiup lilin bersama Raka. Pakai baju ninjamu yang paling keren!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-08-14T15:00:00+07:00",
  place: "Aula Taman Kenari",
  address: "Jl. Kenari Raya No. 8, Cempaka Putih Timur, Kec. Cempaka Putih, Jakarta Pusat",
  story: { title: "Cerita Raka", body: "" },
  stories: [
    { date: "2020", title: "Ninja kecil lahir", body: "Raka lahir di malam bulan purnama. Kata Ayah, tangisnya paling nyaring satu rumah sakit." },
    { date: "2024", title: "Sabuk kuning pertama", body: "Raka mulai ikut kelas bela diri anak dan bangga sekali saat naik sabuk. Hormat dulu, baru berlatih!" },
    { date: "2027", title: "Tujuh tahun!", body: "Sekarang Raka sudah bisa salto di kasur (pelan-pelan) dan ingin merayakannya bersama semua teman." },
  ],
  events: [
    { name: "Pesta Ninja Raka", date: "2027-08-14T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Aula Taman Kenari", address: "Jl. Kenari Raya No. 8, Cempaka Putih Timur, Kec. Cempaka Putih, Jakarta Pusat" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "1270 0081 4202 7", account_name: "Laras Ayuningtyas" },
    { id: "demo-kado", type: "address", address: "Jl. Cempaka Putih Tengah XI No. 5, Cempaka Putih Timur, Jakarta Pusat 10510" },
  ],
  guestName: "Adik Kayla & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Rakha Aditya Pratama", nickname: "Raka", birthDate: "2020-08-12T19:30:00+07:00", parents: "Putra pertama dari Bapak Dimas Pratama & Ibu Laras Ayuningtyas" },
    rundown: { items: [
      { time: "15.00", title: "Datang & ambil ikat kepala ninja", note: "Setiap anak dapat satu ikat kepala dan bintang busa" },
      { time: "15.30", title: "Latihan ninja: lompat ban & lempar bintang busa ke sasaran" },
      { time: "16.20", title: "Berburu gulungan rahasia di taman" },
      { time: "17.00", title: "Tiup lilin, potong kue & bagi bingkisan" },
    ] },
    dressCode: { note: "Pakai baju ninja atau kaus warna cerah: merah, biru, kuning, hijau.", colors: ["#e8553e", "#3b6fd8", "#ffd23f", "#2cc1b5"] },
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Pratama", "Eyang Kakung & Eyang Putri", "Adik Naura"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini yang sedang Raka impikan.", items: [
      { id: "w1", name: "Buku cerita bergambar petualangan", price: "± Rp95.000" },
      { id: "w2", name: "Set bintang busa & papan sasaran", price: "± Rp120.000", claimed_by: "Om Bayu" },
      { id: "w3", name: "Matras senam lipat", price: "± Rp250.000" },
    ] },
    faq: { items: [
      { q: "Apakah bintang lemparnya aman?", a: "Aman, semuanya dari busa lembut dan permainan dipandu kakak pendamping." },
      { q: "Apakah orang tua boleh menemani?", a: "Tentu, ada area duduk dan teh hangat untuk orang tua di samping aula." },
    ] },
  },
});
