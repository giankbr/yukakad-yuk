"use client";
// Theme "Minang Suntiang" — baralek Minang dengan suntiang sebagai mahkota undangan. Sampul beludru merah berpita
// songket balapak: suntiang emas bertingkat (bunga emas bertangkai pegas, laca, kote-kote) dilukis sebagai prada,
// bergetar halus seperti bunga goyang dan disapu kilau emas, tepat di atas nama anak daro dan marapulai. Hero: suntiang
// yang sama bertengger di atas foto bundar. Potret medali emas dengan bungo, kartu acara berpita songket, hitung mundur
// medali di atas beludru, penutup kembali ke suntiang.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rozha One", "Lora:ital,wght@0,400;0,600;0,700;1,400;1,600", "Imperial Script", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/minang-suntiang.py (tools/art/themes in the repo).
const Art = makeArt("minang-suntiang", { suntiang: [700, 461], spray: [300, 40], bungo: [120, 120] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Baralek Gadang",
    sub: "Adat basandi syarak, syarak basandi Kitabullah",
    intro: "Dengan mengharap rahmat dan ridha Allah SWT, kami sekeluarga mengundang Bapak/Ibu/Dunsanak untuk hadir dan memberikan doa restu pada baralek pernikahan putra-putri kami.",
  },
  roles: ["Anak Daro", "Marapulai"],
  couple: ["Anak daro & marapulai", "Kedua Mempelai"],
  count: ["Manjalang hari baralek", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Wakatu jo tampek", "Rangkaian Acara"],
  story: ["Kaba kami", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri Foto"],
  wishes: ["Doa jo ucapan", "Ucapan & Kehadiran"],
  gifts: ["Tando kasih", "Amplop Digital"],
  closing: {
    thanks: "Tarimo Kasih",
    text: "Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Dunsanak berkenan hadir dan memberikan doa restu.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Tarimo kasih, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa untuk anak daro dan marapulai…",
};

const WISHES = [
  { id: "w1", name: "Mak Etek Ros & keluarga", attendance: "yes" as Attendance, message: "Salamaik baralek, Zahra jo Rizal! Samoga manjadi keluarga nan sakinah, mawaddah, warahmah. Mak Etek pasti datang." },
  { id: "w2", name: "Rekan Apoteker Padang", attendance: "yes" as Attendance, message: "Barakallahu lakuma. Ikut bahagia, semoga lancar sampai makan bajamba!" },
  { id: "w3", name: "Uda Fikri (Pekanbaru)", attendance: "no" as Attendance, message: "Maaf alun bisa pulang kampuang. Doa terbaik dari rantau untuk kalian berdua." },
];

export default function MinangSuntiangTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#7a0c14"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverKicker}>Baralek Gadang &middot; {data.eventLabel ?? "Pernikahan"}</p>
          <div className={s.crown} aria-hidden>
            <Art name="suntiang" eager />
            <span className={s.glint} />
          </div>
          <h1 className={s.coverNames}>{data.couple.bride}<span>&amp;</span>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestBox}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Dunsanak</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#4e070c" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0d27e"
        dark="#4e070c"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <span className={s.songket} aria-hidden />
            <p className={s.heroKicker}>Walimatul &lsquo;Ursy</p>
            <div className={photo ? s.heroCrown : `${s.heroCrown} ${s.heroNoPhoto}`}><Art name="suntiang" /></div>
            {photo && <div className={s.heroPhoto}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
            <h1 className={s.heroNames}>{data.couple.bride} <i>&amp;</i> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="spray" className={s.divider} />,
          node: <Art name="bungo" />,
          amp: <Art name="bungo" />,
          portrait: <span className={s.portraitBungo} aria-hidden><Art name="bungo" /></span>,
          closingEmblem: <Art name="suntiang" className={s.closingEmblem} />,
          sentArt: <Art name="bungo" />,
        }}
      />
    </ThemeShell>
  );
}
