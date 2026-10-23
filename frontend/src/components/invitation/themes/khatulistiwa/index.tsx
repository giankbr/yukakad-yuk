"use client";
// Theme "Khatulistiwa" — adat Melayu Pontianak: langit siang di garis khatulistiwa, tugu obelisk orisinal berbola dunia
// dengan cincin dan panah emas, Sungai Kapuas yang lebar dengan speedboat, rumah panggung Melayu di seberang (lukisan
// gouache orisinal), dan tenun corak insang merah-emas sebagai pita di setiap bagian.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Della Respira", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Monsieur La Doulaise", "Amiri"];
// Painted by /tmp/pen/art/themes/khatulistiwa.py (scene + insang are CSS backgrounds).
const Art = makeArt("khatulistiwa", { tugu: [176, 463], divider: [360, 19], rumah: [420, 356], boat: [220, 49] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    sub: "Dari tepian Kapuas, di garis khatulistiwa",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Pengantin Perempuan", "Pengantin Lelaki"],
  couple: ["Dua tepian, satu sungai", "Kedua Mempelai"],
  count: ["Menanti hari baik", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & tempat", "Rangkaian Acara"],
  story: ["Perjalanan kami", "Kisah Kami"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Doa & kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima. Jazakumullahu khairan.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  familyLabel: "Kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Syarif Hamid, Kampung Arab", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga yang sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Kawan-kawan Tambang Kapuas", attendance: "yes" as const, message: "Selamat Nadia dan Haikal! Kami datang semue, sudah tak sabar makan saprahan." },
  { id: "w3", name: "Mak Long Ani & Keluarga, Sambas", attendance: "maybe" as const, message: "Insyaallah kami usahakan hadir. Doa terbaik dari kami sekeluarga di Sambas." },
];

function Names({ bride, groom, className }: { bride: string; groom?: string; className: string }) {
  return <h1 className={className}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>;
}

export default function KhatulistiwaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const kicker = label === "Pernikahan" ? "Walimatul 'Ursy" : label;
  const groom = data.couple.groom?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const initials = [data.couple.bride, groom].filter(Boolean).map(name => name!.slice(0, 1)).join("");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#123c40"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverText}>
            <p className={s.kicker}>{kicker}</p>
            <p className={s.coord}>0° · Garis Khatulistiwa</p>
            <Names bride={data.couple.bride} groom={groom} className={s.coverNames} />
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverBottom}>
            <div className={s.guestBox}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff4dc" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f0d27a"
        dark="#123c40"
        hero={(
          <header className={s.hero}>
            <div className={s.heroGlobe}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{initials}</span>}</div>
            </div>
            <p className={s.heroKicker}>{kicker} · Pontianak</p>
            <Names bride={data.couple.bride} groom={groom} className={s.heroNames} />
            <Art name="divider" className={s.heroDivider} />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="tugu" />,
          amp: <Art name="divider" />,
          countDecor: <Art name="boat" className={s.countBoat} />,
          closingEmblem: <Art name="tugu" className={s.closingEmblem} />,
          closingDecor: <Art name="rumah" className={s.closingScene} />,
          sentArt: <Art name="tugu" />,
        }}
      />
    </ThemeShell>
  );
}
