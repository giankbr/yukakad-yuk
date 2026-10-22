"use client";
// Theme "Natal Keluarga" — perayaan Natal keluarga di rumah: pohon cemara bergouache dengan lampu kuning hangat dan
// ornamen, bintang emas yang berkelip, lilin menyala, ranting cemara & poinsettia, untaian lampu; merah, hijau, krem.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import type { Attendance } from "../kit";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Alegreya:ital,wght@0,400;0,500;0,700;1,400", "Parisienne"];
// Painted by /tmp/pen/art/themes/natal-keluarga.py (tools/art/themes in the repo).
const Art = makeArt("natal-keluarga", {
  tree: [420, 575], star: [150, 147], flame: [60, 98], candles: [360, 271], poinsettia: [150, 135], sprig: [400, 201], lights: [520, 47],
} as const);

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Tobing", attendance: "yes" as Attendance, message: "Selamat Natal! Kiranya damai Kristus memenuhi rumah dan hati keluarga Simanjuntak dan Wenas. Sampai jumpa di meja makan." },
  { id: "w2", name: "Pdt. Lukas & Ibu Ester", attendance: "yes" as Attendance, message: "Salam damai Natal. Tuhan memberkati persekutuan keluarga yang hangat ini, hari ini dan sepanjang tahun yang baru." },
  { id: "w3", name: "Tante Rosa (Manado)", attendance: "maybe" as Attendance, message: "Selamat Natal, ponakan-ponakan tersayang! Semoga bisa menyusul. Simpan satu potong lapis legit buat Tante, ya." },
];

function Candles({ className, eager }: { className?: string; eager?: boolean }) {
  return (
    <div className={className} aria-hidden>
      <Art name="candles" eager={eager} />
      <Art name="flame" eager={eager} className={`${s.flame} ${s.flame1}`} />
      <Art name="flame" eager={eager} className={`${s.flame} ${s.flame2}`} />
      <Art name="flame" eager={eager} className={`${s.flame} ${s.flame3}`} />
    </div>
  );
}

export default function NatalKeluargaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Perayaan Natal";
  const hosts = [data.couple.bride?.trim(), data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const title = /^keluarga/i.test(hosts) ? hosts : `Keluarga ${hosts}`;
  const note = data.couple.note?.trim();
  const table = tableLabel(data.guestTable);
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Salam Damai Natal",
      title: "Selamat Natal",
      sub: "Damai sejahtera bagi kita semua",
      intro: `Dengan sukacita kami mengundang Bapak/Ibu/Saudara/i untuk merayakan Natal bersama ${title}: beribadah, bernyanyi, dan bersantap dalam kehangatan kasih.`,
    },
    // Both host families carry the same visible role; the non-breaking space keeps the two labels distinct as list keys.
    roles: ["Keluarga", "Keluarga "] as [string, string],
    couple: ["Tuan Rumah", "Yang Mengundang"] as [string, string],
    count: ["Menanti Malam Kudus", "Menuju Hari Natal"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
    story: ["Dari Tahun ke Tahun", "Tradisi Natal Kami"] as [string, string],
    gallery: ["Galeri", "Kehangatan Keluarga"] as [string, string],
    wishes: ["Salam Natal", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Kasih", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Selamat Natal", text: "Terima kasih telah menjadi bagian dari sukacita kami. Kiranya damai dan kasih Natal menyertai Bapak/Ibu/Saudara/i sekeluarga.", salam: "Salam damai dalam kasih Kristus" },
    sent: "Terima kasih, salam Natal Anda sudah terkirim. Tuhan memberkati.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: "Tuliskan salam dan doa Natal Anda…",
    closedNote: "Terima kasih atas salam dan doanya. Ucapan Natal masih bisa dikirim lewat form ini.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#14301f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="lights" eager className={s.coverLights} />
          <p className={s.kicker}>{label}</p>
          <p className={s.greet}>Selamat Natal</p>
          <h1 className={s.coverName}>{title}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fbf5e6" />Buka Undangan</button>
          </div>
          <div className={s.scene} aria-hidden>
            <Art name="star" eager className={s.star} />
            <Art name="tree" eager className={s.tree} />
            <Candles className={s.candles} eager />
            <Art name="sprig" eager className={s.sprigR} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!data.couple.bridePhoto && !data.couple.groomPhoto}
        light="#f6e7bd"
        dark="#2b2219"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="sprig" className={`${s.heroSprig} ${s.heroSprigL}`} />
            <Art name="sprig" className={`${s.heroSprig} ${s.heroSprigR}`} />
            <Art name="star" className={s.heroStar} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroName}>{title}</h1>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="poinsettia" className={s.divider} />,
          node: <Art name="poinsettia" />,
          portrait: <Art name="sprig" className={s.wreath} />,
          countDecor: <Art name="lights" className={s.countLights} />,
          closingEmblem: <Candles className={s.closingCandles} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
