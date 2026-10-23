"use client";
// Theme "Peta Bintang" — peta langit malam pernikahan: planisfer cat air biru tua dengan rasi bintang bergaris emas
// tipis, cincin derajat yang berputar pelan, lembar atlas perkamen dengan plat bernomor, fase bulan, dan mawar angin.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bellefair", "EB Garamond:ital,wght@0,400;0,500;1,400", "Geist Mono:wght@400;500", "Mrs Saint Delafield"];
// Painted by /tmp/pen/art/themes/peta-bintang.py (tools/art/themes in the repo).
const Art = makeArt("peta-bintang", { chart: [720, 720], ring: [760, 760], moons: [640, 99], rose: [300, 300], divider: [380, 32] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Yohanes", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru, Alya dan Radit. Semoga kalian selalu menemukan arah pulang satu sama lain." },
  { id: "w2", name: "Teman-teman Klub Astronomi", attendance: "yes" as Attendance, message: "Langit cerah, hati lebih cerah lagi! Kami siapkan teleskopnya untuk malam kalian." },
  { id: "w3", name: "Tante Maria & Om Bram", attendance: "maybe" as Attendance, message: "Bahagia sekali mendengarnya. Kami usahakan datang, doa terbaik menyertai kalian berdua." },
];

function clock(value?: string) {
  if (!toDate(value)) return "";
  const [h, m] = formatDate(value, { hour: "2-digit", minute: "2-digit", hour12: false }).split(/[.:]/);
  return m ? `pukul ${h}.${m}` : "";
}

export default function PetaBintangTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const valid = !!toDate(data.date);
  const numeric = valid ? formatDate(data.date, { day: "2-digit", month: "2-digit", year: "numeric" }).replace(/\//g, ".") : "";
  const year = valid ? formatDate(data.date, { year: "numeric" }) : "";
  const time = clock(data.date);
  const place = data.place?.trim();
  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Salam Hangat",
      title: "Di Bawah Langit yang Sama",
      intro: "Dengan penuh syukur kepada Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk menjadi bagian dari malam ketika dua garis bintang kami bertemu dalam satu rasi. Kehadiran dan doa restu Anda adalah cahaya yang kami harapkan.",
    },
    roles: ["Mempelai Wanita", "Mempelai Pria"],
    couple: ["Dua Bintang", "Kedua Mempelai"],
    count: ["Menuju Malam Itu", "Hitung Mundur"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Koordinat Acara", "Waktu & Tempat"],
    story: ["Lintasan Kami", "Perjalanan Cinta"],
    gallery: ["Album Langit", "Momen Kami"],
    wishes: ["Catatan Pengamatan", "Ucapan & Kehadiran"],
    gifts: ["Tanda Kasih", "Hadiah Pernikahan"],
    closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Anda akan menjadi bintang paling terang di malam bahagia kami." },
    sent: "Terima kasih, ucapan Anda sudah tercatat di langit kami.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
    giftIntro: "Doa restu Anda adalah hadiah terindah. Bila berkenan mengirim tanda kasih, dapat melalui:",
    familyLabel: "Dengan hormat, kami yang berbahagia",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0b1532"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coord}>{numeric ? `Langit ${numeric}` : "Peta Langit"}</p>
          <div className={s.planis}>
            <Art name="ring" eager className={s.ring} />
            <Art name="chart" eager className={s.chart} />
            <span className={s.pin} aria-hidden />
          </div>
          <p className={s.kicker}>Peta langit malam {label.toLowerCase()}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <div className={s.plate}>
            <small>Gambar I</small>
            <p>{place ? `Langit di atas ${place}` : "Langit malam kami"}</p>
            <p>{formatDate(data.date)}</p>
            {time && <b>{time} WIB</b>}
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="currentColor" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={copy}
        demoWishes={WISHES}
        light="#ecd79c"
        dark="#13224a"
        hero={(
          <header className={s.hero}>
            <div className={s.runHead} aria-hidden><span>Lembar I</span><span>Atlas Kami</span><span>{year || "—"}</span></div>
            <div className={s.heroOrb}>
              <Art name="ring" className={s.heroRing} />
              <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
            </div>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="divider" className={s.heroDiv} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="rose" />,
          portrait: <Art name="rose" />,
          countDecor: <Art name="moons" className={s.countMoons} />,
          closingDecor: <Art name="chart" className={s.closingSky} />,
          closingEmblem: <Art name="rose" className={s.closingRose} />,
          sentArt: <Art name="rose" />,
        }}
      />
    </ThemeShell>
  );
}
