"use client";
// Theme "Tenun Troso" — adat Jawa pesisir, Jepara: tenun ikat pakan dari Desa Troso. Corak wajik merah bata, kunyit,
// nila dan putih alam dengan pendar khas ikat (benang pakan yang bergeser saat ditenun), alat tenun bukan mesin dari
// kayu jati dengan benang lungsin, dan sawah Jepara berlatar Gunung Muria dengan kain dijemur. Semua dilukis ulang.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Kurale", "Castoro:ital@0;1", "Amiri"];
// Painted by /tmp/pen/art/themes/tenun-troso.py (ikat, band and fringe are CSS backgrounds).
const Art = makeArt("tenun-troso", { loom: [640, 539], desa: [720, 473], motif: [220, 221], divider: [334, 41] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    sub: "Dua helai benang, satu lembar kain",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Lungsin & Pakan", "Kedua Mempelai"],
  count: ["Menuju Hari Bahagia", "Hitung Hari"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Corak Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Lembar Kenangan"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Matur Suwun",
    text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu. Atas kehadiran dan doanya, kami ucapkan terima kasih.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Matur suwun, doa dan ucapan Anda sudah kami terima. Jazakumullahu khairan.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah bagi kami. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Masrukhan, Pecangaan", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Mbak Umi & Penenun Troso", attendance: "yes" as const, message: "Ikut bungah, Ainun. Semoga rumah tangganya rapat dan awet seperti tenunan ikat yang ditenun pelan-pelan." },
  { id: "w3", name: "Teman Kerja Rizal, Tahunan", attendance: "maybe" as const, message: "Selamat Zal! Insyaallah kami menyusul di ngunduh mantu. Lancar terus sampai hari H." },
];

export default function TenunTrosoTheme(props: ThemeProps) {
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
      background="#f1e6cf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverBand} aria-hidden />
          <div className={s.coverText}>
            <p className={s.kicker}>Undangan {label} · Jepara</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf5e8" />Buka Undangan</button>
          </div>
          <div className={s.coverLoomWrap} aria-hidden><Art name="loom" eager className={s.coverLoom} /></div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#f4d79a"
        dark="#93291f"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="desa" className={s.heroScene} />
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} dan ${groom ?? ""}`.trim()} /> : <span className={s.heroMono} aria-hidden>{initials}</span>}</div>
            </div>
            <p className={s.heroKicker}>Pawiwahan · Troso, Jepara</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="motif" />,
          amp: <Art name="motif" />,
          portrait: <Art name="motif" className={s.portraitArt} />,
          closingEmblem: <Art name="motif" className={s.closingEmblem} />,
          sentArt: <Art name="motif" />,
        }}
      />
    </ThemeShell>
  );
}
