"use client";
// Theme "Peach Syari" — bunga cat air peach dan koral lembut (ranunculus, mawar taman, kuncup, bunga lilin dan daun
// sage) di atas kertas krem. Sampul berkalung bunga asimetris dengan kolam warna peach di balik nama, medali oval
// berinisial, kartu bertepi jahitan. Tanpa foto (syar'i), manis tapi anggun. Gerak lembut: rangkaian bunga berayun pelan.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bellefair", "Mulish:ital,wght@0,400;0,600;0,700;1,400", "Monsieur La Doulaise", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/peach-syari.py.
const Art = makeArt("peach-syari", { garland: [620, 362], corner: [300, 214], bloom: [178, 166], divider: [320, 35], wash: [420, 517] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const WISHES = [
  { id: "w1", name: "Ibu Hj. Fatimah Az-Zahra", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fii khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Teman Kajian Ahad", attendance: "yes" as const, message: "Masyaallah, ikut bahagia untuk Nayla dan Faris. Semoga Allah mudahkan sampai hari H dan seterusnya." },
  { id: "w3", name: "Keluarga Om Hanif", attendance: "maybe" as const, message: "Insyaallah kami usahakan hadir. Doa terbaik dari kami sekeluarga di Semarang." },
];

export default function PeachSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fcf5ee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="wash" eager className={s.coverWash} />
          <Art name="corner" eager className={s.coverCorner} />
          <p className={s.bismillah} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
          <Art name="garland" eager className={s.coverGarland} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#b9524a"
        dark="#ffffff"
        demoWishes={WISHES}
        copy={{
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Wr. Wb.",
            title: "Dengan Memohon Ridha Allah",
            sub: "“Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri.” (QS. Ar-Rum: 21)",
            intro: "Tanpa mengurangi rasa hormat, kami bermaksud mengundang Bapak/Ibu/Saudara/i untuk menghadiri akad nikah dan walimah kami. Kehadiran serta doa restu Anda adalah kebahagiaan bagi kami.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Atas izin Allah", "Kedua Mempelai"],
          count: ["Menanti hari bahagia", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Insyaallah dilaksanakan", "Waktu & Tempat"],
          story: ["Takdir yang indah", "Perjalanan Kami"],
          gallery: ["Album", "Galeri"],
          wishes: ["Doa & kehadiran", "Ucapan & Doa"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: { thanks: "Jazakumullahu Khairan", text: "Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.", salam: "Wassalamu'alaikum Wr. Wb." },
          sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah terkirim.",
          wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
          closedNote: "Jazakumullahu khairan atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="corner" className={s.heroCorner} />
            <div className={s.cameo}>
              <p className={s.initials} aria-hidden>{data.couple.bride.slice(0, 1)}<em>&amp;</em>{data.couple.groom.slice(0, 1)}</p>
              <Art name="bloom" className={s.cameoBloom} />
            </div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="bloom" />,
          amp: <Art name="bloom" />,
          portrait: <Art name="bloom" />,
          countDecor: <span className={s.countDecor} aria-hidden><Art name="corner" /><Art name="corner" /></span>,
          closingDecor: <span className={s.closingGarland} aria-hidden><Art name="garland" /></span>,
          closingEmblem: <Art name="bloom" className={s.closingEmblem} />,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
