"use client";
// Theme "Sakura Sumi" — a sumi-e ink cherry branch with pale pink washed blossoms over fibrous washi, a vermilion
// hanko seal carrying the couple's initials, ink-wash mountains in the mist and a quiet, vertical, scroll-like rhythm.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import type { InvitationData } from "../../types";
import s from "./styles.module.css";

const FONTS = ["Shippori Mincho:wght@400;500;700", "Zen Kaku Gothic New:wght@400;500"];
// Painted by /tmp/pen/art/themes/sakura-sumi.py (tools/art/themes in the repo).
const Art = makeArt("sakura-sumi", { branch: [760, 397], sprig: [300, 94], petal: [44, 32], seal: [160, 158], wash: [640, 186] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Musim Bunga",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan kami. Seperti bunga yang mekar pada musimnya, kami berharap Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Hati", "Mempelai"] as [string, string],
  count: ["Menanti", "Hari yang Dinanti"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Acara", "Waktu & Tempat"] as [string, string],
  story: ["Kisah", "Perjalanan Kami"] as [string, string],
  gallery: ["Galeri", "Kenangan"] as [string, string],
  wishes: ["Doa", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah kebahagiaan yang mekar paling indah bagi kami.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
};

function initial(name?: string) {
  return (name?.trim().charAt(0) ?? "").toUpperCase();
}

function Hanko({ data, eager }: { data: InvitationData; eager?: boolean }) {
  const a = initial(data.couple.bride), b = initial(data.couple.groom);
  return (
    <span className={s.hanko} aria-hidden>
      <Art name="seal" eager={eager} />
      <b>{a}{b && <i>&amp;</i>}{b}</b>
    </span>
  );
}

export default function SakuraSumiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6dfd1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="branch" eager className={s.coverBranch} />
          <Art name="wash" eager className={s.coverMist} />
          <span className={s.petals} aria-hidden><Art name="petal" eager /><Art name="petal" eager /><Art name="petal" eager /><Art name="petal" eager /></span>
          <p className={s.coverVert} aria-hidden>{data.eventLabel ?? "Pernikahan"}</p>
          <div className={s.coverMain}>
            <p className={s.kicker}>Undangan {data.eventLabel ?? "Pernikahan"}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <div className={s.coverRow}>
              <Hanko data={data} eager />
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="currentColor" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#1d1a18"
        dark="#f4efe4"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="branch" className={s.heroBranch} />
            <div className={s.heroScroll}>
              {photo ? <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div> : <div className={s.heroPhoto} />}
            </div>
            <div className={s.heroSide}>
              <h1 className={s.heroVert}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <Hanko data={data} />
            </div>
            <div className={s.heroText}>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="petal" />,
          portrait: <span className={s.portraitSeal}><Hanko data={data} /></span>,
          closingEmblem: <span className={s.closingSeal}><Hanko data={data} /></span>,
          sentArt: <Art name="sprig" />,
        }}
      />
    </ThemeShell>
  );
}
