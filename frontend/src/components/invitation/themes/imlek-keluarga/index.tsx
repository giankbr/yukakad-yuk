"use client";
// Theme "Imlek Keluarga" — undangan makan malam reuni Imlek sebuah keluarga (bukan pernikahan). Sampul di atas kertas
// beras krem berbingkai merah: tiga lampion kertas merah bergouache yang berayun pelan, ranting meihua bertinta dengan
// kuntum merah muda, medali kertas gunting (jianzhi) merah dengan huruf 福 emas, salam "Gong Xi Fa Cai", dan kartu tamu
// berupa angpao. Hero: meja bundar reuni dilihat dari atas (ikan utuh, pangsit, mi panjang umur, jeruk) yang berputar
// sangat pelan seperti meja putar. Nomor acara dalam angka Tionghoa, angpao untuk tanda kasih, lampion di penutup.
// Tanpa gambar dewa; tuan rumah adalah keluarga.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Shippori Mincho:wght@400;600;700;800", "Literata:ital,wght@0,400;0,600;1,400", "Ma Shan Zheng"];
// Painted by /tmp/pen/art/themes/imlek-keluarga.py (tools/art/themes in the repo).
const Art = makeArt("imlek-keluarga", {
  lantern: [120, 235], plum: [380, 232], oranges: [210, 154], papercut: [280, 280], table: [340, 337], cloud: [210, 25],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Xin Nian Kuai Le",
    title: "Selamat Tahun Baru Imlek",
    sub: "Tahun 2578 Kongzili",
    intro: "Tahun berganti, dan meja bundar kami kembali menunggu. Dengan penuh sukacita kami mengundang Bapak/Ibu/Saudara/i sekeluarga untuk pulang, bersantap malam reuni bersama, dan menyambut tahun yang baru dalam kehangatan keluarga.",
  },
  // A family hosts; the non-breaking space keeps the two role labels distinct as list keys.
  roles: ["Tuan Rumah", "Tuan Rumah "] as [string, string],
  couple: ["Yang Mengundang", "Keluarga Kami"] as [string, string],
  count: ["Menanti malam tahun baru", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Waktu & Tempat", "Rangkaian Acara"] as [string, string],
  story: ["Dari Tahun ke Tahun", "Tradisi Keluarga"] as [string, string],
  gallery: ["Kenangan", "Galeri Keluarga"] as [string, string],
  wishes: ["Salam Tahun Baru", "Ucapan & Kehadiran"] as [string, string],
  gifts: ["Angpao Digital", "Titip Angpao"] as [string, string],
  closing: {
    thanks: "Gong Xi Fa Cai",
    text: "Terima kasih telah menjadi bagian dari keluarga besar kami. Semoga tahun yang baru membawa kesehatan, rezeki yang lancar, dan kebahagiaan bagi Bapak/Ibu/Saudara/i sekeluarga.",
    salam: "Selamat Tahun Baru Imlek 2578",
  },
  attend: { maybe: "Mungkin" } as Partial<Record<Attendance, string>>,
  sent: "Terima kasih, salam tahun baru Anda sudah kami terima. Gong Xi Fa Cai!",
  wishPlaceholder: "Tuliskan salam dan doa tahun baru untuk keluarga…",
  closedNote: "Terima kasih atas perhatiannya. Salam tahun baru masih bisa dikirim lewat form ini.",
  giftIntro: "Kehadiran Anda adalah berkah terbesar bagi kami. Bagi keluarga yang berhalangan hadir dan ingin menitipkan angpao untuk para cucu, dapat melalui:",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Keluarga Om Hendra Wijaya", attendance: "yes" as Attendance, message: "Gong Xi Fa Cai, Opa dan Oma! Semoga sehat selalu dan panjang umur. Kami sekeluarga pasti datang ke makan malam." },
  { id: "w2", name: "Tante Mei & Om Rudy (Surabaya)", attendance: "yes" as Attendance, message: "Xin nian kuai le! Kami berangkat sore dari Surabaya, sisakan bandeng presto buat kami, ya." },
  { id: "w3", name: "Kevin & Clara (Melbourne)", attendance: "no" as Attendance, message: "Tahun ini belum bisa pulang. Selamat Tahun Baru Imlek, semoga rezeki lancar dan semua sehat. Rindu meja bundar Oma!" },
];

function Lanterns() {
  return (
    <div className={s.lanterns} aria-hidden>
      <span className={s.lanternA}><Art name="lantern" eager /></span>
      <span className={s.lanternB}><Art name="lantern" eager /></span>
      <span className={s.lanternC}><Art name="lantern" eager /></span>
    </div>
  );
}

function Seal({ className, eager }: { className?: string; eager?: boolean }) {
  return (
    <span className={className} aria-hidden>
      <Art name="papercut" eager={eager} />
      <b lang="zh">福</b>
    </span>
  );
}

export default function ImlekKeluargaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Makan Malam Imlek";
  const hosts = [data.couple.bride?.trim(), data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const title = /^keluarga/i.test(hosts) ? hosts : `Keluarga ${hosts}`;
  const note = data.couple.note?.trim();
  const table = tableLabel(data.guestTable);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#efe4cf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Lanterns />
          <Art name="plum" eager className={s.coverPlum} />
          <Seal className={s.medal} eager />
          <p className={s.greet}>Gong Xi Fa Cai</p>
          <p className={s.greetSub}>Selamat Tahun Baru Imlek 2578</p>
          <h1 className={s.coverName}>{title}</h1>
          <p className={s.coverLabel}>{label}</p>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.angpao}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#f4d68a" />Buka Undangan</button>
          <Art name="oranges" eager className={s.coverOranges} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#f4d68a"
        dark="#2a1a14"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="plum" className={s.heroPlum} />
            <p className={s.heroHan} lang="zh">团圆饭</p>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroName}>{title}</h1>
            <div className={s.heroTable} aria-hidden><Art name="table" /></div>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="cloud" className={s.divider} />,
          node: <Art name="oranges" />,
          portrait: <Seal className={s.hostSeal} />,
          countDecor: <span className={s.countLanterns} aria-hidden><Art name="lantern" /><Art name="lantern" /></span>,
          closingDecor: <span className={s.closeLanterns} aria-hidden><span><Art name="lantern" /></span><span><Art name="lantern" /></span><span><Art name="lantern" /></span></span>,
          closingEmblem: <Art name="oranges" className={s.closingEmblem} />,
          sentArt: <Art name="oranges" />,
        }}
      />
    </ThemeShell>
  );
}
