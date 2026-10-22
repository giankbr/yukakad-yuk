"use client";
// Theme "Pembaptisan" — a gentle Christian (Catholic or Protestant) baptism in soft watercolour and gold leaf (original
// designs): light falls from above onto a carved stone font whose still water ripples, a white dove with an olive sprig
// hovers over the child's name, white lilies frame the cover and the closing. The child sits in a pool-of-water
// medallion, events are arched chapel-window cards, the countdown floats in a pale water band, story nodes are small
// gold crosses. Reverent copy, "Mungkin" for the maybe attendance choice.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Della Respira", "Parisienne", "Spectral:ital,wght@0,400;0,500;1,400"];
// Painted by /tmp/pen/art/themes/pembaptisan.py (tools/art/themes in the repo).
const Art = makeArt("pembaptisan", {
  dove: [300, 252], font: [340, 262], ripple: [200, 60], rays: [300, 380], lilies: [330, 361], olive: [230, 26], cross: [64, 98],
} as const);

const WISHES = [
  { id: "w1", name: "Romo Ignatius & Umat Lingkungan", attendance: "yes" as Attendance, message: "Selamat datang dalam keluarga Allah, Mikha. Semoga tumbuh dalam iman, harapan, dan kasih." },
  { id: "w2", name: "Keluarga Stefanus Hartanto", attendance: "yes" as Attendance, message: "Kami bersyukur boleh menjadi wali baptis Mikha. Tuhan memberkati dan menuntun langkahmu selalu." },
  { id: "w3", name: "Tante Lusi & Om Bernard", attendance: "maybe" as Attendance, message: "Mohon maaf bila belum dapat hadir. Doa kami menyertai Mikha dan keluarga di hari yang kudus ini." },
];

export default function PembaptisanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pembaptisan Kudus";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const full = child?.name.trim() || data.couple.brideFull?.trim();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Salam Damai Kristus",
      title: "Dengan Penuh Syukur",
      intro: `Atas kasih karunia Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan turut mendoakan ${names} yang akan menerima ${label}. Bersama orang tua dan wali baptis, kami menyerahkan buah hati kami ke dalam persekutuan umat Allah, agar ia bertumbuh dalam iman, harapan, dan kasih.`,
    },
    roles: ["Yang Akan Dibaptis", "Bersama"],
    couple: ["Anugerah Tuhan", child ? "Buah Hati Kami" : "Yang Dibaptis"],
    count: ["Menanti Hari Kudus", "Hitung Mundur"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Tata Ibadah", "Waktu & Tempat"],
    story: ["Kisah Kecil", `Perjalanan ${nick}`],
    gallery: ["Galeri", "Momen Penuh Syukur"],
    wishes: ["Doa & Restu", "Ucapan & Kehadiran"],
    gifts: ["Tanda Kasih", "Amplop Digital"],
    closing: {
      thanks: "Tuhan Memberkati",
      text: `Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat bagi kami. Terima kasih telah menyertai langkah iman pertama ${names}.`,
      salam: "Salam damai dalam Kristus",
    },
    sent: "Terima kasih, doa Anda sudah kami terima. Tuhan memberkati.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: `Tuliskan doa dan berkat untuk ${nick}…`,
    closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan dan doa masih dapat dikirim lewat form ini.",
    giftIntro: `Doa Anda adalah hadiah terindah bagi ${nick}. Bila berkenan memberikan tanda kasih, dapat melalui:`,
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf8f2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="rays" eager className={s.rays} />
          <Art name="dove" eager className={s.coverDove} />
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {full && full !== names && <p className={s.coverFull}>{full}</p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={`${s.guest} ${s.card}`}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          <div className={s.stage} aria-hidden>
            <Art name="lilies" eager className={s.lilyL} />
            <Art name="lilies" eager className={s.lilyR} />
            <div className={s.fontBox}>
              <Art name="font" eager className={s.fontImg} />
              <Art name="ripple" eager className={s.fontRipple} />
              <Art name="ripple" eager className={`${s.fontRipple} ${s.fr2}`} />
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffffff"
        dark="#3d4458"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="rays" className={s.heroRays} />
            <Art name="cross" className={s.heroCross} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroName}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="olive" className={s.divider} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="olive" className={s.divider} />,
          node: <Art name="cross" />,
          portrait: <Art name="dove" className={s.portraitDove} />,
          countDecor: <><Art name="ripple" className={`${s.countRipple} ${s.cr1}`} /><Art name="ripple" className={`${s.countRipple} ${s.cr2}`} /></>,
          closingDecor: <><Art name="rays" className={s.closingRays} /><Art name="lilies" className={`${s.closingLily} ${s.clL}`} /><Art name="lilies" className={`${s.closingLily} ${s.clR}`} /></>,
          closingEmblem: <Art name="cross" className={s.closingCross} />,
          sentArt: <Art name="dove" />,
        }}
      />
    </ThemeShell>
  );
}
