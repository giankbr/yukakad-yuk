"use client";
// Theme "Pondok Inggris" — a watercolour storybook: an English thatched stone cottage with climbing roses, hollyhocks,
// foxgloves, delphiniums and a white picket gate. The cover is a book's title page, every section is a "Bab" with an
// illuminated drop cap, portraits are oval cameos with a painted rose, events are seed-packet cards, the guestbook is
// ruled paper and gifts are garden plant labels. Neutral (non-religious) couple.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["IM Fell English:ital@0;1", "Crimson Pro:ital,wght@0,400;0,600;1,400", "Mrs Saint Delafield"];
// Painted by /tmp/pen/art/themes/pondok-inggris.py (tools/art/themes in the repo).
const Art = makeArt("pondok-inggris", { cottage: [580, 586], border: [820, 248], vine: [360, 54], foxglove: [121, 571], rose: [180, 141] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Bab I · Pembuka",
    title: "Salam Hangat dari Kebun Kami",
    intro: "Dengan penuh rasa syukur dan sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi bagian dari kisah kami, ketika dua halaman hidup akhirnya dijilid menjadi satu buku.",
  },
  attend: { maybe: "Mungkin" },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Bab II", "Tokoh Utama Kisah Ini"] as [string, string],
  count: ["Bab III", "Menghitung Musim"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Bab IV", "Hari yang Dinanti"] as [string, string],
  story: ["Bab V", "Kisah Kami"] as [string, string],
  gallery: ["Bab VI", "Album Kebun"] as [string, string],
  wishes: ["Bab VII", "Buku Tamu"] as [string, string],
  gifts: ["Bab VIII", "Tanda Kasih"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa baik Bapak/Ibu/Saudara/i adalah halaman terindah dalam kisah kami.",
    salam: "…dan mereka hidup bahagia, dari satu musim bunga ke musim berikutnya.",
  },
  sent: "Terima kasih, pesan Anda sudah tertulis di buku tamu kami.",
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
  giftIntro: "Doa dan kehadiran Anda adalah hadiah terindah. Jika berkenan memberi tanda kasih, dapat melalui:",
  closedNote: "Terima kasih atas doa dan perhatiannya. Pesan masih bisa dituliskan di buku tamu ini.",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Sutanto", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Kirana & Bastian. Semoga pondok kalian selalu hangat dan kebunnya tak pernah berhenti berbunga." },
  { id: "w2", name: "Komunitas Berkebun Lembang", attendance: "yes" as const, message: "Kami bawakan bibit mawar sebagai kado. Bahagia selalu, dan jangan lupa disiram!" },
  { id: "w3", name: "Nadia & Raka", attendance: "maybe" as const, message: "Semoga bisa menyusul dari Jakarta. Doa terbaik untuk kalian berdua." },
];

export default function PondokInggrisTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9e0cc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.chapter}>Sebuah Kisah {label}</p>
          <div className={s.cottage}><Art name="cottage" eager /></div>
          <Art name="foxglove" className={`${s.coverFox} ${s.coverFoxL}`} eager />
          <Art name="foxglove" className={`${s.coverFox} ${s.coverFoxR}`} eager />
          <p className={s.kicker}>Pada suatu musim bunga…</p>
          <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffaf0" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fffaf0"
        dark="#3f5638"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroChapter}>Prolog</p>
            <p className={s.heroOnce}>Di sebuah pondok batu yang dirambati mawar, dua nama akhirnya ditulis di halaman yang sama:</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            {photo && (
              <div className={s.heroArt}>
                <div className={s.heroFrame}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>
                <Art name="vine" className={`${s.heroVine} ${s.heroVineTop}`} />
                <Art name="vine" className={`${s.heroVine} ${s.heroVineBot}`} />
                <Art name="foxglove" className={`${s.heroFox} ${s.heroFoxL}`} />
                <Art name="foxglove" className={`${s.heroFox} ${s.heroFoxR}`} />
              </div>
            )}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="vine" className={s.divider} />,
          node: <Art name="rose" />,
          amp: <Art name="rose" />,
          portrait: <Art name="rose" className={s.portraitRose} />,
          countDecor: <Art name="border" className={s.countBorder} />,
          closingDecor: <Art name="border" className={s.closingBorder} />,
          closingEmblem: <Art name="vine" className={s.divider} />,
          sentArt: <Art name="rose" />,
        }}
      />
    </ThemeShell>
  );
}
