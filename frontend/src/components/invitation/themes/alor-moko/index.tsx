"use client";
// Theme "Alor Moko" — pernikahan muslim adat Alor. Sampul di atas pasir krem berpita tenun ikat Alor: nama dalam Gloock,
// lalu jendela ke teluk toska di antara pulau-pulau hijau yang curam (cat air) dengan moko perunggu berpatina berdiri di
// tepinya, belis yang menyatukan dua keluarga. Hero: foto pasangan dicetak dalam siluet jam pasir moko, tympanum
// berbintang sebagai tutupnya. Hitung mundur di atas cakram tympanum, kartu acara bertepi tenun, penutup di teluk senja.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Petrona:ital,wght@0,400;0,600;1,400"];
// Painted by /tmp/pen/art/themes/alor-moko.py (tools/art/themes in the repo).
const Art = makeArt("alor-moko", { moko: [200, 332], tympanum: [120, 120], divider: [200, 32] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan memohon rahmat dan rida Allah SWT",
    intro: "Kami bermaksud menyelenggarakan pernikahan putra-putri kami di Kalabahi, Alor. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Keluarga, Satu Ikatan", "Kedua Mempelai"] as [string, string],
  count: ["Menuju hari bahagia", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Dari Teluk Mutiara", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Momen Bahagia"] as [string, string],
  wishes: ["Doa & Restu", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah kehormatan bagi kami sekeluarga. Semoga Allah SWT membalas kebaikan Anda dengan keberkahan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
  familyLabel: "Kami yang berbahagia, keluarga besar",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Hamzah Lamma", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga menjadi keluarga sakinah, mawaddah, warahmah. Kami sekeluarga hadir dari Alor Kecil." },
  { id: "w2", name: "Teman-teman SMA Negeri 1 Kalabahi", attendance: "yes" as const, message: "Akhirnya! Selamat Nur dan Rizal, semoga langgeng seperti moko pusaka. Sampai jumpa di Gedung Serbaguna." },
  { id: "w3", name: "Om Yusuf & Tante Rahma (Kupang)", attendance: "maybe" as const, message: "Mohon maaf kalau kapal belum bersahabat. Doa kami menyertai kalian berdua dari Kupang." },
];

export default function AlorMokoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const heroPhoto = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#12324a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.scene} aria-hidden>
            <span className={s.sceneWater} />
            <Art name="moko" eager className={s.coverMoko} />
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f0c486" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0c486"
        dark="#1c2440"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            {heroPhoto ? <><Art name="tympanum" className={s.heroLid} /><div className={s.heroDrum}><Photo src={heroPhoto} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div></> : <Art name="moko" className={s.heroMoko} />}
            <p className={s.heroKicker}>{label} · Kalabahi, Alor</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="tympanum" />,
          amp: <Art name="tympanum" />,
          portrait: <Art name="tympanum" className={s.portraitLid} />,
          countDecor: <span className={s.ripples} aria-hidden />,
          closingEmblem: <Art name="moko" className={s.closingMoko} />,
          sentArt: <Art name="tympanum" />,
        }}
      />
    </ThemeShell>
  );
}
