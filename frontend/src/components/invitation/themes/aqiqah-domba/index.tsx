"use client";
// Theme "Aqiqah Domba" — tasyakuran aqiqah di padang hijau: domba berbulu lembut (kuas kering di atas cat air), padang
// bunga aster, awan pastel yang melayang, ranting aster sebagai pemisah, dan kartu arti nama sang buah hati.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Mulish:wght@400;600;700;800", "Amiri"];
// Painted by /tmp/pen/art/themes/aqiqah-domba.py (tools/art/themes in the repo).
const Art = makeArt("aqiqah-domba", {
  lamb: [340, 286], rest: [260, 131], meadow: [640, 195], "cloud-0": [220, 119], "cloud-1": [220, 112], sprig: [300, 36], daisy: [72, 75],
} as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

export default function AqiqahDombaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Aqiqah";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const full = child?.name.trim() || data.couple.brideFull?.trim();
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const meaning = child?.meaning?.trim();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      arabic: BISMILLAH,
      kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
      title: `Tasyakuran ${label}`,
      intro: `Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan tasyakuran ${label.toLowerCase()} buah hati kami, ${names}, sebagai wujud syukur atas karunia-Nya. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.`,
    },
    roles: ["Buah Hati Kami", "Bersama"] as [string, string],
    couple: ["Amanah dari Allah", child ? "Sang Buah Hati" : "Yang Didoakan"] as [string, string],
    count: ["Menanti Hari Syukur", "Menuju Hari Aqiqah"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
    story: ["Perjalanan Kecil", `Kisah ${nick}`] as [string, string],
    gallery: ["Galeri", "Momen Bahagia"] as [string, string],
    wishes: ["Doa untuk Si Kecil", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Kasih", "Kado & Amplop Digital"] as [string, string],
    closing: {
      thanks: "Jazakumullah Khairan",
      text: `Atas kehadiran dan doa Bapak/Ibu/Saudara/i untuk ${names}, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas dengan kebaikan berlipat.`,
      salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
    },
    wishPlaceholder: `Tuliskan doa terbaik untuk ${names}…`,
    sent: "Jazakumullah khairan, doa Anda sudah terkirim.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#eaf2fb"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="cloud-0" eager className={`${s.cloud} ${s.cloudA}`} />
          <Art name="cloud-1" eager className={`${s.cloud} ${s.cloudB}`} />
          <Art name="cloud-0" eager className={`${s.cloud} ${s.cloudC}`} />
          <p className={s.bismillah} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.pill}>Tasyakuran {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {child && full && full !== nick && <p className={s.coverFull}>{full}</p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffaf2" />Buka Undangan</button>
          </div>
          <div className={s.field1} aria-hidden>
            <Art name="meadow" eager className={s.meadow} />
            <Art name="lamb" eager className={s.lamb} />
            <Art name="rest" eager className={s.rest} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fffaf2"
        dark="#3f733d"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <Art name="cloud-1" className={`${s.cloud} ${s.cloudA}`} />
            <Art name="cloud-0" className={`${s.cloud} ${s.cloudB}`} />
            <p className={s.pill}>Tasyakuran {label}</p>
            <h1 className={s.coverName}>{names}</h1>
            {child && full && full !== nick && <p className={s.coverFull}>{full}</p>}
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <Art name="lamb" className={s.heroLamb} />
            {meaning && <div className={s.meaning}><small>Arti Nama</small><p>{meaning}</p></div>}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="daisy" />,
          portrait: <Art name="sprig" className={s.portraitSprig} />,
          countDecor: <><Art name="cloud-0" className={`${s.countCloud} ${s.countCloudA}`} /><Art name="cloud-1" className={`${s.countCloud} ${s.countCloudB}`} /></>,
          closingDecor: (
            <div className={s.field2} aria-hidden>
              <Art name="meadow" className={s.meadow} />
              <Art name="lamb" className={s.lamb} />
              <Art name="rest" className={s.rest} />
            </div>
          ),
          sentArt: <Art name="daisy" />,
        }}
      />
    </ThemeShell>
  );
}
