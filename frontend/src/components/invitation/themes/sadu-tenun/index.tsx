"use client";
// Theme "Sadu Tenun" — Al Sadu Bedouin weaving rendered as coarse warp-faced wool (original, inspired-by geometry; no
// figures, no calligraphy): the cover is a woven panel hung from a tent pole inside a goat-hair tent, edged with a
// diamond "eye" band and saw-tooth triangles, wrapped tassels swaying below. Wool cards with stitched borders, diamond
// event numbers, a ticking strip opening every section, a black countdown band and a tent at dusk to close.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Reem Kufi:wght@400;500;600;700", "Alegreya:ital,wght@0,400;0,500;0,700;1,400", "Amiri"];
// Painted by /tmp/pen/art/themes/sadu-tenun.py (tools/art/themes in the repo).
const Art = makeArt("sadu-tenun", {
  bandA: [780, 225], bandB: [780, 198], tick: [780, 63], eye: [126, 126], tassels: [780, 190], tent: [780, 289],
} as const);

const WISHES = [
  { id: "w1", name: "Keluarga Bapak H. Salim Bawazier", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Ustadzah Khadijah", attendance: "yes" as Attendance, message: "Masya Allah, ikut berbahagia. Semoga rumah tangga kalian kuat seperti tenunan yang rapat benangnya." },
  { id: "w3", name: "Teman-teman Panitia Kajian Ampel", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir. Selamat menempuh hidup baru, Aisyah & Faris!" },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dua Benang, Satu Tenunan",
    intro: "Maha Suci Allah yang menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan ridha-Nya, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Ahlan wa Sahlan", "Kedua Mempelai"],
  count: ["Menanti Hari Bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Doa & Restu", "Ucapan & Kehadiran"],
  gifts: ["Hadiah", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan yang berlipat.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah kami terima.",
};

export default function SaduTenunTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#241a16"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
          <span className={s.pole} aria-hidden />
          <div className={s.panel}>
            <Art name="bandA" eager className={s.panelBand} />
            <div className={s.panelField}>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f7f0e2" />Buka Undangan</button>
            </div>
            <Art name="bandB" eager className={s.panelBand} />
            <Art name="tassels" eager className={s.tassels} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f7f0e2"
        dark="#1d1512"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
            <Art name="bandA" className={s.heroBand} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider}><Art name="eye" /></span>,
          node: <Art name="eye" />,
          amp: <Art name="eye" />,
          countDecor: <><Art name="bandA" className={`${s.countEdge} ${s.countEdgeT}`} /><Art name="bandB" className={`${s.countEdge} ${s.countEdgeB}`} /></>,
          closingDecor: <Art name="tick" className={s.closingBand} />,
          closingEmblem: <Art name="tent" className={s.closingTent} />,
          sentArt: <Art name="eye" />,
        }}
      />
    </ThemeShell>
  );
}
