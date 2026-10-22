"use client";
// Theme "Hutan Bambu" — hutan bambu yang menjulang, dilukis dengan gouache dan cat air: batang-batang bambu dengan ruas
// dan cincin bedak putih, satu batang bambu kuning bergaris hijau, semburan daun yang menggantung, berkas cahaya yang
// miring menembus celah, dan daun yang gugur perlahan. Sampul berupa lapangan berkabut di antara dua rumpun bambu;
// foto pasangan ditaruh di dalam satu ruas bambu yang tinggi. Untuk pasangan Hindu Bali (Om Swastyastu).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bellefair", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Mrs Saint Delafield"];
// Painted by /tmp/pen/art/themes/hutan-bambu.py (tools/art/themes in the repo).
const Art = makeArt("hutan-bambu", {
  stand: [230, 857], canopy: [780, 192], sprig: [220, 76], leaf: [110, 21], leaf2: [110, 21],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam pembuka",
    title: "Om Swastyastu",
    sub: "Atas asung kerta wara nugraha Ida Sang Hyang Widhi Wasa",
    intro: "Kami bermaksud menyelenggarakan upacara pawiwahan (pernikahan) putra-putri kami. Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir untuk memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Tumbuh berumpun", "Kedua Mempelai"] as [string, string],
  count: ["Menuju hari baik", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["Ruas demi ruas", "Kisah Kami"] as [string, string],
  gallery: ["Di bawah rumpun", "Galeri"] as [string, string],
  wishes: ["Doa & restu", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Suksma",
    text: "Merupakan suatu kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu kepada kedua mempelai.",
    salam: "Om Shanti, Shanti, Shanti Om",
  },
  attend: { maybe: "Mungkin" },
  sent: "Suksma, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah anugerah terindah. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Keluarga I Ketut Sudarsana", attendance: "yes" as const, message: "Rahajeng nganten, Ayu lan Wira. Dumogi langgeng, rukun, dan selalu dalam lindungan Ida Sang Hyang Widhi Wasa." },
  { id: "w2", name: "Sanggar Anyam Petulu", attendance: "yes" as const, message: "Dari bilah bambu yang sama lahir anyaman yang kuat. Selamat menempuh hidup baru, semoga saling menguatkan." },
  { id: "w3", name: "Komang & Desi", attendance: "maybe" as const, message: "Maaf kalau belum bisa datang ke Sayan. Doa terbaik dari Singaraja untuk kalian berdua!" },
];

function Leaves() {
  return (
    <span className={s.fall} aria-hidden>
      <Art name="leaf" />
      <Art name="leaf2" />
      <Art name="leaf" />
    </span>
  );
}

export default function HutanBambuTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const names = [data.couple.bride, data.couple.groom].filter(n => n?.trim()).join(" & ");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dfe5c8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverRays} aria-hidden />
          <span className={`${s.stand} ${s.standL}`} aria-hidden><Art name="stand" eager /></span>
          <span className={`${s.stand} ${s.standR}`} aria-hidden><Art name="stand" eager /></span>
          <Art name="canopy" eager className={s.coverCanopy} />
          <Leaves />
          <p className={s.coverKicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>
            <span>{data.couple.bride}</span>
            {data.couple.groom?.trim() && <><em>&amp;</em><span>{data.couple.groom}</span></>}
          </h1>
          <span className={s.coverRule} aria-hidden />
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f8f8ec" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f8f8ec"
        dark="#25321f"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="canopy" className={s.heroCanopy} />
            <p className={s.heroKicker}>{label}</p>
            <div className={s.capsuleWrap}>
              <span className={s.heroCulm} aria-hidden><Art name="stand" /></span>
              <div className={s.capsule}>
                {photo ? <Photo src={photo} alt={names} /> : <span className={s.capsuleArt} aria-hidden />}
              </div>
            </div>
            <h1 className={s.heroNames}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="sprig" /></span>,
          node: <Art name="leaf" />,
          amp: <Art name="leaf" />,
          portrait: <span className={s.peek} aria-hidden><Art name="sprig" /></span>,
          countDecor: <><span className={s.countRays} aria-hidden /><Leaves /></>,
          closingDecor: (
            <>
              <span className={`${s.closeStand} ${s.closeL}`} aria-hidden><Art name="stand" /></span>
              <span className={`${s.closeStand} ${s.closeR}`} aria-hidden><Art name="stand" /></span>
              <Art name="canopy" className={s.closeCanopy} />
              <Leaves />
            </>
          ),
          closingEmblem: <Art name="sprig" className={s.closingEmblem} />,
          sentArt: <Art name="sprig" />,
        }}
      />
    </ThemeShell>
  );
}
