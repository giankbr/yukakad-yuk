"use client";
// Theme "Biru Syari" — undangan syar'i modern tanpa foto dalam biru berdebu dan putih. Kertas bergaris cat air menjadi
// latar; di tengah sampul berdiri jendela putih berpuncak lengkung dengan roset bintang delapan di puncaknya, sulur bunga
// kecil biru merambat dari kedua sisinya. Nama ditulis kapital renggang (Tenor Sans) dengan satu sentuhan aksara latin
// sambung, kartu acara berbentuk jendela lengkung, dan monogram dalam cincin di atas roset yang berputar pelan.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Tenor Sans:wght@400", "Nunito Sans:ital,wght@0,400;0,600;0,700;1,400", "Ephesis:wght@400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/biru-syari.py (stripes.webp is a CSS background tile)
const Art = makeArt("biru-syari", { climb: [361, 819], rosette: [240, 240], spray: [360, 59] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const WISHES = [
  { id: "w1", name: "Ibu Hj. Nenden & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Teh Rina, Kajian Pekanan", attendance: "yes" as const, message: "MasyaAllah, ikut bahagia, Syifa. Semoga Allah mudahkan setiap langkah kalian berdua dalam ketaatan." },
  { id: "w3", name: "Keluarga Ustaz Hamdan", attendance: "maybe" as const, message: "Insyaallah kami hadir bila tidak ada uzur. Doa terbaik untuk Fadhil dan Syifa." },
];

export default function BiruSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6ecf2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.windowWrap}>
            <Art name="rosette" eager className={s.coverRosette} />
            <div className={s.window}>
              <span className={s.windowLine} aria-hidden />
              <p className={s.bism} lang="ar" dir="rtl">{BISMILLAH}</p>
              <p className={s.salamCover}>Assalamu&apos;alaikum Wr. Wb.</p>
              <p className={s.coverKicker}>{label}</p>
              <h1 className={s.coverNames}><span>{bride}</span>{groom && <><i>&amp;</i><span>{groom}</span></>}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
              <span className={s.guestRule} aria-hidden />
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#ffffff" />Buka Undangan</button>
            </div>
            <Art name="climb" eager className={`${s.climb} ${s.climbL}`} />
            <Art name="climb" eager className={`${s.climb} ${s.climbR}`} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#ffffff"
        dark="#33496a"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Rahmat Allah",
            intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dipertemukan karena-Nya", "Kedua Mempelai"],
          count: ["Menuju hari yang diberkahi", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & tempat", "Rangkaian Acara"],
          story: ["Perjalanan kami", "Kisah Ta'aruf"],
          gallery: ["Galeri", "Momen Bersama"],
          wishes: ["Doa restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullahu Khairan",
            text: "Kehadiran dan doa Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah terkirim.",
          wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="climb" className={`${s.heroSpray} ${s.heroSprayL}`} />
            <Art name="climb" className={`${s.heroSpray} ${s.heroSprayR}`} />
            <div className={s.heroArch} aria-hidden><Art name="rosette" /></div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{bride}{groom && <><i>&amp;</i>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="spray" className={s.divider} />,
          node: <Art name="rosette" />,
          amp: <Art name="spray" />,
          portrait: <Art name="rosette" className={s.portraitArt} />,
          closingDecor: <><Art name="climb" className={s.closingClimb} /><Art name="climb" className={s.closingClimb} /></>,
          closingEmblem: <Art name="rosette" className={s.closingRosette} />,
          sentArt: <Art name="spray" />,
        }}
      />
    </ThemeShell>
  );
}
