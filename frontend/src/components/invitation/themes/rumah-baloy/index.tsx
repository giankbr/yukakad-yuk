"use client";
// Theme "Rumah Baloy" — balai adat suku Tidung di atas laut Tarakan dalam cat gouache: dinding hijau, ukiran kuning bermotif
// matahari di bubungan, aksen merah, atap sirap ulin dan bakau berakar tunjang. Sampul berupa lukisan Baloy di atas papan
// laut dalam, pita ukiran hijau-kuning sebagai bingkai setiap bagian, potret dan kartu acara berbentuk bubungan rumah.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@500;700", "Alegreya:ital,wght@0,400;0,700;1,400", "Marcellus SC", "Amiri"];
// Painted by /tmp/pen/art/themes/rumah-baloy.py (band is the CSS background of every carved strip).
const Art = makeArt("rumah-baloy", { baloy: [780, 920], bakau: [360, 289], divider: [498, 60], kembang: [120, 120] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga H. Burhanuddin", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga menjadi keluarga sakinah, mawaddah, warahmah, kokoh seperti tiang ulin Baloy." },
  { id: "w2", name: "Rekan Guru SDN 012 Tarakan", attendance: "yes" as Attendance, message: "Selamat Bu Hasnah dan Pak Ridwan! Semoga dilimpahi berkah dan cepat diberi momongan yang soleh-solehah." },
  { id: "w3", name: "Fadli & Keluarga, Nunukan", attendance: "maybe" as Attendance, message: "Insyaallah kami menyeberang ke Tarakan. Kalau terhalang ombak, doa kami tetap sampai untuk kalian berdua." },
];

export default function RumahBaloyTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const heroPhoto = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم",
      kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
      title: "Dengan Rahmat Allah",
      intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami secara adat Tidung. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
    },
    roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
    couple: ["Bismillah, Kami Bersanding", "Kedua Mempelai"],
    count: ["Menanti Pasang Naik", "Menuju Hari Bahagia"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Waktu & Tempat", "Rangkaian Acara"],
    story: ["Perjalanan Kami", "Kisah dari Tepi Laut"],
    gallery: ["Galeri", "Momen Bahagia"],
    wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
    gifts: ["Tanda Kasih", "Amplop Digital"],
    closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas kebaikan Anda sekalian.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
    sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#123f3d"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.scene} aria-hidden>
            <Art name="baloy" eager />
            <span className={s.shimmer} />
          </div>
          <div className={s.plaque}>
            <p className={s.kicker}>Walimatul &apos;Urs · Adat Tidung</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}><Art name="kembang" eager />{formatDate(data.date)}<Art name="kembang" eager /></p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#10322f" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f8dc6c"
        dark="#123f3d"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="bakau" className={`${s.heroBakau} ${s.heroBakauL}`} />
            <Art name="bakau" className={`${s.heroBakau} ${s.heroBakauR}`} />
            {heroPhoto && <div className={s.heroPhoto}><Photo src={heroPhoto} alt="" /></div>}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="kembang" />,
          amp: <Art name="kembang" />,
          countDecor: <><Art name="bakau" className={`${s.countBakau} ${s.countBakauL}`} /><Art name="bakau" className={`${s.countBakau} ${s.countBakauR}`} /></>,
          closingDecor: <div className={s.closingDecor} aria-hidden><Art name="bakau" /><Art name="bakau" /></div>,
          closingEmblem: <Art name="kembang" className={s.closingEmblem} />,
          sentArt: <Art name="kembang" />,
        }}
      />
    </ThemeShell>
  );
}
