"use client";
// Theme "Pesta Teh" — pesta teh sore untuk ulang tahun dewasa: dinding bergaris biru bebek, doily kertas renda yang
// berputar sangat pelan sebagai kartu undangan, mawar cat air, teko dan cangkir porselen biru-putih bertepi emas, dan
// tingkat kue berisi macaron, scone, serta kue mungil di atas taplak renda merah muda.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gilda Display", "Lora:ital,wght@0,400;0,500;0,600;1,400;1,500", "Pinyon Script"];
// Painted by /tmp/pen/art/themes/pesta-teh.py (tools/art/themes in the repo).
const Art = makeArt("pesta-teh", {
  teapot: [420, 334], cup: [280, 146], stand: [320, 400], roses: [420, 242], doily: [560, 560], macaron: [72, 58], sprig: [300, 38],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Teh sudah diseduh, kursi sudah disiapkan",
    title: "Mari minum teh bersama",
    intro: "Dengan hati yang hangat, kami mengundang Bapak/Ibu/Saudara/i untuk hadir di pesta teh sore, merayakan hari istimewa orang yang kami sayangi. Datanglah, duduk sejenak, dan bawa cerita terbaik Anda.",
  },
  roles: ["Yang Berulang Tahun", "Bersama"],
  couple: ["Bintang Sore Ini", "Yang Kami Rayakan"],
  count: ["Sebentar Lagi", "Menuju Jam Minum Teh"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Susunan Jamuan"],
  story: ["Perjalanan Hidup", "Cerita dari Tahun ke Tahun"],
  gallery: ["Album", "Kenangan Manis"],
  wishes: ["Buku Tamu", "Ucapan & Kehadiran"],
  gifts: ["Tanda Kasih", "Kado untuk Beliau"],
  closing: {
    thanks: "Terima kasih",
    text: "Terima kasih telah menjadi bagian dari cerita beliau. Sampai jumpa di meja teh, dan semoga sore itu menjadi kenangan yang manis untuk kita semua.",
  },
  sent: "Terima kasih, ucapan Anda sudah kami simpan di buku tamu.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa terbaik untuk beliau…",
  closedNote: "Terima kasih atas perhatiannya. Ucapan masih bisa dikirim lewat buku tamu ini.",
  giftIntro: "Kehadiran Anda adalah hadiah terbaik. Bila ingin memberi tanda kasih, dapat melalui:",
  familyLabel: "Dengan cinta dari keluarga",
};

const WISHES = [
  { id: "w1", name: "Tante Wiwiek & Om Darmo", attendance: "yes" as Attendance, message: "Selamat ulang tahun ke-60, Ratna sayang. Sehat selalu, tetap secantik mawar di halamanmu. Sampai jumpa di meja teh!" },
  { id: "w2", name: "Murid Piano Angkatan 1998", attendance: "yes" as Attendance, message: "Bu Ratna, terima kasih sudah sabar mengajari kami tangga nada. Selamat ulang tahun, semoga panjang umur dan bahagia." },
  { id: "w3", name: "Ibu-ibu Klub Merangkai Bunga", attendance: "maybe" as Attendance, message: "Mohon maaf bila belum bisa hadir. Doa terbaik untuk Bu Ratna, semoga diberi kesehatan dan kebahagiaan." },
];

export default function PestaTehTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const full = child?.name.trim() || data.couple.brideFull?.trim() || "";
  const age = /(\d{1,3})/.exec(label)?.[1];
  const kicker = age ? `Merayakan ${age} Tahun` : label;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dbe8e6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan Pesta Teh Sore</p>
          <div className={s.doily}>
            <Art name="doily" eager />
            <div className={s.doilyText}>
              <p className={s.doilyAge}>{kicker}</p>
              <h1 className={s.coverNames}>{nick}</h1>
              {full && full !== nick && <p className={s.coverFull}>{full}</p>}
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <Art name="roses" eager className={s.coverRoses} />
          <div className={s.tea} aria-hidden>
            <div className={s.tableTop} />
            <Art name="stand" eager className={s.stand} />
            <Art name="teapot" eager className={s.pot} />
            <span className={s.steam} /><span className={s.steam} />
            <Art name="cup" eager className={s.cup} />
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fbf8f2"
        dark="#2f569b"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroScene} aria-hidden>
              <Art name="stand" className={s.heroStand} />
              <Art name="roses" className={s.heroRoses} />
              <Art name="cup" className={s.heroCup} />
            </div>
            <p className={s.heroAge}>{kicker}</p>
            <h1 className={s.heroNames}>{nick}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="macaron" />,
          portrait: <Art name="roses" className={s.pRoses} />,
          countDecor: <Art name="cup" className={s.countCup} />,
          closingEmblem: <div className={s.clEmblem} aria-hidden><Art name="doily" /><Art name="teapot" /></div>,
          sentArt: <Art name="sprig" />,
        }}
      />
    </ThemeShell>
  );
}
