"use client";
// Theme "Zaitun Tuscan" — watercolour countryside: silvery olive branches heavy with fruit, terracotta pots and a
// hilltop villa reached by a cypress lane at golden hour (original design). Cream cold-press pages, sage bands,
// cotto-tile countdown and ivory cards under a coppo roof-tile edge; the hero photo sits in a shuttered villa window.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Italianno", "Alegreya:ital,wght@0,400;0,500;1,400", "Cormorant SC:wght@500;600"];
// Painted by /tmp/pen/art/themes/zaitun-tuscan.py (tools/art/themes in the repo).
const Art = makeArt("zaitun-tuscan", { villa: [780, 731], branch: [640, 316], sprig: [360, 59], pot: [300, 414], olive: [72, 113] } as const);

const COPY = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Damai Sejahtera",
    title: "Diberkati untuk Bersatu",
    intro: "Dengan penuh syukur atas rahmat dan kasih Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam Misa Sakramen Perkawinan kami, serta berbagi sukacita di meja panjang perjamuan bersama keluarga dan sahabat.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Ranting", "Sang Mempelai"] as [string, string],
  count: ["Menanti Musim Panen", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Tumbuh Bersama", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Sore yang Keemasan"] as [string, string],
  wishes: ["Doa & Kehadiran", "Kirim Ucapan"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah buah terbaik yang melengkapi hari bahagia kami.",
    salam: "Tuhan memberkati.",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima. Tuhan memberkati.",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
};

export default function ZaitunTuscanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9dcc2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.scene} aria-hidden>
            <Art name="villa" eager className={s.sceneArt} />
            <Art name="branch" eager className={s.coverBranch} />
          </div>
          <div className={s.coverBody}>
          <p className={s.kicker}>The Wedding of</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#fff7ea" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3dcae"
        dark="#3a3326"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <div className={s.heroFrame}>
              <div className={s.window}>
                {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
              </div>
              <span className={s.sill} aria-hidden />
              <Art name="pot" className={s.heroPot} />
            </div>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="olive" />,
          amp: <Art name="olive" />,
          portrait: <Art name="sprig" className={s.sprigPortrait} />,
          countDecor: <><Art name="pot" className={s.potL} /><Art name="pot" className={s.potR} /></>,
          closingDecor: <Art name="branch" className={s.closingBranch} />,
          closingEmblem: <Art name="pot" className={s.potEmblem} />,
          sentArt: <Art name="pot" />,
        }}
      />
    </ThemeShell>
  );
}
