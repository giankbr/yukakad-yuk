"use client";
// Theme "Merak Nouveau" — art nouveau dan bulu merak: kipas bulu merak yang dilukis (mata bernila dengan cincin toska,
// perunggu foil, zamrud, dan rumbai keemasan berserat halus) mekar di belakang gapura emas berhias garis lengkung
// whiplash, di atas sutra toska gelap yang berselang dengan kertas krem. Untuk pasangan Kristen Protestan.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Federant", "Sorts Mill Goudy:ital@0;1", "Italianno"];
// Painted by /tmp/pen/art/themes/merak-nouveau.py (tools/art/themes in the repo).
const Art = makeArt("merak-nouveau", {
  fan: [640, 346], frame: [450, 610], feather: [170, 658], eye: [120, 133], divider: [280, 44],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Syalom",
    title: "Salam Sejahtera dalam Kasih Kristus",
    sub: "Kasih itu sabar; kasih itu murah hati. Kasih tidak berkesudahan. (1 Korintus 13:4, 8)",
    intro: "Dengan penuh syukur atas kasih karunia Tuhan Yesus Kristus, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam ibadah pemberkatan nikah dan resepsi pernikahan kami, serta turut mendoakan langkah kami membangun keluarga.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dipersatukan dalam kasih", "Kedua Mempelai"] as [string, string],
  count: ["Menanti hari bahagia", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["Helai demi helai", "Kisah Kami"] as [string, string],
  gallery: ["Kenangan", "Galeri"] as [string, string],
  wishes: ["Doa & restu", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang menyempurnakan sukacita kami.",
    salam: "Tuhan Yesus memberkati",
  },
  attend: { maybe: "Mungkin" },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima. Tuhan memberkati.",
  closedNote: "Terima kasih atas doa dan kasih Anda. Ucapan masih dapat dikirim melalui formulir ini.",
};

export default function MerakNouveauTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  const arch = (eager: boolean, alt: string) => (
    <div className={s.archStage}>
      <span className={s.coverFan} aria-hidden><Art name="fan" eager={eager} /></span>
      <div className={s.archPhoto}>{photo ? <Photo src={photo} alt={alt} /> : null}</div>
      <span className={s.archFrame} aria-hidden><Art name="frame" eager={eager} /></span>
    </div>
  );

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0f3436"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverKicker}>{label === "Pernikahan" ? "The Wedding of" : label}</p>
          {arch(true, "")}
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#0c2a2b" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1dfa8"
        dark="#134446"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.coverKicker}>{label}</p>
            {arch(false, `${data.couple.bride} & ${data.couple.groom}`)}
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="eye" />,
          amp: <Art name="eye" />,
          portrait: <span className={s.portraitFeather} aria-hidden><Art name="feather" /></span>,
          countDecor: <span className={s.countFan} aria-hidden><Art name="fan" /></span>,
          closingDecor: <span className={s.closingFan} aria-hidden><Art name="fan" /></span>,
          closingEmblem: <Art name="eye" className={s.closingEmblem} />,
          sentArt: <Art name="eye" />,
        }}
      />
    </ThemeShell>
  );
}
