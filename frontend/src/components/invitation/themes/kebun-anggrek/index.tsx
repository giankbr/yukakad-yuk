"use client";
// Theme "Kebun Anggrek" — a tropical orchid glasshouse in gouache: moth orchids, dendrobium sprays and a tessellated blue
// vanda; the cover looks out through a white-iron arched glasshouse window with morning condensation (droplets run
// down the pane), names on a fogged pane; arched window portraits with mullions, plant-tag event cards, frosted panes.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bellefair", "Karla:wght@400;600;700", "Allura", "Amiri"];
// Painted by /tmp/pen/art/themes/kebun-anggrek.py (tools/art/themes in the repo).
const Art = makeArt("kebun-anggrek", { phal: [480, 349], dendro: [320, 471], vanda: [380, 308], sprig: [200, 93], leaf: [260, 230] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Rahmat Allah",
    intro: "Maha Suci Allah yang menciptakan segala sesuatu berpasang-pasangan. Dengan memohon rahmat dan ridha-Nya, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Tumbuh Bersama", "Kedua Mempelai"] as [string, string],
  count: ["Menunggu Mekar", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Catatan Kebun", "Kisah Kami"] as [string, string],
  gallery: ["Dari Balik Kaca", "Galeri"] as [string, string],
  wishes: ["Doa & Kehadiran", "Kirim Doa Restu"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu. Jazakumullahu khairan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah kami terima.",
};

export default function KebunAnggrekTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#cfe0ca"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.glass} aria-hidden />
          <span className={`${s.drip} ${s.dripA}`} aria-hidden />
          <span className={`${s.drip} ${s.dripB}`} aria-hidden />
          <span className={`${s.drip} ${s.dripC}`} aria-hidden />
          <Art name="phal" eager className={s.coverPhal} />
          <Art name="dendro" eager className={s.coverDendro} />
          <Art name="vanda" eager className={s.coverVanda} />
          <div className={s.fog}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
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
        light="#f3f8ef"
        dark="#1f4f3a"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            {photo && (
              <div className={s.heroWin}>
                <div className={s.heroPane}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>
                <Art name="phal" className={s.heroPhal} />
                <Art name="vanda" className={s.heroVanda} />
              </div>
            )}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="sprig" className={s.divider} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <span />,
          amp: <Art name="sprig" />,
          portrait: <Art name="vanda" className={s.portraitVanda} />,
          countDecor: <><Art name="leaf" className={`${s.countLeaf} ${s.countLeafA}`} /><Art name="leaf" className={`${s.countLeaf} ${s.countLeafB}`} /></>,
          closingEmblem: (
            <div className={s.closingArt} aria-hidden>
              <Art name="phal" className={s.closingPhal} />
              <Art name="dendro" className={s.closingDendro} />
            </div>
          ),
          sentArt: <Art name="sprig" />,
        }}
      />
    </ThemeShell>
  );
}
