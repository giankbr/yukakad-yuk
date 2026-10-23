"use client";
// Theme "Batik Syari" — batik parang dan kawung yang dilembutkan (sage, biru debu, krem pasir) untuk undangan syar'i
// yang modern dan bersih. Sampul asimetris: selendang parang tegak di tepi kiri yang mengalir pelan, nama rata kiri di
// sampingnya, medali kawung yang berputar di sudut kanan bawah. Tanpa figur; teks Arab hanya ketikan. Foto opsional:
// monogram di ubin parang bila tidak ada foto mempelai. Semua lukisan dari /tmp/pen/art/themes/batik-syari.py.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Tenor Sans", "Lustria", "Italiana", "Amiri"];
const Art = makeArt("batik-syari", { kawung: [520, 519], divider: [379, 36], node: [77, 76] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dengan izin Allah", "Kedua Mempelai"] as [string, string],
  count: ["Menghitung hari", "Menuju Akad"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & tempat", "Rangkaian Acara"] as [string, string],
  story: ["Perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["Galeri", "Momen Kami"] as [string, string],
  wishes: ["Doa & kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah menjadikan pernikahan ini sakinah, mawaddah, wa rahmah.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah. Bila berkenan memberi tanda kasih, dapat melalui:",
};

export default function BatikSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6f1e7"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverLattice} aria-hidden />
          <span className={s.selendang} aria-hidden />
          <Art name="kawung" eager className={s.coverMedal} />
          <div className={s.coverPanel}>
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.coverSalam}>Assalamu&apos;alaikum Wr. Wb.</p>
          <p className={s.coverKicker}>{label}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf8f1" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos={!data.couple.bridePhoto && !data.couple.groomPhoto}
        light="#f1e8d6"
        dark="#3f5848"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <span className={s.heroLattice} aria-hidden />
            <Art name="kawung" className={s.heroMedal} />
            <div className={s.heroCard}>
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
            <span className={s.heroHem} aria-hidden />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="node" />,
          amp: <Art name="node" />,
          countDecor: <span className={s.countLattice} aria-hidden />,
          closingDecor: <><span className={s.closeLattice} aria-hidden /><span className={s.closeHem} aria-hidden /></>,
          closingEmblem: <Art name="kawung" className={s.closeMedal} />,
          sentArt: <Art name="node" />,
        }}
      />
    </ThemeShell>
  );
}
