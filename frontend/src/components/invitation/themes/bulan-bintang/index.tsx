"use client";
// Theme "Bulan Bintang" — syari tanpa foto: langit malam pastel (periwinkle ke lilac) dilukis cat air, bulan sabit krem
// berpendar, bintang empat sudut yang berkelip pelan, awan bergumpal tempat kartu tamu bersandar, dan medali monogram
// bertepi bintang. Tanpa makhluk bernyawa, tanpa kaligrafi yang dilukis (basmalah diketik).
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bellefair", "Mulish:ital,wght@0,400;0,600;0,700;1,400", "Italianno", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/bulan-bintang.py (tools/art/themes in the repo).
const Art = makeArt("bulan-bintang", { moon: [440, 451], clouds: [780, 260], puff: [260, 90], star: [80, 80], medallion: [420, 420], divider: [320, 30] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan keberkahan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bulan & Bintangnya", "Kedua Mempelai"],
  count: ["Menghitung Malam", "Menuju Hari Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan cahaya yang lebih terang.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakallah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Ustadzah Rahmah", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga rumah kalian selalu diterangi cahaya iman." },
  { id: "w2", name: "Teman Remaja Masjid", attendance: "yes" as Attendance, message: "Alhamdulillah, ikut bahagia! Semoga sakinah, mawaddah, warahmah sampai jannah." },
  { id: "w3", name: "Keluarga Om Rizal", attendance: "maybe" as Attendance, message: "Insyaallah hadir bila tidak ada halangan. Doa terbaik dari kami sekeluarga." },
];

export default function BulanBintangTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const initials = [data.couple.bride, data.couple.groom].map(name => name?.trim().slice(0, 1)).filter(Boolean);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#8f9bd8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="moon" eager className={s.coverMoon} />
          <Art name="puff" eager className={s.coverPuff} />
          {[s.s1, s.s2, s.s3, s.s4, s.s5].map(c => <Art key={c} name="star" eager className={`${s.coverStar} ${c}`} />)}
          <p className={s.arabicCover} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.coverLabel}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.cloudBed}>
            <Art name="clouds" eager />
            <div className={s.guestCard}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffaf3" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#fff1cc"
        dark="#5a5fa6"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            {[s.h1s, s.h2s, s.h3s].map(c => <Art key={c} name="star" className={`${s.heroStar} ${c}`} />)}
            <div className={s.heroMedal}>
              <Art name="medallion" />
              <p className={s.heroMono} aria-hidden>{initials[0]}{initials[1] && <><i>&amp;</i>{initials[1]}</>}</p>
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroClouds}><Art name="clouds" /></div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          portrait: <Art name="medallion" className={s.pMedal} />,
          countDecor: (
            <div className={s.countDecor} aria-hidden>
              <Art name="moon" className={s.cdMoon} />
              <Art name="star" className={s.cdStar} />
              <Art name="star" className={s.cdStar} />
              <Art name="star" className={s.cdStar} />
              <Art name="clouds" className={s.cdClouds} />
            </div>
          ),
          closingDecor: <div className={s.closingDecor} aria-hidden><Art name="puff" className={s.clPuff} /><Art name="clouds" className={s.clClouds} /></div>,
          closingEmblem: <Art name="moon" className={s.closingMoon} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
