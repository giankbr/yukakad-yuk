"use client";
// Theme "Buton Wolio" — Benteng Keraton Buton dilukis gouache: tembok batu kapur bergerigi menyusuri punggung bukit,
// baluara dan lawa, istana Kamali/Malige yang tiap lantainya melebar ke atas, Selat Buton dan Pulau Muna di kejauhan.
// Tenun Buton (garis merah-kuning-hijau-hitam yang bersilang) ditenun sampai ke benang. Bahasa bentuk: tepi atas
// bergerigi seperti tembok benteng pada sampul, foto, potret, dan kartu acara.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Barlow:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/buton-wolio.py (tools/art/themes in the repo).
const Art = makeArt("buton-wolio", { keraton: [720, 551], wall: [400, 38], malige: [200, 269] } as const);

const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Pomae-maeka",
    sub: "Saling menghormati dan menjaga, nilai luhur Buton yang kami bawa ke dalam rumah tangga.",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dengan Izin Allah", "Kedua Mempelai"],
  count: ["Batu demi Batu", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Dari Kamali ke Wolio", "Perjalanan Kami"],
  gallery: ["Galeri", "Potret Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Semoga Allah membalas segala kebaikan.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
};

export default function ButonWolioTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#12324e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="keraton" eager className={s.coverScene} />
          <div className={s.coverPlaque}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.coverKicker}>Assalamu&apos;alaikum Wr. Wb.</p>
            <p className={s.coverLabel}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <Art name="wall" eager className={s.coverRule} />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#f2c21b" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f4eddc"
        dark="#12324e"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroPhotoWrap}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="malige" className={s.heroMalige} />
          </header>
        )}
        slots={{
          divider: <Art name="wall" className={s.divider} />,
          amp: <Art name="malige" />,
          closingEmblem: <Art name="malige" className={s.closingMalige} />,
          closingDecor: <Art name="keraton" className={s.closingKeraton} />,
          sentArt: <Art name="malige" />,
        }}
      />
    </ThemeShell>
  );
}
