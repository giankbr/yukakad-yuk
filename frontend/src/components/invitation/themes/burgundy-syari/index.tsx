"use client";
// Theme "Burgundy Syari" — walimah syar'i (foto opsional) dalam burgundy anggur dan emas. Sampulnya kartu gantung dari
// kertas krem dengan lubang bermata emas di atas beludru anggur, buket bunga kering (mawar kering, gandum, baby's
// breath, eukaliptus) yang diikat tali rami melintang di kepala kartu. Bintang delapan emas tekan, kilau beludru, dan
// mawar kering kecil di setiap medali monogram. Tanpa figur makhluk hidup; semua dilukis ulang.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Yeseva One", "Crimson Pro:ital,wght@0,400;0,500;0,600;1,400;1,500", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/burgundy-syari.py (beludru is the CSS velvet tile).
const Art = makeArt("burgundy-syari", { buket: [640, 424], ranting: [420, 51], mawar: [110, 105], bintang: [160, 159] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Walimatul 'Ursy",
    sub: "Bertemu karena-Nya, bersatu dalam ridha-Nya",
    intro: "Maha Suci Allah yang menciptakan makhluk-Nya berpasang-pasangan. Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dengan Izin Allah", "Kedua Mempelai"],
  count: ["Menuju Hari Bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Kenangan"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullahu Khairan",
    text: "Merupakan kebahagiaan dan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa terbaik untuk kedua mempelai…",
  giftIntro: "Doa Anda adalah hadiah terindah bagi kami. Bila berkenan memberi tanda kasih, dapat melalui:",
  wishLabel: "Doa & Ucapan",
};

const WISHES = [
  { id: "w1", name: "Ustadzah Fatimah Az-Zahra", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Halaqah Tahsin Cigadung", attendance: "yes" as Attendance, message: "MasyaAllah, ikut bahagia, Nadhira. Semoga rumah kalian selalu ramai dengan tilawah dan kebaikan." },
  { id: "w3", name: "Keluarga H. Ridwan, Cimahi", attendance: "maybe" as Attendance, message: "Mohon maaf bila belum dapat hadir. Doa terbaik kami untuk Faris dan Nadhira, semoga Allah mudahkan segala urusan." },
];

export default function BurgundySyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const groom = data.couple.groom?.trim();
  const photo = data.gallery[0];
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const noPhotos = !data.couple.bridePhoto && !data.couple.groomPhoto;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#3c0b17"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
          <div className={s.tagWrap}>
            <div className={s.bouquet} aria-hidden><Art name="buket" eager /></div>
            <span className={s.eyelet} aria-hidden />
            <div className={s.tag}>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#f1dca8" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos={noPhotos}
        demoWishes={WISHES}
        light="#f1dca8"
        dark="#5c1626"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="bintang" className={s.heroStar} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}{groom && <><em>&amp;</em>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {photo && <div className={s.heroOval}><Photo src={photo} alt={[data.couple.bride, groom].filter(Boolean).join(" dan ")} className={s.heroPic} /></div>}
            <Art name="ranting" className={s.heroSprig} />
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="ranting" className={s.divider} />,
          node: <Art name="bintang" />,
          amp: <Art name="mawar" />,
          portrait: <Art name="mawar" className={s.portraitArt} />,
          countDecor: <span className={s.countSheen} aria-hidden />,
          closingDecor: <Art name="buket" className={s.closingBouquet} />,
          closingEmblem: <Art name="bintang" className={s.closingEmblem} />,
          sentArt: <Art name="mawar" />,
        }}
      />
    </ThemeShell>
  );
}
