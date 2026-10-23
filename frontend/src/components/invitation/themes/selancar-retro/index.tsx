"use client";
// Theme "Selancar Retro" — poster selancar 70-an (desain orisinal, tanpa merek): matahari senja bergaris di atas
// pita-pita warna senja, ombak bergulung dengan buih krem, palem miring, dan van kemping dua warna yang membawa papan
// selancar dan bergoyang di sudut poster. Dicetak ala sablon gouache oleh /tmp/pen/art/themes/selancar-retro.py.
// Shrikhand + Karla, kartu tebal berbayangan offset, potret berbentuk papan selancar.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Shrikhand", "Karla:wght@400;500;700;800"];
const Art = makeArt("selancar-retro", {
  poster: [340, 340], van: [240, 140], board: [40, 185], wave: [150, 21], sun: [50, 50], palm: [110, 184],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, kawan pantai!",
    title: "Kami mau menikah!",
    sub: "Ayo merayakan di tepi ombak",
    intro: "Dengan penuh syukur dan sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk merayakan hari bahagia kami di tepi pantai. Bawa senyum terbaik, kami siapkan matahari terbenamnya.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Satu papan, dua hati", "Kami Berdua"],
  count: ["Ombak berikutnya datang dalam", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat tanggalnya", "Jadwal Acara"],
  story: ["Dari pasir ke pelaminan", "Kisah Kami"],
  gallery: ["Kenangan musim panas", "Album Pantai"],
  wishes: ["Kirim kabar", "Ucapan & RSVP"],
  gifts: ["Tanda kasih", "Kado Pernikahan"],
  closing: {
    thanks: "Terima kasih!",
    text: "Kehadiran dan doa Anda adalah ombak terbaik yang bisa kami harapkan. Sampai jumpa di pantai!",
  },
  sent: "Asyik, ucapanmu sudah sampai! Terima kasih banyak.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tulis ucapan dan doa untuk kami berdua…",
};

const WISHES = [
  { id: "w1", name: "Geng Ombak Pagi", attendance: "yes" as const, message: "Akhirnya instruktur kita menikah juga! Kami datang lengkap dengan papan. Selamat Nadira dan Raka!" },
  { id: "w2", name: "Tante Ratih & Om Wayan", attendance: "yes" as const, message: "Selamat berbahagia, semoga rumah tangga kalian selalu hangat seperti senja di Canggu." },
  { id: "w3", name: "Kevin Wiratama", attendance: "maybe" as const, message: "Lagi kejar tiket dari Jakarta. Kalau tidak sempat, doa terbaik dari jauh ya. Langgeng terus!" },
];

export default function SelancarRetroTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6e8cc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.posterWrap}>
            <Art name="poster" eager className={s.poster} />
            <Art name="van" eager className={s.van} />
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff6e3" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#f2b440"
        dark="#3a2620"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="board" className={s.boardL} />
            <Art name="board" className={s.boardR} />
            <div className={s.card}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <p className={s.cardText} aria-hidden>Salam dari pantai!</p>
              <Art name="sun" className={s.stamp} />
            </div>
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="wave" className={s.divider} />,
          node: <Art name="sun" />,
          amp: <Art name="board" />,
          countDecor: <><Art name="palm" className={`${s.countPalm} ${s.countPalmL}`} /><Art name="palm" className={`${s.countPalm} ${s.countPalmR}`} /></>,
          closingEmblem: <Art name="van" className={s.closingEmblem} />,
          sentArt: <Art name="van" />,
        }}
      />
    </ThemeShell>
  );
}
