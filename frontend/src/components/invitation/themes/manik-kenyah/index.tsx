"use client";
// Theme "Manik Kenyah" — adat Dayak Kenyah (Malinau, Kalimantan Utara): panel manik yang dilukis butir demi butir dengan
// sulur aso melengkung dan kepala enggang dalam kuning, hitam, putih, merah dan biru; rumbai manik bergoyang di bawah
// pelat undangan, cincin manik di sekeliling foto, dan lamin bermural di tepi sungai. Semua motif digambar ulang, bukan
// salinan karya manik tertentu.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Syne:wght@600;700;800", "Petrona:ital,wght@0,400;0,600;0,700;1,400"];
// Painted by /tmp/pen/art/themes/manik-kenyah.py.
const Art = makeArt("manik-kenyah", { panel: [580, 748], medal: [260, 260], ring: [400, 399], fringe: [631, 151], lamin: [720, 407], divider: [320, 59] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Sejahtera",
    title: "Dirangkai dalam Kasih",
    sub: "Butir demi butir, menjadi satu untaian",
    intro: "Dengan penuh syukur kepada Tuhan Yang Maha Kasih, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan memberikan doa restu pada pemberkatan nikah serta pesta adat Kenyah putra-putri kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Untaian", "Kedua Mempelai"],
  count: ["Menuju Hari Bahagia", "Hitung Hari"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Butir Demi Butir", "Kisah Kami"],
  gallery: ["Galeri", "Kenangan Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Kado Pernikahan"],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang menguatkan kami memulai rumah tangga yang baru. Tuhan memberkati.",
    salam: "Salam hangat dari lamin di tepi Sungai Malinau",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima. Tuhan memberkati.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
  giftIntro: "Doa dan kehadiran Anda sudah menjadi hadiah terindah. Bila berkenan memberi tanda kasih, dapat melalui:",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Lukas Lawai", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Ilun dan Jalung. Kiranya Tuhan memberkati rumah tangga kalian, kuat seperti untaian manik yang dironce rapat." },
  { id: "w2", name: "Pdt. Daniel & Jemaat GKII Malinau", attendance: "yes" as const, message: "Bersukacita bersama kalian. Kasih Kristus menyertai setiap langkah, sampai jumpa di gereja dan di lamin." },
  { id: "w3", name: "Teman-teman Sanggar Kancet", attendance: "maybe" as const, message: "Semoga bisa ikut menari di Setulang! Selamat ya, Tuhan memberkati." },
];

export default function ManikKenyahTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();
  const initials = [data.couple.bride, groom].filter(Boolean).map(name => name!.slice(0, 1)).join("");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#100c09"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="panel" eager className={s.coverPanel} />
          <div className={s.plate}>
            <Art name="medal" eager className={s.medal} />
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>dan</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#e8b52a" />Buka Undangan</button>
            <Art name="fringe" eager className={s.fringe} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#e8b52a"
        dark="#16110e"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="lamin" eager className={s.heroLamin} />
            <div className={s.heroFrame}>
              <Art name="ring" eager className={s.heroRing} />
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} dan ${groom ?? ""}`.trim()} /> : <span className={s.heroMono} aria-hidden>{initials}</span>}</div>
            </div>
            <p className={s.heroKicker}>Pemberkatan &amp; Pesta Adat</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="medal" />,
          amp: <Art name="medal" />,
          portrait: <Art name="ring" className={s.portraitArt} />,
          countDecor: <Art name="medal" className={s.countDecor} />,
          closingDecor: <Art name="lamin" className={s.closingLamin} />,
          closingEmblem: <Art name="medal" className={s.closingEmblem} />,
          sentArt: <Art name="medal" />,
        }}
      />
    </ThemeShell>
  );
}
