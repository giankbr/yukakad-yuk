"use client";
// Theme "Shibori Indigo" — katun celup indigo dengan pola rintang shibori: noren arashi (lilit tiang) yang terbelah di
// sampul, petak itajime (lipat-jepit), ledakan kumo (ikat laba-laba), dan jahitan ori-nui; rembesan pewarna pada serat
// dan tenunan polos. Tata letak Jepang-modern yang tenang, rata kiri, dengan banyak ruang kosong.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Crimson Pro:ital,wght@0,300;0,400;0,600;1,300;1,400", "Outfit:wght@300;400;500;600"];
// Painted by /tmp/pen/art/themes/shibori-indigo.py (tools/art/themes in the repo).
const Art = makeArt("shibori-indigo", {
  kumo: [260, 260], stitch: [320, 36], swatch: [220, 222],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Namo Buddhaya",
    title: "Dua Helai Kain, Satu Celupan",
    sub: "Semoga Tiratana senantiasa memberkahi",
    intro: "Dengan penuh rasa syukur dan sukacita, kami bermaksud melangsungkan pemberkatan pernikahan putra-putri kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Yang Dipertemukan", "Kedua Mempelai"] as [string, string],
  count: ["Celupan Terakhir", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Simpul demi Simpul", "Kisah Kami"] as [string, string],
  gallery: ["Lembar Kenangan", "Galeri"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah warna terindah dalam lembar baru kehidupan kami.",
    salam: "Sabbe satta bhavantu sukhitatta, semoga semua makhluk hidup berbahagia.",
  },
  attend: { maybe: "Mungkin" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim. Semoga berbahagia.",
};

export default function ShiboriIndigoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efede6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.noren} aria-hidden>
            <span className={s.panel} />
            <span className={s.panel} />
            <span className={s.norenMark}><Art name="kumo" eager /></span>
          </div>
          <p className={s.norenKicker}>{label}</p>
          <div className={s.coverBody}>
            {photo ? <Photo src={photo} alt="" className={s.coverPhoto} /> : <span className={s.coverPhoto} aria-hidden />}
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f1efe8" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1efe8"
        dark="#1c2f5e"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroCloth} aria-hidden />
            {photo && <div className={s.heroPhotoBox}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
            <div className={s.heroText}>
              <p className={s.coverKicker}>{label}</p>
              <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
              <Art name="stitch" className={s.heroStitch} />
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="stitch" className={s.divider} />,
          node: <Art name="kumo" />,
          amp: <Art name="stitch" />,
          portrait: <span className={s.portraitSwatch} aria-hidden><Art name="swatch" /></span>,
          countDecor: (
            <>
              <span className={`${s.countKumo} ${s.countKumoA}`} aria-hidden><Art name="kumo" /></span>
              <span className={`${s.countKumo} ${s.countKumoB}`} aria-hidden><Art name="kumo" /></span>
            </>
          ),
          closingEmblem: <Art name="kumo" className={s.closingKumo} />,
          sentArt: <Art name="kumo" />,
        }}
      />
    </ThemeShell>
  );
}
