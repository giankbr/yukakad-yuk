import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Komisi Keluarga", groom: "Keluarga Manuputty",
    brideFull: "Komisi Pelayanan Keluarga Gereja Kasih Karunia Cibubur",
    groomFull: "Bapak Johan Manuputty & Ibu Lidya Pattinama",
    brideParents: "Pnt. Robert Siahaya, Ketua Panitia\nbersama seluruh pengurus komisi",
    groomParents: "Bersama Kezia, Yosua & Oma Martha\nmembuka taman rumah untuk brunch bersama",
    note: "Kubur itu kosong, pagi itu terang. Mari merayakan kebangkitan Kristus bersama keluarga-keluarga jemaat: beribadah, bersantap, dan bersukacita.",
  },
  eventLabel: "Ibadah & Brunch Paskah Keluarga",
  date: "2027-03-28T05:30:00+07:00",
  place: "Gereja Kasih Karunia Cibubur",
  address: "Jl. Alternatif Cibubur No. 21, Jatikarya, Jatisampurna, Kota Bekasi",
  story: { title: "Tradisi Paskah Kami", body: "" },
  stories: [
    { date: "2012", title: "Brunch pertama di taman", body: "Selepas ibadah subuh, lima keluarga membawa bekal ke taman keluarga Manuputty. Sejak itu menjadi tradisi tahunan." },
    { date: "2018", title: "Berburu telur hias", body: "Anak-anak sekolah minggu mulai menghias telur sendiri, lalu menyembunyikannya di antara pot-pot lili Oma Martha." },
    { date: "2027", title: "Persembahan untuk sesama", body: "Tahun ini persembahan brunch disalurkan lewat diakonia untuk keluarga-keluarga yang membutuhkan di sekitar jemaat." },
  ],
  events: [
    { name: "Ibadah Subuh Paskah", date: "2027-03-28T05:30:00+07:00", time: "05.30 – 07.00 WIB", venue: "Gereja Kasih Karunia Cibubur", address: "Jl. Alternatif Cibubur No. 21, Jatikarya, Jatisampurna, Kota Bekasi" },
    { name: "Brunch & Berburu Telur Paskah", date: "2027-03-28T08:30:00+07:00", time: "08.30 – 11.30 WIB", venue: "Taman Kediaman Keluarga Manuputty", address: "Perumahan Citra Grand, Cluster Bougenville B3 No. 7, Jatikarya, Kota Bekasi" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-diakonia", type: "bank", bank_name: "BCA", account_number: "5271 0390 18", account_name: "Komisi Diakonia GKK Cibubur" },
    { id: "demo-bingkisan", type: "address", address: "Sekretariat Gereja Kasih Karunia, Jl. Alternatif Cibubur No. 21, Jatikarya, Kota Bekasi", account_name: "Panitia Paskah Keluarga 2027" },
  ],
  guestName: "Keluarga Bapak Daniel Latuheru",
  guestTable: "",
  extras: {
    quote: { text: "Ia tidak ada di sini, sebab Ia telah bangkit, sama seperti yang telah dikatakan-Nya.", source: "Matius 28:6" },
    rundown: { items: [
      { time: "05.30", title: "Ibadah subuh Paskah", note: "Pujian, pembacaan Injil, dan perjamuan" },
      { time: "08.30", title: "Brunch keluarga di taman", note: "Bekal bersama, hidangan dari tiap keluarga" },
      { time: "09.45", title: "Berburu telur hias", note: "Untuk anak-anak sekolah minggu" },
      { time: "11.00", title: "Doa syukur & foto bersama" },
    ] },
    dressCode: { note: "Nuansa pagi musim semi: putih, lilac lembut, kuning pucat, atau hijau daun.", colors: ["#fbf8ef", "#b7a3cf", "#f2cf86", "#7f9a58"] },
    rsvpDietary: {},
    family: { title: "Dengan sukacita mengundang", names: ["Majelis Jemaat GKK Cibubur", "Komisi Sekolah Minggu", "Keluarga Manuputty"] },
    faq: { items: [
      { q: "Perlu membawa apa untuk brunch?", a: "Setiap keluarga dipersilakan membawa satu hidangan sederhana untuk dinikmati bersama. Minuman disiapkan panitia." },
      { q: "Apakah anak-anak perlu membawa telur?", a: "Tidak perlu. Telur hias sudah disiapkan sekolah minggu; anak-anak cukup membawa keranjang kecil." },
    ] },
  },
});
