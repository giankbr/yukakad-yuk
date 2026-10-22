"use client";
// Theme "Ultah Sirkus" — ulang tahun anak di bawah tenda sirkus bergaris merah-krem: kanopi berlekuk, papan marquee
// berlampu, anjing laut ramah yang menyeimbangkan bola pantai di atas drum, trio balon, popcorn bergaris, karcis
// bersobekan untuk tamu dan acara, tirai beludru merah untuk hitung mundur. Ilustrasi gouache asli, tanpa merek apa pun.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rye", "Nunito Sans:wght@400;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-sirkus.py (tools/art/themes in the repo).
const Art = makeArt("ultah-sirkus", { tent: [560, 526], seal: [300, 507], balloons: [240, 401], popcorn: [189, 309], bunting: [640, 84], star: [96, 91] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Om Fajar", attendance: "yes" as const, message: "Selamat ulang tahun, bintang kecil! Semoga makin sehat, makin pintar, dan selalu jadi anak yang ceria. Kami siap jadi penonton paling heboh!" },
  { id: "w2", name: "Raffa & Bunda", attendance: "yes" as const, message: "Raffa sudah tidak sabar lihat sulapnya! Selamat ulang tahun, semoga semua mimpimu terkabul." },
  { id: "w3", name: "Tante Mira", attendance: "maybe" as const, message: "Maaf belum tentu bisa datang, Sayang. Doa Tante, tumbuh jadi anak salehah yang baik hati dan berani." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

function Divider() {
  return <span className={s.divider} aria-hidden><i /><Art name="star" /><i /></span>;
}

export default function UltahSirkusTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Hadirin Sekalian",
      title: "Pertunjukan Segera Dimulai!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Ada tawa, sulap, balon, dan kue di bawah tenda, kehadiran kalian membuat pertunjukan ini makin meriah!`,
    },
    roles: ["Bintang Pertunjukan", "Bersama"] as [string, string],
    couple: ["Perkenalkan", child ? "Si Bintang Kecil" : "Yang Merayakan"] as [string, string],
    count: ["Tirai Segera Dibuka", "Menuju Hari Pertunjukan"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Jadwal Pertunjukan", "Waktu & Tempat"] as [string, string],
    story: ["Di Balik Layar", `Cerita ${nick}`] as [string, string],
    gallery: ["Album Foto", "Momen Seru"] as [string, string],
    wishes: ["Tepuk Tangan & Doa", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih!", text: `Tepuk tangan, tawa, dan doa teman-teman adalah hadiah paling meriah untuk ${names}. Sampai jumpa di bawah tenda!` },
    sent: "Hore! Ucapanmu sudah sampai. Terima kasih banyak.",
    wishPlaceholder: "Tulis ucapan dan doa untuk si bintang kecil…",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf3e2"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.canopy} aria-hidden />
          <Art name="bunting" eager className={s.bunting} />
          <p className={s.marquee}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.coverAge}>yang ke<span className={s.ageStar}><Art name="star" eager /><b>{age}</b></span>tahun</p>}
          <div className={s.stage} aria-hidden>
            <Art name="balloons" eager className={s.coverBalloons} />
            <Art name="tent" eager className={s.tent} />
            <Art name="seal" eager className={s.coverSeal} />
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.ticket}>
            <div className={s.stub} aria-hidden><small>Karcis</small><b>{age ? String(age).padStart(2, "0") : "01"}</b></div>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fbf1dc" />Masuk ke Tenda</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fbf1dc"
        dark="#2b2140"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="balloons" className={s.heroBalloons} />
            <div className={s.bill}>
              <p className={s.heroKicker}>Pertunjukan Spesial</p>
              <h1 className={s.heroName}>{names}</h1>
              {age && <p className={s.heroAge}>genap <b>{age}</b> tahun</p>}
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
            <Art name="popcorn" className={s.heroPop} />
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="star" />,
          portrait: <Art name="seal" className={s.peek} />,
          countDecor: <Art name="bunting" className={s.countBunting} />,
          closingDecor: <Art name="bunting" className={s.closingBunting} />,
          closingEmblem: <div className={s.finale} aria-hidden><Art name="tent" className={s.finaleTent} /><Art name="balloons" className={s.finaleBalloons} /></div>,
          sentArt: <Art name="popcorn" />,
        }}
      />
    </ThemeShell>
  );
}
