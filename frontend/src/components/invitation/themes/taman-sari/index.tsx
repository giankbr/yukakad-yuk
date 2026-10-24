"use client";
// Theme "Taman Sari" — the Yogyakarta water castle in lime-plaster gouache and soft watercolour (original, inspired-by,
// architecture only): the cover looks through a tall carved gateway with a stepped crest at a turquoise bathing pool
// with mushroom fountains and bougainvillea urns on the coping. Limestone tablets with stepped crowns, the countdown as
// stepping stones over the pool, arched niches for photos, relief plaques as dividers, water that shimmers and ripples.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "Marcellus SC", "Lora:ital,wght@0,400;0,500;0,600;1,400"];
// Painted by /tmp/pen/art/themes/taman-sari.py (tools/art/themes in the repo).
const Art = makeArt("taman-sari", { gate: [780, 1118], pool: [780, 520], urn: [300, 414], relief: [420, 62] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Haryono", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka alaikuma. Semoga rumah tangga kalian sejernih air Taman Sari dan sekokoh gapuranya." },
  { id: "w2", name: "Dimas & Ayu (teman arsitektur)", attendance: "yes" as Attendance, message: "Dari sketsa gapura sampai pelaminan! Selamat menempuh hidup baru, Laras dan Bagas." },
  { id: "w3", name: "Bude Ning, Klaten", attendance: "maybe" as Attendance, message: "Mohon maaf bila berhalangan hadir. Doa kami menyertai, semoga sakinah, mawaddah, wa rahmah." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Pawiwahan Kami",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Putri", "Mempelai Putra"],
  couple: ["Kalih Dados Setunggal", "Kedua Mempelai"],
  count: ["Ngantos Dinten Bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Wekdal & Panggenan", "Rangkaian Acara"],
  story: ["Lampah Tresna", "Kisah Kami"],
  gallery: ["Galeri", "Kenangan di Taman"],
  wishes: ["Doa Restu", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Maturnuwun", text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
};

export default function TamanSariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#d9eeea"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="gate" eager className={s.gate} />
          <div className={s.coverInner}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffaf0" />Buka Undangan</button>
          </div>
          <div className={s.coverPool} aria-hidden>
            <Art name="pool" eager />
            <span className={s.shimmer} />
            <span className={s.ripple} style={{ left: "19%", top: "60%" }} />
            <span className={s.ripple} style={{ left: "81%", top: "60%", animationDelay: "-2.2s" }} />
            <Art name="urn" eager className={`${s.coverUrn} ${s.coverUrnL}`} />
            <Art name="urn" eager className={`${s.coverUrn} ${s.coverUrnR}`} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fffaf0"
        dark="#1d6a6d"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="relief" className={s.heroRelief} />
            {hero && <div className={s.heroWindow}><div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div></div>}
            {hero && <div className={s.heroWater} aria-hidden><span className={s.shimmer} /></div>}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="relief" className={s.divider} />,
          portrait: <Art name="urn" className={s.portraitUrn} />,
          closingEmblem: <Art name="relief" className={s.divider} />,
          closingDecor: (
            <div className={s.closingPool} aria-hidden>
              <Art name="pool" />
              <Art name="urn" className={s.closingUrn} />
              <Art name="urn" className={s.closingUrn} />
              <span className={s.shimmer} />
            </div>
          ),
          sentArt: <Art name="urn" />,
        }}
      />
    </ThemeShell>
  );
}
