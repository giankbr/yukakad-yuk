"use client";
// Theme "Mint Syari" — syari tanpa foto, segar dan lapang: putih bersih dengan hijau mint, tangkai daun mint cat air
// (daun bergerigi berpasangan, bunga mungil lilac), jendela lengkung bersapuan mint berisi monogram, kartu membulat dan
// tata letak modern rata kiri. Hanya flora (tanpa figur makhluk hidup), basmalah sebagai teks.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,300;0,400;0,600;1,300;1,400", "Figtree:wght@400;500;600;700", "Amiri"];
// Painted by /tmp/pen/art/themes/mint-syari.py (wash + disc are CSS backgrounds).
const Art = makeArt("mint-syari", { sprig: [215, 706], sprig2: [300, 92], leaf: [110, 121], cluster: [480, 503] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Rahmat Allah",
    sub: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dipertemukan karena Allah", "Kedua Mempelai"],
  count: ["Menanti hari yang diberkahi", "Hitung Mundur"],
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
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  familyLabel: "Kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Ustazah Faridah & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Teman Kajian Ahad Pagi", attendance: "yes" as const, message: "MasyaAllah, ikut bahagia, Alifa! Semoga Allah mudahkan segala urusannya sampai hari akad." },
  { id: "w3", name: "Keluarga Pak Lik Huda, Blitar", attendance: "maybe" as const, message: "Mohon maaf bila berhalangan hadir. Doa terbaik kami untuk Alifa dan Hanif." },
];

export default function MintSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const kicker = label === "Pernikahan" ? "Walimatul 'Ursy" : label;
  const bride = data.couple.bride;
  const groom = data.couple.groom?.trim();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const place = data.place || data.events[0]?.venue;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#ffffff"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="leaf" eager className={`${s.floatLeaf} ${s.floatA}`} />
          <Art name="leaf" eager className={`${s.floatLeaf} ${s.floatB}`} />
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.coverSalam}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.arch} aria-hidden>
            <span className={s.archMono}>{bride.slice(0, 1)}{groom && <><i>&amp;</i>{groom.slice(0, 1)}</>}</span>
            <Art name="cluster" eager className={s.coverCluster} />
          </div>
          <p className={s.kicker}>{kicker}</p>
          <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        copy={COPY}
        demoWishes={WISHES}
        light="#ffffff"
        dark="#1f6f55"
        hero={(
          <header className={s.hero}>
            <Art name="sprig" className={s.heroSprig} />
            <p className={s.heroKicker}>{kicker}</p>
            <h1 className={s.heroNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <div className={s.facts}>
              <div><small>Tanggal</small><b>{formatDate(data.date)}</b></div>
              <div><small>Tempat</small><b>{place || "Segera diumumkan"}</b></div>
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig2" className={s.divider} />,
          node: <Art name="leaf" />,
          amp: <Art name="leaf" />,
          portrait: <Art name="leaf" className={s.portraitArt} />,
          countDecor: <><Art name="leaf" className={`${s.countLeaf} ${s.countLeafA}`} /><Art name="leaf" className={`${s.countLeaf} ${s.countLeafB}`} /></>,
          closingDecor: <Art name="cluster" className={s.closingCluster} />,
          closingEmblem: <Art name="leaf" className={s.closingEmblem} />,
          sentArt: <Art name="sprig2" />,
        }}
      />
    </ThemeShell>
  );
}
