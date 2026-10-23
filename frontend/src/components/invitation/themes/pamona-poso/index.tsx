"use client";
// Theme "Pamona Poso" — adat Pamona, Sulawesi Tengah: Danau Poso yang jernih di atas pasir putih, jembatan kayu tempat
// danau menjadi Sungai Poso, wayamasapi di arus, dan rumah panggung Pamona beratap curam, dilukis cat air. Manik-manik
// Pamona menjadi pita, cincin potret bundar, dan medali nomor acara. Bagian berganti antara pasir dan air danau.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Kurale", "Alegreya Sans:ital,wght@0,400;0,500;0,700;1,400"];
// Painted by /tmp/pen/art/themes/pamona-poso.py (scene, beads and water are CSS backgrounds)
const Art = makeArt("pamona-poso", { house: [300, 302], emblem: [150, 150] } as const);

const WISHES = [
  { id: "w1", name: "Om Yohanis & Tante Sarce", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru, Debora dan Yosua. Tuhan Yesus memberkati rumah tangga kalian, jernih dan tenang seperti Danau Poso." },
  { id: "w2", name: "Teman Panitia Festival", attendance: "yes" as Attendance, message: "Dari mengatur perahu tamu sampai jadi pengantin! Sampai jumpa di Dodoha, siap ikut Dero sampai malam." },
  { id: "w3", name: "Kak Melki di Palu", attendance: "maybe" as Attendance, message: "Mohon maaf kalau belum bisa pulang ke Tentena. Doa kami menyertai kalian berdua, saling setia sampai tua." },
];

export default function PamonaPosoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();
  const label = data.eventLabel ?? "Pernikahan";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3ecdc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverText}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
          <span className={s.beadBand} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fffbf2"
        dark="#0f4652"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Salam Sejahtera",
            title: "Dalam Kasih Tuhan",
            sub: "Dari tepi Danau Poso, Tentena",
            intro: "Atas berkat dan kasih Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam pemberkatan nikah dan syukuran putra-putri kami. Kehadiran dan doa Anda adalah sukacita bagi kedua keluarga besar.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Hati, Satu Danau", "Kedua Mempelai"],
          count: ["Menanti Hari Itu", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Mengalir Bersama", "Kisah Kami"],
          gallery: ["Galeri", "Cerita di Tepi Danau"],
          wishes: ["Doa & Ucapan", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Terima Kasih",
            text: "Kehadiran dan doa Bapak/Ibu/Saudara/i merupakan kehormatan dan sukacita bagi kami sekeluarga. Tuhan memberkati.",
            salam: "Salam damai dalam kasih Kristus",
          },
          sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
          giftIntro: "Doa dan kehadiran Anda adalah hadiah terindah bagi kami. Jika ingin memberi tanda kasih, dapat melalui:",
          familyLabel: "Keluarga Besar",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Kami akan menikah</p>
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
              <span aria-hidden><Art name="house" className={s.heroHouse} /></span>
            </div>
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden />,
          node: <Art name="emblem" />,
          amp: <Art name="emblem" />,
          portrait: <Art name="emblem" className={s.portraitArt} />,
          closingDecor: <span className={s.beadBand} aria-hidden />,
          closingEmblem: <Art name="house" className={s.closingEmblem} />,
          sentArt: <Art name="emblem" />,
        }}
      />
    </ThemeShell>
  );
}
