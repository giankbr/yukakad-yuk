"use client";
// Theme "Raja Ampat" — pernikahan Kristen Papua dengan lukisan cat air gugusan pulau karst berpayung hutan di laguna
// toska yang jernih dan langit lebar berawan. Nama ditulis di langit, kartu tamu mengapung di air dangkal, portret
// berbentuk batu karang, hitung mundur berupa gelembung di pita laguna, dan bintang laut sebagai penanda.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Instrument Serif:ital@0;1", "Hanken Grotesk:wght@400;500;600"];
// Painted by /tmp/pen/art/themes/raja-ampat.py (tools/art/themes in the repo).
const Art = makeArt("raja-ampat", { isle: [520, 299], cloud: [420, 142], divider: [360, 62], star: [96, 93] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Salam Sejahtera",
    title: "Syalom",
    intro: "Dengan sukacita dan syukur atas kasih karunia Tuhan, kami mengundang Bapak/Ibu/Saudara/i, ade-kaka sekalian, untuk hadir dan turut memberkati pernikahan kami di tanah Raja Ampat.",
  },
  roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
  couple: ["Dua Pulau, Satu Laut", "Kedua Mempelai"],
  count: ["Air Pasang Menuju", "Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Ibadah & Pesta"],
  story: ["Perjalanan Kami", "Kisah di Laut Biru"],
  gallery: ["Galeri", "Cerita dalam Foto"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Trima Kasih Banyak", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang tak ternilai bagi kami dan keluarga besar.", salam: "Tuhan Yesus memberkati" },
  sent: "Trima kasih, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa dan berkat untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Bapak Obaja Rumbekwan & Keluarga", attendance: "yes" as Attendance, message: "Syalom! Tuhan memberkati rumah tangga kalian, kokoh seperti karang dan tenang seperti laut Waisai." },
  { id: "w2", name: "Kaka Selvi Mayor", attendance: "yes" as Attendance, message: "Ade Natalia dan Yosias, selamat e! Torang tunggu di pantai, siap yospan sampai malam." },
  { id: "w3", name: "Tim Survei Karang Dampier", attendance: "maybe" as Attendance, message: "Masih di lapangan minggu itu, semoga bisa menyusul. Doa terbaik dari kami semua." },
];

export default function RajaAmpatTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#12354a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="cloud" className={s.cloudB} eager />
          <Art name="cloud" className={s.cloudA} eager />
          <p className={s.salam}>Syalom</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.tide}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffffff"
        dark="#12354a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="cloud" className={s.cloudA} />
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroPhotoWrap}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <Art name="isle" className={s.heroIsle} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          closingEmblem: <Art name="cloud" className={s.closingEmblem} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
