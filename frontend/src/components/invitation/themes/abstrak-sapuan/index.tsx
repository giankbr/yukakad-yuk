"use client";
// Theme "Abstrak Sapuan" — a contemporary abstract painting (wide flat-brush sweeps and palette-knife planes in blush,
// sage, ochre and charcoal on gesso) hung off-centre above a gallery-catalogue layout: left-aligned numbered rooms,
// stretched-canvas portraits with ochre sweeps behind, wall-label event cards, salon-hung gallery. Hindu Balinese
// couple (Om Swastiastu, Pawiwahan).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bricolage Grotesque:wght@400;600;700;800", "Literata:ital,wght@0,400;0,600;1,400", "Mrs Saint Delafield"];
// Painted by /tmp/pen/art/themes/abstrak-sapuan.py (tools/art/themes in the repo).
const Art = makeArt("abstrak-sapuan", { sweep: [360, 48], ochre: [480, 272], blocks: [180, 173] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Om Swastiastu",
    title: "Atas Asung Kertha Wara Nugraha Ida Sang Hyang Widhi Wasa",
    intro: "Kami bermaksud mengundang Bapak/Ibu/Saudara/i pada upacara Pawiwahan (pernikahan) kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  attend: { maybe: "Mungkin" },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Ruang Potret", "Kedua Mempelai"] as [string, string],
  count: ["Menjelang Pembukaan", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Catatan Kurator", "Kisah Kami"] as [string, string],
  gallery: ["Ruang Pamer", "Galeri"] as [string, string],
  wishes: ["Buku Tamu", "Doa & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Suksma",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah sapuan terindah di kanvas hari bahagia kami.",
    salam: "Om Shanti Shanti Shanti Om",
  },
  sent: "Suksma, ucapan Anda sudah tergantung di dinding galeri kami.",
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
  closedNote: "Suksma atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat buku tamu ini.",
};

const WISHES = [
  { id: "w1", name: "Keluarga I Made Sutama", attendance: "yes" as const, message: "Rahajeng nganten! Semoga menjadi keluarga yang sukhinah, rukun dan selalu dalam lindungan Ida Sang Hyang Widhi." },
  { id: "w2", name: "Kolektif Ruang Sapuan", attendance: "yes" as const, message: "Selamat Saras & Arya! Kami siapkan kuas paling lebar untuk kanvas bersama nanti." },
  { id: "w3", name: "Dewi Lestari", attendance: "maybe" as const, message: "Ikut bahagia dari Jakarta. Semoga langgeng dan terus berkarya berdua." },
];

export default function AbstrakSapuanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = toDate(data.date)?.getFullYear();
  const where = data.place?.split(",").pop()?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e4ddd1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.canvasWrap} aria-hidden>
            <span className={s.canvasPaint} />
            <span className={s.canvasTag}>Akrilik di atas kanvas{year ? ` · ${year}` : ""}</span>
          </div>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf9f5" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf9f5"
        dark="#2d2b2a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}><span>{label}</span><span>{year ?? "Katalog"}</span></p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            {photo && (
              <div className={s.heroArt}>
                <Art name="ochre" className={s.heroSwoosh} />
                <div className={s.heroFrame}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>
                <Art name="blocks" className={s.heroBlocks} />
              </div>
            )}
            {photo && <p className={s.heroCaption}><b>{data.couple.bride} &amp; {data.couple.groom}</b>{where ? `, ${where}` : ""}{year ? ` ${year}` : ""}</p>}
            <Art name="sweep" className={s.divider} />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sweep" className={s.divider} />,
          node: <Art name="blocks" />,
          amp: <Art name="blocks" />,
          portrait: <Art name="ochre" className={s.portraitSwoosh} />,
          countDecor: <span className={s.countScene} aria-hidden />,
          closingDecor: <span className={s.closingScene} aria-hidden />,
          closingEmblem: <Art name="blocks" className={s.closingBlocks} />,
          sentArt: <Art name="blocks" />,
        }}
      />
    </ThemeShell>
  );
}
