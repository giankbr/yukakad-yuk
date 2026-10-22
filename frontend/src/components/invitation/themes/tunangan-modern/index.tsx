"use client";
// Theme "Tunangan Modern" — tunangan minimalis bergaya editorial: putih hangat, garis tinta tipis, satu aksen terakota.
// Cincin bertaut digambar dengan pena di atas sapuan terakota, setangkai bunga cat air, judul rata kiri bernomor,
// potret hitam-putih berdampingan, deret fakta acara di hero.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Italiana", "Manrope:wght@400;500;600;700"];
// Painted by /tmp/pen/art/themes/tunangan-modern.py
const Art = makeArt("tunangan-modern", {
  rings: [420, 338], stem: [240, 697], sprig: [160, 337], loop: [380, 32],
} as const);

function shortDate(iso?: string) {
  const d = toDate(iso);
  if (!d) return "";
  const p = (n: number) => String(n).padStart(2, "0");
  return `${p(d.getDate())}.${p(d.getMonth() + 1)}.${String(d.getFullYear()).slice(2)}`;
}

export default function TunanganModernTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Tunangan";
  const bride = data.couple.bride;
  const groom = data.couple.groom?.trim();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const first = data.events[0];
  const photo = data.gallery[0];
  const stamp = shortDate(data.date);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f5f3ef"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="stem" eager className={s.coverStem} />
          <p className={s.coverTop}><span>{label}</span>{stamp && <span>{stamp}</span>}</p>
          <div className={s.coverBody}>
            <p className={s.coverKicker}>Kami bertunangan</p>
            <h1 className={s.coverNames}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#f5f3ef" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#1f1e1c"
        dark="#f5f3ef"
        demoWishes={[
          { id: "w1", name: "Sekar & Dimas", attendance: "yes", message: "Akhirnya! Selamat bertunangan, kalian berdua. Semoga perjalanan menuju hari besar berjalan ringan dan menyenangkan." },
          { id: "w2", name: "Tante Wulan", attendance: "yes", message: "Ikut bahagia, Mayang. Semoga cincin kecil ini jadi awal dari janji yang besar dan langgeng." },
          { id: "w3", name: "Tim Studio Garis", attendance: "maybe", message: "Selamat Mayang & Rendra! Kami usahakan datang setelah tenggat proyek. Doa terbaik dari kami semua." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Sebuah kabar",
            title: "Dengan sukacita",
            sub: `Undangan ${label}`,
            intro: `Kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menjadi saksi ketika kami saling mengikat janji dalam acara ${label.toLowerCase()}. Kehadiran dan doa Anda akan membuat hari sederhana ini terasa lengkap.`,
          },
          roles: ["Calon Mempelai Wanita", "Calon Mempelai Pria"],
          couple: ["Yang bertunangan", "Kami berdua"],
          count: ["Hitung mundur", "Menuju hari itu"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & tempat", "Jadwal acara"],
          story: ["Cerita", "Sampai di sini"],
          gallery: ["Galeri", "Beberapa momen"],
          wishes: ["Konfirmasi", "Ucapan & kehadiran"],
          gifts: ["Tanda kasih", "Hadiah"],
          closing: {
            thanks: "Terima kasih",
            text: "Kehadiran dan doa Anda adalah hadiah terbaik bagi kami berdua dan keluarga.",
          },
          attend: { maybe: "Mungkin" },
          sent: "Terima kasih, ucapan Anda sudah kami terima.",
          wishPlaceholder: "Tulis ucapan untuk kami berdua…",
          giftIntro: "Doa Anda sudah lebih dari cukup. Bila ingin memberi tanda kasih, dapat melalui:",
          familyLabel: "Bersama keluarga",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroIndex}><b>00</b> — Kabar baik</p>
            <Art name="rings" className={s.heroRings} />
            <h1 className={s.heroNames}>{bride}{groom && <> <em>&amp;</em> {groom}</>}</h1>
            {note && <p className={s.heroNote}>{note}</p>}
            {photo && (
              <figure className={s.heroPhotoWrap}>
                <Photo src={photo} alt={`Foto ${bride}${groom ? ` & ${groom}` : ""}`} className={s.heroPhoto} />
                <figcaption>{bride}{groom ? ` & ${groom}` : ""}, {stamp || label}</figcaption>
              </figure>
            )}
            <dl className={s.facts}>
              <div><dt>Tanggal</dt><dd>{formatDate(first?.date || data.date)}</dd></div>
              <div><dt>Waktu</dt><dd>{first?.time || "Menyusul"}</dd></div>
              <div><dt>Tempat</dt><dd>{first?.venue || data.place}</dd></div>
            </dl>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="loop" /></span>,
          countDecor: <Art name="rings" className={s.countRings} />,
          closingDecor: <Art name="stem" className={s.closingStem} />,
          closingEmblem: <Art name="sprig" className={s.closingSprig} />,
          sentArt: <Art name="rings" />,
        }}
      />
    </ThemeShell>
  );
}
