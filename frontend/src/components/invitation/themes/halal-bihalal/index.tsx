"use client";
// Theme "Halal Bihalal" — silaturahmi Lebaran keluarga atau kantor dalam hijau daun dan kuning janur: ketupat anyaman
// janur (gouache di atas anyaman silang yang sungguhan) yang bergoyang di tali, pelita tanah liat dengan nyala yang
// berkedip, bedug di sudut sampul, pita anyaman janur sebagai pembatas, dan hitung mundur berbentuk empat ketupat.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,500;0,600;1,400;1,500", "Outfit:wght@400;500;600", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/halal-bihalal.py (janur.webp is a CSS background)
const Art = makeArt("halal-bihalal", { ketupat: [220, 370], pelita: [170, 144], bedug: [420, 296] } as const);
const TAQABBAL = "تَقَبَّلَ اللَّهُ مِنَّا وَمِنْكُمْ";

function Pelita({ eager }: { eager?: boolean }) {
  return <span className={s.glowSpan}><Art name="pelita" eager={eager} /></span>;
}

export default function HalalBihalalTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Halal Bihalal";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const hosts = child ? (child.nickname?.trim() || child.name.trim()) : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1d4626"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={`${s.hang} ${s.hang1}`} aria-hidden><Art name="ketupat" eager /></span>
          <span className={`${s.hang} ${s.hang2}`} aria-hidden><Art name="ketupat" eager /></span>
          <span className={`${s.hang} ${s.hang3}`} aria-hidden><Art name="ketupat" eager /></span>
          <div className={s.coverBody}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverTitle}>Minal Aidin<br />wal Faizin</h1>
            <p className={s.coverSub}>Mohon maaf lahir &amp; batin</p>
            <p className={s.hosts}><small>Keluarga</small>{hosts}</p>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#1d4626" />Buka Undangan</button>
            </div>
          </div>
          <div className={s.ground} aria-hidden>
            <Art name="bedug" eager className={s.bedug} />
            <div className={s.pelitas}><Pelita eager /><Pelita eager /><Pelita eager /></div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!data.couple.bridePhoto && !data.couple.groomPhoto && !child?.photo}
        light="#fbe7a6"
        dark="#1d4626"
        demoWishes={[
          { id: "w1", name: "Keluarga Om Bambang", attendance: "yes", message: "Taqabbalallahu minna wa minkum. Mohon maaf lahir dan batin, Pak Hadi sekeluarga. Sampai jumpa hari Minggu!" },
          { id: "w2", name: "Rekan Kantor Divisi Keuangan", attendance: "yes", message: "Minal aidin wal faizin. Terima kasih undangannya, kami datang ramai-ramai, siap menghabiskan ketupatnya." },
          { id: "w3", name: "Bulik Narti & keluarga", attendance: "maybe", message: "Ngapunten lahir batin nggih. Insyaallah menyusul sore kalau perjalanan dari Solo lancar." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: TAQABBAL,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Minal Aidin wal Faizin",
            sub: "Mohon maaf lahir dan batin",
            intro: `Alhamdulillah, Ramadan telah kita lalui bersama. Dengan penuh rasa syukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam acara ${label.toLowerCase()}: bersilaturahmi, saling memaafkan, dan menikmati hidangan Lebaran bersama keluarga ${hosts}.`,
          },
          roles: ["Tuan Rumah", "Nyonya Rumah"],
          couple: ["Yang Mengundang", "Tuan Rumah"],
          count: ["Menuju Hari Silaturahmi", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Setahun Terakhir", "Kabar Keluarga"],
          gallery: ["Galeri", "Kenangan Lebaran"],
          wishes: ["Ucapan Lebaran", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Mohon Maaf Lahir & Batin",
            text: "Terima kasih atas kehadiran dan doa Bapak/Ibu/Saudara/i. Semoga silaturahmi ini membawa berkah dan mempererat persaudaraan kita.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Terima kasih, ucapan Anda sudah kami terima. Mohon maaf lahir dan batin.",
          wishPlaceholder: "Tuliskan ucapan Lebaran Anda…",
          closedNote: "Terima kasih atas perhatiannya. Ucapan Lebaran masih bisa dikirim lewat form ini.",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="ketupat" className={`${s.heroKetupat} ${s.heroKetupatL}`} />
            <Art name="ketupat" className={`${s.heroKetupat} ${s.heroKetupatR}`} />
            <p className={s.heroAr} lang="ar" dir="rtl">{TAQABBAL}</p>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroTitle}>Selamat Idul Fitri</h1>
            <p className={s.heroHosts}>Keluarga {hosts}</p>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="ketupat" /></span>,
          node: <Art name="ketupat" />,
          countDecor: <><Art name="pelita" className={`${s.countPelita} ${s.countPelitaL}`} /><Art name="pelita" className={`${s.countPelita} ${s.countPelitaR}`} /></>,
          closingDecor: <div className={s.closingRow} aria-hidden><Pelita /><Pelita /><Pelita /></div>,
          closingEmblem: <Art name="ketupat" className={s.closingKetupat} />,
          sentArt: <Art name="ketupat" />,
        }}
      />
    </ThemeShell>
  );
}
