"use client";
// Theme "Banda Neira" — adat Maluku (Kepulauan Banda), pasangan Muslim. Teluk biru dilihat dari beranda rumah perkenier:
// kerucut Gunung Api, kora-kora berpanji dan bukit Lonthor (cat air + gouache) di antara dua pilar Toskana putih kapur,
// lisplang bergerigi dan lantai tegel hitam-putih. Ranting pala dengan buah terbelah bersalut fuli merah, jendela dengan
// daun jendela krepyak hijau yang terbuka, rumah perkenier tua di penutup.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Libre Caslon Display", "Lora:ital,wght@0,400;0,600;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/banda-neira.py
const Art = makeArt("banda-neira", { view: [780, 700], column: [90, 1325], house: [640, 299], nutmeg: [320, 245], divider: [300, 40], kora: [360, 65] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const WISHES = [
  { id: "w1", name: "Bapak Hi. Ismail Lamandasa & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga rumah tangga kalian seharum pala Banda." },
  { id: "w2", name: "Regu Kora-kora Dwiwarna", attendance: "yes" as const, message: "Selamat, Hamzah dan Laila! Kali ini kalian menang bersama. Sampai jumpa di dermaga." },
  { id: "w3", name: "Teman kuliah di Ambon", attendance: "maybe" as const, message: "Insyaallah menyeberang kalau ombak bersahabat. Doa terbaik kami dari Ambon untuk kalian berdua." },
];

export default function BandaNeiraTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6f2e8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.valance} aria-hidden />
          <Art name="column" eager className={s.colL} />
          <Art name="column" eager className={s.colR} />
          <div className={s.coverTop}>
            <p className={s.bism} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.kicker}>Undangan {data.eventLabel ?? "Pernikahan"}</p>
            <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.bay} aria-hidden>
            <Art name="view" eager />
            <Art name="nutmeg" eager className={s.coverNut} />
          </div>
          <div className={s.floor}>
            <div className={s.card}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#fcfaf4" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3d9a4"
        dark="#173b5c"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Rahmat Allah",
            intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dari dua rumah di tepi teluk", "Kedua Mempelai"],
          count: ["Menanti di dermaga", "Menghitung Hari"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & tempat", "Rangkaian Acara"],
          story: ["Jejak di pulau pala", "Kisah Kami"],
          gallery: ["Galeri", "Momen Bersama"],
          wishes: ["Doa restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: {
            thanks: "Terima Kasih",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Insyaallah kami menikah</p>
            <div className={s.heroWin}>
              <span className={`${s.shutter} ${s.shutterL}`} aria-hidden />
              <div className={s.heroPhoto}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
              <span className={`${s.shutter} ${s.shutterR}`} aria-hidden />
            </div>
            <span className={s.sill} aria-hidden />
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="house" className={s.heroHouse} />
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="divider" /></span>,
          node: <Art name="nutmeg" />,
          amp: <Art name="divider" />,
          portrait: <Art name="nutmeg" className={s.portraitNut} />,
          countDecor: <Art name="kora" className={s.countKora} />,
          closingEmblem: <Art name="house" className={s.closingHouse} />,
          sentArt: <Art name="nutmeg" />,
        }}
      />
    </ThemeShell>
  );
}
