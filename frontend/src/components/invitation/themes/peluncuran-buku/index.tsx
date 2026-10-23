"use client";
// Theme "Peluncuran Buku" — undangan peluncuran & diskusi buku bergaya editorial modern. Sampul berupa jaket buku:
// punggung buku navy dengan teks vertikal, judul serif besar (nama penulis), tumpukan buku bersampul kain dengan pena
// bulu di atasnya, dan tanggal besar. Di dalam: panggung diskusi (dua kursi, meja kecil, mikrofon, poster buku, tanaman)
// dengan sorot lampu hangat, kepala bagian bergaya "Bab", pena yang menuliskan garis pembatas. Tuan rumah: penulis +
// penerbit (atau extras.child bila diisi).
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Instrument Serif:ital@0;1", "Hanken Grotesk:ital,wght@0,400;0,500;0,600;0,700;1,400"];
// Painted by /tmp/pen/art/themes/peluncuran-buku.py (paper.webp is a CSS background).
const Art = makeArt("peluncuran-buku", { books: [476, 402], stage: [780, 562], pen: [260, 38], open: [240, 107] } as const);

const WISHES = [
  { id: "w1", name: "Klub Buku Sabtu Sore", attendance: "yes" as const, message: "Kami datang ber-12! Sudah tidak sabar mendengar cerita di balik tokoh Eyang Sumi. Selamat, Mbak Kinanti!" },
  { id: "w2", name: "Rani Pramesti", attendance: "yes" as const, message: "Dari draf ketujuh sampai naik cetak. Bangga sekali bisa menemani naskah ini. Sampai jumpa di panggung." },
  { id: "w3", name: "Dimas, pustakawan SMA 3", attendance: "maybe" as const, message: "Semoga sempat datang. Saya titip pertanyaan: bagaimana cara penulis membagi waktu antara mengajar dan menulis?" },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Undangan Terbuka",
    title: "Sebuah Buku, Sebuah Pertemuan",
    intro: "Dengan gembira kami mengundang Bapak/Ibu/Saudara/i, para pembaca dan sahabat literasi, untuk hadir dalam peluncuran sekaligus diskusi buku terbaru kami. Mari merayakan lahirnya sebuah cerita, berbincang tentang proses di baliknya, dan pulang membawa halaman-halaman baru.",
  },
  roles: ["Penulis", "Penerbit"],
  couple: ["Bab 01", "Di Balik Buku"],
  count: ["Bab 02", "Menuju Peluncuran"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Bab 03", "Waktu & Tempat"],
  story: ["Bab 04", "Perjalanan Naskah"],
  gallery: ["Bab 05", "Dari Sesi Sebelumnya"],
  wishes: ["Bab 06", "Konfirmasi & Pesan"],
  gifts: ["Bab 07", "Pre-order & Donasi Buku"],
  closing: { thanks: "Sampai Jumpa di Halaman Berikutnya", text: "Terima kasih telah menjadi bagian dari perjalanan buku ini. Kehadiran Anda adalah pertemuan dengan pembaca yang paling kami nantikan." },
  sent: "Terima kasih, pesan Anda sudah kami terima.",
  attend: { yes: "Hadir", maybe: "Mungkin", no: "Tidak bisa" },
  wishPlaceholder: "Tulis pesan untuk penulis, atau pertanyaan untuk sesi diskusi…",
  closedNote: "Pendaftaran kursi sudah ditutup. Pesan untuk penulis masih bisa dikirim lewat form ini.",
  giftIntro: "Ingin memiliki bukunya lebih dulu? Pesan edisi bertanda tangan (pre-order), atau kirimkan donasi buku untuk Taman Baca Lereng Merapi melalui:",
  giftAddressTitle: "Kirim Donasi Buku",
  familyLabel: null,
};

function Divider() {
  return <span className={s.divider} aria-hidden><Art name="pen" /></span>;
}

export default function PeluncuranBukuTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Peluncuran Buku";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const host = child ? (child.nickname?.trim() || child.name.trim()) : data.couple.bride;
  const partner = child ? "" : (data.couple.groomFull?.trim() || data.couple.groom?.trim() || "");
  const day = /^\d{4}-\d{2}-(\d{2})/.exec(data.date ?? "")?.[1];
  const time = data.events[0]?.time?.trim();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f4ede1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.spine} aria-hidden><span>{partner || label}</span><b>{host}</b></div>
          <div className={s.jacket}>
            <div className={s.jacketTop}><span>Undangan</span><span>{label}</span></div>
            <p className={s.kicker}>{/diskusi|peluncuran|launch/i.test(label) ? "Peluncuran & Diskusi" : label}</p>
            <h1 className={s.coverNames}>{host}</h1>
            {partner && <p className={s.coverWith}>bersama <em>{partner}</em></p>}
            {note && <p className={s.coverNote}>{note}</p>}
            <Art name="books" eager className={s.coverBooks} />
            <div className={s.coverWhen}>
              {day && <b>{Number(day)}</b>}
              <span>{formatDate(data.date)}{time && <small>{time}</small>}</span>
            </div>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}>Buka Undangan<Lucide icon={ic.mailOpen} size={16} color="#faf6ee" /></button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        copy={COPY}
        demoWishes={WISHES}
        light="#f3d08a"
        dark="#1d2437"
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{host}{partner && <><br /><em>bersama {partner}</em></>}</h1>
            <div className={s.heroStage}><Art name="stage" /></div>
            <p className={s.heroDate}>{formatDate(data.date)}{time && ` · ${time}`}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Divider />,
          node: <Art name="open" />,
          closingDecor: <Art name="books" className={s.closingBooks} />,
          closingEmblem: <Art name="open" className={s.closingBook} />,
          sentArt: <Art name="open" />,
        }}
      />
    </ThemeShell>
  );
}
