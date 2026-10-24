import { makeDemo } from "../demo-base";

// Ulang tahun anak bertema petualangan hutan: piknik di bawah pohon pinus Tahura Djuanda, Bandung, bersama teman-teman hutan.
export const demo = makeDemo({
  couple: {
    bride: "Rafa", groom: "",
    brideFull: "Muhammad Rafandra Putra",
    brideParents: "Putra pertama dari Bapak Galih Pratama & Ibu Annisa Rahmawati",
    note: "Rafa sudah enam tahun! Yuk ikut menjelajah hutan, bertemu burung hantu, rubah, dan rusa, lalu tiup lilin di bawah pohon pinus.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-04-17T09:00:00+07:00",
  place: "Area Piknik Pinus, Tahura Djuanda",
  address: "Jl. Ir. H. Juanda No. 99, Ciburial, Cimenyan, Kabupaten Bandung",
  story: { title: "Buku Jelajah Rafa", body: "" },
  stories: [
    { date: "2021", title: "Anak hutan kecil", body: "Rafa lahir di bulan April, saat hujan baru reda dan pohon-pohon sedang hijau-hijaunya." },
    { date: "2024", title: "Teman burung hantu", body: "Boneka burung hantu bernama Kuku jadi teman tidurnya setiap malam sampai sekarang." },
    { date: "2026", title: "Penjelajah cilik", body: "Pertama kali ikut jalan setapak di hutan pinus dan menemukan jamur merah berbintik putih." },
    { date: "2027", title: "Enam tahun!", body: "Sekarang sudah hafal nama hewan hutan dan ingin semua teman ikut berpetualang." },
  ],
  events: [
    { name: "Pesta Hutan Rafa", date: "2027-04-17T09:00:00+07:00", time: "09.00 – 12.00 WIB", venue: "Area Piknik Pinus, Tahura Djuanda", address: "Jl. Ir. H. Juanda No. 99, Ciburial, Cimenyan, Kabupaten Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "2830 4417 09", account_name: "Annisa Rahmawati" },
    { id: "demo-kado", type: "address", address: "Jl. Dago Pakar Timur No. 12, Mekarsaluyu, Cimenyan, Bandung 40198" },
  ],
  guestName: "Adik Kirana & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Muhammad Rafandra Putra", nickname: "Rafa", birthDate: "2021-04-17T07:15:00+07:00", parents: "Putra pertama dari Bapak Galih Pratama & Ibu Annisa Rahmawati" },
    quote: { text: "Semoga Rafa tumbuh seperti pohon di hutan: berakar kuat, tinggi menjulang, dan teduh bagi siapa saja.", source: "Ayah & Bunda" },
    rundown: { items: [
      { time: "09.00", title: "Pakai topi penjelajah & kalung teropong", note: "Disediakan untuk semua penjelajah cilik" },
      { time: "09.30", title: "Jelajah jejak hewan hutan", note: "Ditemani kakak pemandu" },
      { time: "10.30", title: "Mewarnai topeng rubah & burung hantu" },
      { time: "11.15", title: "Tiup lilin kue jamur & piknik bersama" },
    ] },
    dressCode: { note: "Baju nyaman untuk bermain di hutan dan sepatu tertutup. Warna hijau daun, oranye rubah, atau cokelat kayu.", colors: ["#3d6b3f", "#e57a35", "#7a5236", "#f1d6a8"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Pratama", "Aki & Enin Rahmawati"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Rafa.", items: [
      { id: "w1", name: "Teropong anak & buku hewan hutan", price: "± Rp180.000" },
      { id: "w2", name: "Boneka rubah", price: "± Rp120.000", claimed_by: "Tante Dewi" },
      { id: "w3", name: "Senter kepala untuk berkemah", price: "± Rp90.000" },
    ] },
    faq: { items: [
      { q: "Apakah lokasinya aman untuk balita?", a: "Area piknik datar dan berpagar, ada kakak pemandu yang menemani." },
      { q: "Bagaimana jika hujan?", a: "Acara pindah ke saung besar di dekat area piknik, tetap seru!" },
    ] },
  },
});
