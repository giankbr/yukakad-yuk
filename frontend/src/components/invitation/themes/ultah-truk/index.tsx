"use client";
// Theme "Ultah Truk" — ulang tahun anak di lokasi proyek: truk jungkit kuning membawa tanah, ekskavator oranye yang
// sedang menggali dan molen biru bergaris, semuanya tersenyum lewat kaca depan (gouache + krayon, desain asli).
// Garis hazard kuning-hitam, rambu belah ketupat, rambu batas kecepatan berisi umur, papan nama tergantung, aspal
// bermarka untuk hitung mundur dan jalan tanah bertapak ban untuk cerita.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Titan One", "Barlow:wght@400;500;600;700", "Barlow Condensed:wght@600;700"];
// Painted by /tmp/pen/art/themes/ultah-truk.py (tools/art/themes in the repo).
const Art = makeArt("ultah-truk", { dump: [440, 282], digger: [400, 267], mixer: [440, 248], cone: [100, 117], road: [640, 156] } as const);

const WISHES = [
  { id: "w1", name: "Kenzo & Mama", attendance: "yes" as const, message: "Selamat ulang tahun, Arkan! Kenzo sudah siap pakai helm proyek. Semoga sehat selalu dan makin pintar ya." },
  { id: "w2", name: "Keluarga Om Bayu", attendance: "yes" as const, message: "Selamat empat tahun, jagoan! Semoga tumbuh jadi anak yang baik hati, kuat, dan suka menolong seperti truk-truk kesayanganmu." },
  { id: "w3", name: "Tante Sinta", attendance: "maybe" as const, message: "Maaf belum tentu bisa datang, Sayang. Peluk jauh dari Tante, semoga semua mimpimu terbangun tinggi." },
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
  return <span className={s.divider} aria-hidden><Art name="cone" /></span>;
}

export default function UltahTrukTheme(props: ThemeProps) {
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
      kicker: "Perhatian, Kru Cilik!",
      title: "Ada Proyek Pesta!",
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Siapkan helm dan semangat: kita gali pasir, susun balok, dan tiup lilin bersama!`,
    },
    roles: ["Mandor Cilik", "Bersama"] as [string, string],
    couple: ["Kenalan Dulu", child ? "Si Mandor Cilik" : "Yang Merayakan"] as [string, string],
    count: ["Mesin Dipanaskan", "Menuju Hari Pesta"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Lokasi Proyek", "Waktu & Tempat"] as [string, string],
    story: ["Jalan Cerita", `Perjalanan ${nick}`] as [string, string],
    gallery: ["Album", "Foto Proyek"] as [string, string],
    wishes: ["Pesan untuk Mandor", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Kiriman Spesial", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih, Kru!", text: `Kehadiran dan doa teman-teman adalah fondasi paling kokoh untuk pesta ${names}. Sampai jumpa di lokasi proyek!` },
    sent: "Siap, laporan diterima! Terima kasih atas ucapannya.",
    wishPlaceholder: "Tulis ucapan dan doa untuk si mandor cilik…",
    giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling seru. Bila ingin memberi tanda sayang, dapat melalui:",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf3df"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.hazardTop} aria-hidden />
          <div className={s.diamond}><span>Awas! Ada Pesta</span></div>
          <p className={s.ageRow}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {age && <p className={s.ageRow}>yang ke<span className={s.speed}>{age}</span>tahun</p>}
          <div className={s.site} aria-hidden>
            <Art name="road" eager className={s.coverRoad} />
            <Art name="dump" eager className={s.coverTruck} />
            <Art name="cone" eager className={s.coverCone} />
            <Art name="cone" eager className={s.coverCone} />
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.ticket}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#2b2b33" />Ayo Mulai Proyek!</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#f5b819"
        dark="#2b2b33"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.sign}>
              <p className={s.heroKicker}>Pesta {label}</p>
              <h1 className={s.heroName}>{names}</h1>
              {age && <p className={s.heroAge}>genap <b>{age}</b> tahun</p>}
              <p className={s.heroDate}>{formatDate(data.date)}</p>
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroSite} aria-hidden>
              <Art name="road" />
              <Art name="digger" className={s.heroDigger} />
              <Art name="mixer" className={s.heroMixer} />
            </div>
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="cone" />,
          portrait: <Art name="digger" className={s.peek} />,
          countDecor: <><Art name="cone" className={s.countCone} /><Art name="cone" className={s.countCone} /></>,
          closingDecor: <><Art name="road" className={s.closingRoad} /><Art name="mixer" className={s.closingMixer} /></>,
          closingEmblem: <Art name="cone" className={s.closingEmblem} />,
          sentArt: <Art name="dump" />,
        }}
      />
    </ThemeShell>
  );
}
