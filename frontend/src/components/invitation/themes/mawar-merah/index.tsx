"use client";
// Theme "Mawar Merah" — pernikahan romantis di atas krem hangat: setumpuk mawar taman merah tua bergaya gouache pekat
// (daun gelap, kuncup menjuntai) tumpah di tepi atas kartu bergaris ganda merah anggur, nama dalam Playfair italik
// tebal, foto berbingkai lengkung dengan rangkaian mawar di sudutnya, potret oval, pita hitung mundur merah anggur.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Playfair Display:ital,wght@0,500;0,600;1,500;1,600", "Lora:ital,wght@0,400;0,600;1,400"];
// Painted by /tmp/pen/art/themes/mawar-merah.py.
const Art = makeArt("mawar-merah", { bank: [780, 485], spray: [380, 360], rose: [200, 199], divider: [440, 83] } as const);

const WISHES = [
  { id: "w1", name: "Ibu Sinta Maharani & Keluarga", attendance: "yes" as const, message: "Selamat berbahagia, Alya dan Dimas. Semoga cinta kalian selalu mekar seperti mawar di taman Batu, dirawat setiap hari." },
  { id: "w2", name: "Teman Kelas Melukis", attendance: "yes" as const, message: "Dari kanvas ke pelaminan! Ikut bahagia sekali. Sampai jumpa di taman, kami bawa vas yang lurus." },
  { id: "w3", name: "Om Bayu & Tante Rini, Surabaya", attendance: "maybe" as const, message: "Kami usahakan datang. Kalau berhalangan, doa terbaik kami menyertai kalian berdua." },
];

export default function MawarMerahTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0];
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6ecdc"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="bank" eager className={s.bank} />
          <div className={s.coverBody}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <Art name="divider" eager className={s.coverDivider} />
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f6e3cc" />Buka Undangan</button>
          </div>
          <Art name="spray" eager className={s.coverSpray} />
          <Art name="spray" eager className={`${s.coverSpray} ${s.coverSprayL}`} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6e3cc"
        dark="#7a1420"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Dengan penuh sukacita",
            title: "Kami Mengundang Anda",
            intro: "Dengan hati yang bersyukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan berbagi kebahagiaan pada hari pernikahan kami. Kehadiran Anda akan menjadi kenangan terindah bagi kami.",
          },
          roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
          couple: ["Dua hati", "Kedua Mempelai"],
          count: ["Menghitung hari", "Menuju Hari Bahagia"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Simpan tanggalnya", "Waktu & Tempat"],
          story: ["Kisah kami", "Mekar Bersama"],
          gallery: ["Galeri", "Momen Bahagia"],
          wishes: ["Ucapan", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah kebahagiaan yang tak ternilai bagi kami berdua dan keluarga." },
          sent: "Terima kasih, ucapan Anda sudah terkirim.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan ucapan dan doa untuk kami berdua…",
          giftIntro: "Kehadiran Anda adalah hadiah terindah. Bila ingin memberi tanda kasih, dapat melalui:",
        }}
        hero={(
          <header className={s.hero}>
            {hero && (
              <div className={s.heroFrame}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <Art name="spray" className={s.heroSpray} />
                <Art name="rose" className={s.heroRose} />
              </div>
            )}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="rose" />,
          amp: <Art name="rose" />,
          portrait: <Art name="rose" className={s.portraitRose} />,
          countDecor: <><Art name="spray" className={`${s.countRose} ${s.countRoseL}`} /><Art name="spray" className={`${s.countRose} ${s.countRoseR}`} /></>,
          closingDecor: <Art name="bank" className={s.closingBank} />,
          sentArt: <Art name="rose" />,
        }}
      />
    </ThemeShell>
  );
}
