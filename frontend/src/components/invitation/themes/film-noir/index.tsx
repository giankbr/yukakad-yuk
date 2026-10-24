"use client";
// Theme "Film Noir" — undangan bergaya film noir 1940-an, hitam-putih (desain orisinal, siluet distilisasi tanpa wajah
// atau tokoh nyata): jalan basah berhujan di bawah lampu besi tuang, jendela berkerai menyala, sepasang siluet bertopi
// fedora dan bertopi lebar berbagi satu payung, dilukis guas abu-abu. Sampul dibuka kartu judul Art Deco bergaris
// ganda, tamu ditulis seperti kredit film; bayangan kerai melintas pelan, cahaya lampu berkedip. Isi: kartu antarjudul,
// foto hitam-putih sebagai still film, hitung mundur berupa lingkaran pita pembuka film, kisah sebagai adegan, penutup
// "Tamat" dengan siluet di bawah lampu.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Limelight", "Old Standard TT:ital,wght@0,400;0,700;1,400"];
// Painted by /tmp/pen/art/themes/film-noir.py
const Art = makeArt("film-noir", { scene: [760, 1560], blinds: [640, 568], glow: [260, 265], hat: [150, 56], couple: [288, 488] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh sukacita",
    title: "Babak Baru Kami",
    intro: "Setiap kisah besar punya adegan yang ditunggu. Kami mengundang Bapak/Ibu/Saudara/i untuk hadir, menjadi saksi, dan memberikan doa restu di hari pernikahan kami.",
  },
  roles: ["Pemeran Utama Wanita", "Pemeran Utama Pria"],
  couple: ["Dibintangi oleh", "Kedua Mempelai"],
  count: ["Segera tayang", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Jadwal pemutaran", "Waktu & Tempat"],
  story: ["Naskah kami", "Kisah Kami"],
  gallery: ["Foto still", "Galeri"],
  wishes: ["Pesan untuk pemeran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah kebahagiaan bagi kami. Sampai jumpa di adegan berikutnya.",
    salam: "Salam hangat dari kami berdua",
  },
  sent: "Terima kasih, pesan Anda sudah masuk naskah kami.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Rendy & Talitha", attendance: "yes" as Attendance, message: "Sudah siapkan fedora dan sarung tangan. Selamat menempuh hidup baru, semoga kisah kalian lebih indah dari film mana pun." },
  { id: "w2", name: "Klub Film Jumat Malam", attendance: "yes" as Attendance, message: "Dari kursi baris ketiga bioskop Cikini sampai pelaminan. Kami datang lengkap, popcorn kami bawa sendiri." },
  { id: "w3", name: "Tante Mira, Bandung", attendance: "maybe" as Attendance, message: "Semoga bisa hadir. Bahagia selalu ya, Kirana dan Dimas, saling menjaga di musim hujan maupun kemarau." },
];

export default function FilmNoirTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0b0b0c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.sceneBox} aria-hidden>
            <Art name="scene" eager />
            <Art name="glow" eager className={s.lampGlow} />
          </div>
          <Art name="blinds" eager className={s.coverBlinds} />
          <div className={s.titleCard}>
            <p className={s.presents}>{label} · sebuah kisah cinta</p>
            <h1 className={s.names}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <span className={s.spacer} aria-hidden />
          <div className={s.credits}>
            <div className={s.guest}>
              <small>Dipersembahkan untuk Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#121213" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#efede7"
        dark="#121213"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="blinds" className={s.heroBlinds} />
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>dan</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.still}>
                <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div>
                <span className={s.stillCap} aria-hidden>Adegan Pembuka</span>
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="hat" /></span>,
          node: <Art name="hat" />,
          amp: <Art name="hat" />,
          portrait: null,
          countDecor: <Art name="glow" className={s.countGlow} />,
          closingDecor: (
            <div className={s.closingScene} aria-hidden>
              <Art name="glow" className={s.cGlow} />
              <Art name="couple" className={s.cCouple} />
            </div>
          ),
          closingEmblem: <p className={s.endCard} aria-hidden>TAMAT</p>,
          sentArt: <Art name="hat" />,
        }}
      />
    </ThemeShell>
  );
}
