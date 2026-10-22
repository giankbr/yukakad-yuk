"use client";
// Theme "Bali Gringsing" — pawiwahan Bali Aga dari Tenganan Pegringsingan: kain gringsing ikat ganda merah-hitam-krem
// ditenun benang demi benang (tepi kabur khas ikat), rumbai kain tergantung di atas sampul, foto dalam bingkai belah
// ketupat, kartu bersudut berundak, dan desa batu bertingkat dengan bale beratap alang-alang. Salam Om Swastyastu.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Forum", "Vollkorn:ital,wght@0,400;0,600;1,400", "Tangerine:wght@400;700"];
// Painted by /tmp/pen/art/themes/bali-gringsing.py (tools/art/themes in the repo).
const Art = makeArt("bali-gringsing", { desa: [800, 516], bintang: [280, 277] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Om Swastyastu",
    title: "Atas Asung Kertha Wara Nugraha Ida Sang Hyang Widhi Wasa",
    intro: "Kami bermaksud menyelenggarakan upacara Manusa Yadnya Pawiwahan putra-putri kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Sang Mempelai", "Dua Benang, Satu Kain"],
  count: ["Dewasa Ayu", "Menuju Hari Baik"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Upacara"],
  story: ["Kisah", "Ditenun Perlahan"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Punia Kasih", "Amplop Digital"],
  closing: { thanks: "Suksma", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih yang tulus.", salam: "Om Shanti Shanti Shanti Om" },
  sent: "Suksma, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  closedNote: "Suksma atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
};

const WISHES = [
  { id: "w1", name: "Keluarga I Wayan Sutama", attendance: "yes" as Attendance, message: "Rahajeng nganten, Sekar lan Bayu. Dumogi rahayu, langgeng, lan setata kasih-asih kantos kaki-nini." },
  { id: "w2", name: "Komang Tri & Gede Arta", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru! Sampai jumpa di wantilan, kami bawa senyum paling lebar." },
  { id: "w3", name: "Ni Luh Ayu Lestari", attendance: "maybe" as Attendance, message: "Mungkin baru bisa menyusul malam hari. Doa terbaik untuk kalian berdua, semoga rahayu selalu." },
];

export default function BaliGringsingTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pawiwahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#24130f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.swasti}>Om Swastyastu</p>
          <div className={s.lozenge}>
            <div className={s.lozPhoto}>{hero ? <Photo src={hero} alt="" /> : null}</div>
            <Art name="bintang" eager className={`${s.lozStar} ${s.lozStarL}`} />
            <Art name="bintang" eager className={`${s.lozStar} ${s.lozStarR}`} />
          </div>
          <div className={s.panel}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f8f0dd" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#efdfba"
        dark="#24130f"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}><Art name="bintang" />{formatDate(data.date)}<Art name="bintang" /></p>
            <Art name="desa" className={s.heroDesa} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="bintang" /><i /></span>,
          node: <i className={s.nodeMark} />,
          amp: <Art name="bintang" />,
          portrait: <Art name="bintang" />,
          closingEmblem: <Art name="bintang" className={s.closingEmblem} />,
          sentArt: <Art name="bintang" />,
        }}
      />
    </ThemeShell>
  );
}
