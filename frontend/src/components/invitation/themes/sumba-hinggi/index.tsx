"use client";
// Theme "Sumba Hinggi" — adat Sumba Timur: sampul berupa langit senja dan sabana keemasan dengan rumah uma mbatangu
// beratap menara serta kuda sandel, lalu sehelai kain hinggi (ikat kuda, ayam, rusa, udang; merah kombu) dengan rumbai.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Federant", "Alegreya:ital,wght@0,400;0,500;0,700;1,400"];
// Painted by /tmp/pen/art/themes/sumba-hinggi.py (tools/art/themes in the repo).
const Art = makeArt("sumba-hinggi", { sabana: [780, 370], kuda: [300, 262], geo: [360, 64] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Umbu Hapu Mbilu", attendance: "yes" as const, message: "Tuhan Yesus memberkati rumah tangga Ana & Yosua. Kiranya kasih kalian kuat seperti tenunan hinggi, makin indah dari tahun ke tahun." },
  { id: "w2", name: "Mama Ince & Bapa Lukas", attendance: "yes" as const, message: "Selamat menempuh hidup baru. Sampai jumpa di Prailiu, kami datang sekeluarga!" },
  { id: "w3", name: "Rambu Debora", attendance: "maybe" as const, message: "Maaf belum tentu bisa pulang ke Sumba. Doa kami menyertai pemberkatan kalian." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Damai Sejahtera",
    title: "Syalom",
    sub: "Dalam kasih Tuhan Yesus Kristus",
    intro: "Atas kasih karunia Tuhan, kami bermaksud melangsungkan pemberkatan nikah putra-putri kami. Merupakan sukacita bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan turut mendoakan.",
  },
  roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
  couple: ["Dua Helai Benang", "Kedua Mempelai"],
  count: ["Menenun Waktu", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri Foto"],
  wishes: ["Doa & Ucapan", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang sangat berarti bagi kami sekeluarga.", salam: "Tuhan Yesus memberkati" },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
  giftIntro: "Doa dan kehadiran Anda adalah hadiah terindah. Jika berkenan memberi tanda kasih, dapat melalui:",
};

export default function SumbaHinggiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3a140c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.sun} aria-hidden />
          <p className={s.kicker}>Undangan {label}</p>
          <p className={s.shalom}>Syalom, dalam kasih Kristus</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.scene} aria-hidden><Art name="sabana" eager className={s.sabana} /></div>
          <div className={s.cloth}>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#7d2f1e" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f0d79a"
        dark="#5e2114"
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Pemberkatan Nikah</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroCloth}>
              {hero && <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>}
              <span className={s.heroBand} aria-hidden />
            </div>
            <span className={s.heroFringe} aria-hidden />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="geo" className={s.divider} />,
          node: <Art name="kuda" />,
          closingEmblem: <Art name="kuda" className={s.closingEmblem} />,
          sentArt: <Art name="kuda" />,
        }}
      />
    </ThemeShell>
  );
}
