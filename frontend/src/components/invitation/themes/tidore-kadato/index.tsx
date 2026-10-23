"use client";
// Theme "Tidore Kadato" — adat Tidore (Maluku Utara): fajar di atas selat, kerucut Gunung Kie Matubu yang naik dari laut
// (cat air), Kadato Kie putih beratap susun merah cengkih dengan tangga agung (gouache), ranting cengkih berkuncup merah dan
// pala terbelah bersalut fuli. Bingkai foto beratap bertingkat, kartu acara bertepi gelombang, pita hitung mundur selat.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Federant", "Crimson Pro:ital,wght@0,400;0,600;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/tidore-kadato.py
const Art = makeArt("tidore-kadato", { scene: [780, 720], clove: [400, 438], nutmeg: [240, 237], divider: [300, 26] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

export default function TidoreKadatoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6ead8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverTop}>
            <p className={s.bism} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>Undangan {data.eventLabel ?? "Pernikahan"} · Adat Tidore</p>
            <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.sceneWrap} aria-hidden>
            <Art name="scene" eager />
            <span className={s.coverClove}><Art name="clove" eager /></span>
          </div>
          <div className={s.jetty}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#2b1d18" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f2d7a6"
        dark="#4a1a14"
        demoWishes={[
          { id: "w1", name: "Keluarga Hi. Rahman Sangaji", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga rumah tangga kalian seharum cengkih Tidore dan sekokoh Kie Matubu." },
          { id: "w2", name: "Nurhayati Taher", attendance: "yes", message: "Selamat Sarifa dan Fadli! Sampai jumpa di Soasio, semoga acaranya lancar dan penuh berkah." },
          { id: "w3", name: "Teman kampus Unkhair", attendance: "maybe", message: "Mohon maaf belum tentu bisa menyeberang. Doa terbaik kami dari Ternate untuk kalian berdua." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Rahmat Allah",
            intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Keluarga, Satu Ikatan", "Kedua Mempelai"],
          count: ["Dari Soasio ke Hari Akad", "Menghitung Hari"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Jejak di Pulau Rempah", "Kisah Kami"],
          gallery: ["Galeri", "Momen Bersama"],
          wishes: ["Doa Restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Terima Kasih",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Insyaallah kami akan menikah</p>
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
              <span className={s.heroClove} aria-hidden><Art name="clove" /></span>
              <Art name="nutmeg" className={s.heroNut} />
            </div>
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="divider" /></span>,
          node: <Art name="nutmeg" />,
          amp: <Art name="divider" />,
          portrait: <Art name="nutmeg" className={s.portraitNut} />,
          countDecor: <span className={s.countSun} aria-hidden />,
          closingDecor: <><Art name="clove" className={`${s.closingClove} ${s.closingCloveL}`} /><Art name="clove" className={`${s.closingClove} ${s.closingCloveR}`} /></>,
          closingEmblem: <Art name="nutmeg" className={s.closingNut} />,
          sentArt: <Art name="nutmeg" />,
        }}
      />
    </ThemeShell>
  );
}
