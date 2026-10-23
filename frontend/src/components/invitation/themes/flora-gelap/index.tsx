"use client";
// Theme "Flora Gelap" — lukisan alam benda bunga orisinal bergaya lukisan klasik Belanda: peoni, tulip bergaris api,
// mawar, larkspur, dan kupu-kupu dalam jambangan batu di atas birai, disinari tajam dari kiri atas di latar hampir
// hitam. Sampul berupa lukisan penuh dengan nama tertera di birai, kupu-kupu yang mengepak dan kelopak yang jatuh
// perlahan. Hero berupa potongan detail lukisan dengan label museum; potret mempelai dalam bingkai oval klasik.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["IM Fell English:ital@0;1", "Spectral:ital,wght@0,400;0,500;0,600;1,400"];
// Painted by /tmp/pen/art/themes/flora-gelap.py (tools/art/themes in the repo).
const Art = makeArt("flora-gelap", {
  still: [390, 566], rose: [75, 56], tulip: [65, 162], sprig: [170, 26], butterfly: [60, 46], petal: [35, 30],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh sukacita",
    title: "Undangan Pernikahan",
    sub: "Seikat bunga untuk satu hari yang kami nantikan",
    intro: "Dengan rasa syukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi saksi hari pernikahan kami. Kehadiran dan doa restu Anda akan melengkapi kebahagiaan kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Potret", "Kedua Mempelai"] as [string, string],
  count: ["Menanti hari", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["Dari musim ke musim", "Kisah Kami"] as [string, string],
  gallery: ["Koleksi", "Galeri"] as [string, string],
  wishes: ["Doa & kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda kasih", "Hadiah"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih yang setulus-tulusnya.",
  },
  attend: { maybe: "Mungkin" } as Partial<Record<Attendance, string>>,
  sent: "Terima kasih, ucapan dan doa Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
  giftIntro: "Kehadiran Anda adalah hadiah terindah. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Keluarga Antonius Gunawan", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru. Semoga rumah tangga kalian selalu dipenuhi kasih, kesabaran, dan bunga di setiap musim." },
  { id: "w2", name: "Teman-teman Studio Lukis Dago", attendance: "yes" as Attendance, message: "Dari kanvas kecil sampai pelaminan! Ikut bahagia, sampai jumpa di rumah kaca." },
  { id: "w3", name: "Tante Lily", attendance: "maybe" as Attendance, message: "Selamat sayang. Semoga langgeng dan bahagia, maaf kalau belum pasti bisa datang ke Lembang." },
];

export default function FloraGelapTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const names = <>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</>;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#050403"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.painting} aria-hidden><Art name="still" eager /></div>
          <Art name="butterfly" eager className={s.coverFly} />
          <Art name="petal" eager className={s.coverPetal} />
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{names}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <span className={s.coverRule} aria-hidden />
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="currentColor" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#efe4cf"
        dark="#2a0f12"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.detail} aria-hidden><span /><small>detail</small></div>
            <div className={s.label}>
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroNames}>{names}</h1>
              <p className={s.heroMeta}>{formatDate(data.date)}{data.place ? <><br />{data.place}</> : null}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="rose" />,
          amp: <Art name="rose" />,
          portrait: <span className={s.portraitRose} aria-hidden><Art name="rose" /></span>,
          countDecor: <><Art name="tulip" className={`${s.countTulip} ${s.countTulipL}`} /><Art name="tulip" className={`${s.countTulip} ${s.countTulipR}`} /></>,
          closingEmblem: <div className={s.closeArt} aria-hidden><Art name="tulip" /><Art name="rose" /><Art name="tulip" /></div>,
          sentArt: <Art name="rose" />,
        }}
      />
    </ThemeShell>
  );
}
