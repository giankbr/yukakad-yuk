"use client";
// Theme "Mamluk Kairo" — pernikahan Islami bernuansa arsitektur Mamluk di Kairo: dinding batu ablaq berlapis terang dan
// gelap, portal dengan tudung muqarnas dan ambang batu bersambung (joggled) yang pintunya membingkai foto mempelai,
// lampu kuningan berenamel yang berayun pelan. Lengkung runcing bertepi ablaq untuk potret. Tanpa makhluk bernyawa,
// tanpa kaligrafi yang dilukis.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Forum", "Libre Caslon Text:ital,wght@0,400;0,700;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/mamluk-kairo.py (tools/art/themes in the repo).
const Art = makeArt("mamluk-kairo", { portal: [490, 770], lamp: [200, 447], divider: [320, 31], rosette: [120, 120] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Selapis demi Selapis", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakallah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Keluarga Dr. H. Salman Farisi", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Selamat Aisyah dan Hanif." },
  { id: "w2", name: "Kawan Rumah Hay el-Asher", attendance: "yes" as Attendance, message: "Dari Kairo sampai Jakarta, akhirnya. Semoga menjadi keluarga yang sakinah dan penuh ilmu." },
  { id: "w3", name: "Ustadz Fahmi Basyir", attendance: "maybe" as Attendance, message: "Insyaallah hadir bila jadwal kajian di Bandung selesai. Doa terbaik untuk kalian berdua." },
];

export default function MamlukKairoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2f2622"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.wall}>
            <Art name="lamp" className={s.lampL} eager />
            <Art name="lamp" className={s.lampR} eager />
            <div className={s.portal}>
              <div className={s.door}>{photo ? <Photo src={photo} alt="" /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <Art name="portal" eager />
            </div>
          </div>
          <div className={s.plinth}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#2f2622" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ecd08a"
        dark="#2f2622"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroArch}>
              <div className={s.heroFrame}>
                <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              </div>
              <Art name="lamp" className={s.heroLamp} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="rosette" />,
          amp: <Art name="rosette" />,
          closingEmblem: <Art name="lamp" className={s.closingEmblem} />,
          sentArt: <Art name="rosette" />,
        }}
      />
    </ThemeShell>
  );
}
