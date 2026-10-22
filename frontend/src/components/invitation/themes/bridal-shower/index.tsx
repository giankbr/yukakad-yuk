"use client";
// Theme "Bridal Shower" — the bride-to-be's friends throw her a party: loose watercolour with a fine pen line and
// rose-gold foil (original designs). Two flutes of pink bubbly clink on the cover under a satin "Bride to Be" sash,
// garden roses with trailing ribbons frame the page, a blush silk robe swings on its hanger, the guest card and the
// countdown are hanging boutique tags, the bride sits in an oval vanity mirror and the gallery is taped polaroids.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Mrs Saint Delafield", "Figtree:wght@400;500;600;700"];
// Painted by /tmp/pen/art/themes/bridal-shower.py (tools/art/themes in the repo).
const Art = makeArt("bridal-shower", {
  glasses: [360, 496], robe: [320, 446], roses: [420, 255], sash: [640, 100], bubbles: [110, 225], bow: [210, 69],
} as const);

const WISHES = [
  { id: "w1", name: "Kirana (Maid of Honor)", attendance: "yes" as Attendance, message: "Nad, dari sekamar asrama sampai sekarang mau jadi istri orang. Bahagia selalu ya, aku yang paling kencang menangis nanti!" },
  { id: "w2", name: "Tante Wulan", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru, Nadia sayang. Semoga rumah tangga kalian penuh kasih, sabar, dan saling menguatkan." },
  { id: "w3", name: "Meisya", attendance: "maybe" as Attendance, message: "Masih menunggu jadwal dinas, semoga bisa menyusul. Peluk jauh dulu untuk calon pengantin tercantik!" },
];

export default function BridalShowerTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Bridal Shower";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const bride = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Untuk Para Sahabat",
      title: "Bride to Be",
      sub: "Ayo rayakan sang calon pengantin!",
      intro: `Sebentar lagi ${bride} akan melangkah ke hari pernikahannya. Sebelum hari besar itu tiba, kami para sahabatnya ingin merayakannya bersama: bersulang mocktail merah muda, permainan seru, cerita lama, dan doa-doa terbaik untuk babak barunya. Datang ya, kehadiranmu akan membuatnya sangat bahagia.`,
    },
    roles: ["Sang Calon Pengantin", "Bersama"],
    couple: ["The Bride to Be", "Sang Calon Pengantin"],
    count: ["Hitung Mundur", "Menuju Hari Bridal Shower"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Save the Date", "Waktu & Tempat"],
    story: ["Cerita Kami", `Sahabat ${bride}`],
    gallery: ["Galeri", "Momen Bersama Sahabat"],
    wishes: ["Untuk Sang Bride", "Pesan & Doa Manis"],
    gifts: ["Hadiah Kecil", "Kado untuk Sang Bride"],
    closing: { thanks: "Terima Kasih", text: `Terima kasih sudah ikut merayakan ${bride}. Sampai jumpa, dan siapkan pelukan terhangat untuk sang calon pengantin!` },
    sent: "Pesan manismu sudah sampai. Terima kasih!",
    wishPlaceholder: `Tulis pesan, doa, atau nasihat untuk ${bride}…`,
    giftIntro: `Kehadiranmu adalah hadiah terbaik. Bila ingin ikut memberi kado untuk ${bride}, bisa melalui:`,
    familyLabel: null,
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fdf1f0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="roses" eager className={s.rosesTop} />
          <Art name="roses" eager className={s.rosesBot} />
          <p className={s.kicker}>{label}</p>
          <p className={s.forBride}>untuk sang calon pengantin</p>
          <h1 className={s.coverName}>{bride}</h1>
          <div className={s.sash} aria-hidden>
            <Art name="sash" eager />
            <span>Bride to Be</span>
          </div>
          <div className={s.glassBox} aria-hidden>
            <Art name="bubbles" eager className={s.fizz} />
            <Art name="glasses" eager className={s.glasses} />
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={`${s.guest} ${s.tag}`}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffffff"
        dark="#5a2a3e"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <span className={s.rail} aria-hidden />
            <Art name="robe" className={s.robe} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroName}>{bride}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="bow" className={s.divider} />,
          node: <Art name="bow" />,
          portrait: <><Art name="bow" className={s.portraitBow} /><Art name="bubbles" className={s.portraitBubbles} /></>,
          countDecor: <><Art name="bubbles" className={`${s.countBubbles} ${s.cb1}`} /><Art name="bubbles" className={`${s.countBubbles} ${s.cb2}`} /></>,
          closingEmblem: (
            <>
              <Art name="glasses" className={s.closingGlasses} />
              <p className={s.hosts}>Dengan cinta,<br />para sahabat {bride}</p>
            </>
          ),
          sentArt: <Art name="glasses" />,
        }}
      />
    </ThemeShell>
  );
}
