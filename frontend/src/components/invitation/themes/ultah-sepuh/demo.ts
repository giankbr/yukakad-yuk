import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Eyang Sri", groom: "",
    brideFull: "Sri Mulyani Hadiwijaya",
    brideParents: "Bersama anak, cucu & cicit",
    note: "Tujuh puluh tahun penuh kasih, empat generasi yang tumbuh dari satu hati.",
  },
  eventLabel: "Ulang Tahun ke-70",
  date: "2027-05-08T11:00:00+07:00",
  place: "Pendopo Rumah Joglo Hadiwijaya",
  address: "Jl. Pahlawan No. 21, Kemirirejo, Magelang Tengah, Kota Magelang",
  story: { title: "Perjalanan Eyang Sri", body: "" },
  stories: [
    { date: "1957", title: "Lahir di Magelang", body: "Putri ketiga dari tujuh bersaudara, besar di antara kebun jeruk dan suara gamelan tetangga." },
    { date: "1979", title: "Menikah dengan Eyang Kakung", body: "Bertemu di perpustakaan kota. Eyang Kakung meminjam buku yang sama tiga minggu berturut-turut." },
    { date: "1982 – 2012", title: "Tiga puluh tahun mengajar", body: "Guru kelas satu SD Negeri Kemirirejo. Ratusan murid belajar membaca dari tangan sabarnya." },
    { date: "2027", title: "Tujuh puluh tahun", body: "Empat anak, sembilan cucu, dan dua cicit. Masih membuat getuk lindri paling enak se-Magelang." },
  ],
  events: [
    { name: "Doa Syukur Bersama", date: "2027-05-08T09:30:00+07:00", time: "09.30 – 10.30 WIB", venue: "Pendopo Rumah Joglo Hadiwijaya", address: "Jl. Pahlawan No. 21, Kemirirejo, Magelang Tengah, Kota Magelang" },
    { name: "Ramah Tamah & Makan Siang", date: "2027-05-08T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendopo Rumah Joglo Hadiwijaya", address: "Jl. Pahlawan No. 21, Kemirirejo, Magelang Tengah, Kota Magelang" },
  ],
  gallery: ["/themes/img/r53.webp", "/themes/img/r101.webp", "/themes/img/r100.webp", "/themes/img/r58.webp", "/themes/img/r77.webp", "/themes/img/r70.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "0231 557 819", account_name: "Ratna Hadiwijaya" },
  ],
  guestName: "Bapak Haryanto & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Sri Mulyani Hadiwijaya", nickname: "Eyang Sri", birthDate: "1957-05-08T06:00:00+07:00", photo: "/themes/img/r53.webp", parents: "Bersama anak, cucu & cicit" },
    rundown: { items: [
      { time: "09.30", title: "Doa syukur bersama keluarga" },
      { time: "10.30", title: "Persembahan lagu dari para cucu" },
      { time: "11.00", title: "Potong tumpeng & ucapan anak-anak" },
      { time: "12.00", title: "Makan siang & foto empat generasi" },
    ] },
    dressCode: { note: "Batik atau kebaya bernuansa emas, gading, dan cokelat.", colors: ["#c9a24e", "#f8f2e4", "#8a6a4a", "#9aa686"] },
    guestPass: {},
    rsvpDietary: { label: "Pantangan makanan atau kebutuhan khusus (opsional)" },
    family: { title: "Dengan hormat, kami yang berbahagia", names: ["Keluarga Ir. Bambang Hadiwijaya", "Keluarga Ratna Hadiwijaya", "Keluarga Dr. Andreas Hadiwijaya", "Keluarga Wulan Hadiwijaya"] },
    easyRead: { enabled: true },
    faq: { items: [
      { q: "Apakah tersedia kursi roda?", a: "Tersedia dua kursi roda dan jalur landai dari halaman menuju pendopo." },
      { q: "Di mana tamu dapat parkir?", a: "Parkir mobil di halaman SD Negeri Kemirirejo, 100 meter dari rumah." },
    ] },
  },
});
