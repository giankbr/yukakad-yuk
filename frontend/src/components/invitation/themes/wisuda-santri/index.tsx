"use client";
// Theme "Wisuda Santri" — wisuda & khataman pesantren dalam hijau dan putih (gouache): tumpukan kitab bersampul polos
// dengan peci di atasnya, gapura pondok putih bertajug hijau di antara pohon mangga, sarung kotak-kotak terlipat,
// bintang segi delapan. Hero berupa kartu syahadah dan doa yang disusun seperti punggung kitab. Tanpa figur makhluk
// hidup dan tanpa kaligrafi yang digambar (basmalah diketik).
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Castoro:ital@0;1", "Mulish:wght@400;600;700;800", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/wisuda-santri.py
const Art = makeArt("wisuda-santri", {
  kitab: [360, 283], gapura: [420, 238], sarung: [300, 124], band: [320, 22], bintang: [72, 72],
} as const);

const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";
const DOA = [
  { title: "Ilmu yang manfaat", body: "Semoga setiap huruf yang dihafal dan setiap kitab yang dikaji menjadi cahaya bagi dirinya dan sekitarnya." },
  { title: "Akhlak yang mulia", body: "Semoga adab yang ditanam di pondok selalu terbawa, di rumah, di masyarakat, dan di mana pun ia berada." },
  { title: "Istiqamah dalam khidmah", body: "Semoga ia tetap setia mengaji, mengajar, dan berkhidmah kepada guru, orang tua, dan umat." },
] as const;

export default function WisudaSantriTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Wisuda & Khataman Santri";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const full = child?.name.trim() || data.couple.brideFull || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbfbf6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverBismillah} lang="ar" dir="rtl">{BISMILLAH}</p>
          <Art name="bintang" eager className={s.coverStar} />
          <p className={s.coverKicker}>Undangan</p>
          <p className={s.coverLabel}>{label}</p>
          <h1 className={s.coverName}>{names}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbfbf6" />Buka Undangan</button>
          <div className={s.coverGate} aria-hidden><Art name="gapura" eager /></div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fbfbf6"
        dark="#1d4630"
        demoWishes={[
          { id: "w1", name: "Ustadz Mahfudz", attendance: "yes", message: "Barakallahu fiik, Fauzan. Semoga hafalanmu terjaga, ilmumu bermanfaat, dan menjadi kebanggaan orang tua di dunia dan akhirat." },
          { id: "w2", name: "Keluarga Bani Arifin", attendance: "yes", message: "Alhamdulillah. Mabruk atas wisuda dan khatamnya, semoga istiqamah dan menjadi santri yang alim dan berakhlak." },
          { id: "w3", name: "Kang Ridwan (alumni 2024)", attendance: "maybe", message: "Selamat, Kang! Insyaallah menyusul ke pondok kalau pekerjaan selesai. Doa terbaik untukmu." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Alhamdulillah",
            sub: label,
            intro: `Dengan memohon rahmat dan ridha Allah SWT, kami mengundang Bapak/Ibu/Saudara/i untuk menghadiri ${label.toLowerCase()} ananda ${names}. Semoga ilmu dan hafalannya menjadi berkah, dan kehadiran Anda menambah syukur kami sekeluarga.`,
          },
          roles: ["Santri yang Diwisuda", "Bersama"],
          couple: ["Sang Santri", child ? `Kenalan dengan ${nick}` : "Yang Diwisuda"],
          count: ["Menghitung Hari", "Menuju Hari Wisuda"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Perjalanan", "Di Pondok"],
          gallery: ["Galeri", "Kenangan"],
          wishes: ["Doa & Ucapan", "Konfirmasi Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: `Atas kehadiran dan doa Bapak/Ibu/Saudara/i untuk ${names}, kami sekeluarga mengucapkan terima kasih.`,
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
          wishPlaceholder: `Tuliskan doa untuk ${names}…`,
          giftIntro: "Doa Anda adalah hadiah terbaik. Bila berkenan memberi tanda kasih, dapat melalui:",
          familyLabel: "Kami yang berbahagia, Keluarga",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="kitab" className={s.heroKitab} />
            <div className={s.syahadah}>
              <Art name="bintang" /><Art name="bintang" /><Art name="bintang" /><Art name="bintang" />
              <p className={s.heroKicker}>{label}</p>
              <p className={s.heroLead}>Alhamdulillah, telah menamatkan pendidikannya</p>
              <h1 className={s.heroName}>{names}</h1>
              {child && full !== nick && <p className={s.heroFull}>{full}</p>}
              {note && <p className={s.heroNote}>{note}</p>}
              <p className={s.heroDate}>{formatDate(data.date)}</p>
            </div>
            <h2 className={s.doaTitle}>Doa untuk Sang Santri</h2>
            <p className={s.doaSub}>tiga bekal yang kami mohonkan</p>
            <ol className={s.spines}>
              {DOA.map(item => <li key={item.title}><h3>{item.title}</h3><p>{item.body}</p></li>)}
            </ol>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="band" /></span>,
          node: <Art name="bintang" />,
          portrait: <Art name="kitab" className={s.portraitKitab} />,
          countDecor: <Art name="sarung" className={s.countSarung} />,
          closingDecor: <div className={s.closingGate} aria-hidden><Art name="gapura" /></div>,
          closingEmblem: <Art name="bintang" className={s.closingStar} />,
          sentArt: <Art name="bintang" />,
        }}
      />
    </ThemeShell>
  );
}
