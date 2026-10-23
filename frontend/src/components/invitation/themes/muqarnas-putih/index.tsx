"use client";
// Theme "Muqarnas Putih" — a white stucco muqarnas vault seen from below: tiers of honeycomb niche cells around an
// eight-pointed oculus that lets in soft pale-gold light (the couple's initials sit in that light on the cover). Ivory,
// white and pale gold; lancet-niche portraits under a stucco star; a muqarnas cornice hangs from the top of cards and
// sections; the hero photo stands under a muqarnas niche hood. Geometry and architecture only, no figures, no drawn
// calligraphy (the Arabic is typeset).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bellefair", "Spectral:ital,wght@0,400;0,500;0,600;1,400", "Pinyon Script", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/muqarnas-putih.py (tools/art/themes in the repo).
const Art = makeArt("muqarnas-putih", { vault: [760, 760], niche: [300, 254], star: [120, 120], divider: [320, 42], frieze: [390, 75] } as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Rahmat Allah",
    intro: "Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan ridha-Nya, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Atas Izin Allah", "Kedua Mempelai"],
  count: ["Menanti Hari Akad", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah kebahagiaan bagi kami. Semoga Allah membalas setiap kebaikan dengan kebaikan yang berlipat.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakallah khair, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
};

function initial(name?: string) {
  return (name ?? "").trim().slice(0, 1).toUpperCase();
}

export default function MuqarnasPutihTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const a = initial(data.couple.bride);
  const b = initial(data.couple.groom);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#ebe4d6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.dome} aria-hidden>
            <Art name="vault" eager />
            <span className={s.oculus}>{a}{b && <><span>&amp;</span>{b}</>}</span>
            <span className={s.domeFade} />
          </div>
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.coverKicker}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffdf8" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fffdf8"
        dark="#7d6233"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.portal}>
              {hero ? <div className={s.heroPhoto}><Photo src={hero} alt="" /></div> : <span className={s.portalPlain} aria-hidden />}
              <Art name="niche" className={s.portalHood} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          portrait: <Art name="star" />,
          countDecor: <Art name="vault" className={s.countVault} />,
          closingEmblem: <><Art name="vault" className={s.closingVault} /><Art name="star" className={s.closingStar} /></>,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
