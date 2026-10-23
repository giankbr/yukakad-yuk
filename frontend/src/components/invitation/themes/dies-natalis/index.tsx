"use client";
// Theme "Dies Natalis" — undangan dies natalis kampus/sekolah bergaya piagam: perkamen berbingkai garis ganda, lambang
// orisinal (perisai enamel toska, buku terbuka, obor, ombak, laurel emas), angka tahun besar bertekstur foil emas yang
// diambil dari label acara ("Dies Natalis ke-50 ..."), pita satin emas, dan gedung rektorat bermenara jam bergaya gravir.
// Penyelenggara (rektor & ketua panitia) tampil sebagai medali, kisah berisi tonggak sejarah, amplop menjadi donasi alumni.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;0,6..96,600;1,6..96,400", "Libre Caslon Text:ital,wght@0,400;0,700;1,400", "Cormorant SC:wght@500;600;700"];
// Painted by /tmp/pen/art/themes/dies-natalis.py (the foil texture is a CSS background on the number)
const Art = makeArt("dies-natalis", { crest: [240, 288], campus: [760, 347], ribbon: [600, 84], laurel: [220, 27] } as const);

const WISHES = [
  { id: "w1", name: "Ir. Rudy Hartanto (Teknik Kelautan 1984)", attendance: "yes" as const, message: "Bangga pernah ditempa di kampus tepi pantai ini. Selamat Dies Natalis ke-50, semoga terus melahirkan insan maritim yang jujur dan tangguh." },
  { id: "w2", name: "Angkatan Perikanan 2003", attendance: "yes" as const, message: "Kami datang serombongan untuk malam temu alumni. Sampai jumpa di Lapangan Menara Jam, dan selamat setengah abad, almamater!" },
  { id: "w3", name: "Dr. Maya Kusuma (Ekonomi Maritim 1996)", attendance: "maybe" as const, message: "Sedang bertugas di Ambon, semoga bisa menyusul. Terima kasih untuk para dosen yang dulu sabar membimbing kami." },
];

/** "Dies Natalis ke-50 Universitas X" -> { num: "50", inst: "Universitas X" } */
function parseLabel(label: string) {
  const num = /ke[-\u2011\s]?(\d{1,3})/i.exec(label)?.[1];
  const inst = label.replace(/dies\s+natalis/i, "").replace(/ke[-\u2011\s]?\d{1,3}/i, "").replace(/\s+/g, " ").trim();
  return { num, inst };
}

export default function DiesNatalisTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  // Non-breaking hyphen keeps "ke-50" on one line.
  const label = (data.eventLabel?.trim() || "Dies Natalis").replace(/ke-(\d)/gi, "ke\u2011$1");
  const { num, inst } = parseLabel(label);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0f2a2f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="crest" eager className={s.crest} />
          <div className={s.ribbon}><Art name="ribbon" eager /><span>Dies Natalis</span></div>
          {num ? (
            <>
              <p className={`${s.number} ${s.foilText}`} aria-label={`ke-${num}`}>{num}</p>
              <p className={s.ordinal}>Tahun Pengabdian</p>
            </>
          ) : null}
          {inst ? <h1 className={s.inst}>{inst}</h1> : <h1 className={s.titleOnly}>{label}</h1>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guest}>
            <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
            <strong>{guestLabel(data)}</strong>
            {table && <span className={s.table}>{table}</span>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ecd38c" />Buka Undangan</button>
          <Art name="campus" eager className={s.coverCampus} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#ecd38c"
        dark="#173b41"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Salam sejahtera bagi kita semua",
            title: "Dengan Hormat Kami Mengundang",
            intro: `Dalam rangka memperingati ${label}, kami mengundang Bapak/Ibu/Saudara/i, para alumni, mitra, dan sahabat almamater untuk hadir dan merayakan perjalanan pengabdian ini bersama kami.`,
          },
          roles: ["Rektor", "Ketua Panitia"],
          couple: ["Atas nama sivitas akademika", "Penyelenggara"],
          count: ["Menuju puncak perayaan", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Susunan kegiatan", "Agenda Perayaan"],
          story: ["Tonggak sejarah", "Jejak Perjalanan"],
          gallery: ["Dokumentasi", "Kehidupan Kampus"],
          wishes: ["Dari alumni & sahabat", "Ucapan & Konfirmasi"],
          gifts: ["Dana abadi & beasiswa", "Donasi Alumni"],
          closing: {
            thanks: "Terima Kasih",
            text: "Kehadiran dan dukungan Bapak/Ibu/Saudara/i adalah bagian dari perjalanan panjang almamater ini. Sampai jumpa di hari perayaan.",
            salam: "Hormat kami, Panitia Dies Natalis",
          },
          sent: "Terima kasih, ucapan Anda sudah kami terima.",
          attend: { yes: "Hadir", maybe: "Mungkin", no: "Berhalangan" },
          wishPlaceholder: "Tuliskan ucapan atau kenangan Anda untuk almamater…",
          closedNote: "Pendaftaran kehadiran sudah ditutup. Terima kasih, ucapan dan kenangan masih bisa dikirim lewat form ini.",
          giftIntro: "Tanpa mengurangi rasa hormat, alumni dan sahabat yang ingin berbagi dapat berdonasi untuk dana abadi dan beasiswa mahasiswa melalui:",
          familyLabel: null,
        }}
        hero={(
          <header className={s.hero}>
            <Art name="crest" className={s.heroCrest} />
            <p className={s.heroKicker}>{num ? `Dies Natalis ke\u2011${num}` : "Undangan Resmi"}</p>
            {num && <p className={`${s.heroNum} ${s.foilText}`} aria-hidden>{num}</p>}
            <h1 className={s.heroTitle}>{inst || label}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="campus" className={s.heroCampus} />
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="laurel" /></span>,
          node: <Art name="crest" />,
          portrait: <Art name="crest" className={s.seal} />,
          closingDecor: <Art name="campus" className={s.closingCampus} />,
          closingEmblem: <div className={s.closingCrest}><Art name="crest" />{inst && <p>{inst}</p>}</div>,
          sentArt: <Art name="crest" />,
        }}
      />
    </ThemeShell>
  );
}
