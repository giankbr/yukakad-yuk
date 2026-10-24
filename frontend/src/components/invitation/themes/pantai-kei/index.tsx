"use client";
// Theme "Pantai Kei" — adat Maluku, Kepulauan Kei: cakrawala laut tosca berlapis dengan pulau berkabut, perahu kayu Evav
// berhaluan ukir yang terayun, nyiur condong, pasir putih sehalus tepung dan pita tenun Kei merah-hitam-oker. Sampulnya
// membelah layar: laut di atas, nama mempelai tertulis di atas hamparan pasir. Pasangan Katolik (Sakramen Perkawinan).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import type { Attendance } from "../kit";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,600;1,400;1,500;1,600", "Karla:wght@400;500;700"];
// Painted by /tmp/pen/art/themes/pantai-kei.py (sand tile and tenun band are CSS backgrounds)
const Art = makeArt("pantai-kei", { scene: [780, 795], palm: [380, 612], boat: [300, 117], shell: [160, 103] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Damai Kristus",
    title: "Ain ni Ain",
    sub: "kita semua satu saudara",
    intro: "Dengan sukacita dan syukur atas kasih Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam Sakramen Perkawinan dan perjamuan kasih kami di tanah Evav, Kepulauan Kei.",
  },
  roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
  couple: ["Dua Hati, Satu Ohoi", "Mempelai"],
  count: ["Menuju Hari Bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat Tanggalnya", "Rangkaian Acara"],
  story: ["Dari Pasir Ngurbloat", "Kisah Kami"],
  gallery: ["Kartu Pos", "Galeri"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang melengkapi sukacita kami dan kedua keluarga besar.",
    salam: "Tuhan memberkati",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan berkat untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Bapak Paulus Rettob & Keluarga", attendance: "yes" as Attendance, message: "Tuhan memberkati rumah tangga kalian. Semoga kasih kalian setenang laut Ngurbloat dan sekokoh perahu yang pulang ke pantai." },
  { id: "w2", name: "Kakak Lusi Elmas", attendance: "yes" as Attendance, message: "Ade Tesa dan Frans, selamat e! Sampai ketemu di Tual, siap dansa sampai malam." },
  { id: "w3", name: "Teman Guru SD Langgur", attendance: "maybe" as Attendance, message: "Kami masih menunggu jadwal kapal dari Ambon. Doa terbaik dari kami semua untuk kalian berdua." },
];

export default function PantaiKeiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf8f1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverSea}>
            <Art name="scene" eager />
            <Art name="boat" eager className={s.coverBoat} />
          </div>
          <Art name="palm" eager className={s.coverPalm} />
          <Art name="shell" eager className={s.coverShell} />
          <div className={s.coverText}>
            <p className={s.kicker}>{label === "Pernikahan" ? "Sakramen Perkawinan" : `Undangan ${label}`}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#c9f2eb"
        dark="#0f5f6e"
        hero={(
          <header className={s.hero}>
            <div className={s.heroSea}>
              <Art name="scene" />
              <Art name="boat" className={s.coverBoat} />
            </div>
            <div className={s.postcard}>
              <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
              <span aria-hidden><Art name="shell" className={s.postShell} /></span>
            </div>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden />,
          node: <Art name="shell" />,
          amp: <Art name="shell" />,
          portrait: <Art name="shell" className={s.portraitShell} />,
          countDecor: <Art name="boat" className={s.countBoat} />,
          closingDecor: <Art name="palm" className={s.closingPalm} />,
          closingEmblem: <Art name="boat" className={s.closingBoat} />,
          sentArt: <Art name="shell" />,
        }}
      />
    </ThemeShell>
  );
}
