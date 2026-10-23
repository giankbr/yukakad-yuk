"use client";
// Theme "Batik Betawi" — selembar kain batik pesisir Betawi: badan kain merah bermotif kembang kelapa dan ondel-ondel
// kecil (sebagai motif batik), kepala kain krem diapit tumpal hijau-kuning, medali kembang kelapa yang berputar pelan,
// dan panel nusa kelapa (nyiur, perahu layar, ombak) yang bergeser seperti pasang. Dilukis sebagai batik tulis:
// garis malam krem, warna celup, dan retakan halus.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rozha One", "Alegreya:ital,wght@0,400;0,500;0,700;1,400", "Alegreya Sans:wght@500;700;800", "Amiri"];
// Painted by /tmp/pen/art/themes/batik-betawi.py (kain, tumpal and nusa are CSS backgrounds).
const Art = makeArt("batik-betawi", { kembang: [320, 320], divider: [300, 57] } as const);

const WISHES = [
  { id: "w1", name: "Mpok Rohmah & Keluarga", attendance: "yes" as const, message: "Selamat ye Nurul & Fadli! Semoga jadi keluarga sakinah, mawaddah, warahmah. Rukun terus kayak gambang ama kromong." },
  { id: "w2", name: "Bang Jaenudin", attendance: "yes" as const, message: "Barakallahu lakuma. Siap jadi rombongan palang pintu, pantunnya udah dilatih dari kemarin!" },
  { id: "w3", name: "Keluarga Haji Usman, Depok", attendance: "maybe" as const, message: "Mohon maaf kalau belum bisa hadir. Doa terbaik dari kami sekeluarga, semoga lancar sampai hari H." },
];

export default function BatikBetawiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#b51f27"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.kepala}>
            <Art name="kembang" eager className={s.coverKembang} />
            <p className={s.kicker}>Undangan {label}</p>
            <p className={s.salam}>Assalamu&apos;alaikum Wr. Wb.</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff4dc" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fff4dc"
        dark="#2b1712"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم",
            kicker: "Assalamu'alaikum Wr. Wb.",
            title: "Nyok, Kite Bersilaturahmi",
            intro: "Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Penganten Perempuan", "Penganten Laki-laki"],
          couple: ["Penganten", "Kedua Mempelai"],
          count: ["Ngitung Hari", "Menuju Hari Bahagia"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Acara Kawinan", "Waktu & Tempat"],
          story: ["Cerite Kite", "Perjalanan Kami"],
          gallery: ["Potret", "Galeri Bahagia"],
          wishes: ["Doa & Ucapan", "Kirim Doa Restu"],
          gifts: ["Tande Kasih", "Amplop Digital"],
          closing: {
            thanks: "Terime Kasih",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan yang tak ternilai bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Wr. Wb.",
          },
          sent: "Makasih banyak, doa dan ucapan sudah terkirim.",
          giftIntro: "Doa restu Anda adalah kado terindah bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
        }}
        hero={(
          <header className={s.hero}>
            <span className={s.nusa} aria-hidden />
            {hero && <div className={s.heroFrame}><div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div></div>}
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="kembang" />,
          portrait: <Art name="kembang" className={s.portraitArt} />,
          closingEmblem: <Art name="kembang" className={s.closingEmblem} />,
          sentArt: <Art name="kembang" />,
        }}
      />
    </ThemeShell>
  );
}
