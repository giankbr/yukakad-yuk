"use client";
// Theme "Sabana Afrika" — sabana senja dalam pita gouache tebal: langit berpita terung, anggur, jingga dan emas,
// matahari raksasa yang rendah, akasia berpuncak datar, jerapah dan kawanan gajah dalam siluet, rumput emas.
// Sampul berupa poster sabana penuh (nama di langit gelap, tamu di atas rumput gelap), potret cakram matahari,
// kartu acara berkepala pita senja, dan cakrawala siluet dengan jerapah yang berjalan di pita hitung mundur.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Shrikhand:wght@400", "Spectral:ital,wght@0,400;0,600;0,700;1,400", "Archivo:wght@400;700;800"];
// Painted by /tmp/pen/art/themes/sabana-afrika.py (paper tile and ridge strip are CSS backgrounds)
const Art = makeArt("sabana-afrika", { scene: [720, 1300], ridge: [900, 211], acacia: [360, 237], giraffe: [158, 273], sun: [260, 259], stripes: [340, 36] } as const);

export default function SabanaAfrikaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2f1528"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="scene" eager className={s.scene} />
          <span className={s.sunGlow} aria-hidden />
          <div className={s.coverTop}>
            <p className={s.kicker}>Undangan Pernikahan</p>
            <h1 className={s.coverNames}><span>{bride}</span><em>&amp;</em><span>{groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#2f1528" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffd681"
        dark="#561d33"
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Salam Sejahtera",
            title: "Dengan Sukacita",
            intro: "Dengan penuh syukur kepada Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan berbagi kebahagiaan di hari pernikahan kami, di bawah langit senja yang selalu kami cintai.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Pengembara", "Mempelai"],
          count: ["Menuju senja itu", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat Tanggalnya", "Rangkaian Acara"],
          story: ["Jejak Perjalanan", "Kisah Kami"],
          gallery: ["Potret", "Galeri Senja"],
          wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
          gifts: ["Tanda Kasih", "Hadiah Pernikahan"],
          closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah senja terindah yang bisa kami harapkan di hari bahagia kami." },
          sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
          attend: { maybe: "Mungkin" },
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Di bawah langit senja</p>
            <div className={s.pano}>
              {photo ? <div className={s.heroPhoto}><Photo src={photo} alt={`${bride} & ${groom}`} /></div> : <Art name="sun" className={s.panoSun} />}
              <Art name="ridge" className={s.panoRidge} />
            </div>
            <h1 className={s.heroNames}>{bride} <em>&amp;</em> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="stripes" className={s.divider} />,
          node: <Art name="sun" />,
          amp: <Art name="giraffe" />,
          portrait: <Art name="acacia" className={s.portraitTree} />,
          countDecor: <><span className={s.countRidge} aria-hidden /><span className={s.walker} aria-hidden><Art name="giraffe" /></span></>,
          closingDecor: <span className={s.closeRidge} aria-hidden />,
          closingEmblem: <Art name="sun" className={s.emblem} />,
          sentArt: <Art name="sun" />,
        }}
      />
    </ThemeShell>
  );
}
