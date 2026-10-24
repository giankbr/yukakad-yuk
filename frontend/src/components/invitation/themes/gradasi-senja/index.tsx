"use client";
// Theme "Gradasi Senja" — minimalis modern tanpa lanskap. Sampul: langit senja yang dilukis (peach ke koral ke mawar)
// berbutir film, nama raksasa rata kiri bertipe Instrument Serif, cakram matahari cat air yang setengah tenggelam di garis
// cakrawala tipis, dan bidang senja ungu polos untuk tamu. Halaman adalah satu senja yang terus turun saat digulir: tiap
// bagian membawa irisan gradasinya sendiri sampai nila malam di penutup, tempat matahari tinggal busur terakhir.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Instrument Serif:ital@0;1", "Hanken Grotesk:wght@400;500;600", "Geist Mono:wght@400;500"];
// Painted by /tmp/pen/art/themes/gradasi-senja.py
const Art = makeArt("gradasi-senja", { sun: [360, 359], mark: [180, 39] } as const);

const WISHES = [
  { id: "w1", name: "Nadine & Bram", attendance: "yes" as const, message: "Akhirnya! Kami sudah pesan tiket kereta ke Jogja. Bahagia selalu, semoga setiap senja kalian setenang hari itu." },
  { id: "w2", name: "Tante Rosa", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Maya dan Dion. Tuhan memberkati rumah tangga kalian dengan kasih dan kesabaran." },
  { id: "w3", name: "Teman kantor Dion", attendance: "maybe" as const, message: "Semoga bisa menyusul ke Prambanan. Kalaupun tidak, doa terbaik dari kami semua untuk kalian berdua." },
];

function shortDate(value?: string) {
  const d = toDate(value);
  return d ? d.toLocaleDateString("en-GB", { timeZone: "Asia/Jakarta", day: "2-digit", month: "2-digit", year: "2-digit" }).replace(/\//g, ".") : "";
}

export default function GradasiSenjaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const stamp = shortDate(data.date);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1b1b3a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.topbar}><span>Undangan {label}</span>{stamp && <span>{stamp}</span>}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <div className={s.sunBox} aria-hidden><Art name="sun" eager className={s.sun} /></div>
          <span className={s.horizon} aria-hidden />
          <div className={s.dusk}>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#3b1f3a" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fff1e6"
        dark="#3b1f3a"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Dengan sukacita",
            title: "Kami menikah.",
            intro: "Dengan penuh syukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir, menyaksikan, dan merayakan hari pernikahan kami di bawah langit senja yang sama.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Berdua", "Mempelai"],
          count: ["Sebelum matahari turun", "Hitung mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Simpan tanggalnya", "Acara"],
          story: ["Dari pagi ke senja", "Cerita kami"],
          gallery: ["Galeri", "Potret"],
          wishes: ["Ucapan & kehadiran", "RSVP"],
          gifts: ["Tanda kasih", "Hadiah"],
          closing: {
            thanks: "Terima kasih.",
            text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah hadiah terindah bagi kami berdua dan keluarga.",
          },
          sent: "Terima kasih, ucapanmu sudah sampai.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
          familyLabel: "Bersama keluarga",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroTop}><span>{label}</span>{stamp && <span>{stamp}</span>}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            {data.gallery[0] ? (
              <div className={s.heroPhotoWrap}>
                <div className={s.heroPhoto}><Photo src={data.gallery[0]} alt="" /></div>
                <Art name="sun" className={s.heroSun} />
              </div>
            ) : <div className={s.heroEmpty} aria-hidden><Art name="sun" /></div>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="mark" className={s.divider} />,
          node: <Art name="sun" />,
          portrait: <Art name="sun" className={s.portraitSun} />,
          closingDecor: <div className={s.closingSet} aria-hidden><Art name="sun" /></div>,
          sentArt: <Art name="mark" />,
        }}
      />
    </ThemeShell>
  );
}
