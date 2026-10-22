"use client";
// Theme "Shan Shui" — lukisan tinta pegunungan Tionghoa (山水) di atas sutra tua: sampul berupa gulungan gantung yang
// terbuka perlahan, puncak-puncak berlapis kabut dengan pinus, paviliun, air terjun, dan perahu kecil; foto pasangan
// menjadi bulan di langit lukisan, nama ditulis tegak seperti inskripsi, stempel merah 囍, dan amplop angpao.
// Untuk pasangan Tionghoa-Indonesia beragama Buddha.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cormorant Upright:wght@400;500;600;700", "Spectral:ital,wght@0,400;0,500;1,400", "Ma Shan Zheng"];
// Painted by /tmp/pen/art/themes/shan-shui.py (tools/art/themes in the repo).
const Art = makeArt("shan-shui", {
  scroll: [560, 1064], range: [860, 258], pine: [300, 155], mist: [420, 132], rod: [450, 31], seal: [110, 111], divider: [260, 15],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam bahagia",
    title: "Namo Buddhaya",
    sub: "Dua aliran sungai bertemu di kaki gunung yang sama, lalu mengalir bersama menuju laut.",
    intro: "Dengan penuh rasa syukur dan berkah Tiratana, kami bermaksud melangsungkan pernikahan putra-putri kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua jiwa, satu jalan", "Kedua Mempelai"] as [string, string],
  count: ["Menuju hari baik", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["Perjalanan kami", "Kisah Kami"] as [string, string],
  gallery: ["Kenangan", "Galeri"] as [string, string],
  wishes: ["Doa & restu", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Angpao digital", "Tanda Kasih"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah berkah yang menyempurnakan kebahagiaan kami.",
    salam: "Semoga semua makhluk hidup berbahagia. Sadhu, sadhu, sadhu.",
  },
  attend: { maybe: "Mungkin" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim. Semoga Anda selalu berbahagia.",
  giftIntro: "Doa restu Anda adalah hadiah terindah. Bila berkenan memberikan angpao, dapat melalui:",
};

export default function ShanShuiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6dfcc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverKicker}>Undangan {label}</p>
          <div className={s.hanging}>
            <span className={s.rod} aria-hidden><Art name="rod" eager /></span>
            <div className={s.mount}>
              <div className={s.painting}>
                <span className={s.paintImg} aria-hidden><Art name="scroll" eager /></span>
                {photo && <div className={s.moon}><Photo src={photo} alt="" /></div>}
                <span className={s.paintMist} aria-hidden><Art name="mist" eager /></span>
                <h1 className={s.inscription}>
                  <strong>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</strong>
                </h1>
                <span className={s.sealSmall} aria-hidden>囍</span>
              </div>
            </div>
            <span className={s.rod} aria-hidden><Art name="rod" eager /></span>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f6f1e4" />Buka Gulungan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6f1e4"
        dark="#2a2826"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.coverKicker}>{label}</p>
            <div className={s.gate}>
              <div className={s.gatePhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : null}</div>
              <span className={s.gateMist} aria-hidden><Art name="mist" /></span>
              <span className={s.gateRange} aria-hidden><Art name="range" /></span>
            </div>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="seal" />,
          amp: <Art name="seal" />,
          portrait: <span className={s.portraitPine} aria-hidden><Art name="pine" /></span>,
          countDecor: (
            <>
              <span className={s.countRange} aria-hidden><Art name="range" /></span>
              <span className={s.countMist} aria-hidden><Art name="mist" /></span>
            </>
          ),
          closingDecor: (
            <>
              <span className={s.closingPine} aria-hidden><Art name="pine" /></span>
              <span className={s.closingRange} aria-hidden><Art name="range" /></span>
            </>
          ),
          closingEmblem: <span className={s.closingSeal} aria-hidden>囍</span>,
          sentArt: <Art name="seal" />,
        }}
      />
    </ThemeShell>
  );
}
