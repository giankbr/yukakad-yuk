"use client";
// Theme "Kenanga Syari" — syari tanpa foto: setangkai kenanga cat air (kelopak panjang menjuntai kuning-hijau) masuk
// dari pojok kanan atas kertas krem; tipografi rata kiri seperti label herbarium, monogram di atas sapuan cat air.
// Hanya flora (tanpa figur makhluk hidup), basmalah sebagai teks.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "Petrona:ital,wght@0,400;0,500;0,600;1,400", "Ephesis", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/kenanga-syari.py (the monogram wash is a CSS background)
const Art = makeArt("kenanga-syari", { branch: [520, 715], blossom: [180, 181], sprig: [420, 214] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

export default function KenangaSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const label = data.eventLabel ?? "Pernikahan";
  const kicker = label === "Pernikahan" ? "Walimatul 'Ursy" : label;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6f1e3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="branch" eager className={s.branch} />
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.coverSalam}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.coverText}>
            <p className={s.kicker}>{kicker}</p>
            <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f6f1e3" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#e7e2a6"
        dark="#34331f"
        demoWishes={[
          { id: "w1", name: "Ustadzah Rahmah & Keluarga", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
          { id: "w2", name: "Teman Farmasi Angkatan 2019", attendance: "yes", message: "MasyaAllah, ikut bahagia, Dhira! Semoga Allah mudahkan segala urusan dan lancar sampai hari H." },
          { id: "w3", name: "Keluarga Om Hendra", attendance: "maybe", message: "Mohon maaf bila berhalangan hadir. Doa terbaik kami untuk Nadhira dan Ilham." },
        ]}
        copy={{
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Rahmat Allah",
            intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dipertemukan dalam rida-Nya", "Kedua Mempelai"],
          count: ["Menanti hari yang diberkahi", "Menghitung Hari"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & tempat", "Rangkaian Acara"],
          story: ["Perjalanan kami", "Kisah Ta'aruf"],
          gallery: ["Galeri", "Momen Bersama"],
          wishes: ["Doa restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullahu Khairan",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah terkirim.",
          familyLabel: "Kami yang berbahagia",
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroSheet}>
              <Art name="sprig" className={s.heroSprig} />
              <p className={s.heroKicker}>{kicker}</p>
              <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              <dl className={s.heroLabel}>
                <dt>Bunga</dt><dd>Kenanga, Cananga odorata</dd>
                <dt>Tempat</dt><dd>{data.place || data.events[0]?.venue || "Segera diumumkan"}</dd>
              </dl>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="blossom" /></span>,
          node: <Art name="blossom" />,
          portrait: <Art name="blossom" className={s.portraitArt} />,
          countDecor: <Art name="sprig" className={s.countSprig} />,
          closingEmblem: <Art name="sprig" className={s.closingEmblem} />,
          sentArt: <Art name="blossom" />,
        }}
      />
    </ThemeShell>
  );
}
