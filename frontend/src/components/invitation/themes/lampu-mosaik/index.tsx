"use client";
// Theme "Lampu Mosaik" — lampu gantung kaca mosaik (bola, bawang, tetes) yang tersusun dari ratusan keping kaca kecil,
// menyala dari dalam dalam warna delima, pirus, kunyit dan ungu, tergantung pada rantai kuningan di langit malam ungu
// pekat; genangan cahaya warna-warni, potret segi delapan, hitung mundur berupa bola kaca menyala (desain orisinal).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@400;500;600", "Crimson Pro:ital,wght@0,400;0,500;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/lampu-mosaik.py (tools/art/themes in the repo).
const Art = makeArt("lampu-mosaik", {
  lampA: [300, 688], lampB: [230, 519], lampC: [210, 427], lampD: [190, 514], pools: [560, 221], divider: [300, 99], rosette: [220, 220],
} as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dua Cahaya, Satu Rumah",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Atas Izin Allah", "Kedua Mempelai"] as [string, string],
  count: ["Menghitung Malam", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Keping demi Keping", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Momen Bercahaya"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah cahaya yang menghangatkan malam bahagia kami. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
};

export default function LampuMosaikTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#140e22"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.lamps} aria-hidden>
            <span className={`${s.hang} ${s.hD}`}><Art name="lampD" eager /></span>
            <span className={`${s.hang} ${s.hE}`}><Art name="lampC" eager /></span>
            <span className={`${s.hang} ${s.hB}`}><Art name="lampB" eager /></span>
            <span className={`${s.hang} ${s.hC}`}><Art name="lampC" eager /></span>
            <span className={`${s.hang} ${s.hA}`}><Art name="lampA" eager /></span>
          </div>
          <div className={s.coverBody}>
            <Art name="pools" eager className={s.coverPools} />
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#1b1222" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f5cf7d"
        dark="#1b1222"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <span className={s.heroSideL} aria-hidden><Art name="lampD" /></span>
            <span className={s.heroSideR} aria-hidden><Art name="lampB" /></span>
            <span className={s.heroChain} aria-hidden />
            <span className={s.heroCap} aria-hidden />
            {photo && <div className={s.heroGlobe}><div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div></div>}
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="rosette" />,
          amp: <Art name="rosette" />,
          portrait: <Art name="rosette" className={s.rosetteP} />,
          countDecor: <Art name="pools" className={s.poolsCount} />,
          closingDecor: <Art name="pools" className={s.poolsClose} />,
          closingEmblem: <Art name="rosette" className={s.rosetteC} />,
          sentArt: <Art name="rosette" />,
        }}
      />
    </ThemeShell>
  );
}
