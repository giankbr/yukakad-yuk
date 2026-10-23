"use client";
// Theme "Piringan Hitam" — an analog jazz-club record: the cover is an original gouache album sleeve (spotlit stage,
// double bass, saxophone, microphone) with a painted vinyl sliding out and spinning; the hero is a wooden turntable
// with the couple's photo as the record label; portraits are labels on spinning discs, events are a Side A / Side B
// tracklist on cream liner notes, the gallery is a crate of square sleeves. Deep navy, mustard and cream. Neutral couple.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Abril Fatface", "Barlow Condensed:wght@500;600;700", "Barlow:ital,wght@0,400;0,600;1,400", "Caveat:wght@500;600"];
// Painted by /tmp/pen/art/themes/piringan-hitam.py (tools/art/themes in the repo).
const Art = makeArt("piringan-hitam", { sleeve: [600, 600], vinyl: [420, 419], arm: [160, 485], wave: [300, 51] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Intro",
    title: "Selamat Datang di Malam Kami",
    intro: "Dengan penuh sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk hadir di malam ketika dua melodi akhirnya dimainkan dalam satu lagu. Kehadiran dan doa baik Anda akan melengkapi iramanya.",
  },
  attend: { maybe: "Mungkin" },
  roles: ["Vokal · Mempelai Wanita", "Melodi · Mempelai Pria"] as [string, string],
  couple: ["Duet Malam Ini", "Kedua Mempelai"] as [string, string],
  count: ["Hitung Mundur", "Sebelum Jarum Diturunkan"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Daftar Lagu", "Rangkaian Acara"] as [string, string],
  story: ["Catatan Sampul", "Kisah Kami"] as [string, string],
  gallery: ["Koleksi Sampul", "Galeri"] as [string, string],
  wishes: ["Lagu Permintaan", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Tanda Kasih", "Amplop Digital"] as [string, string],
  closing: {
    thanks: "Terima Kasih",
    text: "Terima kasih telah menjadi bagian dari lagu kami. Kehadiran dan doa Bapak/Ibu/Saudara/i adalah tepuk tangan paling indah.",
    salam: "Sampai jumpa di lantai dansa.",
  },
  sent: "Terima kasih! Ucapan Anda sudah masuk daftar putar kami.",
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Susilo", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Kinanti & Elang. Semoga rumah tangga kalian selalu seirama, walau sesekali berimprovisasi." },
  { id: "w2", name: "Trio Kamis Malam", attendance: "yes" as const, message: "Kami sudah latihan lagu pertama kalian. Siapkan sepatu dansa!" },
  { id: "w3", name: "Mbak Sinta, Toko Piringan Blok M", attendance: "maybe" as const, message: "Senang sekali piringan itu akhirnya menemukan dua pemilik. Bahagia selalu." },
];

export default function PiringanHitamTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0c1426"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverLabel}>Rekaman {label}</p>
          <div className={s.album}>
            <Art name="vinyl" className={s.albumDisc} eager />
            <div className={s.sleeve}>
              <Art name="sleeve" eager />
              <span className={s.sleeveTag}>Sisi A</span>
              <div className={s.sleeveBar}><p>Live di {data.place?.trim() || "Panggung Kami"}</p></div>
            </div>
          </div>
          <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Diputar khusus untuk Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.music} size={16} color="#16233d" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0c95e"
        dark="#16233d"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <div className={s.deck}>
              <div className={s.platter}>
                <Art name="vinyl" />
                {photo && <div className={s.heroFrame}><Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} /></div>}
              </div>
              <Art name="arm" className={s.heroArm} />
              <span className={s.deckLight} aria-hidden />
              <span className={s.deckKnob} aria-hidden />
            </div>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="wave" className={s.divider} />,
          node: <Art name="vinyl" />,
          amp: <Art name="wave" />,
          portrait: <Art name="vinyl" className={s.portraitVinyl} />,
          countDecor: <><Art name="vinyl" className={s.countDisc} /><Art name="vinyl" className={`${s.countDisc} ${s.countDisc2}`} /></>,
          closingDecor: <span className={s.closingSpot} aria-hidden />,
          closingEmblem: <Art name="wave" className={s.divider} />,
          sentArt: <Art name="vinyl" />,
        }}
      />
    </ThemeShell>
  );
}
