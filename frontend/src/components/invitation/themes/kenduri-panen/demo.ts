import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kelompok Tani Sri Rejeki", groom: "Pemerintah Desa Sidomakmur",
    brideFull: "Gabungan Kelompok Tani Sri Rejeki",
    brideParents: "Ketua: Bapak Suparman\nBendahara: Ibu Wartini",
    groomFull: "Pemerintah Desa Sidomakmur",
    groomParents: "Kepala Desa: Bapak H. Sutrisno, S.Sos.",
    note: "Alhamdulillah, panen musim ini melimpah. Mari berkumpul, berdoa, dan makan bersama sebagai tanda syukur seluruh warga.",
  },
  eventLabel: "Kenduri Panen Raya",
  date: "2027-04-25T08:00:00+07:00",
  place: "Balai Desa Sidomakmur",
  address: "Jl. Raya Sidomakmur No. 1, Kec. Widodaren, Kabupaten Ngawi, Jawa Timur",
  story: { title: "Perjalanan Musim Ini", body: "" },
  stories: [
    { date: "Desember 2026", title: "Tandur Bersama", body: "Seratus dua puluh hektar sawah ditanami serentak. Ibu-ibu PKK menyiapkan bekal untuk para penanam di pematang." },
    { date: "Februari 2027", title: "Gotong Royong Irigasi", body: "Saluran dari bendung kecil di utara desa sempat tersumbat. Warga dua dusun bekerja bakti tiga hari hingga air kembali mengalir." },
    { date: "April 2027", title: "Panen Raya", body: "Padi menguning serempak dan hasilnya melampaui musim lalu. Sebagian gabah disisihkan untuk lumbung pangan desa." },
  ],
  events: [
    { name: "Doa Bersama & Tasyakuran", date: "2027-04-25T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Balai Desa Sidomakmur", address: "Jl. Raya Sidomakmur No. 1, Kec. Widodaren, Kabupaten Ngawi" },
    { name: "Makan Bersama & Pentas Warga", date: "2027-04-25T10:00:00+07:00", time: "10.00 – 14.00 WIB", venue: "Lapangan Dusun Krajan", address: "Belakang Balai Desa Sidomakmur, Kec. Widodaren, Kabupaten Ngawi" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "6031 0100 2245 538", account_name: "Kas Gapoktan Sri Rejeki" },
    { id: "demo-address", type: "address", address: "Sekretariat Gapoktan Sri Rejeki, Balai Desa Sidomakmur, Jl. Raya Sidomakmur No. 1, Widodaren, Ngawi", account_name: "Ibu Wartini (Bendahara)" },
  ],
  guestName: "Bapak Darmaji & Keluarga",
  guestTable: "RT 03 / RW 01",
  extras: {
    quote: { text: "Ilmu padi: makin berisi, makin merunduk. Semoga hasil panen ini menjadikan kita makin bersyukur dan makin rendah hati.", source: "Pepatah" },
    rundown: { items: [
      { time: "08.00", title: "Pembukaan & sambutan Kepala Desa" },
      { time: "08.30", title: "Doa bersama", note: "Dipimpin tokoh agama desa" },
      { time: "09.30", title: "Pemotongan tumpeng", note: "Diserahkan kepada petani tertua" },
      { time: "10.00", title: "Makan bersama & pentas warga", note: "Karawitan dan hadrah anak-anak" },
    ] },
    dressCode: { note: "Pakaian bebas rapi. Batik atau baju lurik sangat dipersilakan.", colors: ["#d9a441", "#9aae66", "#f7ecd2", "#8a5a32"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Karang Taruna Tunas Muda", "Tim Penggerak PKK Desa", "Paguyuban Pengairan (P3A) Tirto Mulyo", "Seluruh warga Dusun Krajan & Dusun Ngrejo"] },
  },
});
