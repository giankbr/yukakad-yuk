import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "PT Arkana Bumi Persada", groom: "",
    brideFull: "Direksi & Panitia Gala Dinner 2027",
    brideParents: "Hendrawan Saputra, Presiden Direktur\nRatna Kumalasari, Ketua Panitia",
    note: "Satu malam untuk berterima kasih: kepada setiap tim, setiap lembur, dan setiap ide yang membawa kita sejauh ini.",
  },
  eventLabel: "Gala Dinner 2027",
  date: "2027-12-10T18:00:00+07:00",
  place: "Ballroom Samudra, Hotel Cakrawala",
  address: "Jl. Jend. Gatot Subroto Kav. 52, Kuningan Barat, Jakarta Selatan",
  story: { title: "Susunan Acara", body: "" },
  stories: [
    { date: "18.00", title: "Registrasi & Welcome Cocktail", body: "Penukaran kartu meja di foyer, foto di area backdrop, dan minuman sambutan diiringi kuartet gesek." },
    { date: "19.00", title: "Sambutan Presiden Direktur", body: "Refleksi perjalanan 2027 dan arah perusahaan untuk tahun depan." },
    { date: "19.30", title: "Jamuan Makan Malam", body: "Hidangan empat menu di meja bundar, dilanjutkan pertunjukan musik jazz." },
    { date: "20.30", title: "Malam Penghargaan", body: "Penyerahan trofi Karyawan Teladan, Tim Terbaik, dan Penghargaan Masa Bakti 10 & 20 tahun." },
    { date: "21.30", title: "Doorprize & Penutupan", body: "Undian doorprize utama, foto bersama seluruh keluarga besar Arkana, dan salam penutup." },
  ],
  events: [
    { name: "Registrasi & Cocktail", date: "2027-12-10T18:00:00+07:00", time: "18.00 – 19.00 WIB", venue: "Foyer Ballroom Samudra", address: "Hotel Cakrawala, Jl. Jend. Gatot Subroto Kav. 52, Kuningan Barat, Jakarta Selatan" },
    { name: "Gala Dinner & Malam Penghargaan", date: "2027-12-10T19:00:00+07:00", time: "19.00 – 22.00 WIB", venue: "Ballroom Samudra, Hotel Cakrawala", address: "Jl. Jend. Gatot Subroto Kav. 52, Kuningan Barat, Jakarta Selatan" },
  ],
  gallery: [],
  gifts: [],
  guestName: "Bapak Dimas Prasetyo",
  guestTable: "Meja 08",
  extras: {
    dressCode: { note: "Black tie. Jas atau gaun malam; nuansa hitam, biru tua, dan emas.", colors: ["#07080c", "#14203f", "#c8a24f", "#f3ecdc"] },
    guestPass: { note: "Tunjukkan kode ini di meja registrasi untuk menukar kartu meja dan kupon doorprize." },
    rsvpDietary: {},
    faq: { items: [
      { q: "Apakah boleh membawa pasangan?", a: "Boleh, satu pendamping per karyawan. Mohon cantumkan jumlah tamu saat konfirmasi." },
      { q: "Di mana parkir?", a: "Parkir basement Hotel Cakrawala; tiket parkir dapat divalidasi di meja registrasi." },
      { q: "Bagaimana dengan doorprize?", a: "Setiap karyawan yang hadir mendapat satu kupon undian saat registrasi. Undian dilakukan di akhir acara." },
    ] },
  },
});
