"use client";
// Theme "Simalungun Bolon" — pernikahan Kristen Simalungun: rumah bolon berfondasi balok bersilang dengan atap ijuk
// bermahkota tanduk dan bidang singap merah-putih-hitam, berdiri di punggung bukit timur Danau Toba yang berkabut (cat
// air, dilihat lewat bingkai lonjong); kain hiou merah tua ditenun per benang dengan rambu terpilin menggantung di tepi
// sampul dan penutup; pita spiral berwarna tiga. Gading, merah hiou, hitam, dan biru danau.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Castoro:ital@0;1", "Literata:ital,wght@0,400;0,600;1,400"];
// Painted by /tmp/pen/art/themes/simalungun-bolon.py (tools/art/themes in the repo).
const Art = makeArt("simalungun-bolon", { bolon: [760, 877], hiou: [150, 522], gorga: [780, 84], atap: [140, 129] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Horas!",
    title: "Salam Sejahtera",
    intro: "Dengan penuh syukur kepada Tuhan Yang Maha Kasih, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam pemberkatan nikah dan pesta adat putra-putri kami. Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat bagi kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Kedua Mempelai", "Dua Benang, Satu Hiou"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Kisah Kami", "Dari Tepian Toba"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Diatei Tupa", text: "Terima kasih atas kehadiran, doa, dan kasih Bapak/Ibu/Saudara/i. Tuhan memberkati kita sekalian.", salam: "Horas! Horas! Horas!" },
  sent: "Diatei tupa, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan berkat untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga Pdt. Rudolf Sinaga", attendance: "yes" as Attendance, message: "Horas! Selamat menempuh hidup baru. Kiranya Tuhan memberkati rumah tangga kalian dan menjadikannya saksi kasih-Nya." },
  { id: "w2", name: "Naposo GKPS Parapat", attendance: "yes" as Attendance, message: "Selamat Lestari dan Jonatan! Semoga paduan suara di rumah kalian selalu harmonis." },
  { id: "w3", name: "Tulang Mardin & Keluarga, Pematangsiantar", attendance: "maybe" as Attendance, message: "Kami usahakan datang. Doa terbaik dari kami sekeluarga, horas ma!" },
];

export default function SimalungunBolonTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3efe6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="hiou" eager className={`${s.hiou} ${s.hiouL}`} />
          <Art name="hiou" eager className={`${s.hiou} ${s.hiouR}`} />
          <p className={s.horas}>Horas!</p>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.lens} aria-hidden><span className={s.lensIn}><Art name="bolon" eager /></span></div>
          <h1 className={s.coverNames}>{data.couple.bride}<em>pakon</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fcfaf5" />Buka Undangan</button>
          </div>
          <Art name="gorga" eager className={s.coverGorga} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#e8cf9a"
        dark="#7a1a22"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Horas!</p>
            {hero && <div className={s.heroOval}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>}
            <Art name="gorga" className={s.heroBand} />
            <h1 className={s.heroNames}>{data.couple.bride}<em>pakon</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="atap" /><i /></span>,
          node: <Art name="atap" />,
          amp: <Art name="atap" />,
          countDecor: <Art name="gorga" className={s.countGorga} />,
          closingDecor: <><Art name="hiou" className={s.closeHiou} /><Art name="hiou" className={s.closeHiou} /></>,
          closingEmblem: <Art name="atap" className={s.closingEmblem} />,
          sentArt: <Art name="atap" />,
        }}
      />
    </ThemeShell>
  );
}
