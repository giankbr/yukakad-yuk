"use client";
// Theme "Padang Liar" — padang bunga liar yang dilukis cat air longgar: cosmos merah muda, chamomile, cornflower biru,
// rumput liar dan kupu-kupu kuning. Foto pasangan terbit seperti matahari pagi di balik padang yang bergoyang tertiup angin.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,500;0,600;1,400;1,500", "Karla:wght@400;600;700", "Caveat:wght@500;600"];
// Painted by /tmp/pen/art/themes/padang-liar.py (tools/art/themes in the repo).
const Art = makeArt("padang-liar", {
  meadow: [820, 443], cosmos: [230, 736], tuft: [210, 271], posy: [300, 409], sprig: [340, 52], kupu: [100, 73], daisy: [80, 78],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Salam kasih,",
    title: "Di Padang Berbunga",
    intro: "Dengan penuh syukur atas kasih Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir, berdoa, dan berbahagia bersama kami di hari pernikahan kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["dua bunga, satu padang", "Kedua Mempelai"],
  count: ["sebentar lagi", "Menuju Hari Bahagia"],
  units: ["hari", "jam", "menit", "detik"],
  events: ["catat tanggalnya", "Waktu & Tempat"],
  story: ["dari bibit hingga mekar", "Kisah Kami"],
  gallery: ["lembar-lembar kenangan", "Galeri"],
  wishes: ["titip doa", "Ucapan & Kehadiran"],
  gifts: ["tanda kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah bunga terindah di hari bahagia kami. Tuhan memberkati.", salam: "Sampai jumpa di padang bunga" },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa dan harapan untuk kami berdua…",
};

export default function PadangLiarTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dfeaee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffdf7" />Buka Undangan</button>
          </div>
          <div className={s.stage} aria-hidden>
            {photo && <div className={s.sunPhoto}><Photo src={photo} alt="" /></div>}
            <Art name="meadow" eager className={s.stageMeadow} />
            <span className={`${s.sway} ${s.swayL}`}><Art name="cosmos" eager /></span>
            <span className={`${s.sway} ${s.swayR}`}><Art name="tuft" eager /></span>
            <span className={s.kupu}><Art name="kupu" eager /></span>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        light="#fffdf7"
        dark="#2f3a25"
        hero={(
          <header className={s.hero}>
            {photo ? <div className={s.heroPhoto}><Photo src={photo} alt="" /></div> : <div className={s.heroArt}><Art name="meadow" /></div>}
            <span className={s.heroSprig}><Art name="sprig" /></span>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {data.place && <p className={s.heroPlace}>{data.place}</p>}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="daisy" />,
          amp: <Art name="daisy" />,
          portrait: <span className={s.posyWrap}><Art name="posy" /></span>,
          countDecor: <span className={s.countMeadow} aria-hidden />,
          closingEmblem: (
            <div className={s.closingStage} aria-hidden>
              <Art name="meadow" className={s.meadowImg} />
              <span className={s.closingPosy}><Art name="posy" /></span>
              <span className={s.closingKupu}><Art name="kupu" /></span>
            </div>
          ),
          sentArt: <Art name="posy" />,
        }}
      />
    </ThemeShell>
  );
}
