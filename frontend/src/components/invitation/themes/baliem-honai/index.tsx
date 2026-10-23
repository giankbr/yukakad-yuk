"use client";
// Theme "Baliem Honai" — pernikahan Kristen di Lembah Baliem, Papua Pegunungan. Sampul penuh lukisan lembah: punggung
// gunung berlapis kabut yang melayang pelan, kebun ubi berbedeng dan sungai yang berkelok; nama dalam Fraunces di kabut
// pagi, kartu tamu bening dengan noken rajut yang bergoyang, dan sekelompok honai beratap jerami di kaki halaman.
// Hero: foto lembah yang memudar ke kabut, honai di bawahnya. Potret bundar berbingkai simpul noken, hitung mundur di
// dalam kubah honai, kartu acara tergantung pada tali. Tanpa gambar manusia.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,500;0,600;1,400;1,500", "Figtree:wght@400;500;600;700"];
// Painted by /tmp/pen/art/themes/baliem-honai.py (tools/art/themes in the repo).
const Art = makeArt("baliem-honai", { honai: [280, 108], noken: [95, 145], ubi: [160, 23] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Wa wa wa, selamat datang",
    title: "Syalom",
    sub: "Salam kasih dari Lembah Baliem",
    intro: "Atas kasih karunia Tuhan Yesus Kristus, kami bermaksud mempersatukan putra-putri kami dalam ikatan pernikahan kudus. Dengan sukacita kami mengundang Bapak/Ibu/Saudara/i untuk hadir, berdoa, dan bersyukur bersama kami di Wamena.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dirajut dalam kasih", "Kedua Mempelai"] as [string, string],
  count: ["Menuju hari pemberkatan", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Dari lembah yang sama", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Momen Bersama"] as [string, string],
  wishes: ["Doa & Ucapan", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Wa wa, Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat bagi kami sekeluarga. Tuhan Yesus memberkati.",
    salam: "Kasih itu sabar, kasih itu murah hati. (1 Korintus 13:4)",
  },
  attend: { maybe: "Mungkin" } as Partial<Record<Attendance, string>>,
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima. Tuhan memberkati.",
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
  giftIntro: "Doa Anda adalah berkat terbesar bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
  familyLabel: "Kami yang berbahagia, keluarga besar",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Nikolaus Kossay", attendance: "yes" as Attendance, message: "Wa wa! Selamat Marthina dan Yosua. Tuhan memberkati rumah tangga kalian, kuat seperti honai di lereng gunung." },
  { id: "w2", name: "Persekutuan Pemuda Jemaat Elim", attendance: "yes" as Attendance, message: "Kami siap bernyanyi di hari pemberkatan. Selamat menempuh hidup baru, kakak berdua!" },
  { id: "w3", name: "Ibu Debora Hubi (Jayapura)", attendance: "maybe" as Attendance, message: "Semoga penerbangan ke Wamena lancar. Kalau belum bisa hadir, doa Mama menyertai kalian." },
];

export default function BaliemHonaiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const heroPhoto = data.gallery[0];
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#22392c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.mistA} aria-hidden />
          <span className={s.mistB} aria-hidden />
          <div className={s.coverText}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guestCard}>
              <span className={s.cardNoken} aria-hidden><Art name="noken" eager /></span>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff6ea" />Buka Undangan</button>
            </div>
            <Art name="honai" eager className={s.coverHonai} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#e7cf9c"
        dark="#22302a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            {heroPhoto ? <div className={s.heroPhoto}><Photo src={heroPhoto} alt="Lembah tempat kami bertumbuh" /></div> : <div className={s.heroPlain} aria-hidden />}
            <span className={s.heroMist} aria-hidden />
            <Art name="honai" className={s.heroHonai} />
            <p className={s.heroKicker}>{label} · Wamena</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="ubi" className={s.divider} />,
          node: <Art name="noken" />,
          amp: <Art name="ubi" />,
          portrait: <Art name="ubi" className={s.portraitVine} />,
          countDecor: <span className={s.countMist} aria-hidden />,
          closingEmblem: <Art name="honai" className={s.closingHonai} />,
          sentArt: <Art name="noken" />,
        }}
      />
    </ThemeShell>
  );
}
