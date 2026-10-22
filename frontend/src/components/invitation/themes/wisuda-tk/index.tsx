"use client";
// Theme "Wisuda TK" — pelepasan TK yang digambar dengan krayon & pastel minyak di atas kertas manila: si kecil bertoga
// mini memegang ijazah, matahari bersinar, tas sekolah merah, rumput berbunga, kertas gambar ditempel selotip.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import type { Attendance } from "../kit";
import s from "./styles.module.css";

const FONTS = ["Gochi Hand", "Nunito Sans:wght@400;600;700;800"];
// Painted by /tmp/pen/art/themes/wisuda-tk.py (tools/art/themes in the repo).
const Art = makeArt("wisuda-tk", {
  kid: [377, 603], sun: [300, 307], bag: [240, 282], grass: [760, 161], divider: [300, 22], cap: [200, 150], crayons: [202, 178],
} as const);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 1 && age < 12 ? age : undefined;
}

const WISHES = [
  { id: "w1", name: "Bu Guru Ratna", attendance: "yes" as Attendance, message: "Kirana, Bu Guru bangga sekali! Tetap rajin, suka menolong, dan ceria di SD nanti ya, Nak." },
  { id: "w2", name: "Opa & Oma Lestari", attendance: "yes" as Attendance, message: "Selamat cucu Oma yang pintar. Semoga jadi anak yang sehat, berani, dan selalu senang belajar." },
  { id: "w3", name: "Mama Arka (teman sekelas)", attendance: "maybe" as Attendance, message: "Selamat Kirana! Arka pasti kangen main bareng. Semoga satu SD lagi, ya!" },
];

export default function WisudaTkTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pelepasan TK";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Halo, Bapak/Ibu & Teman-teman",
      title: "Hore, Aku Lulus TK!",
      intro: `Dengan penuh syukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir pada acara ${label} ${names}. Terima kasih kepada Bapak/Ibu guru yang telah membimbing dengan sabar. Doa dan kehadiran Anda akan membuat langkah kecilnya ke SD makin mantap.`,
    },
    roles: ["Lulusan TK", "Bersama"] as [string, string],
    couple: ["Kenalan, Yuk", child ? "Si Kecil yang Lulus" : "Yang Diwisuda"] as [string, string],
    count: ["Hitung Mundur", "Menuju Hari Wisuda"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Catat, Ya", "Waktu & Tempat"] as [string, string],
    story: ["Cerita di TK", `Jejak ${nick}`] as [string, string],
    gallery: ["Album", "Momen di Sekolah"] as [string, string],
    wishes: ["Doa untuk Si Kecil", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di hari wisuda! Kehadiran dan doa Bapak/Ibu adalah bekal paling berharga untuk ${names} melangkah ke SD.` },
    sent: "Yay! Ucapanmu sudah sampai. Terima kasih banyak!",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: `Tulis doa & semangat untuk ${names}…`,
    closedNote: "Terima kasih atas doa dan semangatnya. Ucapan untuk si kecil masih bisa dikirim lewat form ini.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#ecd9a6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="sun" eager className={s.sun} />
          <div className={s.sheet}>
            <span className={s.tape} aria-hidden />
            <span className={s.tape} aria-hidden />
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverName}>{names}</h1>
            <Art name="divider" eager className={s.coverRule} />
            {age && <p className={s.age}>{age} tahun, siap masuk SD!</p>}
            {data.place && <p className={s.place}>{data.place}</p>}
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#fffaf0" />Buka Undangan</button>
          </div>
          <div className={s.stage} aria-hidden>
            <Art name="grass" eager className={s.grass} />
            <Art name="crayons" eager className={s.crayons} />
            <Art name="bag" eager className={s.bag} />
            <Art name="kid" eager className={s.kid} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fffaf0"
        dark="#2d2a4a"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="sun" className={s.sun} />
            <p className={s.heroKicker}>Selamat Lulus!</p>
            <h1 className={s.heroName}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroStage} aria-hidden>
              <Art name="grass" className={s.grass} />
              <Art name="bag" className={s.bag} />
              <Art name="kid" className={s.kid} />
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="cap" />,
          portrait: <Art name="cap" className={s.capPeek} />,
          countDecor: <Art name="crayons" className={s.countCrayons} />,
          closingEmblem: (
            <>
              <p className={s.closingName}>{names}</p>
              <div className={s.closingStage} aria-hidden>
                <Art name="grass" className={s.grass} />
                <Art name="crayons" className={s.crayons} />
                <Art name="bag" className={s.bag} />
                <Art name="kid" className={s.kid} />
              </div>
            </>
          ),
          sentArt: <Art name="sun" />,
        }}
      />
    </ThemeShell>
  );
}
