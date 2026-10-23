"use client";
// Theme "Bajo Laut" — kampung panggung suku Bajo di atas laut tosca: lukisan cat air rumah bertiang dan titian kayu,
// perahu lepa berlayar belang yang terapung (dan berlayar melintasi hitung mundur), padang lamun dan karang yang
// bergoyang pelan, tekstur jaring nelayan, tali dengan pelampung sebagai pemisah. Pasangan Muslim, Wakatobi.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,600;1,400;1,600", "Figtree:ital,wght@0,400;0,600;0,700;0,800;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/bajo-laut.py (net is a CSS background).
const Art = makeArt("bajo-laut", { village: [780, 560], lepa: [220, 177], reef: [780, 189], divider: [320, 20], sprig: [80, 79] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami mengundang Bapak/Ibu/Saudara/i untuk hadir di hari pernikahan kami, di kampung kami yang berdiri di atas laut. Kehadiran dan doa restu Anda adalah kebahagiaan bagi kami sekeluarga.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Hati, Satu Perahu", "Kedua Mempelai"],
  count: ["Menunggu Air Pasang", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Arus Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Cerita dari Laut"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan berlipat.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Terima kasih, doa dan ucapan Anda sudah sampai ke kampung kami.",
};

const WISHES = [
  { id: "w1", name: "Keluarga La Ode Hamiru", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma. Selamat Hasnah dan Ardi, semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Teman Relawan Karang Mola", attendance: "yes" as const, message: "Akhirnya! Selamat ya, kami datang naik perahu paling pagi. Semoga langgeng seperti karang yang kalian tanam." },
  { id: "w3", name: "Wa Rina, Kendari", attendance: "maybe" as const, message: "Insyaallah menyusul kalau cuaca bagus. Doa terbaik dari Kendari untuk kalian berdua." },
];

export default function BajoLautTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#d5ece8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.coverKicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.scene} aria-hidden>
            <Art name="village" eager className={s.village} />
            <Art name="lepa" eager className={s.coverLepa} />
          </div>
          <div className={s.sea}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#ffffff"
        dark="#163e48"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="divider" className={s.heroDivider} />
            <Art name="reef" className={s.heroReef} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="sprig" />,
          amp: <Art name="divider" />,
          countDecor: <span className={s.countLepa} aria-hidden><Art name="lepa" /></span>,
          closingDecor: <Art name="reef" className={s.closingReef} />,
          closingEmblem: <Art name="lepa" className={s.closingLepa} />,
          sentArt: <Art name="lepa" />,
        }}
      />
    </ThemeShell>
  );
}
