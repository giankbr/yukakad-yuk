"use client";
// Theme "Priangan Kacapi" — adat Sunda Priangan: sampul berupa jendela di dinding bilik (anyaman bambu) yang memandang
// sawah terasering dan saung, kacapi parahu melintang di ambang jendela, suling bambu sebagai pembatas, untaian padi.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Della Respira", "Lora:ital,wght@0,400;0,500;0,600;1,400", "Caveat:wght@500;600"];
// Painted by /tmp/pen/art/themes/priangan-kacapi.py (tools/art/themes in the repo).
const Art = makeArt("priangan-kacapi", { kacapi: [760, 180], suling: [400, 35], padi: [240, 311], sawah: [780, 471] } as const);

const WISHES = [
  { id: "w1", name: "Wa Haji Encep & Keluarga", attendance: "yes" as const, message: "Wilujeng nempuh hirup anyar. Mugia janten kulawarga sakinah, mawaddah, warahmah, sareng dipaparin barokah." },
  { id: "w2", name: "Teh Nining Kurniawati", attendance: "yes" as const, message: "Barakallahu lakuma, Rini & Asep! Semoga langgeng dan selalu saling menguatkan." },
  { id: "w3", name: "Kang Dede & Teh Lilis", attendance: "maybe" as const, message: "Hapunten upami teu tiasa sumping. Doa kami menyertai, semoga lancar sampai hari H." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Nyuhunkeun Pidu'a",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Panganten Istri", "Panganten Pameget"],
  couple: ["kalih jiwa", "Kedua Mempelai"],
  count: ["ngitung poe", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["waktos & tempat", "Rangkaian Acara"],
  story: ["carita urang", "Kisah Kami"],
  gallery: ["kenangan", "Galeri Foto"],
  wishes: ["pidu'a & ucapan", "Ucapan & Kehadiran"],
  gifts: ["tanda kanyaah", "Amplop Digital"],
  closing: { thanks: "Hatur Nuhun", text: "Kehadiran serta doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan dan kehormatan bagi kami sekeluarga.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Hatur nuhun, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
};

export default function PrianganKacapiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3f2414"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.window}>
            <Art name="padi" eager className={s.padiL} />
            <Art name="padi" eager className={s.padiR} />
            <p className={s.greet}>Wilujeng Sumping</p>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f6ead0" />Buka Undangan</button>
            </div>
            <div className={s.scene} aria-hidden>
              <Art name="sawah" eager className={s.sawah} />
              <Art name="kacapi" eager className={s.coverKacapi} />
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#f3dfa8"
        dark="#4a2b18"
        hero={(
          <header className={s.hero}>
            <Art name="suling" className={s.heroSuling} />
            {hero && <div className={s.heroFrame}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>}
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="suling" className={s.divider} />,
          node: <Art name="padi" />,
          amp: <Art name="padi" />,
          portrait: <Art name="padi" className={s.padiPin} />,
          countDecor: <><Art name="padi" className={s.countDecorL} /><Art name="padi" className={s.countDecorR} /></>,
          closingDecor: <Art name="sawah" className={s.closingSawah} />,
          sentArt: <Art name="kacapi" />,
        }}
      />
    </ThemeShell>
  );
}
