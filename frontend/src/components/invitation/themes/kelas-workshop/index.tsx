"use client";
// Theme "Kelas Workshop" — undangan kelas kriya (contoh: kelas gerabah pemula di studio rekaan "Studio Lempung"):
// selebaran kertas yang ditempel selotip di papan pasak, meja kerja bergaya gouache dengan meja putar dan guci
// berglasir, celemek denim bernoda tanah liat yang berayun di pasaknya, rak pengering, dan tiket pendaftaran
// berlubang. Tuan rumah = pengajar & studio, kisah = silabus, amplop = biaya kelas. Tidak ada nuansa pernikahan.
import { Lucide, ThemeShell, dateParts, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fredoka:wght@500;600;700", "Lexend:wght@400;500;600", "Gochi Hand"];
// Painted by /tmp/pen/art/themes/kelas-workshop.py.
const Art = makeArt("kelas-workshop", { meja: [720, 379], celemek: [240, 405], rak: [600, 462], guci: [240, 116], alat: [220, 143] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, calon perajin!",
    title: "Mari Kotor-kotoran",
    sub: "Kelas untuk pemula, tanpa perlu pengalaman",
    intro: "Kami mengundangmu menghabiskan satu hari bersama tanah liat: menguleni, memilin, mencoba meja putar, lalu memberi warna. Semua alat dan bahan sudah kami siapkan, kamu cukup datang dengan rasa penasaran.",
  },
  roles: ["Pengajar", "Studio"],
  couple: ["Yang akan menemanimu", "Pengajar & Studio"],
  count: ["Kelas dimulai dalam", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat jadwalnya", "Jadwal Kelas"],
  story: ["Silabus hari itu", "Yang Akan Dipelajari"],
  gallery: ["Karya dari studio", "Galeri Karya"],
  wishes: ["Daftar & bertanya", "Pendaftaran Peserta"],
  gifts: ["Biaya kelas", "Pembayaran"],
  closing: {
    thanks: "Sampai Jumpa di Studio!",
    text: "Terima kasih sudah tertarik belajar bersama kami. Datang 15 menit lebih awal, ya: celemek, teh hangat, dan tanah liatmu sudah menunggu.",
    salam: "Salam lempung dari Kasongan",
  },
  sent: "Terima kasih! Pendaftaran dan pesanmu sudah kami catat.",
  attend: { yes: "Ikut Kelas", maybe: "Masih Ragu", no: "Lain Kali" },
  wishPlaceholder: "Ceritakan sedikit tentang dirimu atau tulis pertanyaan…",
  closedNote: "Pendaftaran kelas ini sudah ditutup. Pertanyaan dan kesan masih bisa dikirim lewat form ini.",
  giftIntro: "Biaya kelas Rp350.000 per peserta, sudah termasuk 5 kg tanah liat, glasir, dua kali pembakaran, celemek pinjaman, dan makan siang. Mohon transfer setelah mendaftar:",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Sinta (peserta baru)", attendance: "yes" as const, message: "Sudah lama ingin belajar meja putar! Apakah boleh membawa sketsa motif sendiri untuk ditoreh?" },
  { id: "w2", name: "Bagus, alumni kelas Januari", attendance: "yes" as const, message: "Mangkuk pertamaku miring tapi tetap kupakai tiap pagi. Ikut lagi untuk belajar glasir, sampai jumpa Mbak Laras!" },
  { id: "w3", name: "Ayu & Dita", attendance: "maybe" as const, message: "Kami berdua masih mengatur jadwal. Kalau kelas Maret penuh, apakah ada jadwal April?" },
];

export default function KelasWorkshopTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const title = data.eventLabel?.trim() || "Kelas Workshop";
  const studio = data.couple.groomFull?.trim() || data.couple.groom?.trim() || data.place?.trim();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const when = dateParts(data.date);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#b8946c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="celemek" eager className={s.apron} />
          <Art name="alat" eager className={s.coverTools} />
          <div className={s.flyer}>
            {studio && <p className={s.studio}>{studio}</p>}
            <p className={s.kicker}>Kamu diundang ke</p>
            <h1 className={s.coverTitle}>{title}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <Art name="meja" eager className={s.flyerArt} />
          </div>
          <div className={s.ticket}>
            <div className={s.guest}>
              <small>Tiket peserta</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            {when.day && <p className={s.stub}><span><b>{when.day}</b>{when.monthShort}</span></p>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Lihat Undangan Kelas</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        copy={COPY}
        demoWishes={WISHES}
        light="#fff3d6"
        dark="#3a2a22"
        hero={(
          <header className={s.hero}>
            <Art name="rak" className={s.heroShelf} />
            <div className={s.heroCard}>
              <p className={s.heroKicker}>{studio ? `${studio} mengundang` : "Undangan kelas"}</p>
              <h1 className={s.heroTitle}>{title}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="guci" className={s.divider} />,
          portrait: <Art name="alat" />,
          closingEmblem: <div className={s.closingCard}><Art name="alat" /></div>,
          sentArt: <Art name="guci" />,
        }}
      />
    </ThemeShell>
  );
}
