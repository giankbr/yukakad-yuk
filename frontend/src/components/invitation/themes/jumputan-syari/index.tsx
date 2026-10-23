"use client";
// Theme "Jumputan Syari" — kain jumputan ikat-celup pastel (merah muda, lilac, toska) yang dijemur di galah bambu:
// lingkaran titik pucat, bunga dan percik bintang dari ikatan, rembesan warna yang lembut (dilukis orisinal). Ceria
// namun syar'i: tanpa foto wajah, monogram di atas tambalan kain, salam pembuka Islami.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,500;0,600;1,400", "Nunito:ital,wght@0,400;0,700;0,800;1,400", "Ephesis", "Amiri"];
// Painted by /tmp/pen/art/themes/jumputan-syari.py (tile + tile2 are CSS background textures).
const Art = makeArt("jumputan-syari", { kain1: [209, 588], kain2: [190, 513], kain3: [199, 547], galah: [780, 28], medal: [180, 177], divider: [360, 28] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    sub: "dengan memohon rida Allah",
    intro: "Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan rida-Nya, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Kehadiran dan doa Bapak/Ibu/Saudara/i adalah kebahagiaan bagi kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua simpul, satu kain", "Kedua Mempelai"],
  count: ["Menuju hari akad", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Insyaallah akan diselenggarakan", "Waktu & Tempat"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Kami"],
  wishes: ["Doa & kehadiran", "Ucapan & Doa"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullahu Khairan",
    text: "Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan keberkahan bagi kami.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullahu khairan, doa Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  familyLabel: "Kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Ummi Fatimah & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Teman Remaja Masjid", attendance: "yes" as const, message: "Masya Allah, ikut bahagia! Semoga dimudahkan sampai hari akad dan seterusnya." },
  { id: "w3", name: "Bude Siti, Lampung", attendance: "maybe" as const, message: "Insyaallah diusahakan hadir. Doa terbaik dari kami sekeluarga." },
];

function Names({ bride, groom, className }: { bride: string; groom?: string; className: string }) {
  return <h1 className={className}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>;
}

export default function JumputanSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const kicker = label === "Pernikahan" ? "Walimatul 'Ursy" : label;
  const groom = data.couple.groom?.trim();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const initials = [data.couple.bride, groom].filter(Boolean).map(name => name!.slice(0, 1)).join("");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fdf6ee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.line} aria-hidden>
            <Art name="kain1" eager className={`${s.kain} ${s.kain1}`} />
            <Art name="kain2" eager className={`${s.kain} ${s.kain2}`} />
            <Art name="kain3" eager className={`${s.kain} ${s.kain3}`} />
            <Art name="galah" eager className={s.galah} />
          </div>
          <div className={s.card}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>{kicker}</p>
            <Names bride={data.couple.bride} groom={groom} className={s.coverNames} />
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestBox}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        noPhotos
        light="#ffffff"
        dark="#5b3a5e"
        hero={(
          <header className={s.hero}>
            <div className={s.heroMedal}><Art name="medal" /><span aria-hidden>{initials}</span></div>
            <div className={s.heroCard}>
              <p className={s.heroKicker}>{kicker}</p>
              <Names bride={data.couple.bride} groom={groom} className={s.heroNames} />
              <Art name="divider" className={s.divider} />
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="medal" />,
          amp: <Art name="medal" />,
          portrait: <Art name="medal" className={s.portraitArt} />,
          closingEmblem: <Art name="medal" className={s.closingEmblem} />,
          sentArt: <Art name="medal" />,
        }}
      />
    </ThemeShell>
  );
}
