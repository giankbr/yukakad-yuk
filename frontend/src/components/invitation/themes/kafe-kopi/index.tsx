"use client";
// Theme "Kafe Kopi" — kafe kopi yang hangat (desain orisinal, tanpa merek): papan menu kapur berbingkai kayu berisi
// "menu spesial" pasangan (nama, tanggal, tempat), meja bar kayu dengan latte art hati, croissant, biji kopi dan sirih
// gading, kanopi bergaris terakota, serta sirih gading gantung yang berayun. Dilukis cat air + gouache + kapur oleh
// /tmp/pen/art/themes/kafe-kopi.py. Fraunces, Figtree, Caveat Brush.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,600;1,400", "Figtree:wght@400;600;700", "Caveat Brush"];
const Art = makeArt("kafe-kopi", {
  board: [310, 350], counter: [360, 126], cup: [120, 121], beans: [160, 22], bean: [28, 24], pothos: [93, 280],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Selamat datang",
    title: "Kami akan menikah",
    sub: "Mari duduk, pesanan bahagia sedang diseduh",
    intro: "Dengan penuh syukur kami mengundang Bapak/Ibu/Saudara/i untuk hadir di hari bahagia kami. Kehadiran dan doa Anda adalah racikan terbaik yang melengkapi cangkir kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Racikan istimewa", "Kami Berdua"],
  count: ["Sedang diseduh", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Menu hari itu", "Rangkaian Acara"],
  story: ["Dari secangkir kopi", "Kisah Kami"],
  gallery: ["Sudut favorit", "Galeri Foto"],
  wishes: ["Tulis di slip pesanan", "Ucapan & RSVP"],
  gifts: ["Tanda kasih", "Kado Pernikahan"],
  closing: {
    thanks: "Terima kasih",
    text: "Terima kasih sudah mampir ke cerita kami. Sampai jumpa di meja kafe, kopi pertama kami yang traktir.",
  },
  sent: "Pesanan ucapan diterima! Terima kasih banyak.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tulis ucapan dan doa untuk kami berdua…",
};

const WISHES = [
  { id: "w1", name: "Barista Rumah Kopi Kalijaga", attendance: "yes" as const, message: "Dari pelanggan setia jadi pengantin di kafe sendiri! Kami siapkan biji kopi terbaik untuk hari kalian." },
  { id: "w2", name: "Tante Rini & Om Hadi", attendance: "yes" as const, message: "Selamat Kinan dan Bram. Semoga rumah tangga kalian hangat dan harum seperti kopi pagi." },
  { id: "w3", name: "Sasha Paramitha", attendance: "maybe" as const, message: "Masih mengatur jadwal dari Bandung. Doa terbaik untuk kalian berdua, bahagia selalu!" },
];

export default function KafeKopiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const groom = data.couple.groom?.trim();
  const place = data.place?.trim() || data.events[0]?.venue?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f3eadb"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="pothos" eager className={s.vine} />
          <Art name="pothos" eager className={`${s.vine} ${s.vineR}`} />
          <div className={s.board}>
            <Art name="board" eager className={s.boardImg} />
            <div className={s.boardText}>
              <p className={s.kicker}>Menu spesial: {label}</p>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
              <p className={s.menuRow}><span>Tanggal</span><i aria-hidden /><span>{formatDate(data.date)}</span></p>
              {place && <p className={s.menuRow}><span>Tempat</span><i aria-hidden /><span>{place}</span></p>}
            </div>
          </div>
          <Art name="counter" eager className={s.counter} />
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffaf1" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        demoWishes={WISHES}
        light="#e8c9a0"
        dark="#2e1a10"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.window}>
              <span className={s.awning} aria-hidden />
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{data.couple.bride.slice(0, 1)}</span>}</div>
              <span className={s.sill} aria-hidden />
              <Art name="cup" className={s.heroCup} />
            </div>
            <p className={s.heroKicker}>The Wedding of</p>
            <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="beans" className={s.divider} />,
          node: <Art name="bean" />,
          amp: <Art name="bean" />,
          countDecor: <Art name="cup" className={s.countCup} />,
          closingDecor: <Art name="counter" className={s.closingCounter} />,
          closingEmblem: <Art name="cup" className={s.closingEmblem} />,
          sentArt: <Art name="cup" />,
        }}
      />
    </ThemeShell>
  );
}
