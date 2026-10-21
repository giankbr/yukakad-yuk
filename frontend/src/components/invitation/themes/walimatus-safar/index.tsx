"use client";
// Theme "Walimatus Safar" — syukuran menjelang keberangkatan haji/umrah dalam hijau tua dan emas: lukisan gouache jalan
// pasir yang berkelok ke cakrawala dengan pohon kurma, pesawat kecil dan jejak awannya, lentera emas berlubang bintang,
// pita geometri bertabur khatam, dan doa safar. Tanpa foto, tanpa gambar Ka'bah.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "Noto Serif:ital,wght@0,400;0,500;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/walimatus-safar.py (band and velvet are CSS backgrounds)
const Art = makeArt("walimatus-safar", { path: [560, 765], plane: [280, 130], lamp: [200, 584], star: [120, 120] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";
const DOA_SAFAR = "سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ، وَإِنَّا إِلَى رَبِّنَا لَمُنْقَلِبُونَ";

function Scene({ eager }: { eager?: boolean }) {
  return (
    <div className={s.scene} aria-hidden>
      <Art name="path" eager={eager} />
      <Art name="plane" eager={eager} className={s.plane} />
    </div>
  );
}

function Divider() {
  return <span className={s.divider} aria-hidden><Art name="star" /></span>;
}

export default function WalimatusSafarTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatus Safar";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const first = child ? (child.nickname?.trim() || child.name.trim()) : data.couple.bride;
  const second = child ? "" : data.couple.groom?.trim() ?? "";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0f3b2e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="lamp" eager className={s.lampL} />
          <Art name="lamp" eager className={s.lampR} />
          <p className={s.kicker}>{label}</p>
          <Scene eager />
          <h1 className={s.coverNames}>{first}{second && <><em>&amp;</em>{second}</>}</h1>
          <p className={s.coverSub}>Mohon doa restu menuju Tanah Suci</p>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#0f3b2e" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        celebrant
        light="#ecd48f"
        dark="#0f3b2e"
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Labbaik Allahumma Labbaik",
            intro: "Dengan memohon rahmat Allah Subhanahu wa Ta'ala, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam walimatus safar dan doa bersama, menjelang keberangkatan kami menunaikan ibadah haji ke Baitullah. Mohon doakan agar perjalanan kami dimudahkan dan kami kembali sebagai haji yang mabrur.",
          },
          roles: ["Calon Haji", "Calon Hajjah"],
          couple: ["Mohon Doa Restu", "Calon Jamaah Haji"],
          count: ["Menjelang Keberangkatan", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Langkah Menuju Baitullah", "Perjalanan Panjang"],
          gallery: ["Galeri", "Kenangan"],
          wishes: ["Titip Doa", "Doa & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: "Terima kasih atas doa dan kehadiran Bapak/Ibu/Saudara/i. Mohon maaf lahir dan batin atas segala khilaf kami. Semoga kita semua kelak dipanggil ke Tanah Suci.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa Anda sudah kami terima. Insyaallah kami bawa hingga Tanah Suci.",
        }}
        hero={(
          <header className={s.hero}>
            <Scene />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{first}{second && <><em>&amp;</em>{second}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <section className={s.doa} aria-labelledby="ws-doa">
              <Art name="star" />
              <h2 id="ws-doa">Doa Safar</h2>
              <p className={s.doaAr} lang="ar" dir="rtl">{DOA_SAFAR}</p>
              <p className={s.doaId}>&ldquo;Mahasuci Allah yang telah menundukkan semua ini bagi kami, padahal kami sebelumnya tidak mampu menguasainya. Dan sesungguhnya kami akan kembali kepada Tuhan kami.&rdquo;</p>
              <p className={s.doaSrc}>QS. Az-Zukhruf: 13–14</p>
            </section>
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="star" />,
          portrait: <Art name="star" className={s.portraitStar} />,
          closingDecor: <Art name="plane" className={s.closingPlane} />,
          closingEmblem: <Art name="star" className={s.closingEmblem} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
