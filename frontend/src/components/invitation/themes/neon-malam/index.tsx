"use client";
// Theme "Neon Malam" — a night bar wall: painted old brick under low light, hand-bent neon tube signs in pink, teal and
// amber and a swinging Edison bulb (original design). The names glow as neon script (CSS light on live text), cards are
// smoked-glass panels outlined in light, gallery photos are posters pasted a little crooked on the wall.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Sacramento", "Bricolage Grotesque:wght@400;700;800", "Space Mono:wght@400;700"];
// Bent and lit by /tmp/pen/art/themes/neon-malam.py (tools/art/themes in the repo).
const Art = makeArt("neon-malam", { sign: [560, 718], heart: [240, 220], cheers: [280, 249], rings: [240, 190], star: [80, 80], wave: [320, 58], bulb: [110, 343] } as const);

const COPY = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Namo Buddhaya",
    title: "Dua Cahaya, Satu Nyala",
    intro: "Dengan penuh sukacita dan berkah Tiratana, kami mengundang Bapak/Ibu/Saudara/i untuk hadir pada pemberkatan pernikahan kami, lalu merayakannya bersama di malam yang penuh cahaya, musik, dan tawa.",
  },
  roles: ["The Bride", "The Groom"] as [string, string],
  couple: ["Duet Kami", "Mempelai"] as [string, string],
  count: ["Lampu Hampir Menyala", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Catat Tanggalnya", "Rangkaian Acara"] as [string, string],
  story: ["Setlist Kami", "Kisah Cinta"] as [string, string],
  gallery: ["Galeri", "Malam-Malam Kita"] as [string, string],
  wishes: ["RSVP & Ucapan", "Tinggalkan Pesan"] as [string, string],
  gifts: ["Kado Digital", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah cahaya paling terang di malam bahagia kami.",
    salam: "Sabbe satta bhavantu sukhitatta. Semoga semua makhluk hidup berbahagia.",
  },
  sent: "Pesanmu sudah menyala di dinding kami. Terima kasih!",
  wishPlaceholder: "Tulis ucapan dan doa terbaikmu…",
};

const WISHES = [
  { id: "w1", name: "Nadia & Bimo", attendance: "yes" as const, message: "Akhirnya duet ini resmi! Siap turun ke lantai dansa. Selamat ya Feli dan Ryan, langgeng terus." },
  { id: "w2", name: "Om Johan Halim", attendance: "yes" as const, message: "Selamat menempuh hidup baru. Semoga rukun, saling menjaga, dan selalu berbahagia." },
  { id: "w3", name: "Tim Kafe Lantai Dua", attendance: "maybe" as const, message: "Kami usahakan datang setelah shift! Panggung kecil kita bangga sekali sama kalian." },
];

export default function NeonMalamTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0b0709"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="bulb" eager className={s.bulb} />
          <Art name="bulb" eager className={`${s.bulb} ${s.bulb2}`} />
          <p className={s.kicker}>The Wedding of</p>
          <div className={s.sign}>
            <Art name="sign" eager className={s.signArt} />
            <div className={s.signText}>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            </div>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#ffffff" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffffff"
        dark="#120c10"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{year ? `${label} · ${year}` : label}</p>
            <div className={s.heroFrame}>
              <Art name="heart" className={s.heroHeart} />
              {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
              <span className={s.tape} aria-hidden />
            </div>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="wave" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          portrait: <Art name="star" className={s.starTag} />,
          countDecor: <><Art name="rings" className={s.ringsDecor} /><Art name="cheers" className={s.cheersDecor} /></>,
          closingEmblem: <Art name="heart" className={s.heartEmblem} />,
          sentArt: <Art name="rings" />,
        }}
      />
    </ThemeShell>
  );
}
