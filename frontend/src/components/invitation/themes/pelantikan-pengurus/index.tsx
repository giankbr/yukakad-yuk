"use client";
// Theme "Pelantikan Pengurus" — undangan pelantikan pengurus organisasi (contoh: perhimpunan fiktif PELITA): panggung
// resmi dengan tirai beludru marun berumbai emas, podium jati bersegel emas, dua bendera organisasi berwarna netral
// (tanpa lambang negara atau lambang nyata), pita satin emas, dan piagam undangan berstempel. Penyelenggara tampil
// sebagai potret resmi berpelat nama; kisah berisi perjalanan dan agenda organisasi; tidak ada nuansa pernikahan.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "Old Standard TT:ital,wght@0,400;0,700;1,400", "Imperial Script"];
// Painted by /tmp/pen/art/themes/pelantikan-pengurus.py (velvet is a CSS background).
const Art = makeArt("pelantikan-pengurus", { curtain: [720, 493], stage: [720, 405], seal: [220, 343], ribbon: [340, 45] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam sejahtera bagi kita semua",
    title: "Dengan Hormat",
    sub: "Undangan resmi",
    intro: "Puji syukur kami panjatkan ke hadirat Tuhan Yang Maha Esa. Dengan hormat, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan menyaksikan pelantikan serta serah terima jabatan pengurus masa bakti yang baru.",
  },
  roles: ["Ketua Umum Terpilih", "Ketua Panitia"],
  couple: ["Atas nama organisasi", "Penyelenggara"],
  count: ["Menuju Hari Pelantikan", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Susunan Agenda"],
  story: ["Jejak Langkah", "Perjalanan Organisasi"],
  gallery: ["Dokumentasi", "Kegiatan Kami"],
  wishes: ["Konfirmasi Kehadiran", "Ucapan Selamat"],
  gifts: ["Papan Bunga & Donasi", "Tanda Dukungan"],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas perhatian dan kehadiran Bapak/Ibu/Saudara/i, kami sampaikan terima kasih. Semoga amanah ini membawa manfaat bagi banyak orang.",
  },
  sent: "Terima kasih, ucapan selamat Anda sudah kami terima.",
  attend: { yes: "Hadir", maybe: "Belum Pasti", no: "Berhalangan" },
  wishPlaceholder: "Tuliskan ucapan selamat dan harapan untuk pengurus baru…",
  closedNote: "Terima kasih atas perhatiannya. Ucapan selamat untuk pengurus baru masih bisa dikirim lewat form ini.",
  giftIntro: "Tanpa mengurangi rasa hormat, panitia tidak menerima cendera mata. Ucapan selamat dapat dikirim berupa papan bunga, atau disalurkan sebagai donasi program rumah baca:",
  giftAddressTitle: "Kirim Papan Bunga",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Rumah Baca Pelangi, Kendal", attendance: "yes" as const, message: "Selamat bertugas, Bu Anindya dan seluruh pengurus baru! Kami siap menyambut perpustakaan keliling di Kendal." },
  { id: "w2", name: "Galih Prasetyo (Pengurus 2024–2027)", attendance: "yes" as const, message: "Terima kasih sudah melanjutkan estafet. Semoga amanahnya ringan dijalani dan program digitalisasi koleksi segera terwujud." },
  { id: "w3", name: "Relawan PELITA Magelang", attendance: "maybe" as const, message: "Kami usahakan datang bersama anak-anak kelas menulis. Selamat dilantik, semangat terus menyalakan pelita!" },
];

export default function PelantikanPengurusTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const title = data.eventLabel?.trim() || "Pelantikan Pengurus";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const signer = data.couple.groom?.trim() || data.couple.bride?.trim();
  const signerRole = data.couple.groom?.trim() ? "Ketua Panitia" : "Penyelenggara";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a0710"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="curtain" eager className={s.coverCurtain} />
          <div className={s.coverBody}>
            <p className={s.kicker}>Undangan Resmi</p>
            <h1 className={s.coverTitle}>{title}</h1>
            <Art name="ribbon" eager className={s.coverRibbon} />
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#3f0c19" />Buka Undangan</button>
          </div>
          <Art name="stage" eager className={s.coverStage} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        demoWishes={WISHES}
        light="#ecd38c"
        dark="#5c1324"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <div className={s.piagam}>
              <p className={s.piagamKicker}>Piagam Undangan</p>
              <p className={s.piagamLead}>Dengan hormat mengundang Bapak/Ibu/Saudara/i untuk menghadiri</p>
              <h1 className={s.heroTitle}>{title}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {data.place && <p className={s.heroPlace}>{data.place}</p>}
              {note && <p className={s.heroNote}>{note}</p>}
              {signer && <div className={s.sign}><span>{signer}</span><small>{signerRole}</small></div>}
              <Art name="seal" className={s.heroSeal} />
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="ribbon" className={s.divider} />,
          node: <Art name="seal" />,
          sentArt: <Art name="seal" />,
          closingEmblem: <div className={s.closingSeal}><Art name="seal" /><p>{title}</p></div>,
        }}
      />
    </ThemeShell>
  );
}
