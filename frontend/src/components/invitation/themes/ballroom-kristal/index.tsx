"use client";
// Theme "Ballroom Kristal" — ballroom megah dalam cahaya sampanye. Sampul: lukisan aula (jendela lengkung, tirai sutra,
// meja bundar bercahaya lilin, lantai marmer yang memantulkan cahaya) dengan lampu kristal bertingkat yang bergoyang di
// atas nama dan kartu tempat duduk untuk tamu. Potret dalam cermin oval berbingkai emas, pembatas untaian kristal.
// Dilukis oleh /tmp/pen/art/themes/ballroom-kristal.py.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;0,6..96,600;1,6..96,400", "Spectral:ital,wght@0,400;0,500;0,600;1,400", "Pinyon Script"];
const Art = makeArt("ballroom-kristal", { chandelier: [400, 362], table: [420, 346], divider: [360, 58] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh sukacita",
    title: "Sebuah Malam untuk Dikenang",
    sub: "kami mengundang Anda",
    intro: "Bersama keluarga kami, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan merayakan hari pernikahan kami. Kehadiran Anda akan membuat malam ini semakin bercahaya.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["The Bride & Groom", "Kedua Mempelai"],
  count: ["Menuju malam itu", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Save the date", "Rangkaian Acara"],
  story: ["Our story", "Kisah Kami"],
  gallery: ["Galeri", "Momen Kami"],
  wishes: ["RSVP", "Ucapan & Kehadiran"],
  gifts: ["Tanda kasih", "Hadiah Pernikahan"],
  closing: { thanks: "Terima kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah hadiah terindah bagi kami. Sampai bertemu di lantai dansa." },
  sent: "Terima kasih, ucapan Anda sudah kami terima.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
  closedNote: "Terima kasih atas perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
  giftIntro: "Kehadiran Anda sudah lebih dari cukup. Bila ingin memberi tanda kasih, dapat melalui:",
  familyLabel: "Dengan hormat, kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Keluarga Gunawan", attendance: "yes" as Attendance, message: "Selamat Vivian & Raymond! Semoga rumah tangga kalian selalu hangat dan penuh berkat. Sampai jumpa di ballroom." },
  { id: "w2", name: "Grace & Kevin", attendance: "yes" as Attendance, message: "Akhirnya first dance yang sesungguhnya! Kami sudah siap dengan sepatu dansa." },
  { id: "w3", name: "Om Budi Santoso", attendance: "maybe" as Attendance, message: "Mohon maaf kalau belum bisa pasti hadir. Doa terbaik untuk kalian berdua dan kedua keluarga." },
];

export default function BallroomKristalTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a1f17"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverVeil} aria-hidden />
          <Art name="chandelier" eager className={s.coverLamp} />
          <div className={s.coverText}>
            <p className={s.kicker}>{label}</p>
            <h1 className={s.coverNames}>
              <span>{data.couple.bride}</span>
              {groom && <><em>&amp;</em><span>{groom}</span></>}
            </h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.placeCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ecd6a3" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#ecd6a3"
        dark="#2a1f17"
        hero={(
          <header className={s.hero}>
            <Art name="chandelier" className={s.heroLamp} />
            <div className={s.heroArch}>
              {hero ? <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} ${groom ? `dan ${groom}` : ""}`.trim()} /></div> : <div className={s.heroBlank} aria-hidden />}
            </div>
            <p className={s.kickerHero}>{label}</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="chandelier" />,
          countDecor: <Art name="chandelier" className={s.countLamp} />,
          closingEmblem: <Art name="table" className={s.closeTable} />,
          sentArt: <Art name="divider" />,
        }}
      />
    </ThemeShell>
  );
}
