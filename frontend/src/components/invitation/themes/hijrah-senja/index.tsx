"use client";
// Theme "Hijrah Senja" — walimah bernuansa gurun saat senja: langit cat air aprikot ke plum, bulan sabit, bukit pasir
// berlapis dengan cahaya terakhir, kafilah unta kecil di kejauhan, dan lentera kuningan yang menyala berayun pelan.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["DM Serif Display", "Lora:ital,wght@0,400;0,500;1,400", "Parisienne", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/hijrah-senja.py (scene, dunes and sand are CSS backgrounds)
const Art = makeArt("hijrah-senja", { lantern: [220, 480], divider: [300, 33] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

export default function HijrahSenjaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#24152f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="lantern" eager className={s.lampL} />
          <Art name="lantern" eager className={s.lampR} />
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#2a1830" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3d29a"
        dark="#2a1830"
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Menuju Rida-Nya, Bersama",
            intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan akad dan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Musafir", "Kedua Mempelai"],
          count: ["Sebelum Senja Tiba", "Menghitung Hari"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Jejak di Pasir", "Perjalanan Kami"],
          gallery: ["Galeri", "Potret Senja"],
          wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah bekal terbaik bagi perjalanan kami. Semoga Allah membalasnya dengan kebaikan.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="lantern" className={s.heroLampL} />
            <Art name="lantern" className={s.heroLampR} />
            {hero && <div className={s.heroArch}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          amp: <Art name="divider" />,
          portrait: <Art name="lantern" className={s.portraitLantern} />,
          closingEmblem: <div className={s.closingLamps}><Art name="lantern" /><Art name="lantern" /></div>,
          sentArt: <Art name="lantern" />,
        }}
      />
    </ThemeShell>
  );
}
