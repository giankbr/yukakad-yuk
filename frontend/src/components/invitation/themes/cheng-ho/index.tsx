"use client";
// Theme "Cheng Ho" — pernikahan muslim Tionghoa-Indonesia, terinspirasi masjid-masjid Cheng Ho di Nusantara. Sampul
// hijau giok dengan gerbang bulan berisi lukisan gouache masjid beratap pagoda tiga tingkat (hijau berpinggir merah,
// tiang merah, jendela kisi, pintu lengkung emas, bulan sabit emas), dua lampion merah yang berayun dan sudut kisi
// pernis. Hanya arsitektur: tanpa figur dan tanpa kaligrafi lukis (teks Arab diketik). Hero: segel 囍, nama, foto dalam
// gerbang bulan. Papan acara bersudut kisi, hitung mundur segi delapan, monogram dalam gerbang bulan, angpau digital.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Zen Old Mincho:wght@400;600;700", "Castoro:ital@0;1", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/cheng-ho.py (tools/art/themes in the repo).
const Art = makeArt("cheng-ho", { masjid: [640, 518], lantern: [110, 199], cloud: [300, 35], lattice: [170, 170] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "وَمِنْ اٰيٰتِهٖٓ اَنْ خَلَقَ لَكُمْ مِّنْ اَنْفُسِكُمْ اَزْوَاجًا لِّتَسْكُنُوْٓا اِلَيْهَا",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    sub: "QS. Ar-Rum: 21",
    intro: "“Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan untukmu dari jenismu sendiri, agar kamu merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.”",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua keluarga, satu ikatan", "Kedua Mempelai"],
  count: ["Menuju hari bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Kenangan", "Galeri Foto"],
  wishes: ["Doa & ucapan", "Ucapan & Kehadiran"],
  gifts: ["Angpau digital", "Tanda Kasih"],
  closing: {
    thanks: "Terima Kasih",
    text: "Merupakan kehormatan bagi kami sekeluarga apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu. Semoga Allah membalas kebaikan Anda.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah hadiah terindah bagi kami. Bila berkenan menitipkan angpau, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Keluarga Om Hendra Tan", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma. Selamat Aisyah dan Yusuf, semoga sakinah, mawaddah, warahmah. Kami sekeluarga hadir." },
  { id: "w2", name: "Remaja Masjid Ahad Pagi", attendance: "yes" as Attendance, message: "Dari panitia takjil jadi pengantin! Ikut bahagia, semoga rumah tangganya penuh berkah." },
  { id: "w3", name: "Ci Lina & Ko Daniel (Palembang)", attendance: "no" as Attendance, message: "Maaf belum bisa ke Surabaya. Doa terbaik dari Palembang, semoga lancar sampai resepsi." },
];

function Lanterns() {
  return (
    <div className={s.lanterns} aria-hidden>
      <span className={s.lanternA}><Art name="lantern" eager /></span>
      <span className={s.lanternB}><Art name="lantern" eager /></span>
    </div>
  );
}

export default function ChengHoTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0];
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2f6d57"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="lattice" eager className={s.cornerTL} />
          <Art name="lattice" eager className={s.cornerTR} />
          <Lanterns />
          <div className={s.gate} aria-hidden><Art name="masjid" eager /></div>
          <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</p>
          <p className={s.coverKicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<span>&amp;</span>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f1d692" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#f1d692"
        dark="#22201a"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <span className={s.heroSeal} lang="zh" aria-hidden>囍</span>
            <p className={s.heroKicker}>Walimatul &lsquo;Ursy</p>
            <h1 className={s.heroNames}>{data.couple.bride}<i>&amp;</i>{data.couple.groom}</h1>
            {photo
              ? <div className={s.heroGate}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>
              : <div className={`${s.heroGate} ${s.heroGateArt}`} aria-hidden><Art name="masjid" /></div>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="cloud" className={s.divider} />,
          amp: <Art name="cloud" />,
          portrait: <span className={s.portraitLantern} aria-hidden><Art name="lantern" /></span>,
          countDecor: <span className={s.countDecor} aria-hidden><Art name="lattice" /><Art name="lattice" /></span>,
          closingDecor: <span className={s.closeLanterns} aria-hidden><span><Art name="lantern" /></span><span><Art name="lantern" /></span></span>,
          closingEmblem: <div className={s.closingGate} aria-hidden><Art name="masjid" /></div>,
          sentArt: <Art name="lantern" />,
        }}
      />
    </ThemeShell>
  );
}
