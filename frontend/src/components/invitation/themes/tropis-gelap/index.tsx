"use client";
// Theme "Tropis Gelap" — hutan tropis gelap yang dramatis: lukisan gouache orisinal monstera, daun pisang dan palem
// hijau tua, bunga cenderawasih (strelitzia) dan anthurium, disinari satu berkas cahaya hangat dari kanan atas di latar
// hampir hitam. Sampul berupa lukisan penuh, hero asimetris, bingkai potret berbentuk daun.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;1,400;1,500", "Spectral:ital,wght@0,400;0,600;0,700;1,400"];
// Painted by /tmp/pen/art/themes/tropis-gelap.py (the jungle painting is also a CSS background).
const Art = makeArt("tropis-gelap", { corner: [300, 254], bloom: [332, 460], leaf: [160, 135], divider: [360, 43] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam hangat",
    title: "Di bawah rimbun yang sama",
    sub: "Sebuah undangan pernikahan",
    intro: "Dengan penuh sukacita kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan merayakan hari pernikahan kami. Kehadiran dan doa Anda akan membuat hari itu semakin bermakna.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua yang tumbuh bersama", "Kedua Mempelai"],
  count: ["Menuju hari bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & tempat", "Rangkaian Acara"],
  story: ["Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Potret Kami"],
  wishes: ["Ucapan & kehadiran", "Kirim Ucapan"],
  gifts: ["Tanda kasih", "Kado Digital"],
  closing: {
    thanks: "Terima Kasih",
    text: "Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  sent: "Terima kasih, ucapan Anda sudah kami terima dengan hangat.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
  familyLabel: "Kami yang berbahagia",
};

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Antonius", attendance: "yes" as const, message: "Selamat Kirana dan Damar! Semoga rumah tangga kalian tumbuh rimbun dan teduh seperti kebun yang kalian rawat." },
  { id: "w2", name: "Sekar & Bima", attendance: "yes" as const, message: "Nggak sabar ketemu di Ubud! Siap-siap kami datang paling awal buat lihat senjanya." },
  { id: "w3", name: "Om Ricky Ginting", attendance: "maybe" as const, message: "Semoga bisa terbang ke Bali minggu itu. Bahagia selalu untuk kalian berdua." },
];

function Names({ bride, groom, className }: { bride: string; groom?: string; className: string }) {
  return <h1 className={className}><span>{bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>;
}

export default function TropisGelapTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const kicker = label === "Pernikahan" ? "Undangan Pernikahan" : label;
  const groom = data.couple.groom?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const initials = [data.couple.bride, groom].filter(Boolean).map(name => name!.slice(0, 1)).join("");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#070b09"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverBg} aria-hidden />
          <div className={s.coverInner}>
            <p className={s.kicker}>{kicker}</p>
            <Names bride={data.couple.bride} groom={groom} className={s.coverNames} />
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestBox}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#1b0f06" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        light="#efdcb0"
        dark="#1b0f06"
        hero={(
          <header className={s.hero}>
            <Art name="corner" className={s.heroCorner} />
            <div className={s.heroPhotoWrap}>
              <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`${data.couple.bride}${groom ? ` dan ${groom}` : ""}`} /> : <span className={s.heroMono} aria-hidden>{initials}</span>}</div>
            </div>
            <div className={s.heroLabel}>
              <p className={s.heroKicker}>{kicker}</p>
              <Names bride={data.couple.bride} groom={groom} className={s.heroNames} />
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="leaf" />,
          amp: <Art name="leaf" />,
          portrait: <Art name="leaf" className={s.portraitArt} />,
          closingEmblem: <Art name="bloom" className={s.closingEmblem} />,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
