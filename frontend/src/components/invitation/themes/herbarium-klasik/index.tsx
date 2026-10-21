"use client";
// Theme "Herbarium Klasik" — pressed dried specimens mounted on herbarium sheets over kraft: a taped cosmos and fern,
// a typed specimen label with handwritten entries, sepia ink and plate numbering like a nineteenth-century botanical plate.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Old Standard TT:ital,wght@0,400;0,700;1,400", "Courier Prime:wght@400;700", "Homemade Apple"];
// Painted by /tmp/pen/art/themes/herbarium-klasik.py (tools/art/themes in the repo).
const Art = makeArt("herbarium-klasik", { cosmos: [300, 659], fern: [248, 901], sprig: [158, 671], twig: [300, 64], tape: [130, 32] } as const);

const COPY = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Salam Damai Kristus",
    title: "Dengan penuh syukur",
    intro: "Atas berkat dan kasih Tuhan, kami bermaksud mempersatukan hidup kami dalam Sakramen Perkawinan. Dengan sukacita kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan mendoakan kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Spesimen Terpilih", "Kedua Mempelai"] as [string, string],
  count: ["Masa Mekar", "Menuju Hari Bahagia"] as [string, string],
  units: ["hari", "jam", "menit", "detik"] as [string, string, string, string],
  events: ["Catatan Lapangan", "Waktu & Tempat"] as [string, string],
  story: ["Buku Harian", "Kisah Kami"] as [string, string],
  gallery: ["Koleksi", "Lembar Kenangan"] as [string, string],
  wishes: ["Buku Tamu", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: { thanks: "Terima kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i akan kami simpan dan rawat, seperti bunga yang ditekan di antara halaman buku." },
  sent: "Terima kasih, ucapan Anda sudah kami catat di buku tamu.",
};

export default function HerbariumKlasikTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const no = formatDate(data.date, { day: "2-digit", month: "2-digit" }).replace(/\D/g, "");
  const year = formatDate(data.date, { year: "numeric" }).replace(/\D/g, "");
  const specNo = no ? `No. ${no}${year ? `/${year}` : ""}` : "No. —";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#a57d52"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverSheet}>
            <div className={s.coverHead}><span>Plate I</span><span>{specNo}</span></div>
            <p className={s.coverTitle}>UNDANGAN {(data.eventLabel ?? "Pernikahan").toUpperCase()}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <div className={s.specimen} aria-hidden>
              <Art name="fern" eager className={s.specFern} />
              <Art name="cosmos" eager className={s.specMain} />
              <Art name="tape" eager className={s.tapeA} />
              <Art name="tape" eager className={s.tapeB} />
            </div>
            <div className={s.label}>
              <h2>Herbarium Nuptiale</h2>
              <dl>
                <dt>Nama</dt><dd>{data.couple.bride} &amp; {data.couple.groom}</dd>
                <dt>Tgl.</dt><dd>{formatDate(data.date)}</dd>
                {data.place && <><dt>Lokasi</dt><dd>{data.place}</dd></>}
                <dt>Untuk</dt><dd className={s.labelGuest}>{guestLabel(data)}{table ? ` · ${table}` : ""}</dd>
              </dl>
            </div>
          </div>
          <div className={s.coverFoot}>
            <small>Kepada Yth.<br />Bapak/Ibu/Saudara/i</small>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#3b2a1c" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#3b2a1c"
        dark="#f6efdf"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroHead}><span>Plate II</span><span>Fig. 1</span></div>
            {photo && (
              <div className={s.heroPrint}>
                <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>
                <Art name="sprig" className={s.heroSprig} />
              </div>
            )}
            <p className={s.figCap}>Fig. 1 — {data.couple.bride} &amp; {data.couple.groom}{data.place ? `, ${data.place}` : ""}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="twig" className={s.divider} />,
          amp: <Art name="twig" />,
          portrait: <Art name="sprig" className={s.portraitSpec} />,
          closingEmblem: (
            <div className={s.closingSpecimens} aria-hidden>
              <Art name="fern" />
              <Art name="cosmos" />
              <Art name="sprig" />
            </div>
          ),
          sentArt: <Art name="twig" />,
        }}
      />
    </ThemeShell>
  );
}
