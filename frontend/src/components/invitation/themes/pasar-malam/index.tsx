"use client";
// Theme "Pasar Malam" — poster gouache retro pasar malam (desain orisinal): langit malam hijau-biru tua dengan bulan dan
// kabut lampu jingga, bianglala besar bergondola warna-warni, komidi putar berkuda kayu, deretan lapak beratap belang,
// untaian bohlam yang berkedip, dan gulali. Nama bercahaya seperti papan nama, kartu tamu berupa gondola yang berayun;
// potret di dalam gondola, hitung mundur empat gondola kecil, acara di bawah tenda lapak, galeri ala cetakan photobox.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Shrikhand", "Bricolage Grotesque:wght@400;600;700;800"];
// Painted by /tmp/pen/art/themes/pasar-malam.py
const Art = makeArt("pasar-malam", { bianglala: [594, 709], komidi: [440, 424], lapak: [780, 124], lampu: [820, 125], gulali: [138, 313] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam hangat dari pasar malam",
    title: "Naik Bianglala Bersama Kami",
    intro: "Dengan penuh sukacita kami mengundang Bapak/Ibu/Saudara/i untuk merayakan hari pernikahan kami. Lampu sudah dinyalakan, lapak sudah dibuka, tinggal kehadiran dan doa restu Anda yang kami nantikan.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Satu gondola berdua", "Kedua Mempelai"],
  count: ["Bianglala berputar dalam", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Jadwal keramaian", "Waktu & Tempat"],
  story: ["Putaran demi putaran", "Kisah Kami"],
  gallery: ["Foto box", "Galeri Kami"],
  wishes: ["Titip pesan", "Ucapan & Konfirmasi"],
  gifts: ["Tanda kasih", "Amplop Digital"],
  closing: {
    thanks: "Terima Kasih!",
    text: "Sampai jumpa di bawah lampu-lampu pasar malam. Kehadiran dan doa Anda membuat malam kami makin meriah.",
  },
  sent: "Terima kasih! Ucapan Anda sudah tergantung di untaian lampu kami.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tulis ucapan dan doa untuk kedua mempelai…",
};

const WISHES = [
  { id: "w1", name: "Mas Bagus & Mbak Rani", attendance: "yes" as Attendance, message: "Selamat menempuh hidup baru! Kami sudah latihan lempar gelang dari minggu lalu, siap menang hadiah utama." },
  { id: "w2", name: "Geng Semawis Jumat Malam", attendance: "yes" as Attendance, message: "Dari langganan lumpia sampai pelaminan. Bahagia selalu, Tari dan Gilang, semoga rukun seperti gulali yang lengket." },
  { id: "w3", name: "Tante Wulan, Surabaya", attendance: "maybe" as Attendance, message: "Semoga bisa datang. Selamat ya, Nak. Semoga rumah tangga kalian selalu terang dan hangat." },
];

export default function PasarMalamTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0b2029"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="lampu" eager className={s.lampu} />
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.names}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.fair} aria-hidden>
            <Art name="bianglala" eager className={s.wheel} />
            <Art name="lapak" eager className={s.stalls} />
            <Art name="komidi" eager className={s.carousel} />
            <Art name="gulali" eager className={s.gulaliC} />
          </div>
          <div className={s.gondola}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#fff3dc"
        dark="#0f2a36"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="lampu" className={s.heroLampu} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            {hero && <div className={s.heroRing}><div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div></div>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="lampu" className={s.divider} />,
          node: <Art name="gulali" />,
          amp: <Art name="gulali" />,
          portrait: <span className={s.roof} aria-hidden />,
          countDecor: <Art name="lampu" className={s.countLampu} />,
          closingDecor: <Art name="lapak" className={s.closingLapak} />,
          closingEmblem: <Art name="komidi" className={s.closingKomidi} />,
          sentArt: <Art name="gulali" />,
        }}
      />
    </ThemeShell>
  );
}
