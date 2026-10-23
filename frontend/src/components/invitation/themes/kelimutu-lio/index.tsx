"use client";
// Theme "Kelimutu Lio" — adat NTT (Ende-Lio): fajar di atas lautan awan dan tiga danau kawah Kelimutu yang dilukis tangan,
// tenun ikat Lio (dasar hitam, belah ketupat merah bata dan kunyit) sebagai bingkai potret, tepi kartu, dan latar.
// Tata letak rata kiri seperti label tenun; awan bergerak pelan di pita hitung mundur dan penutup.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Spectral:ital,wght@0,400;0,500;0,600;1,400"];
// Painted by /tmp/pen/art/themes/kelimutu-lio.py (scene, ikat and clouds are CSS backgrounds)
const Art = makeArt("kelimutu-lio", { lakes: [320, 66], motif: [120, 139] } as const);

export default function KelimutuLioTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();
  const label = data.eventLabel ?? "Pernikahan";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1d1512"
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
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff8ea" />Buka Undangan</button>
          </div>
          <span className={s.ikatEdge} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f2c97a"
        dark="#1d1512"
        demoWishes={[
          { id: "w1", name: "Om Paulus Dhae & Keluarga", attendance: "yes", message: "Selamat menempuh hidup baru, Yohana dan Alfons. Tuhan memberkati rumah tangga kalian, rukun dan setia sampai tua." },
          { id: "w2", name: "Teman Angkatan Uniflor", attendance: "yes", message: "Akhirnya! Dari catatan kuliah sampai altar. Sampai jumpa di gawi, siap menari sampai pagi." },
          { id: "w3", name: "Sr. Maria Yuliana, CIJ", attendance: "maybe", message: "Doa kami menyertai kalian berdua. Semoga keluarga kalian menjadi berkat bagi banyak orang." },
        ]}
        copy={{
          opening: {
            kicker: "Salam Sejahtera",
            title: "Dalam Kasih Tuhan",
            sub: "Dari tanah Lio, Ende, Flores",
            intro: "Atas berkat Tuhan Yang Maha Kasih, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan turut mendoakan Sakramen Perkawinan putra-putri kami. Kehadiran Anda adalah sukacita bagi kedua keluarga besar.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Hati, Satu Tenun", "Kedua Mempelai"],
          count: ["Menanti Fajar Itu", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Perjalanan Kami", "Kisah Kami"],
          gallery: ["Galeri", "Potongan Kenangan"],
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
            <span className={s.ikatEdge} aria-hidden />
            <div className={s.heroInner}>
              <p className={s.heroKicker}>Kami akan menikah</p>
              <div className={s.heroFrame}>
                <div className={s.heroPhoto}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
              </div>
              <Art name="lakes" className={s.heroLakes} />
              <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="lakes" /></span>,
          node: <Art name="motif" />,
          amp: <Art name="motif" />,
          portrait: <Art name="motif" className={s.portraitArt} />,
          countDecor: <span className={s.countClouds} aria-hidden />,
          closingDecor: <><span className={s.ikatEdge} aria-hidden /><span className={s.closingClouds} aria-hidden /></>,
          closingEmblem: <Art name="motif" className={s.closingEmblem} />,
          sentArt: <Art name="motif" />,
        }}
      />
    </ThemeShell>
  );
}
