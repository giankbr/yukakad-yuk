"use client";
// Theme "Ultah Pemadam" — ulang tahun anak bertema pemadam kebakaran, gouache buku cerita: pos pemadam bata dengan
// pintu lengkung, bendera segitiga dan balon, papan nama si kecil, truk merah bertangga yang keluar dari garasi,
// selang yang menyemprotkan lengkung air, helm merah berlencana bintang untuk usia, pita reflektor, dial pengukur
// tekanan untuk hitung mundur, dan tangga untuk lini masa. Riang, tanpa api menakutkan.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Sniglet:wght@400;800", "Nunito:wght@500;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-pemadam.py (the station is a CSS background).
const Art = makeArt("ultah-pemadam", { truck: [560, 222], helmet: [220, 119], water: [420, 192], divider: [300, 29] } as const);

const WISHES = [
  { id: "w1", name: "Kirana & Bunda", attendance: "yes" as const, message: "Selamat ulang tahun, Kapten Gibran! Kirana sudah siap pakai helm merah. Semoga sehat, makin pintar, dan suka menolong." },
  { id: "w2", name: "Keluarga Om Dika", attendance: "yes" as const, message: "Selamat lima tahun, jagoan! Semoga jadi anak yang berani, baik hati, dan selalu sayang Ayah Bunda." },
  { id: "w3", name: "Tante Mira, Bandung", attendance: "maybe" as const, message: "Maaf belum tentu bisa datang, Sayang. Kadonya menyusul ya. Peluk jauh dari Bandung!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahPemadamTheme(props: ThemeProps) {
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
      background="#a6dcf3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.board}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{names}</h1>
            {age && <p className={s.ageRow}>yang ke-<span className={s.ageHelmet}><Art name="helmet" eager /><b>{age}</b></span></p>}
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
          </div>
          <div className={s.garage} aria-hidden>
            <Art name="water" eager className={s.spray} />
            <Art name="truck" eager className={s.coverTruck} />
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
        dark="#1f2a44"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Panggilan untuk pemadam cilik!",
            title: "Ayo Ikut Pesta Pemadam",
            intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Pakai helm merahmu, kita latihan menyemprot air, naik tangga mini, lalu tiup lilin bersama!`,
          },
          roles: ["Kapten yang Berulang Tahun", "Bersama"],
          couple: ["Kenalan dulu", child ? "Si Kapten Cilik" : "Yang Merayakan"],
          count: ["Siaga", "Menuju Hari Pesta"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Titik kumpul", "Waktu & Tempat"],
          story: ["Catatan tugas", `Cerita ${nick}`],
          gallery: ["Album", "Foto Ceria"],
          wishes: ["Kirim pesan ke pos", "Ucapan & Kehadiran"],
          gifts: ["Tanda sayang", "Kado & Amplop Digital"],
          closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman membuat hari ${names} makin seru. Sampai jumpa di pos pemadam!` },
          sent: "Pesanmu sudah sampai di pos. Terima kasih, Pemadam Cilik!",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa untuk si kecil…",
          closedNote: "Terima kasih sudah ikut merayakan! Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling indah. Bila ingin memberi tanda sayang, dapat melalui:",
          familyLabel: "Dengan sayang,",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Pesta {label}</p>
            <div className={s.heroStage}>
              <Art name="water" className={s.heroSpray} />
              <Art name="truck" className={s.heroTruck} />
              {age && <span className={s.heroHelmet} aria-hidden><Art name="helmet" /><b>{age}</b></span>}
            </div>
            <h1 className={s.heroNames}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="helmet" />,
          amp: <Art name="helmet" />,
          portrait: <Art name="helmet" className={s.portraitArt} />,
          closingDecor: <div className={s.closingTruck} aria-hidden><Art name="truck" /></div>,
          closingEmblem: <Art name="helmet" className={s.closingEmblem} />,
          sentArt: <Art name="helmet" />,
        }}
      />
    </ThemeShell>
  );
}
