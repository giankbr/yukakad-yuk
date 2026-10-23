"use client";
// Theme "Baju Bodo" — adat Makassar/Bugis. Baju bodo jingga yang tembus pandang (cat air berlipat halus) tergantung di
// tongkat kayu di atas lipatan sarung lipa' sabbe, sehingga kotak-kotak sutranya terlihat menembus kain. Kalung emas,
// pantai Losari saat senja di pembuka dan penutup, potret berbingkai kain sabbe. Bodoni Moda + Jost.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600", "Jost:wght@400;500", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/baju-bodo.py (sabbe and losari are CSS backgrounds)
const Art = makeArt("baju-bodo", { bodo: [640, 333], hijau: [420, 234], kalung: [420, 164], kembang: [120, 120] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const WISHES = [
  { id: "w1", name: "Keluarga Daeng Tutu", attendance: "yes" as const, message: "Tabe', selamat menempuh hidup baru Ayu dan Fikri. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah, dan dilimpahkan rezeki yang berkah." },
  { id: "w2", name: "dr. Nadia & teman koas", attendance: "yes" as const, message: "Akhirnya! Dari lorong Wahidin sampai pelaminan. Barakallahu lakuma, kami datang pakai baju bodo semua." },
  { id: "w3", name: "Om Syamsul di Parepare", attendance: "maybe" as const, message: "Insyaallah menyusul ke Makassar. Doa terbaik dari kami sekeluarga, semoga langgeng sampai tua." },
];

export default function BajuBodoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const hero = data.gallery[0] ?? data.couple.bridePhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f7eee2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.bism} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.tabe}>Tabe&apos;</p>
          <p className={s.coverKicker}>Undangan {label}</p>
          <div className={s.display} aria-hidden>
            <span className={s.sarong} />
            <Art name="bodo" eager className={s.bodo} />
            <Art name="kalung" eager className={s.kalung} />
          </div>
          <h1 className={s.coverNames}>{bride}{groom && <><i>&amp;</i>{groom}</>}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestBox}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f6dfa6" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6dfa6"
        dark="#12383d"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Tabe', Salama' Ki'",
            sub: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala",
            intro: "Kami bermaksud menyelenggarakan akad dan resepsi pernikahan putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua keluarga, satu ikatan", "Kedua Mempelai"],
          count: ["Menuju hari bahagia", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & tempat", "Rangkaian Acara"],
          story: ["Perjalanan kami", "Kisah Kami"],
          gallery: ["Galeri", "Momen Bersama"],
          wishes: ["Doa restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: {
            thanks: "Terima Kasih",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah kehormatan yang tak ternilai bagi kami dan keluarga besar.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroSea} aria-hidden />
            {hero && <div className={s.heroPhoto}><Photo src={hero} alt={`${bride} dan ${groom}`} /></div>}
            {hero && <Art name="kalung" className={s.heroKalung} />}
            <p className={s.heroKicker}>Pernikahan Adat Makassar</p>
            <h1 className={s.heroNames}>{bride}{groom && <><i>&amp;</i>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="kembang" /></span>,
          node: <Art name="kembang" />,
          amp: <Art name="kembang" />,
          portrait: <Art name="kalung" className={s.peek} />,
          closingDecor: <div className={s.closingSea} aria-hidden />,
          closingEmblem: <Art name="hijau" className={s.closingBodo} />,
          sentArt: <Art name="kalung" />,
        }}
      />
    </ThemeShell>
  );
}
