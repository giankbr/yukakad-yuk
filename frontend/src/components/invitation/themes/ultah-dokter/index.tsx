"use client";
// Theme "Ultah Dokter" — pesta ulang tahun dokter cilik dalam gouache anak bergaris ungu tua: sampul papan klip "Kartu
// Pasien" berisi isian tulisan tangan (nama, umur, diagnosa: ulang tahun!), stetoskop merah yang berayun,
// kotak P3K dan boneka beruang pasien berperban di lantai; kue dengan topper palang merah, hitung mundur di atas plester,
// kartu acara bergaya kartu berobat berlubang, form ucapan bergaya kertas resep.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Baloo 2:wght@600;700;800", "Nunito:wght@400;600;700;800", "Patrick Hand"];
// Painted by /tmp/pen/art/themes/ultah-dokter.py (tools/art/themes in the repo).
const Art = makeArt("ultah-dokter", { teddy: [300, 384], steto: [280, 250], kit: [240, 214], plester: [220, 55], kue: [260, 224] } as const);

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

const WISHES = [
  { id: "w1", name: "Dek Kenzo & Keluarga", attendance: "yes" as Attendance, message: "Selamat ulang tahun, Dokter Syila! Kenzo sudah siap jadi pasien, bawa boneka kelinci yang sakit perut." },
  { id: "w2", name: "Bu Guru Ratna, TK Tunas Bangsa", attendance: "yes" as Attendance, message: "Selamat ulang tahun ke-5, Syila sayang. Semoga sehat selalu, makin pintar, dan tetap suka menolong teman." },
  { id: "w3", name: "Om Bayu & Tante Dina", attendance: "maybe" as Attendance, message: "Happy birthday, Syila! Doa terbaik dari kami, semoga panjang umur dan selalu ceria." },
];

export default function UltahDokterTheme(props: ThemeProps) {
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
      kicker: "Halo, Teman-teman!",
      title: `Dokter ${names} Buka Praktik!`,
      intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Bawa boneka kesayanganmu, kita periksa bersama, pasang plester, lalu tiup lilin!`,
    },
    roles: ["Dokter Cilik", "Bersama"],
    couple: ["Kenalan dengan Dokternya", child ? "Si Dokter Cilik" : "Yang Merayakan"],
    count: ["Klinik Dibuka Dalam", "Hitung Mundur Pesta"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Jadwal Periksa", "Waktu & Tempat"],
    story: ["Catatan Kesehatan", `Tumbuh Sehat Bersama ${nick}`],
    gallery: ["Dokumentasi", "Momen Seru"],
    wishes: ["Tulis Resep Doa", "Ucapan & Kehadiran"],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
    closing: { thanks: "Terima Kasih!", text: `Sampai jumpa di klinik pesta! Kehadiran dan doa teman-teman adalah obat paling manjur untuk ${names}.` },
    sent: "Resep doa sudah diterima. Terima kasih atas ucapannya!",
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
      background="#3f8fc4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.board}>
            <span className={s.clip} aria-hidden />
            <div className={s.sheet}>
              <p className={s.sheetHead}><span>Kartu Pasien</span><span><Lucide icon={ic.heart} size={13} color="#ffffff" />No. {age ? String(age).padStart(2, "0") : "01"}</span></p>
              <p className={s.row}><span>Dokter</span></p>
              <h1 className={s.coverName}>{names}</h1>
              <p className={s.row}><span>Diagnosa</span><b>{age ? `Ulang tahun ke-${age}!` : "Pesta ulang tahun!"}</b></p>
              <p className={s.row}><span>Jadwal</span><b>{formatDate(data.date)}</b></p>
              <p className={s.row}><span>Resep</span><b>Kue, balon &amp; tawa</b></p>
              <span className={s.stamp}>Undangan {label}</span>
              <div className={s.guestWrap}>
                <div className={s.guest}>
                  <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                  <strong>{guestLabel(data)}</strong>
                  {table && <span className={s.table}>{table}</span>}
                </div>
                <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
              </div>
            </div>
          </div>
          <div className={s.floor} aria-hidden>
            <Art name="kit" eager className={s.kit} />
            <Art name="steto" eager className={s.steto} />
            <Art name="teddy" eager className={s.teddy} />
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
        dark="#3b2a4a"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="kue" className={s.heroCake} />
            <p className={s.heroKicker}>Hore! {label}{age ? ` ke-${age}` : ""}</p>
            <h1 className={s.heroName}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="plester" className={s.divider} />,
          node: <Art name="plester" />,
          amp: <Art name="plester" />,
          portrait: <Art name="steto" className={s.portraitArt} />,
          closingEmblem: <div className={s.closingArt} aria-hidden><Art name="kit" /><Art name="teddy" /></div>,
          sentArt: <Art name="kit" />,
        }}
      />
    </ThemeShell>
  );
}
