"use client";
// Theme "Buka Bersama" — a Ramadan iftar invitation for alumni, office or family groups: a painted maghrib sky (plum,
// rose, amber) with a thin crescent and a far mosque skyline, brass lanterns that sway and glow, and a long table
// dressed in cream cloth with dates, kolak and iced tea. Hosts are a committee, so the people section is one host card
// under a hanging lantern. No figurative ornament.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@400;600;700", "Plus Jakarta Sans:wght@400;500;600;700", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/buka-bersama.py (langit.webp is a CSS background)
const Art = makeArt("buka-bersama", { lentera: [130, 252], meja: [640, 230], kurma: [150, 50] } as const);
const RAMADAN = "رَمَضَانُ كَرِيمٌ";

export default function BukaBersamaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Buka Bersama";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const hosts = child ? (child.nickname?.trim() || child.name.trim()) : (data.couple.brideFull?.trim() || [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & "));
  const short = child ? hosts : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const time = data.events[0]?.time?.trim();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a1830"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={`${s.hang} ${s.hang1}`} aria-hidden><Art name="lentera" eager /></span>
          <span className={`${s.hang} ${s.hang2}`} aria-hidden><Art name="lentera" eager /></span>
          <span className={`${s.hang} ${s.hang3}`} aria-hidden><Art name="lentera" eager /></span>
          <div className={s.coverBody}>
            <p className={s.coverAr} lang="ar" dir="rtl">{RAMADAN}</p>
            <p className={s.kicker}>Undangan</p>
            <h1 className={s.coverTitle}>{label}</h1>
            <p className={s.hosts}>{hosts}</p>
            <p className={s.coverWhen}>{formatDate(data.date)}{time && <span>{time}</span>}</p>
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#3b1d35" />Buka Undangan</button>
          </div>
          <Art name="meja" eager className={s.coverTable} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#f6d79a"
        dark="#3b1d35"
        demoWishes={[
          { id: "w1", name: "Andika (XII IPA 4)", attendance: "yes", message: "Siap datang! Sudah lama nggak ketemu. Saya bawa kurma Ajwa titipan dari umrah kemarin buat takjil." },
          { id: "w2", name: "Rani & suami", attendance: "yes", message: "Insyaallah hadir berdua. Terima kasih panitia, semoga santunannya jadi berkah buat kita semua." },
          { id: "w3", name: "Bayu Saputra", attendance: "maybe", message: "Masih dinas di Surabaya, kalau pesawat sore aman saya langsung meluncur ke aula. Iuran sudah ditransfer ya." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: RAMADAN,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Marhaban ya Ramadan",
            sub: "Mari berbuka bersama",
            intro: `Di bulan penuh berkah ini, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam acara ${label.toLowerCase()}: menanti azan magrib bersama, berbuka dengan yang manis, shalat berjamaah, dan mempererat silaturahmi.`,
          },
          roles: ["Penyelenggara", "Panitia"],
          couple: ["Yang Mengundang", "Tuan Rumah"],
          count: ["Menuju Waktu Berbuka", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Susunan Acara"],
          story: ["Jejak Kebersamaan", "Cerita Kita"],
          gallery: ["Galeri", "Bukber Tahun Lalu"],
          wishes: ["Konfirmasi", "Hadir & Titip Pesan"],
          gifts: ["Iuran & Santunan", "Transfer ke Panitia"],
          closing: {
            thanks: "Sampai Jumpa di Meja Berbuka",
            text: "Terima kasih atas kehadirannya. Semoga Allah menerima puasa dan amal ibadah kita, dan mempertemukan kita kembali di Ramadan berikutnya.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Terima kasih, konfirmasi dan pesan Anda sudah diterima panitia.",
          wishPlaceholder: "Tuliskan pesan atau doa untuk acara ini…",
          closedNote: "Pendaftaran sudah ditutup. Pesan dan doa masih bisa dikirim lewat form ini.",
          giftIntro: "Iuran acara dan sumbangan santunan anak yatim dapat ditransfer ke rekening panitia berikut:",
          familyLabel: null,
        }}
        hero={(
          <header className={s.hero}>
            <span className={`${s.hang} ${s.hang1}`} aria-hidden><Art name="lentera" /></span>
            <p className={s.heroKicker}>Ramadan 1448 H</p>
            <h1 className={s.heroTitle}>{label}</h1>
            <p className={s.heroHosts}>{short}</p>
            <p className={s.heroDate}>{formatDate(data.date)}{time ? ` · ${time}` : ""}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="kurma" className={s.heroKurma} />
          </header>
        )}
        slots={{
          divider: <Art name="kurma" className={s.divider} />,
          node: <Art name="kurma" />,
          portrait: <Art name="lentera" className={s.hostLantern} />,
          countDecor: <><Art name="lentera" className={`${s.countLantern} ${s.countLanternL}`} /><Art name="lentera" className={`${s.countLantern} ${s.countLanternR}`} /></>,
          closingDecor: <><div className={s.closingLanterns} aria-hidden><span><Art name="lentera" /></span><span><Art name="lentera" /></span><span><Art name="lentera" /></span></div><Art name="meja" className={s.closingTable} /></>,
          sentArt: <Art name="kurma" />,
        }}
      />
    </ThemeShell>
  );
}
