"use client";
// Theme "Malam Gurun" — Islami: bukit-bukit pasir di bawah langit malam berbintang dengan bulan sabit tipis. Pasir
// diterangi bulan dari kanan atas, oasis kurma dan sebuah tenda berlampu di kejauhan (tanpa sosok makhluk hidup),
// bintang delapan sudut bersepuh emas sebagai ornamen. Halaman berirama malam -> pasir -> malam.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Forum", "Lustria", "Reem Kufi:wght@400;500", "Amiri"];
// Painted by /tmp/pen/art/themes/malam-gurun.py (sky, sand and the dune band are CSS backgrounds).
const Art = makeArt("malam-gurun", { dunes: [720, 544], star: [160, 160], divider: [322, 24] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    sub: "Di bawah langit yang sama",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dengan Izin Allah", "Kedua Mempelai"],
  count: ["Menanti Malam Bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Jejak di Pasir", "Kisah Kami"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullahu Khairan",
    text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu. Semoga Allah membalas setiap kebaikan dengan keberkahan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullahu khairan, doa Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa Anda adalah hadiah terindah bagi kami. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Ustadzah Maryam & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga yang sakinah dan selalu dekat dengan-Nya." },
  { id: "w2", name: "Teman Kajian PPMI Kairo", attendance: "yes" as const, message: "Dari Kairo sampai Surabaya, akhirnya! Mabruk, Hafiz dan Salma. Kami datang serombongan, insyaallah." },
  { id: "w3", name: "Rina Apoteker", attendance: "maybe" as const, message: "Selamat ya Salma sayang. Insyaallah menyusul selepas dinas malam, doa terbaik untuk kalian berdua." },
];

export default function MalamGurunTheme(props: ThemeProps) {
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
      background="#0a0f2a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div aria-hidden>{[0, 1, 2, 3, 4].map(i => <span key={i} className={s.twinkle} />)}</div>
          <Art name="dunes" eager className={s.coverDunes} />
          <div className={s.coverSky}>
            <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
            <p className={s.kicker}>Walimatul &apos;Ursy · {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#0a0f2a" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#ecd39a"
        dark="#111940"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} dan ${groom ?? ""}`.trim()} /> : <span className={s.heroMono} aria-hidden>{initials}</span>}</div>
            </div>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          portrait: <Art name="star" className={s.portraitArt} />,
          closingEmblem: <Art name="star" className={s.closingEmblem} />,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
