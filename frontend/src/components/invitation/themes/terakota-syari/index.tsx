"use client";
// Theme "Terakota Syari" — undangan syari tanpa foto bernuansa tanah: gerbang lengkung terakota bertekstur tanah liat di
// atas dinding plester krem, daun palem kering dan pampas dalam vas gerabah, deretan arkade, dan medali bintang delapan
// dari tanah liat. Tanpa gambar makhluk hidup; teks Arab diketik, bukan kaligrafi lukis.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "Hanken Grotesk:wght@400;500;600", "Amiri"];
// Painted by /tmp/pen/art/themes/terakota-syari.py.
const Art = makeArt("terakota-syari", { arch: [600, 879], arcade: [720, 204], vase: [440, 591], pampas: [300, 489], sprig: [306, 27], emblem: [220, 219] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    sub: "Dengan memohon ridha Allah",
    intro: "Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan ridha-Nya, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Bismillah", "Kedua Mempelai"],
  count: ["Menuju Hari Bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Kami"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullahu Khairan",
    text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu. Semoga Allah membalas setiap kebaikan dengan yang lebih baik.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah bagi kami. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Ustadzah Khadijah & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Teman Kelas Keramik Sabtu", attendance: "yes" as const, message: "Dari mangkuk retak sampai pelaminan. Ikut bahagia, semoga rumah kalian selalu hangat seperti tungku." },
  { id: "w3", name: "Keluarga Bapak Hendra Gunawan", attendance: "maybe" as const, message: "Mohon maaf bila belum bisa hadir. Doa terbaik kami untuk Nadhira dan Rayyan." },
];

export default function TerakotaSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();
  const initials = [data.couple.bride, groom].filter(Boolean).map(name => name!.slice(0, 1));

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3e9dc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.portal}>
            <Art name="arch" eager className={s.portalArch} />
            <div className={s.portalInner}>
              <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ</p>
              <p className={s.kicker}>Walimatul &apos;Ursy</p>
              <span className={s.coverMono} aria-hidden>{initials.join("")}</span>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
            <Art name="vase" eager className={s.vaseArt} />
            <Art name="pampas" eager className={s.pampasArt} />
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf5ec" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        demoWishes={WISHES}
        light="#f6ece0"
        dark="#7a3218"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            <div className={s.heroNiche} aria-hidden>
              <span className={s.heroMono}>{initials[0]}{initials[1] && <><em>&amp;</em>{initials[1]}</>}</span>
            </div>
            <h1 className={s.heroNames}>{data.couple.bride}{groom && <> &amp; {groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <span className={s.arcadeWrap}><Art name="arcade" eager /></span>
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="emblem" />,
          amp: <Art name="emblem" />,
          portrait: <Art name="emblem" className={s.portraitArt} />,
          countDecor: <Art name="emblem" className={s.countDecor} />,
          closingDecor: <span className={s.closingArcade}><Art name="arcade" /></span>,
          closingEmblem: <Art name="emblem" className={s.closingEmblem} />,
          sentArt: <Art name="emblem" />,
        }}
      />
    </ThemeShell>
  );
}
