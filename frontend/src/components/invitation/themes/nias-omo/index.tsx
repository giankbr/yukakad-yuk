"use client";
// Theme "Nias Omo Sebua" — hitam, merah, kuning, dan emas: rumah Omo Sebua bergaya gouache di atas tiang ehomo
// dan tiang silang driwa, atap jerami menjulang di bawah langit oker, pita ukiran kayu bercat merah-kuning seperti
// cetakan cukil, dan roset ukir sebagai lambang. Sampul: rumah menjulang di atas alas hitam bertuliskan nama.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rozha One", "Alegreya:ital,wght@0,400;0,700;0,800;1,400"];
// Painted by /tmp/pen/art/themes/nias-omo.py (tools/art/themes in the repo).
const Art = makeArt("nias-omo", { omo: [700, 858], divider: [354, 50], rosette: [180, 178] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Kasih",
    title: "Ya'ahowu!",
    sub: "“Kasih itu sabar; kasih itu murah hati. Ia menutupi segala sesuatu, percaya segala sesuatu, mengharapkan segala sesuatu.” — 1 Korintus 13:4, 7",
    intro: "Dengan sukacita dan syukur kepada Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam pemberkatan nikah dan pesta pernikahan putra-putri kami. Kehadiran dan doa Anda adalah berkat bagi keluarga besar kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dipersatukan Tuhan", "Kedua Mempelai"],
  count: ["Menanti Hari Bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan Kami", "Kisah Cinta"],
  gallery: ["Galeri", "Momen Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Saohagölö", text: "Terima kasih atas kehadiran, doa, dan kasih Bapak/Ibu/Saudara/i bagi kami. Ya'ahowu!", salam: "Tuhan memberkati" },
  sent: "Saohagölö, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan berkat untuk kedua mempelai…",
};

export default function NiasOmoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#151010"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}>
            <p className={s.coverKicker}>Ya&apos;ahowu!</p>
            <p className={s.coverLabel}>Undangan {label}</p>
          </div>
          <Art name="omo" eager className={s.coverHouse} />
          <div className={s.coverBody}>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#151010" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f8ecd2"
        dark="#151010"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            {hero && <span className={s.heroShade} aria-hidden />}
            <div className={hero ? s.heroText : `${s.heroText} ${s.noPhoto}`}>
              <p className={s.heroKicker}>Undangan {label}</p>
              <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
            <span className={s.heroBeam} aria-hidden />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          closingEmblem: <Art name="rosette" className={s.closingRosette} />,
          sentArt: <Art name="rosette" />,
        }}
      />
    </ThemeShell>
  );
}
