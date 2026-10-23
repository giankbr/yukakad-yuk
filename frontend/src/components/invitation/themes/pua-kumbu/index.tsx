"use client";
// Theme "Pua Kumbu" — adat Dayak Iban, Kapuas Hulu: kain pua kumbu tenun ikat lungsin (merah tanah engkudu, hitam,
// krem) dengan belah ketupat berkait, buaya dan pakis, tergantung di kayu; rumah panjai di tepi Kapuas saat senja.
// Seluruh motif dilukis ulang sebagai tenunan (tepi pewarna yang merembes sepanjang benang), bukan salinan kain asli.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Alegreya:ital,wght@0,400;0,700;1,400"];
// Painted by /tmp/pen/art/themes/pua-kumbu.py.
const Art = makeArt("pua-kumbu", { kain: [640, 484], betang: [640, 312], motif: [180, 197], patch: [220, 246], divider: [260, 35] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Sejahtera",
    title: "Dalam Kasih Kristus",
    sub: "Dua keluarga, satu tenunan",
    intro: "Dengan penuh syukur kepada Tuhan Yang Maha Kasih, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan memberikan doa restu pada pemberkatan nikah serta Gawai Melah Pinang putra-putri kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Yang Dipersatukan", "Kedua Mempelai"],
  count: ["Menuju Hari Bahagia", "Hitung Hari"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Benang Demi Benang", "Kisah Kami"],
  gallery: ["Galeri", "Kenangan Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Kado Pernikahan"],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang menguatkan kami memulai rumah tangga yang baru. Tuhan memberkati.",
    salam: "Salam sejahtera dari ruai rumah panjai",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima. Tuhan memberkati.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
  giftIntro: "Doa dan kehadiran Anda sudah menjadi hadiah terindah. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Ignasius Ngalai", attendance: "yes" as const, message: "Selamat menempuh hidup baru. Kiranya Tuhan memberkati rumah tangga kalian seperti pua yang kuat ditenun, rapat dan tak mudah koyak." },
  { id: "w2", name: "Sr. Agnes & umat Stasi Embaloh", attendance: "yes" as const, message: "Bahagia sekali melihat kalian dipersatukan. Doa kami menyertai, sampai jumpa di gereja dan di rumah panjai." },
  { id: "w3", name: "Rinto & teman-teman Sintang", attendance: "maybe" as const, message: "Semoga bisa ikut menyusul ke Sungai Utik. Selamat ya Natalia dan Yohanes, Tuhan memberkati!" },
];

export default function PuaKumbuTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();
  const initials = [data.couple.bride, groom].filter(Boolean).map(name => name!.slice(0, 1)).join("");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#170e0a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="kain" eager className={s.coverKain} />
          <div className={s.coverText}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <Art name="betang" eager className={s.coverBetang} />
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#5e2214" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#eadbbd"
        dark="#5e2214"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Gawai Melah Pinang</p>
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} dan ${groom ?? ""}`.trim()} /> : <span className={s.heroMono} aria-hidden>{initials}</span>}</div>
            </div>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="patch" />,
          amp: <Art name="motif" />,
          portrait: <Art name="patch" className={s.portraitArt} />,
          countDecor: <Art name="motif" className={s.countMotif} />,
          closingDecor: <Art name="betang" className={s.closingBetang} />,
          closingEmblem: <Art name="motif" className={s.closingEmblem} />,
          sentArt: <Art name="patch" />,
        }}
      />
    </ThemeShell>
  );
}
