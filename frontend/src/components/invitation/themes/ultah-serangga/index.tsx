"use client";
// Theme "Ultah Serangga" — ulang tahun anak di taman yang cerah: nama si kecil di dalam kaca pembesar raksasa, kepik,
// lebah, kupu-kupu dan siput lucu (gambar orisinal bergaya gouache buku cerita), kartu berbentuk daun, dan hitung mundur
// berupa kepik merah. Gerak riang: sayap mengepak, lebah berdengung, siput merayap pelan.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Chewy", "Quicksand:wght@500;600;700"];
// Painted by /tmp/pen/art/themes/ultah-serangga.py.
const Art = makeArt("ultah-serangga", {
  lens: [420, 480], garden: [720, 212], ladybug: [200, 212], bee: [220, 196], butterfly: [220, 178], snail: [240, 152], sun: [200, 200], sprig: [340, 66],
} as const);

const WISHES = [
  { id: "w1", name: "Nadia & Mama", attendance: "yes" as const, message: "Selamat ulang tahun, Arsya! Nadia sudah siap bawa kaca pembesar. Semoga sehat, makin pintar, dan selalu penasaran." },
  { id: "w2", name: "Keluarga Om Fikri", attendance: "yes" as const, message: "Selamat lima tahun, jagoan kecil. Semoga harimu seceria taman penuh kupu-kupu." },
  { id: "w3", name: "Tante Rani", attendance: "maybe" as const, message: "Maaf belum tentu bisa datang, Sayang. Kadonya sudah Tante siapkan, peluk jauh dari Surabaya!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahSeranggaTheme(props: ThemeProps) {
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
      background="#bfe6f5"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="sun" eager className={s.sun} />
          <div className={s.lensWrap}>
            <div className={s.lensFace}>
              <p className={s.kicker}>Undangan {label}</p>
              <h1 className={s.coverNames}>{names}</h1>
              {age && <p className={s.age}><b>{age}</b>tahun</p>}
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
            <Art name="lens" eager className={s.lensArt} />
            <Art name="bee" eager className={s.bugBee} />
            <Art name="butterfly" eager className={s.bugFly} />
            <Art name="ladybug" eager className={s.bugLady} />
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
          </div>
          <Art name="garden" eager className={s.coverGarden} />
          <Art name="snail" eager className={s.coverSnail} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffffff"
        dark="#2f6f2a"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Halo, para penjelajah cilik!",
            title: "Ayo Berburu Serangga",
            intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Bawa rasa penasaranmu, kita intip kepik, lebah dan kupu-kupu, lalu tiup lilin bersama!`,
          },
          roles: ["Yang Berulang Tahun", "Bersama"],
          couple: ["Kenalan yuk", child ? "Si Penjelajah Cilik" : "Yang Merayakan"],
          count: ["Sebentar lagi", "Menuju Hari Pesta"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat tanggalnya", "Waktu & Tempat"],
          story: ["Daun demi daun", `Cerita ${nick}`],
          gallery: ["Album", "Foto Ceria"],
          wishes: ["Kirim doa terbaik", "Ucapan & Kehadiran"],
          gifts: ["Tanda sayang", "Kado & Amplop Digital"],
          closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman membuat hari ${names} makin ceria. Sampai jumpa di taman!` },
          sent: "Hore! Ucapanmu sudah terkirim. Terima kasih!",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa untuk si kecil…",
          closedNote: "Terima kasih sudah ikut merayakan! Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling indah. Bila ingin memberi tanda sayang, dapat melalui:",
          familyLabel: "Dengan sayang,",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Pesta {label}</p>
            <div className={s.heroLeaf}>
              <Art name="butterfly" className={`${s.heroBug} ${s.heroBugA}`} />
              <Art name="bee" className={`${s.heroBug} ${s.heroBugB}`} />
              <h1 className={s.heroNames}>{names}</h1>
              {age && <span className={s.heroAge} aria-hidden>{age}</span>}
            </div>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="ladybug" />,
          amp: <Art name="ladybug" />,
          portrait: <Art name="ladybug" className={s.portraitArt} />,
          countDecor: <span className={s.countDecor} aria-hidden><Art name="butterfly" /><Art name="bee" /></span>,
          closingDecor: <span className={s.closingGarden} aria-hidden><Art name="garden" /><Art name="snail" /></span>,
          closingEmblem: <Art name="sun" className={s.closingEmblem} />,
          sentArt: <Art name="butterfly" />,
        }}
      />
    </ThemeShell>
  );
}
