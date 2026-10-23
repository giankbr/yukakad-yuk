"use client";
// Theme "Kenduri Panen" — undangan syukuran panen desa dalam cat air yang hangat: sawah menguning di bawah matahari pagi,
// bukit berkabut, nyiur dan rumah kampung, lumbung kayu bertiang, ikat padi berdiri di petak sawah. Tumpeng di atas
// tampah berlapis daun pisang menjadi lambang makan bersama (bukan sesaji). Penyelenggaranya panitia desa/kelompok tani,
// bukan pasangan. Sampul berupa panorama penuh dengan judul di langit. Lukisan: /tmp/pen/art/themes/kenduri-panen.py.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Libre Caslon Display", "Vollkorn:ital,wght@0,400;0,500;0,600;1,400", "Tangerine:wght@400;700"];
const Art = makeArt("kenduri-panen", {
  sheaf: [260, 220], tumpeng: [409, 266], lumbung: [252, 308], stalks: [780, 173], divider: [347, 47],
} as const);

export default function KenduriPanenTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Kenduri Panen";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const host = data.couple.bride;
  const cohost = data.couple.groom?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f8efd9"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.scene} aria-hidden />
          <div className={s.coverSky}>
            <p className={s.coverKicker}>Undangan</p>
            <h1 className={s.coverTitle}>{label}</h1>
            <p className={s.coverHost}>{host}{cohost && <><em>bersama</em>{cohost}</>}</p>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverCard}>
            <Art name="divider" eager className={s.coverRule} />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff6df" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#f3dc9c"
        dark="#4a3420"
        demoWishes={[
          { id: "w1", name: "Pak Kasno, Dusun Ngrejo", attendance: "yes", message: "Alhamdulillah, panen tahun ini berkah sekali. Kami sekeluarga insyaallah datang membawa urap dan rempeyek." },
          { id: "w2", name: "Ibu-ibu PKK RT 05", attendance: "yes", message: "Siap membantu dapur umum dari pagi. Semoga hasil bumi desa kita makin melimpah setiap musim." },
          { id: "w3", name: "Mas Arif, Karang Taruna", attendance: "maybe", message: "Masih ada tugas jaga di bendungan, kalau sempat menyusul sesudah dzuhur. Selamat untuk seluruh petani!" },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Assalamu'alaikum Wr. Wb. · Salam sejahtera",
            title: "Syukur atas Hasil Bumi",
            intro: `Puji syukur ke hadirat Allah Yang Maha Kuasa atas panen yang melimpah musim ini. Dengan segala kerendahan hati, kami mengundang Bapak/Ibu/Saudara/i warga desa untuk hadir dalam ${label}: berdoa bersama, menyisihkan sebagian hasil untuk lumbung desa, dan menikmati hidangan bersama.`,
          },
          roles: ["Penyelenggara", "Didukung oleh"],
          couple: ["Yang mengundang", "Panitia Kenduri"],
          count: ["Menghitung hari", "Menuju Hari Kenduri"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & tempat", "Susunan Kegiatan"],
          story: ["Dari tandur sampai panen", "Perjalanan Musim Ini"],
          gallery: ["Dokumentasi", "Suasana Desa"],
          wishes: ["Doa & kabar kehadiran", "Ucapan Warga"],
          gifts: ["Iuran & sumbangan", "Gotong Royong Kenduri"],
          closing: {
            thanks: "Terima Kasih",
            text: "Atas kehadiran, doa, dan uluran tangan Bapak/Ibu/Saudara/i. Semoga sawah kita selalu subur, lumbung selalu terisi, dan desa kita tetap guyub rukun.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Terima kasih, ucapan dan doa Anda sudah diterima panitia.",
          wishPlaceholder: "Tuliskan doa dan ucapan untuk panen desa…",
          closedNote: "Pendataan kehadiran sudah ditutup. Ucapan dan doa masih bisa dikirim lewat form ini.",
          giftIntro: "Bagi warga dan donatur yang berkenan menyumbang untuk konsumsi kenduri dan lumbung pangan desa, iuran dapat disalurkan melalui:",
          giftAddressTitle: "Titip Bahan Kenduri",
          familyLabel: null,
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroArch}>
              <span className={s.heroSun} aria-hidden />
              <Art name="lumbung" className={s.heroLumbung} />
            </div>
            <p className={s.heroKicker}>{formatDate(data.date)}</p>
            <h1 className={s.heroTitle}>{label}</h1>
            <p className={s.heroHost}>{host}{cohost && <><em>bersama</em>{cohost}</>}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="stalks" className={s.heroStalks} />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="sheaf" />,
          portrait: <Art name="sheaf" className={s.portraitSheaf} />,
          countDecor: <Art name="stalks" className={s.countStalks} />,
          closingDecor: <Art name="stalks" className={s.closeStalks} />,
          closingEmblem: <Art name="tumpeng" className={s.closeTumpeng} />,
          sentArt: <Art name="sheaf" />,
        }}
      />
    </ThemeShell>
  );
}
