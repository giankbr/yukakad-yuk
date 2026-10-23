"use client";
// Theme "Ukir Jepara" — ukiran jati Jepara (hanya flora): sampul berupa panel ukir relief dalam dengan sulur lung-lungan,
// daun bergerigi dan bunga bertumpuk, disorot lampu dari kiri atas; nama mempelai di kartus jati yang dipoles. Isi
// halaman memakai papan serat jati, sudut ukel pada bingkai potret, dan ambang ukir di atas kartu acara.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "Vollkorn:ital,wght@0,400;0,600;1,400", "Italianno", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/ukir-jepara.py (tools/art/themes in the repo).
const Art = makeArt("ukir-jepara", { panel: [560, 770], ukel: [300, 300], garis: [420, 75], kembang: [220, 222] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga H. Sholikhin", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Rekan Sanggar Ukir Mulyoharjo", attendance: "yes" as const, message: "Selamat, Mas Fikri dan Mbak Nadia! Semoga rumah tangganya kokoh seperti jati tua dan indah seperti ukiran terbaik." },
  { id: "w3", name: "Bu Lilis & Guru SD Kauman", attendance: "maybe" as const, message: "Insyaallah kami hadir selepas Zuhur. Doa terbaik untuk kalian berdua." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Bismillah",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dipahat Bersama", "Kedua Mempelai"],
  count: ["Hitung Mundur", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Sulur Kisah", "Perjalanan Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Restu", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan dan kehormatan bagi kami sekeluarga.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
};

export default function UkirJeparaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1a0c05"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.bismillah} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.panel}>
            <Art name="panel" eager className={s.panelArt} />
            <span className={s.light} aria-hidden />
            <div className={s.cartouche}>
              <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#2b1508" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#ffe1ad"
        dark="#3d1a07"
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.heroFrame}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <Art name="ukel" className={`${s.heroUkel} ${s.heroUkelL}`} />
                <Art name="ukel" className={`${s.heroUkel} ${s.heroUkelR}`} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="garis" className={s.divider} />,
          node: <Art name="kembang" />,
          amp: <Art name="kembang" />,
          portrait: <><Art name="ukel" className={`${s.pCorner} ${s.pCornerA}`} /><Art name="ukel" className={`${s.pCorner} ${s.pCornerB}`} /></>,
          countDecor: <><Art name="ukel" className={`${s.countUkel} ${s.countUkelL}`} /><Art name="ukel" className={`${s.countUkel} ${s.countUkelR}`} /></>,
          closingEmblem: <Art name="kembang" className={s.closingEmblem} />,
          sentArt: <Art name="kembang" />,
        }}
      />
    </ThemeShell>
  );
}
