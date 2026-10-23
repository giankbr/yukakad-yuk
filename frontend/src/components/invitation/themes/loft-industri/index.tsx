"use client";
// Theme "Loft Industri" — loft industrial yang hangat dan temaram: dinding bata ekspos, jendela rangka baja hitam
// dengan foto pasangan di balik kaca, bohlam Edison berayun di ujung kabel, ambang beton, dan sirih gading menjuntai.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Big Shoulders Display:wght@600;700;800", "Hanken Grotesk:wght@400;500;600;700;800", "Homemade Apple"];
// Painted by /tmp/pen/art/themes/loft-industri.py (tools/art/themes in the repo).
const Art = makeArt("loft-industri", { jendela: [320, 410], bohlam: [130, 544], tanaman: [260, 541], pipa: [280, 67] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Hangat",
    title: "Dua Nada, Satu Ruang",
    sub: "dari loft kecil kami di Bandung",
    intro: "Dengan penuh sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan merayakan hari pernikahan kami. Kehadiran dan doa restu Anda akan membuat ruang ini terasa lengkap.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Penghuni Loft", "Kami Berdua"] as [string, string],
  count: ["Lampu Menyala Dalam", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Agenda Hari H"] as [string, string],
  story: ["Catatan Kami", "Cerita di Balik Bata"] as [string, string],
  gallery: ["Galeri", "Potret Loft"] as [string, string],
  wishes: ["Pesan & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Hadiah Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Terima kasih sudah menjadi bagian dari cerita kami. Sampai bertemu di bawah lampu-lampu loft, dengan lagu, tawa, dan pelukan hangat.",
  },
  sent: "Terima kasih, ucapan Anda sudah kami terima.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tulis ucapan dan doa terbaik untuk kami…",
  familyLabel: "Dengan hangat,",
};

const WISHES = [
  { id: "w1", name: "Bayu & Sasha", attendance: "yes" as const, message: "Dari malam open mic sampai pelaminan. Bahagia selalu, Tara dan Kevin! Kami siap menyanyi di panggung terbuka." },
  { id: "w2", name: "Tante Lina Santoso", attendance: "yes" as const, message: "Selamat menempuh hidup baru. Semoga rumah tangga kalian selalu hangat, kokoh, dan penuh tawa." },
  { id: "w3", name: "Tim Studio Gudang", attendance: "maybe" as const, message: "Masih menunggu jadwal proyek, tapi doa kami sudah sampai duluan. Congrats, partners!" },
];

export default function LoftIndustriTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const coverPhoto = data.gallery[0] ?? data.couple.bridePhoto;
  const heroPhoto = data.gallery[1] ?? data.gallery[0] ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1c1a19"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.bulbs} aria-hidden>
            <Art name="bohlam" eager />
            <Art name="bohlam" eager />
            <Art name="bohlam" eager />
          </div>
          <div className={s.window}>
            <div className={s.windowPhoto}>{coverPhoto && <Photo src={coverPhoto} alt="" />}</div>
            <Art name="jendela" eager className={s.grid} />
          </div>
          <div className={s.sill} aria-hidden><Art name="tanaman" eager className={s.plant} /></div>
          <div className={s.slab}>
            <p className={s.kicker}>The Wedding of · {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#1c1a19" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffd18a"
        dark="#1c1a19"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {heroPhoto && (
              <div className={s.heroFrame}>
                <div className={s.heroPhoto}><Photo src={heroPhoto} alt="" /></div>
                <Art name="bohlam" className={s.heroBulb} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="pipa" className={s.divider} />,
          portrait: <Art name="bohlam" />,
          closingEmblem: (
            <div className={s.closingBulbs} aria-hidden>
              <Art name="bohlam" />
              <Art name="bohlam" />
              <Art name="bohlam" />
            </div>
          ),
          sentArt: <Art name="tanaman" />,
        }}
      />
    </ThemeShell>
  );
}
