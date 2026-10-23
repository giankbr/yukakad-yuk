"use client";
// Theme "Pameran Seni" — undangan pembukaan pameran tunggal: sampul berdiri di dalam galeri putih (lampu sorot rel,
// dua lukisan abstrak orisinal berbingkai, bangku kayu di lantai beton), teks dinding di atas dan label karya museum
// sebagai kartu tamu. Seniman & kurator sebagai tuan rumah, konsep pameran sebagai linimasa, galeri berisi karyanya.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Instrument Serif:ital@0;1", "Hanken Grotesk:wght@400;500;600;700"];
// Painted by /tmp/pen/art/themes/pameran-seni.py (the gallery wall is a CSS background; karya-* are the demo works)
const Art = makeArt("pameran-seni", { "karya-2": [480, 600] } as const);

export default function PameranSeniTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const label = data.eventLabel ?? "Pembukaan Pameran";
  const storyTitle = data.story?.title?.trim();
  const title = storyTitle && !/^kisah|^cerita|^konsep/i.test(storyTitle) ? storyTitle : bride;
  const curator = groom?.trim();
  const heroSrc = data.gallery[0];
  const note = data.couple.note?.trim();
  const parsedYear = data.date ? new Date(data.date).getFullYear() : NaN;
  const year = Number.isFinite(parsedYear) ? parsedYear : undefined;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f4f2ee"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverTitle}>{title}</h1>
          {title !== bride && <p className={s.coverArtist}>Pameran tunggal {bride}{curator && <span> · kurator {curator}</span>}</p>}
          <p className={s.coverDate}>{formatDate(data.date)}{data.place && ` · ${data.place}`}</p>
          <div className={s.label}>
            <div className={s.guest}>
              <small>Kepada Yth.</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbfaf8" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        light="#f4f2ee"
        dark="#161616"
        demoWishes={[
          { id: "w1", name: "Komunitas Sketsa Kotabaru", attendance: "yes", message: "Selamat atas pameran tunggalnya, Mbak Laras! Kami datang serombongan, sudah tidak sabar melihat seri Garis Surut dari dekat." },
          { id: "w2", name: "Andini Puspitasari, kolektor", attendance: "yes", message: "Karya-karya pantai selatanmu selalu terasa tenang dan jujur. Selamat untuk Laras dan Mas Yudhis, semoga pamerannya ramai." },
          { id: "w3", name: "Bayu, Galeri Rumah Kertas", attendance: "maybe", message: "Masih di Bandung saat pembukaan, tapi pasti mampir sebelum pameran ditutup. Selamat dan sukses!" },
        ]}
        copy={{
          opening: {
            kicker: "Dengan hormat",
            title: "Undangan Pembukaan",
            sub: year ? `Pameran tunggal ${bride}, ${year}` : `Pameran tunggal ${bride}`,
            intro: "Kami mengundang Bapak/Ibu/Saudara/i untuk hadir pada pembukaan pameran ini, menikmati karya bersama, dan berbincang langsung dengan seniman serta kurator. Kehadiran Anda adalah apresiasi yang berarti bagi kami.",
          },
          roles: ["Seniman", "Kurator"],
          couple: ["Di balik pameran", "Seniman & Kurator"],
          count: ["Pintu galeri dibuka dalam", "Menuju Pembukaan"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & tempat", "Jadwal Pameran"],
          story: ["Pengantar kuratorial", "Konsep Pameran"],
          gallery: ["Karya pilihan", "Yang Dipamerkan"],
          wishes: ["Buku tamu", "Kesan & Konfirmasi"],
          gifts: ["Katalog pameran", "Pesan Katalog"],
          closing: {
            thanks: "Sampai jumpa di galeri",
            text: "Terima kasih atas perhatian dan kehadiran Bapak/Ibu/Saudara/i. Kami menantikan percakapan di depan karya-karya ini.",
            salam: "Salam budaya",
          },
          sent: "Terima kasih, kesan Anda sudah tercatat di buku tamu.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan kesan, harapan, atau ucapan untuk seniman…",
          closedNote: "Terima kasih sudah datang. Kesan dan pesan masih bisa ditulis di buku tamu ini.",
          giftIntro: "Katalog pameran edisi terbatas (120 halaman, esai kuratorial dan seluruh karya) dapat dipesan seharga Rp150.000 melalui transfer berikut, lalu diambil di meja resepsionis galeri.",
          familyLabel: null,
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroTitle}>{title}</h1>
            <p className={s.heroBy}>{bride}{curator && <span> · kurator {curator}</span>}</p>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {heroSrc && (
              <div className={s.spot}>
                <span className={s.spotLamp} aria-hidden />
                <div className={s.frame}><div><div className={s.heroPhoto}><Photo src={heroSrc} alt={`Karya ${bride}`} /></div></div></div>
                <p className={s.wallLabel}><strong>{bride}</strong><em>{title}</em><span>{year ? `${year} · ` : ""}{data.place || label}</span></p>
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden />,
          closingEmblem: <div className={s.closingEmblem} aria-hidden><Art name="karya-2" /></div>,
          sentArt: <Art name="karya-2" />,
        }}
      />
    </ThemeShell>
  );
}
