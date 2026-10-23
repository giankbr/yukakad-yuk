"use client";
// Theme "Rumah Limas" — adat Palembang: rumah limas bertingkat di atas tiang di tepi Sungai Musi saat senja (lukisan
// gouache orisinal), lintel kayu ukir berlakuer merah dengan sulur dan bunga berlapis emas, songket limar merah-emas,
// bingkai foto berbentuk atap limas, dan plakat lacquer hitam. Arsitektur dan ukiran lakuer, bukan busana pengantin.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "Lora:ital,wght@0,400;0,600;1,400", "Pinyon Script", "Amiri"];
// Painted by /tmp/pen/art/themes/rumah-limas.py (lakuer + songket are CSS background tiles).
const Art = makeArt("rumah-limas", { limas: [720, 663], panel: [280, 280], divider: [340, 41], simbar: [130, 91] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    sub: "Dari rumah limas di tepian Musi",
    intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Tiang Satu Atap", "Kedua Mempelai"],
  count: ["Menanti hari baik", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & tempat", "Rangkaian Acara"],
  story: ["Perjalanan kami", "Kisah Kami"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Doa & kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima. Jazakumullahu khairan.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  familyLabel: "Kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Keluarga Kgs. H. Amiruddin, 30 Ilir", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga jadi keluargo yang sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Teman-teman Bidar Kuto Besak", attendance: "yes" as const, message: "Selamat yo Zahira samo Fadli! Kami galo datang, sudah siap makan pindang patin di resepsi." },
  { id: "w3", name: "Wak Yusuf & Keluarga, Jakarta", attendance: "maybe" as const, message: "Mohon maaf kalau belum biso pulang ke Palembang. Doa terbaik dari kami sekeluarga." },
];

function Names({ bride, groom, className }: { bride: string; groom?: string; className: string }) {
  return <h1 className={className}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>;
}

export default function RumahLimasTheme(props: ThemeProps) {
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
      background="#1c0f0c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverScene}><Art name="limas" eager className={s.coverSceneImg} /></div>
          <span className={s.coverBand} aria-hidden />
          <div className={s.coverBody}>
            <Art name="simbar" eager className={s.coverSimbar} />
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
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f0d488" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f0d488"
        dark="#5e1010"
        hero={(
          <header className={s.hero}>
            <Art name="simbar" className={s.heroSimbar} />
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{initials}</span>}</div>
            </div>
            <div className={s.plaque}>
              <p className={s.heroKicker}>{kicker} · Palembang</p>
              <Names bride={data.couple.bride} groom={groom} className={s.heroNames} />
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="simbar" />,
          amp: <Art name="simbar" />,
          portrait: <Art name="simbar" className={s.portraitArt} />,
          countDecor: <><Art name="panel" className={`${s.countPanel} ${s.countPanelL}`} /><Art name="panel" className={`${s.countPanel} ${s.countPanelR}`} /></>,
          closingDecor: <Art name="limas" className={s.closingScene} />,
          closingEmblem: <Art name="panel" className={s.closingEmblem} />,
          sentArt: <Art name="panel" />,
        }}
      />
    </ThemeShell>
  );
}
