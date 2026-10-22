"use client";
// Theme "Maluku Tifa" — pesisir Ambon dalam gouache: sepasang tifa berukir dengan kepala kulit, cincin rotan anyam dan
// tali rotan berpasak; tenun ikat Tanimbar yang ditenun sampai ke benang (pewarna merembes searah lungsin) menjadi
// tepian kain di sisi kiri seluruh halaman; ranting cengkih & pala; laut toska Teluk Ambon. Tipografi tebal, rata kiri.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bricolage Grotesque:wght@400;600;700;800", "Crimson Pro:ital,wght@0,400;0,600;1,400"];
// Painted by /tmp/pen/art/themes/maluku-tifa.py (tools/art/themes in the repo).
const Art = makeArt("maluku-tifa", { tifa: [440, 619], sprig: [420, 290], sea: [720, 444], twig: [380, 64] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Syalom",
    title: "Dangke, Tuhan",
    sub: "Untuk kasih yang mempertemukan dan menyatukan kami.",
    intro: "Dengan penuh syukur atas kasih karunia Tuhan Yesus Kristus, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan turut berbahagia dalam pemberkatan nikah serta resepsi pernikahan kami.",
  },
  roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
  couple: ["Dipersatukan Tuhan", "Kedua Mempelai"],
  count: ["Tifa Su Bunyi", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Katong Pung Carita", "Perjalanan Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Dangke Banyak", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang besar bagi kami sekeluarga. Tuhan Yesus memberkati.", salam: "Syalom" },
  sent: "Dangke banyak, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan berkat untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Om Nus & Tante Ina Sahetapy", attendance: "yes" as Attendance, message: "Dangke Tuhan for katong pung anak dua. Tuhan Yesus berkati rumah tangga baru ini, selalu rukun deng saling sayang." },
  { id: "w2", name: "Kevin Tuhumury", attendance: "yes" as Attendance, message: "Selamat bro deng nona! Sampai ketemu di pesta, siap dansa lenso sampai pagi." },
  { id: "w3", name: "Keluarga Matulessy (Saparua)", attendance: "maybe" as Attendance, message: "Mohon maaf kalau belum bisa datang. Doa katong menyertai kalian berdua, Tuhan memberkati." },
];

export default function MalukuTifaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0b4a5a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="sprig" eager className={s.coverSprig} />
          <div className={s.coverText}>
            <p className={s.coverKicker}>Syalom!</p>
            <p className={s.coverLabel}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <Art name="tifa" eager className={s.coverTifa} />
          <div className={s.coverGuest}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6efe0"
        dark="#4a1c17"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="sea" eager className={s.heroSea} />
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroPhotoWrap}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="twig" className={s.heroTwig} />
          </header>
        )}
        slots={{
          divider: <Art name="twig" className={s.divider} />,
          amp: <Art name="twig" />,
          closingEmblem: <Art name="tifa" className={s.closingTifa} />,
          closingDecor: <span className={s.closingCloth} aria-hidden />,
          sentArt: <Art name="sprig" />,
        }}
      />
    </ThemeShell>
  );
}
