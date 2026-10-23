"use client";
// Theme "Ultah Putri Duyung" — ulang tahun anak di bawah laut pastel dalam gouache: Nila, putri duyung kecil ciptaan
// sendiri, duduk di batu karang mengangkat mutiara; istana kerang beratap ungu di belakangnya, rumput laut bergoyang,
// gelembung naik, pita ombak pastel. Nama si kecil di atas kartu putih; hitung mundur berupa gelembung di laut dalam.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cherry Swash:wght@400;700", "Fredoka:wght@400;500;600", "Patrick Hand"];
// Painted by /tmp/pen/art/themes/ultah-putri-duyung.py
const Art = makeArt("ultah-putri-duyung", {
  nila: [380, 432], castle: [360, 364], shells: [239, 106], pearl: [120, 120], weed: [113, 403],
} as const);

const WISHES = [
  { id: "w1", name: "Naira & Bunda", attendance: "yes" as const, message: "Selamat ulang tahun, Alesha! Naira sudah siap pakai mahkota kerang. Semoga sehat, ceria, dan makin pintar berenang!" },
  { id: "w2", name: "Keluarga Om Rendra", attendance: "yes" as const, message: "Selamat enam tahun, Sayang. Semoga hatimu selalu secerah mutiara dan seluas lautan." },
  { id: "w3", name: "Tante Mira", attendance: "maybe" as const, message: "Tante usahakan datang ya, Alesha. Bukunya sudah Tante bungkus dengan pita ungu!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahPutriDuyungTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#bfe9ec"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.card}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{names}</h1>
            {age && <p className={s.age}><b>{age}</b>tahun di bawah laut</p>}
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <div className={s.scene} aria-hidden>
            <Art name="castle" eager className={s.castle} />
            <Art name="pearl" eager className={s.pearlFloat} />
            <Art name="pearl" eager className={s.pearlFloat} />
            <Art name="nila" eager className={s.nila} />
            <Art name="weed" eager className={`${s.weed} ${s.weedL}`} />
            <Art name="weed" eager className={`${s.weed} ${s.weedR}`} />
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Ayo Menyelam!</button>
          <span className={s.wave} aria-hidden />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffffff"
        dark="#3b2a52"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Halo, teman-teman laut!",
            title: "Ayo ke Istana Kerang",
            intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Bawa senyum paling cerah, kita bermain air, berburu mutiara, dan tiup lilin bersama!`,
          },
          roles: ["Yang Berulang Tahun", "Bersama"],
          couple: ["Kenalan yuk", child ? "Putri Kecil Hari Ini" : "Yang Merayakan"],
          count: ["Gelembung demi gelembung", "Menuju Hari Pesta"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat tanggalnya", "Waktu & Tempat"],
          story: ["Ombak demi ombak", `Cerita ${nick}`],
          gallery: ["Album", "Foto Ceria"],
          wishes: ["Kirim doa terbaik", "Ucapan & Kehadiran"],
          gifts: ["Tanda sayang", "Kado & Amplop Digital"],
          closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman membuat hari ${names} berkilau seperti mutiara. Sampai jumpa di istana kerang!` },
          sent: "Yay! Ucapanmu sudah terkirim. Terima kasih!",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa untuk si kecil…",
          closedNote: "Terima kasih sudah ikut merayakan! Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling indah. Bila ingin memberi tanda sayang, dapat melalui:",
          familyLabel: "Dengan sayang,",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Pesta {label}</p>
            <div className={s.heroArt}>
              <Art name="shells" />
              {age && <span className={s.heroAge} aria-hidden>{age}</span>}
            </div>
            <h1 className={s.heroNames}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="shells" /></span>,
          node: <Art name="pearl" />,
          portrait: <Art name="weed" className={s.portraitArt} />,
          countDecor: <span className={s.bubbles} aria-hidden><i /><i /><i /><i /></span>,
          closingEmblem: <Art name="castle" className={s.closingCastle} />,
          sentArt: <Art name="shells" />,
        }}
      />
    </ThemeShell>
  );
}
