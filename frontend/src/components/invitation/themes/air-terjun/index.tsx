"use client";
// Theme "Air Terjun" — a rainforest waterfall painted in gouache: basalt cliffs with moss and hanging vines, a white
// water column (with a moving shimmer layer and pulsing spray), a turquoise plunge pool, mossy boulders and big ferns.
// Names sit in the morning mist; the guest panel is frosted over the ferns.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500", "Karla:wght@400;500;700;800"];
// Painted by /tmp/pen/art/themes/air-terjun.py (tools/art/themes in the repo).
const Art = makeArt("air-terjun", { scene: [600, 1080], fern: [300, 301], frond: [320, 40], stone: [72, 50] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan Penuh Sukacita",
    title: "Seperti air yang menemukan jalannya",
    intro: "Dengan penuh syukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan merayakan hari pernikahan kami di tengah hutan, ditemani suara air dan sejuknya kabut. Kehadiran dan doa Anda akan melengkapi kebahagiaan kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Aliran, Satu Muara", "Kedua Mempelai"],
  count: ["Menuju Hari Bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Jejak di Jalur Setapak", "Kisah Kami"],
  gallery: ["Galeri", "Momen di Alam"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih yang sebesar-besarnya." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan untuk kedua mempelai masih bisa dikirim lewat form ini.",
};

export default function AirTerjunTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1f3d30"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.stage} aria-hidden>
            <Art name="scene" eager className={s.scene} />
            <span className={s.falls} />
            <span className={s.spray} />
          </div>
          <div className={s.coverTop}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          </div>
          <div className={s.panel}>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#123a2e" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffffff"
        dark="#123a2e"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            {hero
              ? (
                <div className={s.heroFrame}>
                  <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                  <Art name="fern" className={s.heroFern} />
                  <Art name="fern" className={s.heroFern2} />
                </div>
              )
              : <Art name="fern" className={s.heroArt} />}
            <h1 className={s.heroNames}>{data.couple.bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="frond" className={s.divider} />,
          node: <Art name="stone" />,
          portrait: <Art name="fern" className={s.portraitFern} />,
          closingEmblem: <Art name="frond" className={s.closingFrond} />,
          sentArt: <Art name="fern" />,
        }}
      />
    </ThemeShell>
  );
}
