"use client";
// Theme "Ultah Pertama" — ulang tahun pertama si kecil di kamar bayi yang tenang: krem linen, hijau sage, merah muda
// pucat. Boneka beruang karamel berpita sage duduk di rak kayu di samping balok huruf (huruf diketik di atas balok kosong
// sehingga mengeja inisial dan umur anak), kue mungil satu lilin, untaian bola felt, kartu berjahit putus-putus.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Sniglet", "Quicksand:wght@400;500;600;700", "Gochi Hand"];
// Painted by /tmp/pen/art/themes/ultah-pertama.py (tools/art/themes in the repo).
const Art = makeArt("ultah-pertama", { teddy: [300, 401], "block-a": [132, 132], "block-b": [132, 132], "block-c": [132, 132], cake: [220, 243], garland: [640, 104], sprig: [200, 52] } as const);

const WISHES = [
  { id: "w1", name: "Eyang Putri Wicaksono", attendance: "yes" as const, message: "Selamat ulang tahun pertama, cucu Eyang. Tumbuhlah sehat, ceria, dan jadi cahaya bagi keluarga, seperti namamu." },
  { id: "w2", name: "Om Raka & Tante Sinta", attendance: "yes" as const, message: "Setahun yang penuh keajaiban! Selamat untuk si kecil dan Ayah-Ibu yang hebat. Kami bawa kado balok yang paling besar, ya." },
  { id: "w3", name: "Keluarga Bu Wulan", attendance: "maybe" as const, message: "Selamat ulang tahun, Sayang. Semoga selalu sehat, pintar, dan disayang banyak orang. Insyaallah kami mampir." },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahPertamaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun Pertama";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date) ?? 1;
  const initial = (nick.trim()[0] ?? "A").toUpperCase();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const meaning = child?.meaning?.trim();
  const first = age === 1;
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Dengan Penuh Syukur",
      title: first ? "Setahun Penuh Cinta" : `${age} Tahun Penuh Cinta`,
      sub: "langkah kecil, kebahagiaan besar",
      intro: `Rasanya baru kemarin kami menggendongnya pulang. Dengan penuh syukur, kami mengundang Bapak/Ibu/Saudara/i untuk merayakan ${first ? "ulang tahun pertama" : `ulang tahun ke-${age}`} ${names}. Kehadiran dan doa Anda akan menjadi kenangan manis yang kelak kami ceritakan kepadanya.`,
    },
    roles: ["Si Kecil yang Berulang Tahun", "Bersama"] as [string, string],
    couple: ["Kenalan dengan", child ? "Bintang Kecil Kami" : "Yang Merayakan"] as [string, string],
    count: ["Menghitung Hari", first ? "Menuju Lilin Pertama" : "Menuju Hari Bahagia"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Catat Tanggalnya", "Waktu & Tempat"] as [string, string],
    story: ["Bulan demi Bulan", `Setahun ${nick}`] as [string, string],
    gallery: ["Album Kecil", "Momen Manis"] as [string, string],
    wishes: ["Doa untuk Si Kecil", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Sayang", "Kado & Amplop Digital"] as [string, string],
    closing: { thanks: "Terima Kasih", text: `Terima kasih telah menjadi bagian dari tahun pertama ${names}. Doa dan kasih sayang Anda adalah hadiah yang akan ia bawa sepanjang hidupnya.` },
    sent: "Terima kasih, doa manismu sudah sampai.",
    wishPlaceholder: "Tuliskan doa dan harapan untuk si kecil…",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3ebe0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="garland" eager className={s.garland} />
          <p className={s.label}>Undangan {label}</p>
          <h1 className={s.coverName}>{names}</h1>
          <p className={s.coverSub}>{first ? "genap satu tahun" : `genap ${age} tahun`}</p>
          <div className={s.shelf} aria-hidden>
            <Art name="teddy" eager className={s.teddy} />
            <Art name="cake" eager className={s.coverCake} />
            <div className={s.blocks}>
              <span className={s.block}><Art name="block-a" eager /><b>{initial}</b></span>
              <span className={s.block}><Art name="block-c" eager /><b>♥</b></span>
              <span className={s.block}><Art name="block-b" eager /><b>{age}</b></span>
            </div>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.tag}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fbf7f0" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fbf7f0"
        dark="#4a3a30"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.bigOne} aria-hidden><span>{age}</span><Art name="cake" /></div>
            <p className={s.heroKicker}>{first ? "Ulang Tahun Pertama" : label}</p>
            <h1 className={s.heroName}>{child?.name.trim() || names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {meaning && <p className={s.heroMeaning}>{meaning}</p>}
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="sprig" className={s.heroSprig} />
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="block-a" />,
          portrait: <Art name="block-b" className={s.peek} />,
          countDecor: <Art name="garland" className={s.countGarland} />,
          closingDecor: <Art name="garland" className={s.closingGarland} />,
          closingEmblem: <div className={s.teddyWrap} aria-hidden><Art name="teddy" className={s.closingTeddy} /></div>,
          sentArt: <Art name="cake" />,
        }}
      />
    </ThemeShell>
  );
}
