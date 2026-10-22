"use client";
// Theme "Kebun Teh" — pernikahan di kebun teh Puncak dalam cat air pagi yang segar: barisan perdu teh berundak, jalan
// setapak pemetik bercaping, pohon pelindung, pondok kayu bertiang, gunung kembar dan kabut tipis yang bergerak.
// Foto dalam bingkai berbentuk daun, pucuk teh sebagai ornamen, keranjang bambu pemetik. Ilustrasi asli.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Petrona:ital,wght@0,400;0,500;0,600;1,400;1,500", "Work Sans:wght@400;500;600", "Ephesis"];
// Painted by /tmp/pen/art/themes/kebun-teh.py (tools/art/themes in the repo).
const Art = makeArt("kebun-teh", { scene: [660, 578], band: [640, 190], sprig: [150, 166], basket: [170, 199], mist: [560, 124] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Ujang Suryana", attendance: "yes" as const, message: "Wilujeng nikah, Nisa sareng Fikri. Mugia janten kulawarga nu sakinah, mawaddah, warahmah. Insyaallah kami hadir." },
  { id: "w2", name: "Rekan Agronomi 51", attendance: "yes" as const, message: "Dari praktik lapang ke pelaminan! Barakallahu lakuma, semoga rumah tangga kalian selalu sejuk seperti pagi di Gunung Mas." },
  { id: "w3", name: "Teh Rina & Kang Dedi", attendance: "maybe" as const, message: "Hapunten, belum tentu bisa naik ke Puncak. Doa terbaik untuk kalian berdua, semoga lancar sampai hari H." },
];

function Divider() {
  return <span className={s.divider} aria-hidden><i /><Art name="sprig" /><i /></span>;
}

export default function KebunTehTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const { bride, groom } = data.couple;
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
      kicker: "Sampurasun",
      title: "Pucuk yang Dinanti",
      sub: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
      intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
    },
    roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
    couple: ["Dua Hati", "Kedua Mempelai"] as [string, string],
    count: ["Kabut Pagi Menanti", "Menuju Hari Bahagia"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
    story: ["Jalan Setapak", "Kisah Kami"] as [string, string],
    gallery: ["Galeri", "Pagi di Kebun"] as [string, string],
    wishes: ["Doa & Restu", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
    closing: { thanks: "Hatur Nuhun", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan yang tak ternilai bagi kami sekeluarga.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
    sent: "Hatur nuhun, doa dan ucapan Anda sudah kami terima.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f7f3e8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.scene} aria-hidden>
            <Art name="scene" eager className={s.sceneImg} />
            <Art name="mist" eager className={s.sceneMist} />
          </div>
          <div className={s.coverHead}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{bride}<em>&amp;</em>{groom}</h1>
          </div>
          <div className={s.photoWrap}>
            <div className={s.coverPhoto}><Photo src={hero} alt="" /></div>
            <Art name="sprig" eager className={s.coverSprig} />
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffdf6" />Buka Undangan</button>
          <Art name="band" eager className={s.coverRows} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f2e6c4"
        dark="#26392b"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroScene} aria-hidden><Art name="scene" /></div>
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt={`${bride} & ${groom}`} /></div>}
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{bride} &amp; {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="sprig" />,
          amp: <Art name="sprig" />,
          portrait: <Art name="sprig" className={s.peek} />,
          countDecor: <><Art name="mist" className={s.countMist} /><Art name="band" className={s.countRows} /></>,
          closingDecor: <Art name="band" className={s.closingScene} />,
          closingEmblem: <Art name="basket" className={s.closingEmblem} />,
          sentArt: <Art name="basket" />,
        }}
      />
    </ThemeShell>
  );
}
