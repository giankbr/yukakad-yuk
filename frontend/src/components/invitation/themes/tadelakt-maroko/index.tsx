"use client";
// Theme "Tadelakt Maroko" — Islami, minimal dan bersahaja: dinding plester tadelakt yang dipoles (tekstur cat ulas
// berkilau lembut dalam warna tanah liat kemerahan), lentera kuningan berlubang yang berayun dan berpendar, pintu kayu
// cedar berukir bintang geometri dengan paku kuningan, dan permadani tenun Berber. Tanpa foto, tanpa figur, tanpa
// kaligrafi lukis (bismillah sebagai teks).
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bellefair", "Karla:ital,wght@0,400;0,500;0,700;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/tadelakt-maroko.py (dinding.webp is the CSS wall texture).
const Art = makeArt("tadelakt-maroko", { pintu: [320, 573], lentera: [200, 370], permadani: [800, 170], anyam: [420, 44] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Rahmat Allah",
    intro: "Maha suci Allah yang menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon ridha-Nya, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan mendoakan pernikahan kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bismillah, kami berdua", "Kedua Mempelai"],
  count: ["Lentera sudah dinyalakan", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Pintu kami terbuka", "Waktu & Tempat"],
  story: ["Perlahan dan sabar", "Perjalanan Kami"],
  gallery: ["Kenangan", "Galeri"],
  wishes: ["Doa untuk kami", "Doa & Konfirmasi"],
  gifts: ["Tanda kasih", "Hadiah Pernikahan"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Terima kasih atas doa dan kehadiran Bapak/Ibu/Saudara/i. Semoga Allah membalas kebaikan Anda dengan sebaik-baik balasan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakallah khair, doa Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa Anda adalah hadiah terbaik bagi kami. Bila berkenan berbagi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Ibu Hj. Khadijah & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga rumah kalian selalu hangat dan penuh berkah." },
  { id: "w2", name: "Studio Ruang Tanah", attendance: "yes" as const, message: "Selamat Nadia dan Faris! Akhirnya rumah impian kalian ada penghuninya. Sampai jumpa di Dago." },
  { id: "w3", name: "Aisyah Putri", attendance: "maybe" as const, message: "Insyaallah aku usahakan datang. Semoga menjadi keluarga yang sakinah, mawaddah, warahmah." },
];

export default function TadelaktMarokoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const label = data.eventLabel?.trim() || "Walimatul 'Ursy";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2f190e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.lampWrap} aria-hidden><Art name="lentera" eager /></div>
          <div className={s.coverText}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>{bride}<em>&amp; {groom}</em></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <Art name="pintu" eager className={s.door} />
            <div className={s.guestCol}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f0d49a" />Buka Undangan</button>
            </div>
            <Art name="permadani" eager className={s.rug} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        copy={COPY}
        demoWishes={WISHES}
        light="#f0d49a"
        dark="#3e2214"
        hero={(
          <header className={s.hero}>
            <div className={s.niche}><Art name="lentera" /></div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}<em>&amp; {groom}</em></h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="anyam" className={s.divider} />,
          closingDecor: <Art name="permadani" className={s.closingRug} />,
          closingEmblem: <Art name="lentera" className={s.closingLamp} />,
          sentArt: <Art name="lentera" />,
        }}
      />
    </ThemeShell>
  );
}
