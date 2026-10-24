"use client";
// Theme "Ultah Polisi" — ulang tahun anak bertema polisi cilik, gouache buku cerita: jalan kota berzebra cross,
// papan nama biru bergaya rambu jalan, lencana bintang emas (generik, tanpa lambang resmi) memuat usia, lampu lalu
// lintas yang berganti merah-kuning-hijau, mobil patroli ramah yang melaju masuk dengan sirene berkedip, kerucut,
// dan peluit. Hitung mundur bergaya lampu lalu lintas, kartu acara bergaya rambu.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One", "Fredoka:wght@500;600;700"];
// Painted by /tmp/pen/art/themes/ultah-polisi.py (the street is a CSS background).
const Art = makeArt("ultah-polisi", { car: [460, 205], badge: [220, 245], light: [100, 280], cone: [110, 140], whistle: [150, 108], divider: [380, 17] } as const);

const WISHES = [
  { id: "w1", name: "Naura & Mama", attendance: "yes" as const, message: "Selamat ulang tahun, Pak Polisi Arkan! Naura sudah siap patroli. Semoga sehat, makin pintar, dan suka menolong teman." },
  { id: "w2", name: "Keluarga Om Bagas", attendance: "yes" as const, message: "Selamat lima tahun, jagoan! Semoga jadi anak yang berani, jujur, dan selalu sayang Ayah Bunda." },
  { id: "w3", name: "Tante Rara, Jakarta", attendance: "maybe" as const, message: "Maaf Tante belum tentu bisa datang, Sayang. Kadonya menyusul ya. Peluk jauh dari Jakarta!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahPolisiTheme(props: ThemeProps) {
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
      background="#9fd3f2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan {label}</p>
          <div className={s.sign}>
            {age && <span className={s.ageBadge}><Art name="badge" eager /><b>{age}</b><small>tahun</small></span>}
            <h1 className={s.coverNames}>{names}</h1>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.ticket}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#1d3a6e" />Buka Undangan</button>
          </div>
          <div className={s.street} aria-hidden>
            <div className={s.light}>
              <Art name="light" eager />
              <span className={`${s.lamp} ${s.lampR}`} />
              <span className={`${s.lamp} ${s.lampY}`} />
              <span className={`${s.lamp} ${s.lampG}`} />
            </div>
            <div className={s.carWrap}>
              <Art name="car" eager className={s.car} />
              <span className={`${s.siren} ${s.sirenR}`} />
              <span className={`${s.siren} ${s.sirenB}`} />
            </div>
            <Art name="cone" eager className={`${s.cone} ${s.coneR}`} />
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
        dark="#1d3a6e"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Panggilan untuk polisi cilik!",
            title: "Ayo Ikut Patroli Pesta",
            intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Pakai topi dan lencanamu, kita belajar rambu, menyeberang di zebra cross, lalu tiup lilin bersama!`,
          },
          roles: ["Polisi Cilik yang Berulang Tahun", "Bersama"],
          couple: ["Kenalan dulu", child ? "Si Polisi Cilik" : "Yang Merayakan"],
          count: ["Siap siaga", "Menuju Hari Pesta"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Titik kumpul patroli", "Waktu & Tempat"],
          story: ["Laporan tugas", `Cerita ${nick}`],
          gallery: ["Album", "Foto Ceria"],
          wishes: ["Kirim pesan ke pos", "Ucapan & Kehadiran"],
          gifts: ["Tanda sayang", "Kado & Amplop Digital"],
          closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman membuat hari ${names} makin seru. Sampai jumpa di titik kumpul patroli!` },
          sent: "Pesanmu sudah diterima di pos. Terima kasih, Polisi Cilik!",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa untuk si kecil…",
          closedNote: "Terima kasih sudah ikut merayakan! Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling indah. Bila ingin memberi tanda sayang, dapat melalui:",
          familyLabel: "Dengan sayang,",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Pesta {label}</p>
            {age ? <span className={s.heroBadge} aria-hidden><Art name="badge" /><b>{age}</b></span> : <span className={s.heroBadge} aria-hidden><Art name="badge" /></span>}
            <h1 className={s.heroNames}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroCones} aria-hidden><Art name="cone" /><Art name="cone" /><Art name="cone" /></div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="cone" />,
          amp: <Art name="badge" />,
          portrait: <Art name="whistle" className={s.portraitWhistle} />,
          closingDecor: <div className={s.closingRoad} aria-hidden><Art name="car" className={s.car} /></div>,
          closingEmblem: <Art name="badge" className={s.closingEmblem} />,
          sentArt: <Art name="badge" />,
        }}
      />
    </ThemeShell>
  );
}
