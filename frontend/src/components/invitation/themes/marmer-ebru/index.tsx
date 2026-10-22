"use client";
// Theme "Marmer Ebru" — Turkish-style paper marbling floated by simulation: blush, teal and ochre pigment raked into
// gel-git combs with threads of gold ink, laid on cold-press paper (original design). The cover is a bookbinder's
// endpaper with a pasted label plate; cards carry marbled fore-edges, the countdown sits on a teal feathered bath, and
// an ebru hatip bloom and a turning nightingale's-nest spiral are the ornaments.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;1,400", "Jost:wght@300;400;500"];
// Floated and combed by /tmp/pen/art/themes/marmer-ebru.py (tools/art/themes in the repo).
const Art = makeArt("marmer-ebru", { sheet: [780, 743], ribbon: [360, 42], hatip: [200, 199], yuva: [240, 240] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dua Warna, Satu Lembar",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan akad nikah dan walimah putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Bismillah", "Kedua Mempelai"] as [string, string],
  count: ["Menuju Hari Bahagia", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Lembar demi Lembar", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Warna yang Kami Kumpulkan"] as [string, string],
  wishes: ["Doa & Kehadiran", "Kirim Ucapan"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullahu Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakallahu khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

export default function MarmerEbruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe6d8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.endpaper} aria-hidden>
            <Art name="sheet" eager className={s.sheetArt} />
          </div>
          <div className={s.plate}>
            <Art name="hatip" eager className={s.plateBloom} />
            <p className={s.kicker}>The Wedding of</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#f4ece0" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f4ece0"
        dark="#1f4f4f"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.mat}>
              {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
            </div>
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="ribbon" className={s.divider} />,
          node: <Art name="hatip" />,
          amp: <Art name="hatip" />,
          portrait: <Art name="hatip" className={s.portraitBloom} />,
          countDecor: <span className={s.bath} aria-hidden />,
          closingDecor: <span className={s.bath} aria-hidden />,
          closingEmblem: <span className={s.nest} aria-hidden><Art name="yuva" /></span>,
          sentArt: <Art name="yuva" />,
        }}
      />
    </ThemeShell>
  );
}
