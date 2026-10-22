"use client";
// Theme "Prom Perpisahan" — an SMA farewell night (original designs): a mirror disco ball swings on its cord while two
// stage spotlights sweep and coloured disco reflections drift over a glitter-dusted dance floor; a rosette class-year
// badge, neon-edged glass cards, an LED scoreboard countdown, yearbook polaroids for the ketua angkatan & ketua OSIS,
// a photobooth-strip gallery and a linocut crowd of classmates (hands up, a cap in the air) closing the page.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Monoton", "Righteous", "Outfit:wght@400;500;600"];
// Painted by /tmp/pen/art/themes/prom-perpisahan.py (tools/art/themes in the repo).
const Art = makeArt("prom-perpisahan", {
  disco: [300, 422], beam: [180, 450], crowd: [780, 234], badge: [200, 269], divider: [220, 38], glitter: [300, 300],
} as const);

const WISHES = [
  { id: "w1", name: "Bu Ratna (Wali Kelas XII MIPA 2)", attendance: "yes" as Attendance, message: "Selamat atas kelulusan kalian, anak-anakku. Terbanglah setinggi mungkin, tapi jangan lupa pulang menengok sekolah ini." },
  { id: "w2", name: "Clarissa XII IPS 3", attendance: "yes" as Attendance, message: "Gak nyangka udah mau pisah. Makasih tiga tahunnya, Angkatan 27! Sampai ketemu di lantai dansa." },
  { id: "w3", name: "Orang tua Bagas", attendance: "maybe" as Attendance, message: "Terima kasih panitia dan para guru. Semoga semua lulusan sukses di jalannya masing-masing." },
];

export default function PromPerpisahanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Malam Perpisahan";
  const year = toDate(data.date)?.getFullYear();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: year ? `Angkatan ${year}` : "Kelas XII",
      title: "See You on the Dance Floor",
      sub: "Satu malam terakhir bersama",
      intro: "Tiga tahun kita lewati bersama: upacara Senin pagi, ulangan dadakan, pensi, dan tawa di kantin. Sebelum melangkah ke jalan masing-masing, mari berkumpul sekali lagi untuk merayakan perpisahan dengan meriah. Kehadiran kalian, para guru, dan orang tua akan membuat malam ini tak terlupakan.",
    },
    roles: ["Ketua Angkatan", "Ketua OSIS"],
    couple: ["Mengundang Kalian", "Dari Kami, Panitia"],
    count: ["Hitung Mundur", "Menuju Malam Perpisahan"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Line Up", "Acara Malam Itu"],
    story: ["Jejak Angkatan", "Tiga Tahun Kita"],
    gallery: ["Photobooth", "Kenangan Sekelas"],
    wishes: ["Buku Kenangan", "Pesan & Konfirmasi"],
    gifts: ["Kenang-Kenangan", "Sumbangan untuk Sekolah"],
    closing: { thanks: "Terima Kasih", text: "Terima kasih untuk tiga tahun yang luar biasa. Apa pun jalan yang kita pilih setelah ini, kita tetap satu angkatan." },
    sent: "Pesanmu sudah tertulis di buku kenangan. Terima kasih!",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: "Tulis pesan, kenangan, atau doa untuk angkatan…",
    giftIntro: "Bagi yang ingin ikut menyumbang kenang-kenangan angkatan untuk sekolah (bangku taman & pohon peneduh), dapat melalui:",
    familyLabel: "Panitia Perpisahan",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0b0720"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.glitterBg} aria-hidden />
          <span className={s.spots} aria-hidden />
          <Art name="beam" eager className={s.beamL} />
          <Art name="beam" eager className={s.beamR} />
          <div className={s.discoBox} aria-hidden><Art name="disco" eager className={s.disco} /></div>
          <p className={s.kicker}>Undangan Kelas XII</p>
          <h1 className={s.coverTitle}>Prom Night</h1>
          <p className={s.coverSub}>{label}</p>
          {year && (
            <div className={s.badgeBox} aria-hidden>
              <Art name="badge" eager />
              <span className={s.badgeYear}><small>Angkatan</small>{year}</span>
            </div>
          )}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={`${s.guest} ${s.pass}`}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          <Art name="crowd" eager className={s.crowd} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        light="#ffffff"
        dark="#120b2e"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="disco" className={s.heroDisco} />
            <p className={s.heroKicker}>{year ? `Kelas XII · Angkatan ${year}` : "Kelas XII"}</p>
            <h1 className={s.heroTitle}>{label}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="divider" className={s.divider} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="disco" />,
          portrait: <Art name="badge" className={s.portraitBadge} />,
          countDecor: <><Art name="beam" className={`${s.countBeam} ${s.cbL}`} /><Art name="beam" className={`${s.countBeam} ${s.cbR}`} /></>,
          closingEmblem: <Art name="disco" className={s.closingDisco} />,
          closingDecor: <Art name="crowd" className={s.closingCrowd} />,
          sentArt: <Art name="badge" />,
        }}
      />
    </ThemeShell>
  );
}
