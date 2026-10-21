"use client";
// Theme "Sweet Seventeen" — malam glam merah muda & mutiara: angka "17" bergaya balon satin, pita satin dengan kilap
// yang dilukis, untaian mutiara berjuntai, dan kilau malam lukisan tangan di atas langit plum.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;1,400;1,500", "Pinyon Script", "Jost:wght@300;400;500"];
// Painted by /tmp/pen/art/themes/sweet-seventeen.py (tools/art/themes in the repo).
const Art = makeArt("sweet-seventeen", { seventeen: [440, 496], bow: [300, 327], pearls: [410, 150], divider: [220, 20] } as const);

export default function SweetSeventeenTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Sweet Seventeen";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "You Are Invited",
      title: "Malam Tujuh Belas",
      intro: `Dengan penuh sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk merayakan ulang tahun ketujuh belas ${names}. Kehadiran dan doa Anda akan membuat malam ini semakin berkilau.`,
    },
    roles: ["The Birthday Girl", "Bersama"] as [string, string],
    couple: ["Tujuh Belas Tahun", child ? `Hai, aku ${nick}` : "Yang Berulang Tahun"] as [string, string],
    count: ["Menuju Malam Istimewa", "Hitung Mundur"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Save the Date", "Waktu & Tempat"] as [string, string],
    story: ["Perjalanan", "Tujuh Belas Tahun"] as [string, string],
    gallery: ["Galeri", "Momen Berkilau"] as [string, string],
    wishes: ["Ucapan & Doa", "Kirim Ucapan"] as [string, string],
    gifts: ["Tanda Kasih", "Kado Digital"] as [string, string],
    closing: { thanks: "Thank You", text: `Terima kasih atas doa dan kehadiran Anda. Sampai jumpa di malam penuh kilau bersama ${names}.` },
    sent: "Terima kasih, ucapan manis Anda sudah terkirim.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1d0c27"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.sparkle} aria-hidden />
          <Art name="pearls" eager className={s.pearls} />
          <p className={s.kicker}>{label}</p>
          <div className={s.seventeenWrap} aria-hidden>
            <Art name="seventeen" eager className={s.seventeen} />
            <Art name="bow" eager className={s.bow} />
          </div>
          <h1 className={s.coverName}>{names}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#5a2448" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        light="#fbe3ec"
        dark="#3a1a35"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <Art name="pearls" className={s.pearls} />
            <Art name="seventeen" className={s.hero17} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroName}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="bow" />,
          portrait: <Art name="bow" className={s.portraitBow} />,
          countDecor: <Art name="pearls" className={s.countPearls} />,
          closingEmblem: <><Art name="seventeen" className={s.closing17} /><p className={s.closingName}>{names}</p></>,
          sentArt: <Art name="bow" />,
        }}
      />
    </ThemeShell>
  );
}
