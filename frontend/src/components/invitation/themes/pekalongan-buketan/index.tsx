"use client";
// Theme "Pekalongan Buketan" — batik pesisir Pekalongan: buket bunga gaya Eropa (mawar, krisan, lili, bunga biru kecil)
// bergaris canting dan bercecek, kupu-kupu dan burung kecil, pastel cerah di atas mori krem dengan pinggiran biru-merah muda.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Yeseva One", "Sorts Mill Goudy:ital@0;1", "Parisienne", "Amiri"];
// Painted by /tmp/pen/art/themes/pekalongan-buketan.py (tools/art/themes in the repo).
const Art = makeArt("pekalongan-buketan", { buket: [640, 740], kupu: [130, 117], burung: [240, 139], sprig: [260, 90] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Seikat Bunga, Sepenuh Doa",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Kuntum, Satu Buket", "Kedua Mempelai"] as [string, string],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Kisah Kami", "Dari Kampung Batik"] as [string, string],
  gallery: ["Galeri", "Lembar Kenangan"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah bunga terindah dalam buket kebahagiaan kami. Semoga Allah membalas setiap kebaikan dengan berlipat.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  familyLabel: "Kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Maskur", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah dan selalu berwarna seperti batik pesisir." },
  { id: "w2", name: "Rina, Teman Kelas Batik", attendance: "yes" as const, message: "Dari tumpahan malam sampai pelaminan! Ikut bahagia, Laila dan Faris. Sampai jumpa di Kauman." },
  { id: "w3", name: "Pak Darsono & Bu Endang", attendance: "maybe" as const, message: "Mohon maaf bila berhalangan. Doa kami menyertai, semoga lancar sampai hari H." },
];

export default function PekalonganBuketanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f8f0e1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>{label}</p>
          <div className={s.buketBox} aria-hidden>
            <Art name="buket" eager className={s.buket} />
            <Art name="burung" eager className={s.burung} />
            <Art name="kupu" eager className={s.kupu} />
          </div>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff6ea" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fff6ea"
        dark="#7a2f5a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            {hero && (
              <div className={s.heroPanel}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <Art name="kupu" className={s.heroKupu} />
              </div>
            )}
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="sprig" className={s.heroSprig} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="kupu" />,
          amp: <Art name="kupu" />,
          portrait: <Art name="kupu" />,
          closingEmblem: <Art name="buket" className={s.closingBuket} />,
          sentArt: <Art name="buket" />,
        }}
      />
    </ThemeShell>
  );
}
