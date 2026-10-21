"use client";
// Theme "Tenun NTT" — kain tenun ikat Sumba yang dirender sampai ke tingkat benang (nila, karat, krem) dengan motif kuda
// dan ayam jantan geometris (desain orisinal), rumah kerucut Mbaru Niang di sabana senja, kartu persegi berumbai benang.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Barlow:wght@400;600", "EB Garamond:ital,wght@0,400;0,500;0,600;1,400"];
// Painted/woven by /tmp/pen/art/themes/ntt-tenun.py (tools/art/themes in the repo).
const Art = makeArt("ntt-tenun", { scene: [720, 480], kuda: [200, 162], ayam: [170, 159] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Syalom",
    title: "Salam Damai",
    intro: "Atas kasih dan penyertaan Tuhan, kami bermaksud mempersatukan dua keluarga dalam ikatan pernikahan kudus. Merupakan sukacita bagi kami bila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
  couple: ["Dua Benang, Satu Kain", "Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Tenunan Kisah", "Perjalanan Kami"],
  gallery: ["Galeri", "Momen Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Doa dan kehadiran Bapak/Ibu/Saudara/i adalah anugerah yang menghangatkan hati kami sekeluarga.", salam: "Tuhan memberkati" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
};

export default function NttTenunTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#141c38"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.colL} aria-hidden />
          <span className={s.colR} aria-hidden />
          <p className={s.salam}>Syalom</p>
          <p className={s.kicker}>Undangan {label}</p>
          {photo && <div className={s.coverPhoto}><Photo src={photo} alt="" /></div>}
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf3e2" />Buka Undangan</button>
          </div>
          <Art name="scene" eager className={s.coverScene} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        light="#f3d9a4"
        dark="#22305a"
        hero={(
          <header className={s.hero}>
            <span className={s.band} aria-hidden />
            {photo && <div className={s.heroPhoto}><Photo src={photo} alt="" /></div>}
            {photo && <Art name="kuda" className={s.heroKuda} />}
            <p className={s.kickerDark}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden />,
          node: <Art name="ayam" />,
          amp: <Art name="kuda" />,
          countDecor: <><span className={`${s.band} ${s.countDecor} ${s.countDecorT}`} aria-hidden /><span className={`${s.band} ${s.countDecor} ${s.countDecorB}`} aria-hidden /></>,
          closingDecor: <span className={s.band} aria-hidden />,
          closingEmblem: <Art name="scene" className={s.closingScene} />,
          sentArt: <Art name="kuda" />,
        }}
      />
    </ThemeShell>
  );
}
