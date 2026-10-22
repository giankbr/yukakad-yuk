"use client";
// Theme "Rote Sasando" — pernikahan Kristen di Pulau Rote: sasando berdawai dalam kipas daun lontar berlipit (cat air),
// topi ti'i langga, pohon lontar dan laguna toska Nemberala. Nama rata kiri dengan dawai toska, potret berbentuk kipas
// sasando, hitung mundur dalam tabung bambu berdawai, kartu berpinggir anyaman lontar. Salam "Syalom".
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,500;0,600;1,400;1,500", "Nunito Sans:wght@400;700;800", "Sacramento"];
// Painted by /tmp/pen/art/themes/rote-sasando.py (tools/art/themes in the repo).
const Art = makeArt("rote-sasando", { nemberala: [700, 485], sasando: [543, 506], tiilangga: [220, 191], palm: [260, 490] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Syalom",
    title: "Dalam Kasih Tuhan",
    intro: "Dengan sukacita dan syukur atas kasih karunia Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan turut mendoakan pemberkatan nikah putra-putri kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Kedua Mempelai", "Dua Dawai, Satu Lagu"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Kisah Kami", "Dari Ba'a ke Nemberala"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang melengkapi sukacita kami sekeluarga.", salam: "Tuhan Yesus memberkati" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan berkat untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Pdt. Simon Lenggu", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru, Merlin dan Yosua. Kiranya kasih Kristus menjadi dasar rumah tangga kalian." },
  { id: "w2", name: "Paduan Suara Pemuda Imanuel", attendance: "yes" as Attendance, message: "Kami siap bernyanyi lagi bersama sasando di hari bahagia kalian. Tuhan berkati!" },
  { id: "w3", name: "Ince & Keluarga, Kupang", attendance: "maybe" as Attendance, message: "Mungkin hanya bisa hadir di resepsi Kupang. Doa kami menyertai kalian berdua." },
];

export default function RoteSasandoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#173447"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverText}>
            <p className={s.syalom}>Syalom</p>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <Art name="tiilangga" eager className={s.coverHat} />
          <div className={s.scene} aria-hidden>
            <Art name="nemberala" eager className={s.sceneArt} />
            <Art name="sasando" eager className={s.sasando} />
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f2d899" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f2d899"
        dark="#173447"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroFan}>
              {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
            </div>
            <p className={s.heroKicker}>Syalom</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="tiilangga" className={s.heroHat} />
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="tiilangga" /><i /></span>,
          node: <Art name="tiilangga" />,
          countDecor: <><Art name="palm" className={`${s.countPalm} ${s.countPalmL}`} /><Art name="palm" className={`${s.countPalm} ${s.countPalmR}`} /></>,
          closingDecor: <><Art name="palm" className={`${s.closingPalm} ${s.closingPalmL}`} /><Art name="palm" className={`${s.closingPalm} ${s.closingPalmR}`} /></>,
          closingEmblem: <Art name="sasando" className={s.closingEmblem} />,
          sentArt: <Art name="tiilangga" />,
        }}
      />
    </ThemeShell>
  );
}
