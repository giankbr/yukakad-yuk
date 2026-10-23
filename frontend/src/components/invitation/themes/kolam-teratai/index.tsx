"use client";
// Theme "Kolam Teratai" — an original impressionist morning pond painted in broken colour: hanging willow, a warm
// wooden arched footbridge and its broken reflection, lily pads and pink lotus, light glinting on the water. The cover
// is the full painting with a soft morning-mist glow behind the names and a shimmer on the water; portraits are
// notched lily-pad rounds with a floating lotus, the countdown is a strip of the pond, events are misty pools and the
// closing returns to the water's edge. Neutral (non-religious) couple.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Ephesis"];
// Painted by /tmp/pen/art/themes/kolam-teratai.py (tools/art/themes in the repo).
const Art = makeArt("kolam-teratai", { lotus: [220, 146], pads: [760, 171], dab: [240, 38] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Selamat Pagi",
    title: "Di Tepi Kolam Teratai",
    intro: "Dengan penuh sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk menyaksikan pagi ketika kami saling berjanji, di antara teratai yang baru mekar dan cahaya yang menari di permukaan air.",
  },
  attend: { maybe: "Mungkin" },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Kuntum", "Kedua Mempelai"] as [string, string],
  count: ["Menanti Pagi Itu", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Di Seberang Jembatan", "Rangkaian Acara"] as [string, string],
  story: ["Riak Kenangan", "Kisah Kami"] as [string, string],
  gallery: ["Pantulan", "Galeri"] as [string, string],
  wishes: ["Pesan di Permukaan Air", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa baik Bapak/Ibu/Saudara/i akan menjadi cahaya pagi yang paling hangat bagi kami.",
    salam: "Sampai bertemu di tepi kolam.",
  },
  sent: "Terima kasih, pesan Anda sudah mengapung sampai ke kami.",
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Darmawan", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Anjani & Raditya. Semoga rumah tangga kalian setenang kolam di pagi hari dan seindah teratai yang mekar." },
  { id: "w2", name: "Murid Kelas Cat Air Minggu", attendance: "yes" as const, message: "Bu Anjani, kami sudah siapkan lukisan kecil sebagai kado. Bahagia selalu!" },
  { id: "w3", name: "Sekar & Bram", attendance: "maybe" as const, message: "Semoga penerbangan dari Medan tepat waktu. Doa terbaik untuk kalian." },
];

export default function KolamTerataiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dfe3ea"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.shimmer} aria-hidden />
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <span className={s.coverSpacer} aria-hidden />
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffcf6" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fffcf6"
        dark="#4f6f8f"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <Art name="dab" className={s.divider} />
            {photo && (
              <div className={s.heroArt}>
                <div className={s.heroFrame}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>
                <Art name="lotus" className={`${s.heroLotus} ${s.heroLotusL}`} />
                <Art name="lotus" className={`${s.heroLotus} ${s.heroLotusR}`} />
              </div>
            )}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="dab" className={s.divider} />,
          node: <Art name="lotus" />,
          amp: <Art name="lotus" />,
          portrait: <Art name="lotus" className={s.portraitLotus} />,
          countDecor: <Art name="pads" className={s.countPads} />,
          closingDecor: <Art name="pads" className={s.closingPads} />,
          closingEmblem: <Art name="lotus" className={s.divider} />,
          sentArt: <Art name="lotus" />,
        }}
      />
    </ThemeShell>
  );
}
