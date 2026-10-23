"use client";
// Theme "Bali Endek" — a Hindu-Balinese pawiwahan in endek ikat: an endek waistband across the top of the cover with
// "Om Swastiastu", a penjor of janur arching over right-aligned names, a canang sari resting on the guest card and the
// terraced rice fields of Ubud below (gouache). The endek cloth (jade ground, magenta lattice, saffron flowers, feathered
// along the weft) frames every portrait, card and gift like a kamen border. Penjor and canang appear only as context;
// no deity imagery.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Della Respira", "Alegreya Sans:ital,wght@0,400;0,500;0,700;0,800;1,400", "Italianno"];
// Painted by /tmp/pen/art/themes/bali-endek.py (tools/art/themes in the repo).
const Art = makeArt("bali-endek", { sawah: [780, 485], penjor: [210, 542], canang: [230, 162], jepun: [110, 110], divider: [280, 25] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga I Nyoman Raka", attendance: "yes" as Attendance, message: "Om Swastiastu. Rahajeng nganten anyar, semoga menjadi keluarga yang sukhinah, rukun, dan selalu dalam lindungan Ida Sang Hyang Widhi Wasa." },
  { id: "w2", name: "Komang Ayu & Gus Adi", attendance: "yes" as Attendance, message: "Selamat Saras dan Wira! Semoga langgeng sampai tua, saling menjaga seperti subak menjaga sawahnya." },
  { id: "w3", name: "Teman Sanggar Peliatan", attendance: "maybe" as Attendance, message: "Kami usahakan datang ke resepsi. Doa terbaik untuk kalian berdua, semoga bahagia selalu." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Om Swastiastu",
    title: "Atas Asung Kertha Wara Nugraha",
    sub: "Ida Sang Hyang Widhi Wasa",
    intro: "Dengan memohon restu dan anugerah Ida Sang Hyang Widhi Wasa, kami bermaksud menyelenggarakan upacara Manusa Yadnya Pawiwahan putra-putri kami. Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Pawiwahan", "Kedua Mempelai"],
  count: ["Menuju Dewasa Ayu", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Upacara"],
  story: ["Perjalanan Kami", "Kisah Kami"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Punia Kasih", "Amplop Digital"],
  closing: { thanks: "Suksma", text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu. Atas kehadiran dan doanya, kami ucapkan terima kasih.", salam: "Om Shanti Shanti Shanti Om" },
  sent: "Suksma, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
};

export default function BaliEndekTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pawiwahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dfe8cf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.scene} aria-hidden>
            <Art name="sawah" eager className={s.sawah} />
            <div className={s.penjorBox}><Art name="penjor" eager /></div>
          </div>
          <div className={s.band}><span>Om Swastiastu</span></div>
          <p className={s.coverKicker}>Undangan {label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          {data.place && <p className={s.coverPlace}>{data.place}</p>}
          <span className={s.coverSpacer} aria-hidden />
          <div className={s.guestCard}>
            <Art name="canang" eager className={s.coverCanang} />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fdf6e3" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fdf6e3"
        dark="#155450"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="penjor" className={s.heroPenjor} />
            {hero && <div className={s.heroFrame}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>}
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="jepun" />,
          amp: <Art name="jepun" />,
          portrait: <Art name="jepun" />,
          closingDecor: <><Art name="sawah" className={s.closingSawah} /><Art name="penjor" className={s.closingPenjor} /></>,
          closingEmblem: <Art name="canang" className={s.closingCanang} />,
          sentArt: <Art name="canang" />,
        }}
      />
    </ThemeShell>
  );
}
