"use client";
// Theme "Malakit Hijau" — Luxury: lempeng batu malakit berpita konsentris yang dipoles dan dibelah-cermin (book-matched),
// tatahan garis emas, plakat onyx krem bersudut potong, dan kabosyon malakit berbingkai emas berbutir. Sampul: plakat
// onyx bertatah emas di atas lempeng malakit; potret oval seperti liontin; kartu acara dari batu malakit.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;1,400;1,500", "Tenor Sans:wght@400", "Mea Culpa:wght@400"];
// Painted by /tmp/pen/art/themes/malakit-hijau.py (slab, band, onyx and gold are CSS backgrounds)
const Art = makeArt("malakit-hijau", { gem: [110, 134], divider: [360, 36] } as const);

export default function MalakitHijauTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#04140c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.plaqueWrap}>
            <Art name="gem" className={s.coverGem} eager />
            <div className={s.plaque}>
              <div className={s.plaqueRing}>
                <div className={s.plaqueLine}>
                  <div className={s.plaqueCore}>
                    <p className={s.kicker}>{data.eventLabel ?? "Pernikahan"}</p>
                    <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
                    <Art name="divider" className={s.coverRule} eager />
                    <p className={s.coverDate}>{formatDate(data.date)}</p>
                    <div className={s.guest}>
                      <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                      <strong>{guestLabel(data)}</strong>
                      {table && <span className={s.table}>{table}</span>}
                    </div>
                    <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#ecd59a" />Buka Undangan</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ecd59a"
        dark="#082b1b"
        demoWishes={[
          { id: "w1", name: "Keluarga Bapak Robert Gunawan", attendance: "yes", message: "Selamat menempuh hidup baru, Kirana dan Adrian. Semoga rumah tangga kalian kokoh, berkilau, dan makin indah setiap tahunnya." },
          { id: "w2", name: "Natasha & Kevin", attendance: "yes", message: "Dari teman satu angkatan: kami sudah siap dansa sampai lampu dimatikan. Bahagia selalu!" },
          { id: "w3", name: "Tante Lily Santoso", attendance: "maybe", message: "Semoga bisa terbang dari Medan tepat waktu. Kalau belum, doa Tante menyertai kalian berdua." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Dengan Penuh Sukacita",
            title: "Kami Mengundang Anda",
            intro: "Dengan penuh sukacita dan rasa syukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan berbagi kebahagiaan di hari pernikahan kami. Kehadiran Anda akan melengkapi hari istimewa ini.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Hati", "Kedua Mempelai"],
          count: ["Menuju Hari Bahagia", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Lapis demi Lapis", "Kisah Kami"],
          gallery: ["Galeri", "Momen Berharga"],
          wishes: ["Ucapan & Doa", "Konfirmasi Kehadiran"],
          gifts: ["Tanda Kasih", "Hadiah Pernikahan"],
          closing: {
            thanks: "Terima Kasih",
            text: "Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          sent: "Terima kasih, ucapan Anda sudah kami terima.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
          giftIntro: "Kehadiran Anda adalah hadiah terbesar bagi kami. Bila ingin memberikan tanda kasih, dapat melalui:",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Save the Date</p>
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
              <Art name="gem" className={s.heroGem} />
            </div>
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="divider" /></span>,
          node: <Art name="gem" />,
          amp: <Art name="gem" />,
          portrait: <Art name="gem" className={s.portraitGem} />,
          closingEmblem: <Art name="gem" className={s.closingGem} />,
          sentArt: <Art name="gem" />,
        }}
      />
    </ThemeShell>
  );
}
