"use client";
// Theme "Lampung Tapis" — kain tapis yang dibentangkan: pita sulaman benang emas (couching) di atas lurik merah-hitam,
// siger Lampung sembilan lekuk berlapis emas, jendela foto bersudut tangga, dan kain kapal bertenun sebagai penutup.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Italiana", "EB Garamond:ital,wght@0,400;0,500;0,600;1,400", "Pinyon Script"];
// Painted by /tmp/pen/art/themes/lampung-tapis.py (tools/art/themes in the repo).
const Art = makeArt("lampung-tapis", { siger: [440, 237], kapal: [640, 323], divider: [320, 23] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Tabik Pun",
    title: "Assalamu'alaikum",
    sub: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kedua jurai keluarga apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Muli & Mekhanai", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Restu", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami dan kedua jurai keluarga besar mengucapkan terima kasih.", salam: "Tabik pun · Wassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
};

export default function LampungTapisTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3a0a10"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverBand} aria-hidden />
          <Art name="siger" eager className={s.siger} />
          <p className={s.kicker}>Tabik Pun</p>
          <p className={s.coverLabel}>Undangan {label}</p>
          {hero && <div className={s.window}><Photo src={hero} alt="" /></div>}
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>dan</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#4a0b12" />Buka Undangan</button>
          </div>
          <span className={s.coverBand} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0d38a"
        dark="#4a0b12"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <span className={s.heroBand} aria-hidden />
            <Art name="siger" className={s.siger} />
            <p className={s.heroKicker}>Sai Bumi Ruwa Jurai</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="kapal" className={s.heroKapal} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          amp: <Art name="divider" />,
          closingEmblem: <Art name="kapal" className={s.closingKapal} />,
          sentArt: <Art name="siger" />,
        }}
      />
    </ThemeShell>
  );
}
