"use client";
// Theme "Karavanserai" — Islami, Jalur Sutra: halaman karavanserai bata saat senja (iwan dan arkade dua lantai) dilukis
// tangan, lentera tembaga berlubang yang berayun pelan, karpet merah delima dan biru nila sebagai panel nama dan kartu
// acara, potret dalam lengkung runcing. Hanya arsitektur dan benda: tanpa figur, tanpa kaligrafi lukis.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@400;500;600", "Crimson Pro:ital,wght@0,400;0,500;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/karavanserai.py (court, carpet and brick are CSS backgrounds)
const Art = makeArt("karavanserai", { lantern: [150, 352], arch: [400, 460] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

function Lanterns({ className, n }: { className: string; n: number }) {
  return (
    <span className={className} aria-hidden>
      {Array.from({ length: n }, (_, i) => <span key={i}><Art name="lantern" /></span>)}
    </span>
  );
}

export default function KaravanseraiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a1a34"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverScene}>
            <p className={s.bism} lang="ar" dir="rtl">{BISMILLAH}</p>
            <span className={`${s.lantern} ${s.lanternL}`}><Art name="lantern" eager /></span>
            <span className={`${s.lantern} ${s.lanternR}`}><Art name="lantern" eager /></span>
          </div>
          <div className={s.rug}>
            <span className={s.rugFringe} aria-hidden />
            <p className={s.kicker}>{data.eventLabel ?? "Walimatul 'Ursy"}</p>
            <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#5e1a16" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0c48a"
        dark="#5e1a16"
        demoWishes={[
          { id: "w1", name: "Keluarga H. Salim Bahasuan", attendance: "yes", message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
          { id: "w2", name: "Rombongan Studi Sejarah 2024", attendance: "yes", message: "MasyaAllah, dari halaman karavanserai sampai pelaminan. Semoga perjalanan kalian selalu dimudahkan." },
          { id: "w3", name: "Ustazah Farida", attendance: "maybe", message: "Insyaallah hadir bila tidak ada halangan. Doa terbaik untuk Zahira dan Rayhan." },
        ]}
        copy={{
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Memohon Rahmat Allah",
            intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Kafilah, Satu Tujuan", "Kedua Mempelai"],
          count: ["Menuju Hari Akad", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Perjalanan Kami", "Kisah Kami"],
          gallery: ["Galeri", "Catatan Perjalanan"],
          wishes: ["Doa Restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
          wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
          familyLabel: "Keluarga Besar",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Insyaallah Kami Menikah</p>
            <div className={s.heroArch}>
              <div className={s.heroPhoto}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
              <Art name="arch" className={s.heroFrame} />
            </div>
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden />,
          node: <Art name="lantern" />,
          amp: <span className={s.ampRug} />,
          portrait: <Art name="lantern" className={s.portraitArt} />,
          countDecor: <Lanterns className={s.countLanterns} n={2} />,
          closingDecor: <Lanterns className={s.closingLanterns} n={3} />,
          closingEmblem: <span className={s.closingRug} aria-hidden />,
          sentArt: <Art name="lantern" />,
        }}
      />
    </ThemeShell>
  );
}
