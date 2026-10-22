"use client";
// Theme "Ultah Samudra" — a kids' birthday under the sea in chunky gouache with a crayon contour (original designs): a
// round yellow submarine with brass portholes bobbing and trailing bubbles, a friendly coral octopus in a party hat,
// striped and spotted fish swimming across, kelp swaying over a seabed with a treasure chest. The page dives deeper
// as you scroll (water darkens), sections carry depth tags, events are punched dive tickets, the countdown is bubbles.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Chewy", "Nunito:wght@500;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-samudra.py (tools/art/themes in the repo).
const Art = makeArt("ultah-samudra", {
  sub: [560, 354], octopus: [420, 436], fish: [150, 83], fish2: [140, 108], bubble: [72, 71], kelp: [120, 430], seabed: [780, 171], divider: [210, 56],
} as const);

const WISHES = [
  { id: "w1", name: "Tante Dewi & Kak Bella", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Kapten Arka! Semoga makin pintar, sehat, dan berani menjelajah dunia seperti penjelajah samudra." },
  { id: "w2", name: "Bu Guru Ratna (TK Bintang Laut)", attendance: "yes" as Attendance, message: "Selamat ulang tahun yang ke-6, Arka sayang. Tetap rajin bertanya dan suka menolong teman, ya." },
  { id: "w3", name: "Keluarga Om Rudi", attendance: "maybe" as Attendance, message: "Maaf kami belum tentu bisa datang. Selamat ulang tahun, Arka, semoga semua mimpimu terwujud!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahSamudraTheme(props: ThemeProps) {
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
      kicker: "Kedalaman 0 m",
      title: "Ayo Menyelam Bersama!",
      intro: `Kapal selam kuning sudah siap berangkat! ${names} mau merayakan ${label.toLowerCase()}${age ? ` yang ke-${age}` : ""} di dasar laut, bersama ikan-ikan, gurita ramah, dan peti harta karun. Ajak senyum terbaikmu dan ikut menyelam bersama kami, ya!`,
    },
    roles: ["Yang Berulang Tahun", "Bersama"],
    couple: ["Kedalaman 5 m", child ? "Kapten Kapal Selam" : "Yang Merayakan"],
    count: ["Kedalaman 10 m", "Hitung Mundur Menyelam"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Kedalaman 20 m", "Waktu & Tempat Pesta"],
    story: ["Kedalaman 30 m", `Petualangan ${nick}`],
    gallery: ["Kedalaman 40 m", "Album Bawah Laut"],
    wishes: ["Kedalaman 50 m", "Pesan dalam Botol"],
    gifts: ["Peti Harta Karun", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di dasar laut! Kehadiran dan doa teman-teman adalah harta karun paling berharga untuk ${names}.` },
    sent: "Hore, pesan dalam botolmu sudah sampai! Terima kasih banyak.",
    wishPlaceholder: `Tulis ucapan & doa untuk ${nick}…`,
    giftIntro: "Kehadiran teman-teman sudah jadi harta karun terbesar. Jika ingin memberi tanda sayang, bisa melalui:",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#bff0f0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.rays} aria-hidden />
          <span className={s.gauge} aria-hidden />
          <Art name="fish" eager className={s.fishA} />
          <Art name="fish2" eager className={s.fishB} />
          <Art name="bubble" eager className={`${s.bubbleUp} ${s.bu1}`} />
          <Art name="bubble" eager className={`${s.bubbleUp} ${s.bu2}`} />
          <Art name="bubble" eager className={`${s.bubbleUp} ${s.bu3}`} />
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.ageRow}>ulang tahun ke <span className={s.age}>{age}</span></p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.ticket}>
            <span>Tiket Menyelam</span>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Ayo Menyelam!</button>
          <div className={s.stage} aria-hidden>
            <div className={s.subBox}>
              <Art name="bubble" eager className={s.trail} />
              <Art name="bubble" eager className={`${s.trail} ${s.t2}`} />
              <Art name="bubble" eager className={`${s.trail} ${s.t3}`} />
              <Art name="sub" eager className={s.sub} />
            </div>
            <Art name="kelp" eager className={s.coverKelp} />
            <Art name="octopus" eager className={s.coverOcto} />
            <Art name="seabed" eager className={s.seabed} />
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
        dark="#1f3550"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="fish" className={s.heroFish} />
            <Art name="octopus" className={s.heroOcto} />
            <p className={s.heroKicker}>Hore, {label.toLowerCase()}!</p>
            <h1 className={s.heroName}>{names}{age && <span className={s.heroAge}>{age} Tahun</span>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="bubble" />,
          portrait: <><Art name="fish" className={s.portraitFish} /><Art name="bubble" className={`${s.portraitBubble} ${s.pb1}`} /><Art name="bubble" className={`${s.portraitBubble} ${s.pb2}`} /></>,
          countDecor: <><Art name="fish" className={`${s.countFish} ${s.cf1}`} /><Art name="fish2" className={`${s.countFish} ${s.cf2}`} /></>,
          closingEmblem: (
            <>
              <p className={s.closingName}>{names}</p>
              <div className={s.closingStage} aria-hidden>
                <Art name="sub" className={s.closingSub} />
                <Art name="kelp" className={`${s.closingKelp} ${s.ck1}`} />
                <Art name="kelp" className={`${s.closingKelp} ${s.ck2}`} />
                <Art name="seabed" className={s.closingSeabed} />
              </div>
            </>
          ),
          sentArt: <Art name="octopus" />,
        }}
      />
    </ThemeShell>
  );
}
