"use client";
// Theme "Batik Gentongan" — walimah Madura dari Tanjung Bumi: sampul berupa selembar kain gentongan merah mengkudu
// (bunga pesisir, burung, sulur, cecek, retak lilin biru nila) yang perlahan bergeser, label kain krem berisi nama,
// sepasang gentong tanah liat berselampir kain di kakinya; pinggiran tumpal-ombak, kartu acara bergaya contoh kain,
// potret dan foto terhampar di atas kain. Pembuka Islami (basmalah + salam), penutup "Sakalangkong".
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Literata:ital,wght@0,400;0,600;1,400", "Karla:wght@500;700", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/batik-gentongan.py (tools/art/themes in the repo).
const Art = makeArt("batik-gentongan", { gentong: [300, 309], burung: [240, 138], sekar: [320, 59] } as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: BISMILLAH,
    kicker: "Assalamu'alaikum Wr. Wb.",
    title: "Dua Helai Benang, Satu Lembar Kain",
    intro: "Dengan memohon rahmat dan ridha Allah SWT, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami di Tanjung Bumi, Bangkalan. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Helai Benang", "Kedua Mempelai"],
  count: ["Kain Hampir Rampung", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Motif Perjalanan", "Kisah Kami"],
  gallery: ["Lembar Kenangan", "Galeri"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Sakalangkong", text: "Terima kasih atas kehadiran dan doa restu Bapak/Ibu/Saudara/i. Semoga Allah membalas setiap kebaikan dengan berlipat ganda.", salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh" },
  sent: "Sakalangkong, doa dan ucapan Anda sudah terkirim.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
  giftIntro: "Doa restu Anda adalah kado terindah bagi kami. Jika berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Mat Sahri", attendance: "yes" as Attendance, message: "Barakallahu lakuma. Semoga rumah tangga Fitriyah dan Hasyim awet seperti warna batik gentongan, makin lama makin indah." },
  { id: "w2", name: "Sanggar Batik Telaga Biru", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru! Kami datang membawa kain terbaik untuk pengantin." },
  { id: "w3", name: "Mas Faisal & Mbak Rina", attendance: "maybe" as Attendance, message: "Mohon maaf belum tentu bisa pulang ke Bangkalan. Doa terbaik kami dari Surabaya, semoga sakinah mawaddah warahmah." },
];

function Jars({ eager }: { eager?: boolean }) {
  return (
    <div className={s.jars} aria-hidden>
      <Art name="gentong" eager={eager} className={s.jar} />
      <Art name="gentong" eager={eager} className={`${s.jar} ${s.jarSmall}`} />
    </div>
  );
}

export default function BatikGentonganTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#5e120e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.label}>
            <Art name="burung" eager className={s.labelBird} />
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>dan</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
            </div>
          </div>
          <Jars eager />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#efe2c4"
        dark="#1f2e57"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>dan</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && <div className={s.heroCloth}><div className={s.heroPhoto}><Photo src={hero} alt="" /></div></div>}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sekar" className={s.divider} />,
          node: <Art name="burung" />,
          amp: <Art name="sekar" />,
          closingDecor: <Jars />,
          closingEmblem: <Art name="burung" className={s.closingBird} />,
          sentArt: <Art name="burung" />,
        }}
      />
    </ThemeShell>
  );
}
