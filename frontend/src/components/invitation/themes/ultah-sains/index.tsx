"use client";
// Theme "Ultah Sains" — pesta ulang tahun ilmuwan cilik: halaman buku catatan lab bergaris kotak, meja lab gouache dengan
// labu Erlenmeyer bergelembung, rak tabung reaksi, gunung soda kue yang berbusa merah muda dan kaca pembesar, roket mini
// yang melayang, usia di dalam gelas ukur, monogram di cawan petri, hitung mundur dalam tabung reaksi, doodle atom.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fredoka:wght@500;600;700", "Lexend:wght@400;500;600", "Space Mono:wght@400;700"];
// Painted by /tmp/pen/art/themes/ultah-sains.py (tools/art/themes in the repo).
const Art = makeArt("ultah-sains", {
  bench: [780, 524], rocket: [130, 215], flame: [48, 149], beaker: [150, 176], atom: [120, 106], bubble: [48, 48], divider: [320, 63], flask: [110, 216],
} as const);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

const WISHES = [
  { id: "w1", name: "Kak Bima & Keluarga", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Kayla! Semoga makin pintar, makin penasaran, dan eksperimennya selalu berhasil." },
  { id: "w2", name: "Bu Guru Wulan, TK Pelangi", attendance: "yes" as Attendance, message: "Selamat ulang tahun ke-7, ilmuwan kecil kami. Semoga sehat selalu dan tetap rajin bertanya ya, Nak." },
  { id: "w3", name: "Om Fajar & Tante Mira", attendance: "maybe" as Attendance, message: "Happy birthday, Kayla! Kalau sempat, Om bawakan kit kristal warna-warni. Doa terbaik dari kami." },
];

export default function UltahSainsTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Halo, Ilmuwan Cilik!",
      title: "Ayo Bereksperimen di Pestaku!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Siapkan rasa penasaranmu, kita akan membuat busa, gelembung, dan banyak tawa bersama!`,
    },
    roles: ["Kepala Laboratorium", "Bersama"],
    couple: ["Kenalan dengan Ilmuwannya", child ? "Si Ilmuwan Cilik" : "Yang Merayakan"],
    count: ["Eksperimen Dimulai Dalam", "Hitung Mundur Pesta"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Jadwal Eksperimen", "Waktu & Tempat"],
    story: ["Catatan Lab", `Penemuan ${nick}`],
    gallery: ["Dokumentasi", "Momen Seru"],
    wishes: ["Kirim Hasil Pengamatan", "Ucapan & Kehadiran"],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di laboratorium! Kehadiran dan doa teman-teman adalah campuran paling ajaib untuk ${names}.` },
    wishPlaceholder: `Tuliskan ucapan dan doa untuk ${names}…`,
    sent: "Hasil pengamatan diterima! Terima kasih atas ucapannya.",
    closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
    giftIntro: `Kehadiranmu sudah jadi hadiah terbaik. Jika ingin memberi tanda sayang untuk ${names}, dapat melalui:`,
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#24406e"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.rocketWrap} aria-hidden><Art name="flame" className={s.flame} eager /><Art name="rocket" className={s.rocket} eager /></div>
          <Art name="atom" className={s.atomFloat} eager />
          <p className={s.tape}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          <div className={s.ageRow}>
            {age && <div className={s.beaker}><Art name="beaker" eager /><b>{age}</b></div>}
            <p className={s.ageText}><small>Eksperimen</small><strong>{age ? `Ulang tahun ke-${age}` : "Pesta Ulang Tahun"}</strong></p>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.pass}>
            <p className={s.passHead}><span>Kartu Akses Lab</span><span>No. {age ? String(age).padStart(2, "0") : "01"}</span></p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
          </div>
          <div className={s.bench} aria-hidden>
            <Art name="bubble" className={s.bubble} eager />
            <Art name="bubble" className={s.bubble} eager />
            <Art name="bubble" className={s.bubble} eager />
            <Art name="bench" className={s.benchImg} eager />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffffff"
        dark="#24406e"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="atom" className={s.heroAtom} />
            <p className={s.heroKicker}>Hore! {label}</p>
            <h1 className={s.heroName}>{names}{age ? ` ${age} Tahun` : ""}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="atom" />,
          amp: <Art name="atom" />,
          portrait: <Art name="flask" className={s.portraitArt} />,
          countDecor: <><Art name="bubble" className={s.bubble} /><Art name="bubble" className={s.bubble} /></>,
          closingDecor: <Art name="atom" className={s.closingAtom} />,
          closingEmblem: (
            <div className={s.launch} aria-hidden>
              <Art name="flame" className={s.flame} />
              <Art name="rocket" className={s.rocket} />
            </div>
          ),
          sentArt: <Art name="flask" />,
        }}
      />
    </ThemeShell>
  );
}
