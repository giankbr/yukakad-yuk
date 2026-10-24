"use client";
// Theme "Ultah Pilot" — pesta ulang tahun pilot cilik dalam gouache cerah: langit biru berawan, pesawat baling-baling
// merah bermuka ramah yang menarik spanduk bertuliskan nama, landasan pacu berlampu dengan hanggar, menara kontrol dan
// kantong angin; topi pilot di atas bingkai foto, hitung mundur berupa jam instrumen kokpit, lencana sayap sebagai pembatas.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One", "Fredoka:wght@400;500;600", "Gochi Hand"];
// Painted by /tmp/pen/art/themes/ultah-pilot.py (tools/art/themes in the repo).
const Art = makeArt("ultah-pilot", { pesawat: [380, 202], spanduk: [380, 100], awan: [210, 94], bandara: [560, 240], topi: [220, 139], sayap: [220, 32] } as const);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

const WISHES = [
  { id: "w1", name: "Dek Alea & Keluarga", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Kapten Gibran! Alea sudah siap naik pesawatmu, jangan lupa kuenya ya." },
  { id: "w2", name: "Bu Guru Sinta, KB Pelangi", attendance: "yes" as Attendance, message: "Selamat ulang tahun ke-4, Gibran sayang. Semoga sehat selalu, makin berani, dan terus bermimpi setinggi langit." },
  { id: "w3", name: "Om Dimas & Tante Rara", attendance: "maybe" as Attendance, message: "Happy birthday, Kapten kecil! Doa terbaik dari kami, semoga panjang umur dan selalu ceria." },
];

export default function UltahPilotTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const bannerSize = names.length <= 7 ? 26 : names.length <= 10 ? 20 : 15;
  const copy: ThemeCopy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Halo, Para Penumpang!",
      title: `Kapten ${names} Siap Lepas Landas!`,
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk ikut dalam penerbangan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kencangkan sabuk pengaman, kita terbang bersama ke pesta!`,
    },
    roles: ["Kapten Cilik", "Kopilot"],
    couple: ["Kenalan dengan Kaptennya", child ? "Sang Pilot Cilik" : "Yang Merayakan"],
    count: ["Menara Kontrol", "Hitung Mundur Lepas Landas"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Rencana Penerbangan", "Waktu & Tempat"],
    story: ["Catatan Penerbangan", `Jam Terbang ${nick}`],
    gallery: ["Dokumentasi", "Momen Seru"],
    wishes: ["Pesan untuk Kapten", "Ucapan & Kehadiran"],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di landasan pesta! Kehadiran dan doa teman-teman membuat penerbangan ${names} makin seru.` },
    sent: "Pesan sudah diterima menara kontrol. Terima kasih atas ucapannya!",
    attend: { maybe: "Mungkin" },
    wishLabel: "Ucapan & Doa",
    wishPlaceholder: `Tuliskan ucapan dan doa untuk ${names}…`,
    closedNote: "Terima kasih atas doa dan perhatiannya. Ucapan masih bisa dikirim lewat form ini.",
    giftIntro: `Kehadiranmu sudah jadi hadiah terbaik. Jika ingin memberi tanda sayang untuk ${names}, dapat melalui:`,
    familyLabel: "Salam sayang dari keluarga",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#22427a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="awan" eager className={`${s.cloud} ${s.cloud1}`} />
          <Art name="awan" eager className={`${s.cloud} ${s.cloud2}`} />
          <Art name="awan" eager className={`${s.cloud} ${s.cloud3}`} />
          <p className={s.chip}>Undangan {label}</p>
          <div className={s.flight} aria-hidden>
            <div className={s.banner}>
              <Art name="spanduk" eager className={s.bannerArt} />
              <span className={s.bannerText} style={{ fontSize: bannerSize }}>{names}</span>
            </div>
            <div className={s.plane}>
              <Art name="pesawat" eager className={s.planeArt} />
              <span className={s.prop} />
            </div>
          </div>
          <p className={s.captain}>Kapten</p>
          <h1 className={s.coverName}>{names}</h1>
          <p className={s.age}>{age ? <>ulang tahun ke-<b>{age}</b></> : "berulang tahun!"}</p>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
          </div>
          <div className={s.field2} aria-hidden><Art name="bandara" eager /></div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffffff"
        dark="#22427a"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="topi" className={s.heroCap} />
            <p className={s.heroKicker}>Hore! {label}{age ? ` ke-${age}` : ""}</p>
            <h1 className={s.heroName}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sayap" className={s.divider} />,
          node: <Art name="sayap" />,
          amp: <Art name="sayap" />,
          portrait: <Art name="topi" className={s.portraitCap} />,
          closingEmblem: <div className={s.closingArt} aria-hidden><Art name="awan" className={s.cloudArt} /><Art name="pesawat" className={s.planeArt} /></div>,
          sentArt: <Art name="pesawat" />,
        }}
      />
    </ThemeShell>
  );
}
