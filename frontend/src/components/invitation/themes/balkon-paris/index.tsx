"use client";
// Theme "Balkon Paris" — matte gouache travel-sketch of a Parisian limestone facade: French window with slate-blue
// shutters, wrought-iron Juliet balcony, wisteria and lilac cascading in spring; a striped café awning tops the cover,
// the couple's names sit on an enamel street-name plaque, events are bistro menu cards, photos are tall arched windows
// with a balcony rail. Buddhist Chinese-Indonesian couple (Namo Buddhaya).
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Italiana", "EB Garamond:ital,wght@0,400;0,500;1,400", "Parisienne"];
// Painted by /tmp/pen/art/themes/balkon-paris.py (tools/art/themes in the repo).
const Art = makeArt("balkon-paris", { window: [560, 717], wisteria: [260, 318], railing: [640, 142], sprig: [150, 143], garland: [260, 94] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Namo Buddhaya",
    title: "Dengan Penuh Sukacita",
    intro: "Dengan cinta kasih dan berkah Tiratana, kami bermaksud melangsungkan pernikahan kami. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  attend: { maybe: "Mungkin" },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dari Balik Jendela", "Kedua Mempelai"] as [string, string],
  count: ["Musim Semi Kami", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Le Menu du Jour", "Rangkaian Acara"] as [string, string],
  story: ["Kisah dari Braga", "Cerita Kami"] as [string, string],
  gallery: ["Jendela Kenangan", "Galeri"] as [string, string],
  wishes: ["Pesan untuk Kami", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Merci",
    text: "Terima kasih atas kehadiran dan doa restu Bapak/Ibu/Saudara/i. Sampai jumpa di bawah wisteria.",
    salam: "Sabbe satta bhavantu sukhitatta — semoga semua makhluk berbahagia",
  },
  sent: "Merci! Ucapan Anda sudah kami terima dengan bahagia.",
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Tjandra", attendance: "yes" as const, message: "Selamat menempuh hidup baru. Semoga cinta kasih, kesabaran, dan kebijaksanaan selalu menyertai kalian berdua." },
  { id: "w2", name: "Kelas Bahasa Prancis Braga", attendance: "yes" as const, message: "Félicitations, Felicia & Jonathan! Akhirnya je t'aime kalian terdengar sempurna." },
  { id: "w3", name: "Vania & Kevin", attendance: "maybe" as const, message: "Semoga kami bisa terbang dari Singapura tepat waktu. Bahagia selalu!" },
];

export default function BalkonParisTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e8dfcf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverAwning} aria-hidden />
          <Art name="wisteria" className={`${s.coverWis} ${s.coverWisL}`} eager />
          <Art name="wisteria" className={`${s.coverWis} ${s.coverWisR}`} eager />
          <div className={s.windowArt}><Art name="window" eager /></div>
          <div className={s.plaque}>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffbf4" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fffbf4"
        dark="#36304a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <span className={s.heroAwning} aria-hidden />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <Art name="garland" className={s.divider} />
            {photo && (
              <div className={s.heroArt}>
                <div className={s.heroFrame}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>
                <Art name="wisteria" className={`${s.heroWis} ${s.heroWisL}`} />
                <Art name="wisteria" className={`${s.heroWis} ${s.heroWisR}`} />
                <Art name="railing" className={s.heroRail} />
              </div>
            )}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="garland" className={s.divider} />,
          node: <Art name="sprig" />,
          amp: <Art name="sprig" />,
          portrait: <Art name="railing" className={s.portraitRail} />,
          countDecor: <span className={s.awningTop} aria-hidden />,
          closingDecor: <><Art name="wisteria" className={s.closingWisteria} /><Art name="wisteria" className={s.closingWisteria} /></>,
          closingEmblem: <Art name="garland" className={s.divider} />,
          sentArt: <Art name="sprig" />,
        }}
      />
    </ThemeShell>
  );
}
