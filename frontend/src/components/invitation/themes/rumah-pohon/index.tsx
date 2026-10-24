"use client";
// Theme "Rumah Pohon" — a storybook treehouse in a big tree at golden hour, painted in gouache with a soft brown-pencil
// contour (original designs): the cover is the tree itself with a plank house (shingled roof, glowing round window,
// balcony, bunting, fairy lights), the names on a pine sign swinging from two ropes and a rope ladder swaying beside
// it. Inside: taped polaroids, sign-board cards, tree-ring countdown slices under fairy lights, a rope-ladder timeline.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:opsz,wght@9..144,600;9..144,700", "Nunito:wght@500;600;700;800", "Caveat Brush"];
// Painted by /tmp/pen/art/themes/rumah-pohon.py (tools/art/themes in the repo).
const Art = makeArt("rumah-pohon", {
  canopy: [780, 780], trunk: [780, 1200], ladder: [102, 896], forest: [520, 373], bunting: [420, 67],
} as const);

const WISHES = [
  { id: "w1", name: "Tante Lia & Om Ferry", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru, Sekar dan Dion! Semoga rumah kalian selalu hangat seperti lampu-lampu kecil di rumah pohon itu." },
  { id: "w2", name: "Geng Perkemahan 2019", attendance: "yes" as Attendance, message: "Dari terpal bocor sampai pelaminan. Kami bawa jaket dan suara terbaik untuk dansa nanti!" },
  { id: "w3", name: "Kak Monika, Yogyakarta", attendance: "maybe" as Attendance, message: "Semoga bisa menyusul ke Lembang. Bahagia selalu dan saling menjaga, ya." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, teman-teman!",
    title: "Naik ke Rumah Pohon Kami",
    intro: "Tangga sudah terpasang dan lampu-lampu kecil sudah menyala. Dengan penuh sukacita kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan merayakan hari pernikahan kami bersama keluarga dan sahabat.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Penghuni Rumah Pohon", "Kami Berdua"],
  count: ["Sebentar lagi", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat tanggalnya", "Waktu & Tempat"],
  story: ["Anak tangga demi anak tangga", "Cerita Kami"],
  gallery: ["Album kecil", "Galeri Foto"],
  wishes: ["Tinggalkan pesan", "Ucapan & Kehadiran"],
  gifts: ["Tanda kasih", "Kado & Amplop Digital"],
  closing: { thanks: "Terima kasih!", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah hadiah terindah untuk rumah kecil kami." },
  sent: "Hore, pesanmu sudah sampai ke rumah pohon! Terima kasih.",
  attend: { maybe: "Mungkin" },
};

export default function RumahPohonTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy: ThemeCopy = { ...COPY, wishPlaceholder: `Tulis ucapan untuk ${data.couple.bride} & ${data.couple.groom}…` };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6c27e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="forest" eager className={s.forest} />
          <Art name="trunk" eager className={s.trunk} />
          <Art name="canopy" eager className={s.canopy} />
          <Art name="ladder" eager className={s.ladder} />
          <span className={s.lights} aria-hidden />
          <div className={s.sign}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#3b2a1d" />Naik ke Atas</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fffaf0"
        dark="#3b2a1d"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="bunting" className={s.heroBunting} />
            {hero && (
              <div className={s.heroPolaroid}>
                <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>
                <span className={s.heroCaption} aria-hidden>kami, di hutan kecil</span>
              </div>
            )}
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="bunting" className={s.divider} />,
          closingEmblem: <Art name="bunting" className={s.divider} />,
          closingDecor: <div className={s.closingTree} aria-hidden><Art name="canopy" /></div>,
          sentArt: <Art name="bunting" />,
        }}
      />
    </ThemeShell>
  );
}
