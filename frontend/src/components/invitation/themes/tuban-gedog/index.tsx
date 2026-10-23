"use client";
// Theme "Tuban Gedog" — adat Jawa pesisir, Tuban: kain tenun gedog dari kapas pintal tangan (putih alam yang kasar dan
// biru indigo) dengan batik gedog bermotif ganggeng, kijing miring dan burung, jahitan jelujur, serta laut utara Jawa
// dengan perahu nelayan Palang. Motif dilukis ulang dengan tekstur benang, bukan salinan kain tertentu.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Instrument Serif:ital@0;1", "Vollkorn:ital,wght@0,400;0,600;1,400", "Amiri"];
// Painted by /tmp/pen/art/themes/tuban-gedog.py.
const Art = makeArt("tuban-gedog", { laut: [720, 530], perahu: [360, 233], motif: [240, 244], divider: [332, 38] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Urs",
    sub: "Ditenun dengan doa, helai demi helai",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Helai Benang", "Kedua Mempelai"],
  count: ["Menuju Hari Bahagia", "Hitung Hari"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Lungsin & Pakan", "Kisah Kami"],
  gallery: ["Galeri", "Potret Kami"],
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
  { id: "w1", name: "Keluarga H. Mashuri, Merakurak", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Mbak Siti & Penenun Kedungrejo", attendance: "yes" as const, message: "Ikut bungah, Nduk Laila. Semoga rumah tangganya rapat seperti tenunan gedog, makin lama makin lembut." },
  { id: "w3", name: "Arif & Teman TPI Palang", attendance: "maybe" as const, message: "Selamat ya Dhil! Insyaallah kami menyusul selepas melaut. Semoga lancar sampai hari H." },
];

export default function TubanGedogTheme(props: ThemeProps) {
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
      background="#e7dcc3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverSea}>
            <Art name="laut" eager className={s.coverSeaImg} />
            <Art name="perahu" eager className={s.coverBoat} />
          </div>
          <div className={s.coverCloth}>
            <span className={s.selvedge} aria-hidden />
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <span className={s.coverRule} aria-hidden />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f3ecdb" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#f3ecdb"
        dark="#22395c"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Pawiwahan · Tuban</p>
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
          node: <Art name="motif" />,
          portrait: <Art name="motif" className={s.portraitArt} />,
          countDecor: <Art name="motif" className={s.countDecor} />,
          closingDecor: <Art name="laut" className={s.closingSea} />,
          closingEmblem: <Art name="motif" className={s.closingEmblem} />,
          sentArt: <Art name="motif" />,
        }}
      />
    </ThemeShell>
  );
}
