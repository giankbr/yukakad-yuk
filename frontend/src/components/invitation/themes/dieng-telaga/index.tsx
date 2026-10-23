"use client";
// Theme "Dieng Telaga" — pernikahan adat Jawa (Muslim) di dataran tinggi Dieng, Wonosobo: lukisan cat air Telaga Warna
// yang hijau toska di bawah kabut tebal, uap kawah yang naik pelan, Sindoro di kejauhan, dan kebun kentang-kubis berteras.
// Nama mempelai melayang di tengah kabut, kartu tamu bertepi undakan teras, foto pembuka berbentuk telaga (oval), potret
// dipotong bertingkat seperti teras ladang, hitung mundur berupa riak telaga, dan buah carica sebagai penanda.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Forum", "Literata:ital,wght@0,400;0,600;0,700;1,400", "Tangerine:wght@400;700", "Amiri"];
// Painted by /tmp/pen/art/themes/dieng-telaga.py (tools/art/themes in the repo).
const Art = makeArt("dieng-telaga", { carica: [360, 74], fruit: [81, 230] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Sugeng Rawuh",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan pahargyan pernikahan putra-putri kami di Dieng Wetan. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Putri", "Mempelai Kakung"],
  couple: ["Sigaraning Nyawa", "Kedua Mempelai"],
  count: ["Ngetung Dina", "Menuju Hari Bahagia"],
  units: ["Dina", "Jam", "Menit", "Detik"],
  events: ["Rerangkening Adicara", "Waktu & Tempat"],
  story: ["Lelampahan", "Kisah di Lereng Dieng"],
  gallery: ["Galeri", "Kenangan di Dataran Tinggi"],
  wishes: ["Pandonga & Rawuh", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Katresnan", "Amplop Digital"],
  closing: { thanks: "Matur Nuwun", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan yang tak ternilai bagi kami sekeluarga.", salam: "Wassalamu'alaikum Wr. Wb." },
  sent: "Matur nuwun, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  closedNote: "Matur nuwun atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
};

const WISHES = [
  { id: "w1", name: "Bapak Kusnadi & Keluarga", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga rumah tangga kalian sejuk seperti udara Dieng dan jernih seperti Telaga Warna." },
  { id: "w2", name: "Mas Joko, Kelompok Tani Sumber Rejeki", attendance: "yes" as Attendance, message: "Selamat, Fajar! Insyaallah kami datang setelah panen. Semoga sakinah, mawaddah, warahmah." },
  { id: "w3", name: "Bu Ratna, Dosen Agronomi", attendance: "maybe" as Attendance, message: "Ikut bahagia, Nadia. Semoga bisa naik ke Dieng hari itu, doa terbaik dari kami di kampus." },
];

export default function DiengTelagaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#173f3e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.steam} aria-hidden />
          <span className={s.steam} aria-hidden />
          <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
          <p className={s.salam}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.coverMain}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.card}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#2a1a08" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f7dca4"
        dark="#173f3e"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.lakeWrap}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /> : <span aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <span className={s.steam} aria-hidden />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
            <span className={s.heroFields} aria-hidden />
          </header>
        )}
        slots={{
          divider: <Art name="carica" className={s.divider} />,
          node: <Art name="fruit" />,
          amp: <Art name="fruit" />,
          portrait: <Art name="fruit" className={s.portraitArt} />,
          countDecor: <><span className={s.steam} aria-hidden /><span className={s.steam} aria-hidden /></>,
          closingDecor: <span className={s.steam} aria-hidden />,
          closingEmblem: <Art name="fruit" className={s.closingEmblem} />,
          sentArt: <Art name="fruit" />,
        }}
      />
    </ThemeShell>
  );
}
