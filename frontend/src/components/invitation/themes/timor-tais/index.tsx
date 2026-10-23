"use client";
// Theme "Timor Tais" — adat Timor (Atoni): sehelai tais ikat lungsin merah-hitam-jingga menjuntai di tepi kiri sampul
// dengan rumbainya, langit biru di atas padang lontar dan rumah bulat ume kbubu (gouache), tata letak rata kiri,
// bingkai potret dari tenunan tais, dan kartu acara bertepi selvedge kain.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rozha One", "Petrona:ital,wght@0,400;0,600;0,700;1,400"];
// Painted by /tmp/pen/art/themes/timor-tais.py (tools/art/themes in the repo).
const Art = makeArt("timor-tais", { padang: [720, 492], band: [420, 51], ume: [240, 218] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Yeremias Tefa", attendance: "yes" as const, message: "Tuhan Yesus memberkati Ester & Imanuel. Kiranya rumah tangga kalian kuat dan indah seperti tais yang ditenun dengan sabar." },
  { id: "w2", name: "Pemuda GMIT Kota Kupang", attendance: "yes" as const, message: "Selamat menempuh hidup baru! Kami siap menyanyi lagi di pemberkatan nanti, sampai jumpa di Kupang." },
  { id: "w3", name: "Mama Yuli Selan", attendance: "maybe" as const, message: "Mama belum tentu bisa turun ke Soe, tapi doa Mama selalu menyertai kalian berdua." },
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
  couple: ["Lungsin & Pakan", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
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

export default function TimorTaisTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe6d4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.hang} aria-hidden>
            <div className={s.hangInner}><span className={s.hangCloth} /><span className={s.hangFringe} /></div>
          </div>
          <div className={s.coverBody}>
            <p className={s.kicker}>Undangan {label}</p>
            <p className={s.shalom}>Syalom, dalam kasih Kristus</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f4b768" />Buka Undangan</button>
            </div>
          </div>
          <div className={s.scene} aria-hidden><Art name="padang" eager className={s.padang} /></div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f4b768"
        dark="#1c1412"
        hero={(
          <header className={hero ? s.hero : `${s.hero} ${s.heroNoPhoto}`}>
            {hero && (
              <div className={s.heroPhotoWrap}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <span className={s.heroStrip} aria-hidden />
              </div>
            )}
            <div className={s.heroText}>
              <p className={s.heroKicker}>Pemberkatan Nikah</p>
              <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="band" className={s.divider} />,
          node: <Art name="ume" />,
          closingEmblem: <Art name="ume" className={s.closingEmblem} />,
          sentArt: <Art name="ume" />,
        }}
      />
    </ThemeShell>
  );
}
