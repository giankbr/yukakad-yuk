"use client";
// Theme "Kertas Quilling" — seni gulungan kertas di atas kartu katun: karangan bunga dari pita kertas yang berdiri
// (gulungan longgar, tetes, mata, daun bergaris, bunga rumbai, gulungan terbuka) dengan bayangan lembut, monogram bergaris
// pita di tengah karangan, dan sampul kotak bayangan.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "Lora:ital,wght@0,400;0,500;1,400", "Parisienne"];
// Painted by /tmp/pen/art/themes/kertas-quilling.py (tools/art/themes in the repo).
const Art = makeArt("kertas-quilling", { wreath: [640, 640], corner: [420, 399], divider: [420, 60], bloom: [200, 194] } as const);

const WISHES = [
  { id: "w1", name: "Ibu Lestari & Keluarga", attendance: "yes" as Attendance, message: "Selamat Tiara dan Yosua. Semoga rumah tangga kalian rapi dan indah seperti karya-karya kalian, kuat di setiap lilitannya." },
  { id: "w2", name: "Komunitas Quilling Semarang", attendance: "yes" as Attendance, message: "Dari satu kelas Minggu jadi satu keluarga! Kami datang dan siap membuat bunga kertas bersama." },
  { id: "w3", name: "Kevin & Grace", attendance: "maybe" as Attendance, message: "Bahagia sekali untuk kalian. Kami usahakan hadir, doa terbaik dari Surabaya." },
];

export default function KertasQuillingTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const a = data.couple.bride.trim().slice(0, 1).toUpperCase();
  const b = (data.couple.groom ?? "").trim().slice(0, 1).toUpperCase();
  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Dengan Sukacita",
      title: "Kabar Bahagia",
      intro: "Atas kasih dan berkat Tuhan Yang Maha Esa, kami bermaksud melangsungkan pernikahan. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
    },
    roles: ["Mempelai Wanita", "Mempelai Pria"],
    couple: ["Dua Hati", "Kedua Mempelai"],
    count: ["Menghitung Hari", "Menuju Hari Bahagia"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Simpan Tanggalnya", "Rangkaian Acara"],
    story: ["Lilitan Demi Lilitan", "Kisah Kami"],
    gallery: ["Galeri", "Momen Kami"],
    wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
    gifts: ["Tanda Kasih", "Hadiah Pernikahan"],
    closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i akan melengkapi kebahagiaan kami, seperti lilitan terakhir yang menyempurnakan sebuah bunga." },
    sent: "Terima kasih, ucapan Anda sudah kami terima dengan sukacita.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
    giftIntro: "Doa restu Anda adalah hadiah terindah. Bila berkenan mengirim tanda kasih, dapat melalui:",
    familyLabel: "Kami yang berbahagia",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9e1d6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.box}>
            <Art name="corner" eager className={s.cornerTL} />
            <Art name="corner" eager className={s.cornerBR} />
            <p className={s.kicker}>Undangan {label}</p>
            <div className={s.wreathWrap}>
              <Art name="wreath" eager className={s.wreath} />
              <p className={s.mono} aria-hidden>{a}{b && <><i>&amp;</i>{b}</>}</p>
            </div>
            <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={copy}
        demoWishes={WISHES}
        light="#fbeedd"
        dark="#3d3532"
        hero={(
          <header className={s.hero}>
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
              <Art name="corner" className={s.heroSpray} />
            </div>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="divider" className={s.heroDiv} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="bloom" />,
          portrait: <Art name="bloom" />,
          countDecor: <><Art name="corner" className={s.countCorner} /><Art name="corner" className={s.countCorner} /></>,
          closingDecor: <><Art name="corner" className={s.closingCorner} /><Art name="corner" className={s.closingCorner} /></>,
          closingEmblem: <Art name="bloom" className={s.closingBloom} />,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
