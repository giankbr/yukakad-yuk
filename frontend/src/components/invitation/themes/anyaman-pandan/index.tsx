"use client";
// Theme "Anyaman Pandan" — undangan Islami bernuansa kerajinan Nusantara: latar tikar anyaman pandan alami, pita anyaman
// berwarna (merah saga, hijau daun, hitam, kunyit) dengan tepi berjahit, tampah rotan bundar yang memuat nama, ikat daun
// pandan. Gouache orisinal; tanpa figur dan tanpa kaligrafi lukis (basmalah ditulis sebagai teks).
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Yeseva One", "Kurale", "Amiri:wght@400;700"];
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";
// Painted by /tmp/pen/art/themes/anyaman-pandan.py.
const Art = makeArt("anyaman-pandan", {
  tampah: [480, 480], pandan: [360, 235], divider: [360, 79],
} as const);

const WISHES = [
  { id: "w1", name: "Ustadzah Aminah & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Teman Bengkel Anyaman", attendance: "yes" as const, message: "Dari helai pandan sampai pelaminan! Selamat Salma dan Rizal, semoga rumah tangganya rapat dan kuat seperti anyaman terbaik." },
  { id: "w3", name: "Keluarga Bapak Asep", attendance: "maybe" as const, message: "Insyaallah kami hadir selepas zuhur. Doa terbaik untuk kedua mempelai dan keluarga." },
];

export default function AnyamanPandanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { couple } = data;
  const table = tableLabel(data.guestTable);
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const note = couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#d8bb80"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverBand} aria-hidden />
          <p className={s.bismillah} lang="ar" dir="rtl">{BISMILLAH}</p>
          <div className={s.tampah}>
            <Art name="tampah" eager className={s.tampahRing} />
            <div className={s.tampahText}>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}>{couple.bride}<i>&amp;</i>{couple.groom}</h1>
              <Art name="divider" eager className={s.coverDiv} />
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <Art name="pandan" eager className={s.coverPandan} />
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fffaee" />Buka Undangan</button>
          </div>
          <span className={s.coverBand} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f6d98a"
        dark="#2f6b4a"
        demoWishes={WISHES}
        copy={{
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Wr. Wb.",
            title: "Dengan Memohon Ridha Allah",
            sub: "Tikar telah digelar, kami menanti kehadiran Anda",
            intro: "Maha Suci Allah yang menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan ridha-Nya, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Kehadiran dan doa Bapak/Ibu/Saudara/i adalah kehormatan bagi kami.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua Helai, Satu Anyaman", "Kedua Mempelai"],
          count: ["Menghitung Hari", "Menuju Akad"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Helai demi Helai", "Kisah Kami"],
          gallery: ["Galeri", "Kenangan"],
          wishes: ["Doa & Restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: { thanks: "Jazakumullah Khairan", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas setiap kebaikan dengan pahala yang berlipat.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
          sent: "Jazakallah khairan, doa dan ucapan Anda sudah terkirim.",
          wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
        }}
        hero={(
          <header className={s.hero}>
            <span className={s.band} aria-hidden />
            <div className={s.heroCloth}>
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroNames}>{couple.bride} <i>&amp;</i> {couple.groom}</h1>
              <Art name="divider" className={s.divider} />
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
            <Art name="pandan" className={s.heroPandan} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          amp: <Art name="divider" />,
          portrait: <Art name="tampah" className={s.portraitRing} />,
          closingDecor: <Art name="pandan" className={s.closingPandan} />,
          closingEmblem: <Art name="divider" className={s.closingEmblem} />,
          sentArt: <Art name="divider" />,
        }}
      />
    </ThemeShell>
  );
}
