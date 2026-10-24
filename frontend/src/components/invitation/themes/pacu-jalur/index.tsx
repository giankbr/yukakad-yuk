"use client";
// Theme "Pacu Jalur" — walimah Melayu Kuantan Singingi dalam lukisan gouache rakyat: jalur panjang berukir dengan haluan
// bercat dan barisan anak pacu mendayung di Batang Kuantan, tepian penuh penonton, umbul-umbul bambu yang berkibar dan
// bendera segitiga di langit sampul, papan nomor jalur untuk tanggal, potret berbentuk umbul-umbul, hitung mundur
// berlajur seperti lintasan pacu. Pembuka Islami (basmalah + salam).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Alegreya:ital,wght@0,400;0,500;0,700;0,800;1,500", "Alegreya Sans:wght@400;500;700", "Barlow Condensed:wght@500;600;700", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/pacu-jalur.py (tools/art/themes in the repo).
const Art = makeArt("pacu-jalur", {
  jalur: [780, 206], river: [780, 430], umbul: [99, 603], bunting: [780, 79], mini: [320, 61], prow: [120, 188],
} as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Sedayung Sehaluan",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami di tepian Batang Kuantan. Merupakan suatu kehormatan apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Pengantin Perempuan", "Pengantin Lelaki"],
  couple: ["Anak Pacu Sejalur", "Kedua Mempelai"],
  count: ["Menanti Bunyi Meriam", "Menuju Hari Bersanding"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Lintasan Acara", "Waktu & Tempat"],
  story: ["Hikayat Kami", "Mendayung Bersama"],
  gallery: ["Tepian Kenangan", "Galeri"],
  wishes: ["Sorak & Doa", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga menghaturkan terima kasih. Semoga Allah membalas setiap kebaikan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Terima kasih, doa dan ucapan Anda sudah sampai ke tepian.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
  giftIntro: "Doa restu Anda adalah hadiah terindah bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Keluarga Datuk Rajo Mangkuto", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga sedayung sehaluan sampai ke tepian bahagia." },
  { id: "w2", name: "Anak Pacu Jalur Siposan Rimbo", attendance: "yes" as Attendance, message: "Selamat Fadhil dan Nurul! Kami datang beramai-ramai, sorak paling kencang untuk pengantin." },
  { id: "w3", name: "Ibu Hj. Ernawati", attendance: "maybe" as Attendance, message: "Insyaallah hadir selepas Zuhur. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
];

function River({ className, eager }: { className: string; eager?: boolean }) {
  return (
    <div className={className} aria-hidden>
      <Art name="river" eager={eager} className={s.river} />
      <Art name="jalur" eager={eager} className={s.boat} />
    </div>
  );
}

export default function PacuJalurTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#24493d"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="bunting" eager className={s.bunting} />
          <Art name="umbul" eager className={`${s.umbul} ${s.umbulL}`} />
          <Art name="umbul" eager className={`${s.umbul} ${s.umbulR}`} />
          <p className={s.kicker}>Undangan {label}</p>
          <p className={s.place}>{data.place || "Walimatul 'Ursy"}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.board}><span>Hari H</span><strong>{formatDate(data.date)}</strong></p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
          </div>
          <River className={s.stage} eager />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6d36a"
        dark="#1f4d3c"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroFrame}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>}
            <Art name="mini" className={s.heroMini} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="mini" className={s.divider} />,
          node: <Art name="prow" />,
          amp: <Art name="prow" />,
          portrait: <Art name="umbul" className={s.portraitPole} />,
          closingDecor: <River className={s.closingStage} />,
          sentArt: <Art name="mini" />,
        }}
      />
    </ThemeShell>
  );
}
