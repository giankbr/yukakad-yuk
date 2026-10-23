"use client";
// Theme "Sengkang Sutra" — kilau sutra Sengkang, Wajo: tirai lipa' sabbe kotak-kotak hijau giok dan emas yang
// berkilau perlahan, rumah apung Danau Tempe saat senja, alat tenun kayu dan kepompong sutra emas. Potret dalam bingkai
// walasuji belah ketupat, kartu berbingkai emas ganda. Gerak anggun: kilau menyapu kain, kepompong berayun pelan.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;0,600;1,400;1,500", "Jost:wght@300;400;500;600", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/sengkang-sutra.py.
const Art = makeArt("sengkang-sutra", { drape: [780, 330], lake: [780, 700], loom: [360, 333], divider: [360, 15], cocoon: [100, 135] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const WISHES = [
  { id: "w1", name: "Keluarga H. Andi Mappanyukki", attendance: "yes" as const, message: "Barakallahu lakuma. Semoga Rahmah dan Faisal menjadi keluarga yang sakinah, rukun seperti benang sutra yang ditenun rapat." },
  { id: "w2", name: "Teman-teman SMA 3 Sengkang", attendance: "yes" as const, message: "Selamat menempuh hidup baru! Sampai ketemu di Atakkae, kami datang ramai-ramai." },
  { id: "w3", name: "Puang Hasna di Makassar", attendance: "maybe" as const, message: "Insyaallah diusahakan datang. Doa terbaik untuk kalian berdua, semoga langgeng sampai tua." },
];

export default function SengkangSutraTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#083735"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.drapeWrap} aria-hidden>
            <Art name="drape" eager className={s.drape} />
            <span className={s.sheen} />
          </div>
          <div className={s.lakeWrap} aria-hidden><Art name="lake" eager /></div>
          <p className={s.bismillah} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#062625" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f3d98f"
        dark="#093f3e"
        demoWishes={WISHES}
        copy={{
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Wr. Wb.",
            title: "Tabe'",
            sub: "Dengan memohon rahmat dan ridha Allah SWT",
            intro: "Kami bermaksud menyelenggarakan akad nikah dan resepsi pernikahan putra-putri kami. Merupakan kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua helai sutra", "Kedua Mempelai"],
          count: ["Menuju hari baik", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & tempat", "Rangkaian Acara"],
          story: ["Ditenun perlahan", "Kisah Kami"],
          gallery: ["Album", "Momen Kami"],
          wishes: ["Doa restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: { thanks: "Terima Kasih", text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Semoga Allah membalas dengan kebaikan.", salam: "Wassalamu'alaikum Wr. Wb." },
          sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
          wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
          closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroFrame}>
              <div className={s.heroPhoto}>
                {photo ? <Photo src={photo} alt={`${data.couple.bride} dan ${data.couple.groom}`} /> : <span className={s.heroMono} aria-hidden>{data.couple.bride.slice(0, 1)}{data.couple.groom.slice(0, 1)}</span>}
              </div>
            </div>
            <div className={s.heroCard}>
              <p className={s.heroKicker}>Pernikahan</p>
              <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="cocoon" />,
          amp: <Art name="cocoon" />,
          portrait: <Art name="cocoon" />,
          closingDecor: <span className={s.closingLake} aria-hidden><Art name="lake" /></span>,
          closingEmblem: <Art name="loom" className={s.closingEmblem} />,
          sentArt: <Art name="cocoon" />,
        }}
      />
    </ThemeShell>
  );
}
