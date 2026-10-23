"use client";
// Theme "Haul & Tahlil" — undangan keluarga untuk haul dan tahlilan (doa bersama) mengenang almarhum/almarhumah: krem dan
// hijau tua yang teduh, tasbih hijau 33 butir bertali sutra (gouache) dengan ranting melati cat air. Tanpa figur dan tanpa
// kaligrafi gambar (hanya teks Arab ketik). Sampul seperti kartu cetak bergaris rambut; judul bagian rata kiri.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cormorant Upright:wght@400;500;600", "Petrona:ital,wght@0,400;0,500;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/haul-tahlil.py
const Art = makeArt("haul-tahlil", { tasbih: [420, 560], sprig: [320, 311], bloom: [96, 98], divider: [300, 40] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";
const ISTIRJA = "إِنَّا لِلَّٰهِ وَإِنَّا إِلَيْهِ رَاجِعُونَ";

export default function HaulTahlilTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Haul & Tahlil";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const short = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const full = child?.name.trim() || data.couple.brideFull?.trim() || data.couple.bride;
  const female = /almarhumah|\bhj\.|\bibu\b|\bnyai\b/i.test(`${full} ${short}`);
  const alm = female ? "Almarhumah" : "Almarhum";
  const fullName = /^alm/i.test(full) ? full : `${alm} ${full}`;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f4eddc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.istirja} lang="ar" dir="rtl">{ISTIRJA}</p>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.tasbihWrap} aria-hidden><Art name="tasbih" eager /></div>
          <p className={s.coverLabel}>Mengenang dan mendoakan</p>
          <h1 className={s.coverName}>{fullName}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf8ef" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#eadfbf"
        dark="#1f4a3a"
        demoWishes={[
          { id: "w1", name: "Kyai H. Mashuri", attendance: "yes", message: "Allahummaghfirlahu warhamhu wa 'afihi wa'fu 'anhu. Semoga almarhum husnul khatimah dan dilapangkan kuburnya." },
          { id: "w2", name: "Jamaah Majelis Taklim Nurul Huda", attendance: "yes", message: "Kami akan hadir membaca tahlil bersama. Semoga amal jariyah Abah dari majelis ini terus mengalir." },
          { id: "w3", name: "Keluarga Bapak Hasyim, Surabaya", attendance: "maybe", message: "Mohon maaf bila belum dapat hadir. Al-Fatihah untuk almarhum, semoga keluarga yang ditinggalkan diberi kesabaran." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Haul & Doa Bersama",
            intro: `Dengan memohon rahmat Allah Subhanahu wa Ta'ala, kami mengharap kehadiran Bapak/Ibu/Saudara/i dalam majelis ${label} untuk bersama-sama mendoakan ${fullName}. Semoga Allah mengampuni dosa-dosanya, menerima amal ibadahnya, dan menempatkannya di sisi terbaik.`,
          },
          roles: [alm, "Bersama"],
          couple: ["Dengan penuh kasih kami mengenang", `Yang Kami Doakan`],
          count: ["Insyaallah dilaksanakan dalam", "Waktu Majelis"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Susunan Majelis"],
          story: ["Riwayat Singkat", "Mengenang Beliau"],
          gallery: ["Galeri", "Kenangan"],
          wishes: ["Kirim Doa", "Doa & Kehadiran"],
          gifts: ["Sedekah & Santunan", "Titipan Sedekah"],
          closing: {
            thanks: "Jazakumullah Khairan",
            text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i, kami sekeluarga menghaturkan terima kasih. Semoga Allah membalas dengan kebaikan yang berlipat.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: `Jazakumullah khairan. Doa Anda telah kami terima, semoga menjadi cahaya bagi ${short}.`,
          wishPlaceholder: `Tuliskan doa untuk ${alm.toLowerCase()} dan keluarga…`,
          closedNote: "Terima kasih atas doa dan perhatiannya. Doa masih dapat dikirim melalui form ini.",
          giftIntro: `Bagi Bapak/Ibu/Saudara/i yang berkenan menitipkan sedekah atas nama ${alm.toLowerCase()} untuk santunan anak yatim dan dhuafa, dapat melalui:`,
          giftAddressTitle: "Kirim Bingkisan",
          familyLabel: `Kami yang mendoakan,\nkeluarga besar ${alm.toLowerCase()}`,
        }}
        hero={(
          <header className={s.hero}>
            <Art name="sprig" className={s.heroSprig} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroTitle}>Doa untuk yang Telah Mendahului</h1>
            <p className={s.heroName}>{fullName}</p>
            <span className={s.heroRule} aria-hidden />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="divider" /></span>,
          node: <Art name="bloom" />,
          portrait: <Art name="bloom" className={s.portraitBloom} />,
          countDecor: <Art name="sprig" className={s.countSprig} />,
          closingDecor: <Art name="sprig" className={s.closingSprig} />,
          closingEmblem: <Art name="bloom" className={s.closingBloom} />,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
