"use client";
// Theme "Ladang Tulip" — spring in gouache: a painted field of striped tulip rows running to the horizon with a windmill
// whose sails turn slowly (separate layer), a postcard photo with a tulip stamp, tulip-cup portrait frames with striped
// rims, countdown blooms on a leaf-green band, and striped ribbons (the field's colours) as every divider and edge.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif:wght@400", "Karla:wght@400;500;700"];
// Painted by /tmp/pen/art/themes/ladang-tulip.py
const Art = makeArt("ladang-tulip", { ladang: [620, 938], wiek: [260, 260], tulip: [110, 302], buket: [620, 248] } as const);

export default function LadangTulipTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dcebe0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.scene} aria-hidden>
            <Art name="ladang" eager />
            <span className={s.sails}><Art name="wiek" eager /></span>
          </div>
          <div className={s.coverBody}>
            <p className={s.kicker}>Undangan Pernikahan</p>
            <h1 className={s.names}>{data.couple.bride} <span>&amp;</span> {data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffdf7" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fde7a6"
        dark="#356a2a"
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Dengan sukacita",
            title: "Musim Semi Kami",
            intro: "Setiap bunga mekar pada waktunya. Dengan penuh syukur kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan berbagi kebahagiaan di hari pernikahan kami.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Yang Berbahagia", "Kedua Mempelai"],
          count: ["Sebentar Lagi Mekar", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Tumbuh Bersama", "Kisah Kami"],
          gallery: ["Galeri", "Kartu Pos Kami"],
          wishes: ["Ucapan & Kehadiran", "Kirim Ucapan"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i akan membuat hari kami mekar sempurna." },
          sent: "Terima kasih, ucapan Anda sudah kami terima.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan ucapan dan doa untuk kami berdua…",
        }}
        hero={(
          <header className={s.hero}>
            {photo && (
              <figure className={s.postcard}>
                <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} />
                <figcaption>Salam dari ladang tulip</figcaption>
                <span className={s.stamp} aria-hidden><Art name="tulip" /></span>
              </figure>
            )}
            <p className={s.heroKicker}>{data.eventLabel ?? "Pernikahan"}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <span>&amp;</span> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="tulip" /></span>,
          node: <Art name="tulip" />,
          amp: <Art name="tulip" />,
          countDecor: <Art name="buket" className={s.countBuket} />,
          closingDecor: <Art name="buket" className={s.closingBuket} />,
          closingEmblem: <Art name="tulip" className={s.closingTulip} />,
          sentArt: <Art name="tulip" />,
        }}
      />
    </ThemeShell>
  );
}
