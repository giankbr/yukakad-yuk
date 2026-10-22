"use client";
// Theme "Riso Cetak" — a risograph-printed zine: two spot inks (fluorescent pink + blue) with halftone dots,
// misregistered overprints and soy-ink grain on cream stock. Huge grotesque type, two-plate duotone photos (CSS blend
// plates), offset-shadow blocks and a hand-printed halftone flower.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bricolage Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800", "Space Mono"];
// Printed by /tmp/pen/art/themes/riso-cetak.py (tools/art/themes in the repo); every asset is a multiply plate.
const Art = makeArt("riso-cetak", { bloom: [420, 423], seal: [150, 147], squiggle: [360, 25], blob: [280, 315] } as const);

const COPY = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Namo Buddhaya",
    title: "Kami Menikah",
    intro: "Dengan penuh sukacita dan atas berkah Tiratana, kami mengundang Bapak/Ibu/Saudara/i untuk hadir, berbagi kebahagiaan, dan memberikan doa restu di hari pernikahan kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["01 — Kami", "Dua Tinta"] as [string, string],
  count: ["02 — Hitung Mundur", "Naik Cetak Dalam"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["03 — Jadwal", "Waktu & Tempat"] as [string, string],
  story: ["04 — Arsip", "Cerita Kami"] as [string, string],
  gallery: ["05 — Cetakan", "Galeri"] as [string, string],
  wishes: ["06 — Kolom Pembaca", "Ucapan & RSVP"] as [string, string],
  gifts: ["07 — Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah warna terbaik untuk lembar baru kami.",
    salam: "Sabbe satta bhavantu sukhitatta. Semoga semua makhluk berbahagia.",
  },
  sent: "Terima kasih! Ucapan Anda sudah masuk ke mesin cetak kami.",
  wishPlaceholder: "Tulis ucapan dan doa untuk Vania & Kelvin…",
};

/** Two-plate risograph duotone: a grey pink plate + a high-contrast blue plate, slightly misregistered. */
function Duo({ src, alt, className }: { src?: string; alt: string; className?: string }) {
  return (
    <div className={`${s.duo} ${className ?? ""}`}>
      <span className={s.plateP}><Photo src={src} alt={alt} /></span>
      {src && (
        <span className={s.plateB} aria-hidden>
          {/* eslint-disable-next-line @next/next/no-img-element -- decorative second print plate of the same photo */}
          <img src={src} alt="" data-nolightbox draggable={false} loading="lazy" decoding="async" />
        </span>
      )}
    </div>
  );
}

export default function RisoCetakTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();
  const copy = { ...COPY, wishPlaceholder: `Tulis ucapan dan doa untuk ${data.couple.bride} & ${data.couple.groom}…` };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9e2d3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.masthead}><span>Edisi Khusus</span><span>{year ?? "—"}</span></p>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.coverStage} aria-hidden>
            <Duo src={photo} alt="" className={s.coverPhoto} />
            <Art name="bloom" eager className={s.coverBloom} />
          </div>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#f6f1e7" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6f1e7"
        dark="#1d2a7a"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}><span>{label}</span><span>{year ?? ""}</span></p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            {photo && (
              <div className={s.heroPhoto}>
                <Duo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} className={s.fill} />
                <Art name="seal" className={s.heroBloom} />
              </div>
            )}
            <p className={s.heroDate}>{formatDate(data.date)} · {data.place}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="squiggle" className={s.divider} />,
          node: <Art name="seal" />,
          portrait: <Art name="blob" className={s.blob} />,
          countDecor: <Art name="seal" className={s.countSeal} />,
          closingEmblem: <Art name="seal" className={s.closeSeal} />,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
