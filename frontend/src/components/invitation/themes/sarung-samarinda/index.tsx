"use client";
// Theme "Sarung Samarinda" — tenun sarung sutra Samarinda dan Sungai Mahakam. Sampulnya alat tenun gedokan: balok
// kayu berukir, benang lungsin merah tua-hitam-emas-toska yang turun melewati sisir, dan kain kotak-kotak yang baru
// setengah jadi dengan teropong di atasnya; nama mempelai berada di kain gelap di bawahnya. Di dalam: Mahakam saat
// senja (ketinting, tongkang batu bara, rumah panggung, masjid di kejauhan), potret yang dibalut sarung, hitung mundur
// di atas selembar sarung tempat ketinting melintas. Dilukis oleh /tmp/pen/art/themes/sarung-samarinda.py.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Marcellus", "Spectral:ital,wght@0,400;0,600;1,400", "Tenor Sans", "Amiri"];
const Art = makeArt("sarung-samarinda", { gedokan: [780, 504], mahakam: [780, 460], ces: [283, 44], benang: [140, 181] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Mohon Doa Restu",
    sub: "Dari tepian Mahakam, dua benang menjadi satu kain",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Lungsin & Pakan", "Kedua Mempelai"],
  count: ["Menghitung Hari", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat Tanggalnya", "Waktu & Tempat"],
  story: ["Sehelai demi Sehelai", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i akan menjadi benang emas dalam tenunan hidup kami. Atas perhatiannya, kami ucapkan terima kasih.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah bagi kami. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Nenek Hj. Masnah, Samarinda Seberang", attendance: "yes" as Attendance, message: "Barakallahu lakuma. Pakailah sarung itu baik-baik, Nak. Semoga rumah tangga kalian rapat dan kuat seperti tenunan gedokan." },
  { id: "w2", name: "Teman Kantor Dinas PU", attendance: "yes" as Attendance, message: "Selamat Fahri & Nadia! Semoga sakinah, mawaddah, warahmah, dan selalu akur seperti Mahakam dan tepiannya." },
  { id: "w3", name: "Keluarga Om Saiful, Tenggarong", attendance: "maybe" as Attendance, message: "Insyaallah kami menyusul kalau tidak terhalang. Doa terbaik dari Tenggarong untuk kalian berdua." },
];

export default function SarungSamarindaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const groom = data.couple.groom?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a0810"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.loom} aria-hidden><Art name="gedokan" eager /></div>
          <div className={s.coverText}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#3e0c16" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#f0d9a6"
        dark="#5a1420"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.heroRiver}>
              <Art name="mahakam" />
              <div className={s.heroHead}>
                <p className={s.heroKicker}>Walimatul &apos;Ursy · Samarinda</p>
                <h1 className={s.heroNames}>{data.couple.bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
              </div>
            </div>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {photo && (
              <div className={s.heroWrap}>
                <Photo src={photo} alt={[data.couple.bride, groom].filter(Boolean).join(" dan ")} className={s.heroPic} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="ces" className={s.divider} />,
          node: <Art name="benang" />,
          amp: <Art name="benang" />,
          portrait: <Art name="benang" className={s.portraitArt} />,
          countDecor: <Art name="ces" className={s.drift} />,
          closingDecor: <Art name="mahakam" className={s.closingScene} />,
          closingEmblem: <Art name="benang" className={s.closingEmblem} />,
          sentArt: <Art name="benang" />,
        }}
      />
    </ThemeShell>
  );
}
