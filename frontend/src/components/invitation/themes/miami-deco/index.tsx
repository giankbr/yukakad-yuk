"use client";
// Theme "Miami Deco" — tepi pantai art deco pastel dalam gouache: hotel merah muda bertingkat dengan sirip tengah,
// jendela kapal (porthole) dan alis jendela, tetangga mint dan lemon, palem, payung pantai bergaris. Nama mempelai
// menyala di papan neon lembut, tamu mendapat gantungan kunci kamar, foto pembuka berupa kartu pos air mail, potret
// berbingkai jendela kapal, lantai terrazzo, dan flamingo neon yang berkedip di malam hitung mundur.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Righteous:wght@400", "Lexend:wght@400;600", "Sacramento:wght@400", "Monoton:wght@400"];
// Painted by /tmp/pen/art/themes/miami-deco.py (terrazzo tile is a CSS background)
const Art = makeArt("miami-deco", { facade: [720, 1320], neon: [300, 480], palm: [240, 385], porthole: [120, 120], divider: [320, 42] } as const);

export default function MiamiDecoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const room = table.replace(/^(Meja|Kamar)\s+/i, "");
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#7fcdee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="facade" eager className={s.facade} />
          <p className={s.ribbon}><i aria-hidden />{formatDate(data.date)}<i aria-hidden /></p>
          <div className={s.sign}>
            <p className={s.signKicker}>Undangan Pernikahan</p>
            <h1 className={s.coverNames}><span>{bride}</span><em>&amp;</em><span>{groom}</span></h1>
          </div>
          <div className={s.key}>
            <span className={s.keyHole} aria-hidden />
            <div className={s.keyBody}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
            </div>
            {room && <span className={s.keyRoom}>{/^Kamar/i.test(table) ? "Kamar" : "Meja"}<br />{room}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fff1a6"
        dark="#1f3b5c"
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Halo, Sahabat!",
            title: "Ayo Berpesta di Tepi Pantai",
            intro: "Dengan sukacita dan penuh syukur kepada Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk hadir merayakan hari pernikahan kami: satu sore penuh matahari, musik, dan tawa bersama orang-orang tersayang.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Tamu Kehormatan", "Kedua Mempelai"],
          count: ["Check-in dalam", "Menuju Hari H"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Agenda Pesta", "Rangkaian Acara"],
          story: ["Dari Antrean ke Pelaminan", "Kisah Kami"],
          gallery: ["Kartu Pos", "Galeri Kami"],
          wishes: ["Buku Tamu", "Ucapan & Konfirmasi"],
          gifts: ["Layanan Kamar", "Kado Pernikahan"],
          closing: { thanks: "Sampai Jumpa!", text: "Terima kasih sudah menjadi bagian dari hari bahagia kami. Siapkan kacamata hitam dan senyum terbaikmu, ya!" },
          sent: "Yay! Ucapanmu sudah masuk buku tamu kami.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa terbaik untuk kami…",
          giftIntro: "Kehadiranmu sudah jadi kado terbaik. Jika ingin mengirim tanda kasih, bisa melalui:",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Salam hangat dari tepi pantai</p>
            <div className={s.card}>
              {photo ? <div className={s.heroPhoto}><Photo src={photo} alt={`${bride} & ${groom}`} /></div> : <div className={s.cardNoPhoto}><Art name="palm" /></div>}
              <span className={s.stamp} aria-hidden><Art name="porthole" /></span>
            </div>
            <h1 className={s.heroNames}>{bride} <em>&amp;</em> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="porthole" />,
          amp: <Art name="palm" />,
          portrait: <Art name="palm" className={s.portraitPalm} />,
          countDecor: <span className={s.neonBird} aria-hidden><Art name="neon" /></span>,
          closingDecor: <><Art name="palm" className={`${s.closePalm} ${s.closePalmL}`} /><Art name="palm" className={`${s.closePalm} ${s.closePalmR}`} /></>,
          closingEmblem: <Art name="neon" className={s.emblem} />,
          sentArt: <Art name="porthole" />,
        }}
      />
    </ThemeShell>
  );
}
