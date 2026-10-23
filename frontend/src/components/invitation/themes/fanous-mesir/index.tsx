"use client";
// Theme "Fanous Mesir" — malam Ramadan di lorong Kairo: lentera fanous kuningan berkaca warna permata (delima, zamrud,
// kobalt, kuning) tergantung dari balkon mashrabiya kayu berkisi yang menyala hangat; nama di jendela berbingkai kisi.
// Tanpa foto dan tanpa figur: hanya arsitektur, geometri, dan cahaya.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@400;500;600;700", "Lustria", "Amiri"];
// Painted by /tmp/pen/art/themes/fanous-mesir.py (tools/art/themes in the repo).
const Art = makeArt("fanous-mesir", { fanous: [420, 580], fanous2: [240, 401], balkon: [780, 515], divider: [260, 58], bintang: [80, 81] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Cahaya untuk Dua Hati",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Kehadiran dan doa Bapak/Ibu/Saudara/i akan menjadi pelita yang menerangi langkah pertama kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Dua Pelita", "Kedua Mempelai"] as [string, string],
  count: ["Menanti Malam Bercahaya", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Kisah Kami", "Dari Kairo ke Jakarta"] as [string, string],
  gallery: ["Galeri", "Momen Bahagia"] as [string, string],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Terima kasih atas doa dan kehadiran Bapak/Ibu/Saudara/i. Semoga Allah membalas setiap kebaikan dengan cahaya dan keberkahan.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
  familyLabel: "Kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Ustadz Fadlan & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Teman Kos Hay Asyir", attendance: "yes" as const, message: "Dari lorong Kairo sampai pelaminan! Ikut bahagia untuk Salma dan Yusuf, sampai jumpa di Al-Azhar." },
  { id: "w3", name: "Keluarga Alaydrus", attendance: "maybe" as const, message: "Mohon maaf jika belum bisa hadir. Doa terbaik kami untuk kedua mempelai." },
];

export default function FanousMesirTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#121829"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.scene} aria-hidden>
            <Art name="fanous2" eager className={s.lampL} />
            <Art name="fanous" eager className={s.lampC} />
            <Art name="fanous2" eager className={s.lampR} />
            <Art name="balkon" eager className={s.balkon} />
          </div>
          <div className={s.panel}>
            <div className={s.panelIn}>
              <p className={s.arabicTop} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
              <span className={s.glassRule} aria-hidden />
              <div className={s.guestWrap}>
                <div className={s.guest}>
                  <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                  <strong>{guestLabel(data)}</strong>
                  {table && <span className={s.table}>{table}</span>}
                </div>
                <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#1a1208" />Buka Undangan</button>
              </div>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f6dfaa"
        dark="#1a1208"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="balkon" className={s.heroBalkon} />
            <Art name="fanous" className={s.heroLamp} />
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="bintang" />,
          amp: <Art name="bintang" />,
          portrait: <Art name="bintang" />,
          closingEmblem: (
            <div className={s.closingLamps} aria-hidden>
              <Art name="fanous2" />
              <Art name="fanous" />
              <Art name="fanous2" />
            </div>
          ),
          sentArt: <Art name="fanous2" />,
        }}
      />
    </ThemeShell>
  );
}
