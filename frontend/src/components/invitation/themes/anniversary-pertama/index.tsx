"use client";
// Theme "Anniversary Pertama" — syukuran satu tahun pernikahan (ulang tahun kertas): surat cinta di kertas bergaris yang
// menyembul dari amplop kraft bersegel lilin koral, polaroid hari pernikahan berselotip washi, mawar kertas, hati
// origami yang melayang, label karton untuk hitung mundur, kartu pos untuk acara, catatan harian untuk tahun pertama.
import { Lucide, Photo, ThemeShell, dateParts, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,500;0,600;1,500;1,600", "Literata:ital,wght@0,400;0,600;1,400", "Caveat:wght@500;600"];
// Painted by /tmp/pen/art/themes/anniversary-pertama.py (cut-paper medium).
const Art = makeArt("anniversary-pertama", {
  envback: [400, 300], envfront: [400, 300], flowers: [400, 273], heart: [120, 106], heart2: [120, 106], heart3: [120, 103], tape: [150, 30], garland: [360, 57],
} as const);

const WORDS = ["", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam", "Tujuh", "Delapan", "Sembilan", "Sepuluh"];

const WISHES = [
  { id: "w1", name: "Mama & Papa Bogor", attendance: "yes" as Attendance, message: "Selamat satu tahun pernikahan, Ayu dan Rendra! Rasanya baru kemarin kalian kehujanan di sesi foto. Semoga selalu rukun, saling sabar, dan saling sayang." },
  { id: "w2", name: "Geng Kantor Lantai 7", attendance: "yes" as Attendance, message: "Happy anniversary yang pertama! Kami datang bawa martabak. Semoga surat-suratnya makin panjang tiap tahun." },
  { id: "w3", name: "Tante Lina, Surabaya", attendance: "maybe" as Attendance, message: "Selamat ulang tahun pernikahan, Sayang. Tante usahakan datang. Semoga tahun kedua lebih hangat lagi." },
];

export default function AnniversaryPertamaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const label = data.eventLabel?.trim() || "Syukuran Satu Tahun Pernikahan";
  const years = Number(/(\d{1,2})/.exec(label)?.[1] ?? 1) || 1;
  const yearWord = WORDS[years] ?? String(years);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const pic = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const day = dateParts(data.date);
  const caption = day.day ? `${day.day} ${day.month} ${Number(day.year) - years}` : "Hari pernikahan kami";
  const names = <>{bride}{groom && <> <em>&amp;</em> {groom}</>}</>;

  const COPY: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Untuk keluarga & sahabat",
      title: `${yearWord} Tahun Bersama`,
      intro: `${years > 1 ? `${yearWord} tahun` : "Setahun"} lalu kami mengucap janji di hadapan kalian. Kini kami ingin bersyukur atas ${years > 1 ? "tahun-tahun" : "tahun pertama"} yang penuh belajar, tawa, dan sedikit drama soal giliran mencuci piring. Kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam syukuran kecil kami.`,
    },
    roles: ["Istri tercinta", "Suami tercinta"],
    couple: ["Yang merayakan", "Kami Berdua"],
    count: ["Tinggal menghitung hari", "Menuju Hari Jadi"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Datang, ya", "Syukuran Kecil"],
    story: ["Dua belas bulan", years > 1 ? "Perjalanan Kami" : "Tahun Pertama Kami"],
    gallery: ["Album kami", "Kenangan"],
    wishes: ["Tinggalkan pesan", "Ucapan & Kehadiran"],
    gifts: ["Tanpa kado", "Berbagi Bersama"],
    closing: {
      thanks: "Terima Kasih",
      text: "Terima kasih sudah menemani perjalanan kami. Doakan kami tetap saling menulis surat, sampai tahun-tahun yang jauh.",
    },
    sent: "Terima kasih! Pesan Anda kami simpan bersama surat-surat kami.",
    wishLabel: "Ucapan",
    wishPlaceholder: "Tuliskan ucapan dan doa untuk hari jadi kami…",
    giftIntro: "Kehadiran kalian sudah lebih dari cukup, tidak perlu membawa kado. Bila ingin berbagi, kami mengajak menyalurkannya untuk taman baca anak di kampung kami:",
    familyLabel: null,
    closedNote: "Terima kasih sudah ikut merayakan. Ucapan masih bisa dikirim lewat form ini.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6ede0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="garland" eager className={s.garland} />
          <Art name="heart" eager className={`${s.float} ${s.f1}`} />
          <Art name="heart3" eager className={`${s.float} ${s.f2}`} />
          <Art name="heart2" eager className={`${s.float} ${s.f3}`} />
          <div className={s.envelope}>
            <Art name="envback" eager className={s.envBack} />
            <div className={s.letter}>
              <p className={s.letterHi}>Untuk yang kami sayangi,</p>
              <p className={s.kicker}>{label}</p>
              <div className={s.one} aria-hidden><b>{years}</b><span>tahun<br />bersama</span></div>
              <h1 className={s.coverNames}>{names}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
            <Art name="envfront" eager className={s.envFront} />
            {pic && (
              <div className={s.polaroid} aria-hidden>
                <div className={s.heroPhoto}><Photo src={pic} alt="" /></div>
                <Art name="tape" eager />
              </div>
            )}
            <Art name="flowers" eager className={s.flowers} />
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffaf2" />Buka Surat Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#fffaf2"
        dark="#2d3a5c"
        hero={(
          <header className={s.hero}>
            <Art name="heart" className={s.heroHeart} />
            <figure className={s.heroPolaroid}>
              <div className={s.heroPhoto}>{pic && <Photo src={pic} alt="Foto hari pernikahan" />}</div>
              <Art name="tape" className={s.heroTape} />
              <figcaption>{caption}</figcaption>
            </figure>
            <p className={s.heroKicker}>{yearWord} tahun yang lalu…</p>
            <h1 className={s.heroNames}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="garland" className={s.divider} />,
          node: <Art name="heart" />,
          amp: <Art name="heart2" />,
          closingDecor: <Art name="garland" className={s.closingGarland} />,
          closingEmblem: <Art name="flowers" className={s.closingFlowers} />,
          sentArt: <Art name="heart" />,
        }}
      />
    </ThemeShell>
  );
}
