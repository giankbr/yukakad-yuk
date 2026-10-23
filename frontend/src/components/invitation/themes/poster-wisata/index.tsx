"use client";
// Theme "Poster Wisata" — a vintage stone-lithograph travel poster of an original Indonesian coast: stepped sky bands,
// a smoking volcano, a two-funnel steamship, an outrigger sail and palm silhouettes. The cover is the poster itself with
// the names on a coral print band, the hero is a second poster with a round travel sticker, the countdown sits under a
// steam-train-on-viaduct panel, events are mini posters with sky bands, photos are postcards with offset print shadows
// and gifts are perforated stamps. Neutral (non-religious) couple.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Big Shoulders Display:wght@700;800;900", "Josefin Sans:ital,wght@0,400;0,600;1,400", "Fraunces:ital,wght@1,400"];
// Painted by /tmp/pen/art/themes/poster-wisata.py (tools/art/themes in the repo).
const Art = makeArt("poster-wisata", { poster: [600, 800], train: [820, 344], waves: [320, 65], palm: [240, 387] } as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Selamat Datang",
    title: "Ikut Berlayar Bersama Kami",
    intro: "Dengan penuh sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk menjadi saksi ketika dua pelancong memulai perjalanan terpanjang mereka: perjalanan hidup bersama.",
  },
  attend: { maybe: "Mungkin" },
  roles: ["Mempelai Wanita", "Mempelai Pria"] as [string, string],
  couple: ["Para Penumpang", "Kedua Mempelai"] as [string, string],
  count: ["Keberangkatan", "Menuju Hari Bahagia"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Rute Perjalanan", "Rangkaian Acara"] as [string, string],
  story: ["Catatan Perjalanan", "Kisah Kami"] as [string, string],
  gallery: ["Kartu Pos", "Galeri Kenangan"] as [string, string],
  wishes: ["Kirim Kabar", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Bekal Perjalanan", "Tanda Kasih"] as [string, string],
  closing: {
    thanks: "Sampai Jumpa",
    text: "Terima kasih atas doa dan kehadiran Bapak/Ibu/Saudara/i. Kehadiran Anda adalah oleh-oleh terindah bagi perjalanan kami.",
    salam: "Sampai bertemu di tepi pantai.",
  },
  sent: "Terima kasih! Kabar dari Anda sudah sampai di dermaga kami.",
  wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
  giftIntro: "Doa restu Anda adalah bekal terbaik. Jika berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Haris", attendance: "yes" as const, message: "Selamat berlayar ke babak baru, Nadine & Arga. Semoga perjalanan kalian selalu tenang ombaknya dan indah pemandangannya." },
  { id: "w2", name: "Klub Ransel Nusantara", attendance: "yes" as const, message: "Akhirnya dua anggota paling rajin kirim kartu pos menikah juga! Kami datang naik kapal cepat." },
  { id: "w3", name: "Tiara & Bima", attendance: "maybe" as const, message: "Sedang di Flores, semoga keburu menyeberang. Bahagia selalu!" },
];

export default function PosterWisataTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto ?? data.couple.groomPhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = /^(\d{4})/.exec(data.date ?? "")?.[1];
  const place = data.place?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6d6b4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.poster}>
            <div className={s.posterTop}><span>{label}</span>{year && <span>{year}</span>}</div>
            <div className={s.posterArt}><Art name="poster" eager /></div>
            <div className={s.posterBand}>
              <p className={s.kicker}>Berlayar ke Pelaminan</p>
              <h1 className={s.coverNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fbf3e2" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fbf3e2"
        dark="#1d4f5c"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <span className={s.heroSky} aria-hidden />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            {photo && (
              <div className={s.heroArt}>
                <div className={s.heroFrame}>
                  <Photo src={photo} alt={`${data.couple.bride} & ${data.couple.groom}`} />
                  {place && <span className={s.heroCaption}>{place}</span>}
                </div>
                <span className={s.sticker} aria-hidden><span>Edisi<b>{year ?? "Cinta"}</b>Istimewa</span></span>
              </div>
            )}
            <Art name="waves" className={s.heroWaves} />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="waves" className={s.divider} />,
          node: <Art name="waves" />,
          amp: <Art name="waves" />,
          portrait: <Art name="palm" className={s.portraitPalm} />,
          countDecor: <div className={s.trainPanel}><Art name="train" /><span>Kereta Bahagia</span></div>,
          closingDecor: <><Art name="palm" className={s.closingPalm} /><Art name="palm" className={s.closingPalm} /></>,
          closingEmblem: <Art name="waves" className={s.divider} />,
          sentArt: <Art name="waves" />,
        }}
      />
    </ThemeShell>
  );
}
