"use client";
// Theme "Renda Putih" — Syari: renda putih berlapis di atas satin gading, dilukis sampai helai benangnya (jaring tulle
// segi enam, bunga anyaman rapat, benang timbul, tepi berpico, bayangan lembut di satin). Sampul: tirai renda dengan
// jendela oval berisi nama; monogram dalam medali guipure; pita renda menjuntai di tepi atas setiap bagian.
// Tanpa foto pun lengkap: foto hanya tampil bila diunggah (galeri / foto sampul).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["WindSong:wght@400;500", "Cormorant SC:wght@500;600", "EB Garamond:ital,wght@0,400;0,600;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/renda-putih.py (satin, tulle, veilmask and trim are CSS backgrounds/masks)
const Art = makeArt("renda-putih", { veil: [624, 848], doily: [300, 301], sprig: [110, 125], divider: [360, 29] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

export default function RendaPutihTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0];
  const note = data.couple.note?.trim();
  const initials = `${bride.trim().slice(0, 1)}${groom.trim() ? ` & ${groom.trim().slice(0, 1)}` : ""}`;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3ede2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.veil}>
            <span className={s.veilNet} aria-hidden />
            <Art name="veil" eager />
            <div className={s.window}>
              <p className={s.bism} lang="ar" dir="rtl">{BISMILLAH}</p>
              <p className={s.kicker}>{data.eventLabel ?? "Walimatul 'Ursy"}</p>
              <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.coverFoot}>
            <Art name="sprig" className={s.footSprig} eager />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf8f2" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f4ece0"
        dark="#533f48"
        demoWishes={[
          { id: "w1", name: "Ibu Hj. Fatimah Zahra", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga yang sakinah, mawaddah, wa rahmah." },
          { id: "w2", name: "Akhwat Rumah Tahfidz Kotagede", attendance: "yes", message: "MasyaAllah, ikut berbahagia untuk Ustazah Hanifa. Semoga Allah mudahkan segala urusan di hari bahagia ini." },
          { id: "w3", name: "Keluarga Bapak Sholeh", attendance: "maybe", message: "Insyaallah hadir bila Allah mudahkan. Doa terbaik untuk Hanifa dan Rasyid." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Rahmat Allah",
            intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Insan", "Kedua Mempelai"],
          count: ["Menuju Hari Akad", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Ikhtiar Kami", "Kisah Kami"],
          gallery: ["Galeri", "Momen Bersama"],
          wishes: ["Doa Restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Insyaallah kami menikah</p>
            <div className={s.heroMedal}>
              {heroSrc
                ? <div className={s.heroPhoto}><Photo src={heroSrc} alt={`${bride} & ${groom}`} /></div>
                : <><Art name="doily" /><span className={s.heroInitials} aria-hidden>{initials}</span></>}
            </div>
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="divider" /></span>,
          node: <Art name="sprig" />,
          amp: <Art name="sprig" />,
          portrait: <Art name="doily" className={s.portraitDoily} />,
          closingEmblem: <Art name="doily" className={s.closingDoily} />,
          sentArt: <Art name="sprig" />,
        }}
      />
    </ThemeShell>
  );
}
