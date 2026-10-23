"use client";
// Theme "Jali Merah" — bangunan batu pasir merah ala Fatehpur Sikri: layar jali berlubang bintang di bawah lengkung
// bergerigi, cahaya keemasan yang menembus kisi-kisi dan jatuh berpola di lantai, kubah chhatri, pita tatahan marmer
// krem, dan bingkai lengkung batu untuk foto. Pembuka Islami (basmalah + salam), tanpa makhluk bernyawa, tanpa kaligrafi.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rozha One", "Spectral:ital,wght@0,400;0,500;0,600;0,700;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/jali-merah.py (stone and inlay band are CSS backgrounds).
const Art = makeArt("jali-merah", { jali: [420, 600], light: [420, 760], frame: [390, 525], chhatri: [200, 241], divider: [215, 46] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum",
    title: "Warahmatullahi Wabarakatuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Insan, Satu Cahaya", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Bingkai Kenangan"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan cahaya dan keberkahan.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Yusuf Alatas", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Selamat Zahra dan Faiz." },
  { id: "w2", name: "Teman Studio Arsitektur '18", attendance: "yes" as const, message: "Dari tugas fasad sampai ke pelaminan! Semoga rumah tangganya kokoh seperti batu dan terang seperti cahaya di balik jali." },
  { id: "w3", name: "Ustazah Mariam", attendance: "maybe" as const, message: "Insyaallah hadir bila tidak ada halangan. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
];

export default function JaliMerahTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#5a2214"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.coverKicker}>{label}</p>
          <div className={s.jaliWrap} aria-hidden>
            <Art name="chhatri" eager className={`${s.chhatri} ${s.chhatriL}`} />
            <Art name="jali" eager className={s.jali} />
            <Art name="chhatri" eager className={`${s.chhatri} ${s.chhatriR}`} />
          </div>
          <Art name="light" eager className={s.coverLight} />
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#7d321f" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#f3d9a0"
        dark="#7d321f"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="chhatri" className={s.heroChhatri} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.heroArch}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <Art name="frame" className={s.heroArchFrame} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="chhatri" />,
          amp: <Art name="divider" />,
          portrait: <Art name="frame" className={s.portraitArch} />,
          countDecor: <><Art name="light" className={s.countLight} /><Art name="chhatri" className={`${s.countChhatri} ${s.countChhatriL}`} /><Art name="chhatri" className={`${s.countChhatri} ${s.countChhatriR}`} /></>,
          closingDecor: <Art name="light" className={s.closingLight} />,
          closingEmblem: <Art name="chhatri" className={s.closingChhatri} />,
          sentArt: <Art name="chhatri" />,
        }}
      />
    </ThemeShell>
  );
}
