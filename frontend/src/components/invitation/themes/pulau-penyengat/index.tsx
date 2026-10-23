"use client";
// Theme "Pulau Penyengat" — adat Melayu Riau dalam kuning dan hijau: masjid kuning bersejarah di Pulau Penyengat
// dipandang dari selat (arsitektur saja), pompong yang berlayar dari Tanjungpinang, lisplang lebah bergantung,
// selembayung bersilang, dan awan larat, semuanya dilukis gouache. Pantun pembuka dan bismillah diketik.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Della Respira", "Spectral:ital,wght@0,400;0,600;0,700;1,400", "Ephesis", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/pulau-penyengat.py.
const Art = makeArt("pulau-penyengat", {
  scene: [640, 496], pompong: [220, 73], pompong2: [160, 53], selembayung: [200, 101], divider: [260, 30], kuntum: [70, 69],
} as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللّٰهِ وَبَرَكَاتُهُ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Urs",
    sub: "Dari Tanah Melayu, Bumi Segantang Lada",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud melangsungkan akad nikah dan kenduri pernikahan putra-putri kami. Merupakan suatu kehormatan apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Pengantin Perempuan", "Pengantin Lelaki"],
  couple: ["Yang Akan Bersanding", "Kedua Pengantin"],
  count: ["Menanti Hari Bersanding", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Masa & Tempat", "Rangkaian Majelis"],
  story: ["Dari Seberang Selat", "Kisah Kami"],
  gallery: ["Galeri", "Kenangan"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas segala kebaikan dengan berlipat ganda.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua pengantin…",
};

const WISHES = [
  { id: "w1", name: "Keluarga Datuk Raja Ahmad", attendance: "yes" as const, message: "Barakallahu lakuma. Semoga menjadi keluarga sakinah, mawaddah, warahmah, dan kekal hingga ke anak cucu." },
  { id: "w2", name: "Sanggar Gurindam Penyengat", attendance: "yes" as const, message: "Kalau ada sumur di ladang, boleh kita menumpang mandi. Selamat bersanding Atikah dan Faiz, kami tunggu di pelaminan!" },
  { id: "w3", name: "Wan Syarifah, Batam", attendance: "maybe" as const, message: "Insyaallah menyusul dengan feri sore. Doa terbaik untuk kalian berdua, semoga penuh berkah." },
];

export default function PulauPenyengatTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();
  const names = <><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</>;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e7efe0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverEave} aria-hidden />
          <Art name="selembayung" eager className={s.coverCrest} />
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{names}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverScene} aria-hidden>
            <Art name="scene" eager />
            <Art name="pompong2" eager className={s.boat2} />
            <Art name="pompong" eager className={s.boat1} />
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#174732" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#f3d672"
        dark="#174732"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Walimatul &apos;Urs</p>
            <div className={s.heroWin}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} ${groom ? `dan ${groom}` : ""}`.trim()} /> : <span className={s.heroMono} aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
            </div>
            <h1 className={s.heroNames}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="kuntum" />,
          amp: <Art name="kuntum" />,
          portrait: <Art name="selembayung" className={s.portraitCrest} />,
          countDecor: <Art name="pompong" className={s.countBoat} />,
          closingDecor: <Art name="scene" className={s.closingScene} />,
          closingEmblem: <Art name="selembayung" className={s.closingEmblem} />,
          sentArt: <Art name="kuntum" />,
        }}
      />
    </ThemeShell>
  );
}
