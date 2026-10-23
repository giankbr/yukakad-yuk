import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Arka", groom: "",
    brideFull: "Arkana Rafisqi Putra",
    brideParents: "Putra pertama dari Bapak Rendy Saputra & Ibu Maya Anggraini",
    note: "Kota aman, tugas sekolah beres, saatnya misi paling seru: pesta ulang tahun keenam Arka!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-07-10T15:00:00+07:00",
  place: "Aula Rumah Pohon",
  address: "Jl. Dago Atas No. 12, Coblong, Kota Bandung",
  stories: [
    { date: "2021", title: "Lahir di hari Sabtu", body: "Arka lahir pagi-pagi, tangannya mengepal seperti sedang bersiap terbang." },
    { date: "2023", title: "Jubah pertama", body: "Sarung bantal biru jadi jubah kesayangan. Sejak itu, sofa adalah gedung pencakar langit." },
    { date: "2025", title: "Penolong kecil", body: "Membantu Bunda menyiram tanaman dan menjaga adik sepupu. Pahlawan tidak harus bisa terbang." },
    { date: "2027", title: "Enam tahun!", body: "Sekarang sudah bisa naik sepeda tanpa roda bantu dan ingin jadi pemadam kebakaran." },
  ],
  events: [
    { name: "Pesta Pahlawan Cilik", date: "2027-07-10T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Aula Rumah Pohon", address: "Jl. Dago Atas No. 12, Coblong, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0812 3344 5566", account_name: "Maya Anggraini" },
    { id: "demo-kado", type: "address", address: "Jl. Cigadung Raya Timur No. 8, Cibeunying Kaler, Kota Bandung 40191" },
  ],
  guestName: "Kak Naila & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Arkana Rafisqi Putra", nickname: "Arka", birthDate: "2021-07-10T07:20:00+07:00", parents: "Putra pertama dari Bapak Rendy Saputra & Ibu Maya Anggraini" },
    rundown: { items: [
      { time: "15.00", title: "Datang & pilih topeng pahlawan", note: "Topeng dan jubah kertas disediakan" },
      { time: "15.30", title: "Lomba misi penyelamatan", note: "Rintangan bantal dan terowongan kardus" },
      { time: "16.30", title: "Tiup lilin & potong kue", note: "Nyanyi bersama" },
      { time: "17.00", title: "Foto bersama & bagi bingkisan" },
    ] },
    dressCode: { note: "Datang sebagai pahlawan versimu sendiri! Jubah, topeng, atau kaus warna merah, biru, dan kuning.", colors: ["#ff5a36", "#2f5bd8", "#ffc93c", "#16213e"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Saputra", "Eyang Anggraini", "Om Dimas & Tante Sari"] },
    wishlist: { note: "Kehadiranmu sudah jadi kado terbaik. Kalau ingin memberi, ini kesukaan Arka.", items: [
      { id: "w1", name: "Buku cerita bergambar", price: "± Rp85.000" },
      { id: "w2", name: "Set balok susun kota", price: "± Rp150.000", claimed_by: "Om Dimas" },
      { id: "w3", name: "Senter kepala untuk patroli malam", price: "± Rp70.000" },
    ] },
    faq: { items: [
      { q: "Wajib pakai kostum?", a: "Tidak wajib, tapi seru! Topeng kertas tersedia di pintu masuk." },
      { q: "Orang tua boleh menemani?", a: "Tentu, ada area duduk dan camilan untuk Ayah dan Bunda." },
    ] },
  },
});
