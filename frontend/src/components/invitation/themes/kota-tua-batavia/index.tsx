"use client";
// Theme "Kota Tua Batavia" — a vintage picture postcard: pen-and-wash watercolour of an (original) colonial town-hall
// square in warm late-afternoon light with onthel bicycles and a cast-iron lamp post; the cover pairs the postcard
// front with its address side (perangko, cap pos, handwritten guest name). Album-corner photo prints, cancelled
// postcard event cards, ticket-stub countdown, airmail-envelope gifts. Betawi Muslim couple (Assalamu'alaikum).
import { Lucide, Photo, ThemeShell, dateParts, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Libre Caslon Display", "Libre Caslon Text:ital,wght@0,400;0,700;1,400", "Courier Prime:wght@400;700", "Homemade Apple"];
// Painted by /tmp/pen/art/themes/kota-tua-batavia.py (tools/art/themes in the repo).
const Art = makeArt("kota-tua-batavia", { bike: [240, 131], lamp: [90, 401], stamp: [130, 156], postmark: [240, 102], waves: [200, 32] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Dengan Memohon Rahmat Allah",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Pengirim Kartu Pos", "Kedua Mempelai"] as [string, string],
  count: ["Sampai Bertemu di Alun-alun", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Surat-surat Kami", "Kisah Cinta"] as [string, string],
  gallery: ["Album Lama", "Galeri"] as [string, string],
  wishes: ["Kirim Kabar", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Pos Udara", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Sampai jumpa di bawah lampu-lampu Kota Tua.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Terima kasih, kabar dan doa Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Ridwan Saleh", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga menjadi keluarga sakinah, mawaddah, warahmah." },
  { id: "w2", name: "Bang Jali & Mpok Ita", attendance: "yes" as const, message: "Selamat ye Amira sama Fikri! Kite dateng bawa rombongan onthel dari Condet." },
  { id: "w3", name: "Teman Pemandu Sejarah", attendance: "maybe" as const, message: "Insyaallah menyusul selepas tur sore. Doa terbaik untuk kalian berdua." },
];

export default function KotaTuaBataviaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const d = dateParts(data.date);
  const city = data.address?.split(",").pop()?.trim() || "Batavia";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e2d3b4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.postFront} aria-hidden>
            <div className={s.postScene}><span /></div>
            <p className={s.postHello}>Salam dari Kota Tua</p>
            <p className={s.postCaption}><span>Alun-alun Kota Tua</span><span>No. {d.year || "—"}</span></p>
          </div>
          <div className={s.postBack}>
            <Art name="postmark" className={s.postMark} eager />
            {d.day && <span className={s.postMarkDate} aria-hidden>{d.day} {d.monthShort}<br />{d.year}</span>}
            <Art name="stamp" className={s.postStamp} eager />
            <p className={s.kicker}>Kartu Pos {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride} <em>dan</em> {data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf5e8" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf5e8"
        dark="#3a2a20"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
            <Art name="waves" className={s.divider} />
            {photo && (
              <div className={s.heroPrint}>
                <div className={s.heroFrame}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>
                <p className={s.heroPrintNote} aria-hidden>{city}, {d.year}</p>
              </div>
            )}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroRide} aria-hidden><Art name="bike" className={s.heroBike} /></div>
          </header>
        )}
        slots={{
          divider: <Art name="waves" className={s.divider} />,
          node: <Art name="stamp" />,
          amp: <Art name="waves" />,
          portrait: <Art name="stamp" className={s.portraitStamp} />,
          countDecor: <span className={s.countScene} aria-hidden />,
          closingDecor: <span className={s.closingScene} aria-hidden />,
          closingEmblem: <Art name="lamp" className={s.closingLamp} />,
          sentArt: <Art name="bike" />,
        }}
      />
    </ThemeShell>
  );
}
