"use client";
// Theme "Venesia Kanal" — pemandangan: kanal kecil Venesia dilukis cat air longgar yang larut ke kertas kosong, fasad
// pastel, jendela lengkung bertirai hijau, jembatan batu, menara lonceng, tiang tambat bergaris, pantulan pecah, dan
// gondola kosong yang mengayun pelan. Potret dalam jendela lengkung gotik, acara sebagai kartu pos bercap.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;1,400;1,500", "Libre Caslon Text:ital,wght@0,400;0,700;1,400", "Italianno"];
// Painted by /tmp/pen/art/themes/venesia-kanal.py
const Art = makeArt("venesia-kanal", { scene: [580, 803], gondola: [420, 143], poles: [180, 93], houses: [720, 240] } as const);

const WISHES = [
  { id: "w1", name: "Tante Margaretha", attendance: "yes" as Attendance, message: "Selamat Livia dan Adrian! Semoga perjalanan kalian selalu seindah sore di kanal itu, saling menunggu di setiap jembatan." },
  { id: "w2", name: "Teman Studio Arsitektur", attendance: "yes" as Attendance, message: "Dari sketsa yang ketumpahan kopi sampai pelaminan. Kami datang bawa payung, siapa tahu hujan di taman!" },
  { id: "w3", name: "Kevin & Sasha", attendance: "maybe" as Attendance, message: "Semoga bisa terbang pulang tepat waktu. Kalaupun belum, doa dan pelukan kami sampai duluan." },
];

export default function VenesiaKanalTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();
  const label = data.eventLabel ?? "Pernikahan";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf6ee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
          <div className={s.coverScene} aria-hidden>
            <Art name="scene" eager />
            <Art name="gondola" eager className={s.coverGondola} />
          </div>
          <div className={s.coverFoot}>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf6ee" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf6ee"
        dark="#22344d"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Dengan penuh sukacita",
            title: "Kami Akan Menikah",
            sub: "dan ingin berbagi hari itu bersama Anda",
            intro: "Dengan rasa syukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi bagian dari hari bahagia kami. Kehadiran dan doa restu Anda adalah hadiah yang paling berarti.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Jendela, Satu Kanal", "Kedua Mempelai"],
          count: ["Menuju Hari Itu", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Kartu Pos Acara", "Waktu & Tempat"],
          story: ["Menyusuri Kanal", "Kisah Kami"],
          gallery: ["Galeri", "Album Perjalanan"],
          wishes: ["Pesan & Doa", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Grazie",
            text: "Terima kasih atas kehadiran, doa, dan kasih sayang Bapak/Ibu/Saudara/i. Sampai jumpa di hari bahagia kami.",
            salam: "dengan cinta, dari kami berdua",
          },
          sent: "Terima kasih, pesan dan doa Anda sudah terkirim.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan pesan dan doa untuk kedua mempelai…",
          giftIntro: "Kehadiran Anda sudah lebih dari cukup. Namun jika ingin memberi tanda kasih, dapat melalui:",
          familyLabel: "Kami yang berbahagia",
        }}
        hero={(
          <header className={s.hero}>
            <figure className={s.postcard} style={{ margin: 0 }}>
              <div className={s.heroPhoto}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
              <figcaption><span>Saluti da Venezia</span><b>{bride} &amp; {groom}</b></figcaption>
              <span className={s.stamp} aria-hidden><Art name="poles" /></span>
            </figure>
            <p className={s.heroKicker}>Kami akan menikah</p>
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="poles" /></span>,
          node: <Art name="poles" />,
          amp: <Art name="poles" />,
          countDecor: <Art name="houses" className={s.countHouses} />,
          closingDecor: <Art name="houses" className={s.closingHouses} />,
          closingEmblem: <Art name="gondola" className={s.closingEmblem} />,
          sentArt: <Art name="gondola" />,
        }}
      />
    </ThemeShell>
  );
}
