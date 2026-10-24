"use client";
// Theme "Lomba Catur" — undangan turnamen catur antarwarga yang ceria. Sampul di atas kertas krem berpetak samar: lencana
// undangan, judul grotesk tebal, jam catur analog di samping tanggal, kartu tamu berupa formulir notasi bergaris bermargin
// merah, lalu papan kayu berperspektif dengan bidak boxwood dan eboni; kudanya melompat huruf L. Panitia tampil di bingkai
// petak dijaga bidak, hitung mundur di kotak kayu walnut, jadwal babak di laken hijau, amplop menjadi biaya pendaftaran,
// penutupnya raja yang tumbang di papan.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bricolage Grotesque:wght@600;700;800", "Figtree:wght@400;500;600;700", "Courier Prime:wght@400;700"];
// Painted by /tmp/pen/art/themes/lomba-catur.py
const Art = makeArt("lomba-catur", {
  board: [780, 415], king: [170, 274], "king-d": [170, 272], knight: [170, 258], "knight-l": [170, 258], pawn: [170, 227], "pawn-d": [170, 229], clock: [300, 219],
} as const);

const WISHES = [
  { id: "w1", name: "Pak Hartono, juara bertahan", attendance: "yes" as const, message: "Siap mempertahankan piala! Tapi anak-anak klub pelajar makin berbahaya, jadi saya latihan pembukaan tiap malam." },
  { id: "w2", name: "Nadia, kategori pelajar", attendance: "yes" as const, message: "Daftar bareng tiga teman sekelas. Semoga tahun ini bisa tembus papan satu. Terima kasih panitia!" },
  { id: "w3", name: "Bu Sri, warga RT 04", attendance: "maybe" as const, message: "Saya datang menonton sambil bawa pisang goreng untuk panitia. Semangat semua pemain, main yang sportif ya." },
];

function Board({ className }: { className?: string }) {
  return (
    <div className={className ? `${s.boardWrap} ${className}` : s.boardWrap} aria-hidden>
      <Art name="board" eager className={s.boardImg} />
      <Art name="king" eager className={`${s.pc} ${s.pcKing}`} />
      <Art name="pawn" eager className={`${s.pc} ${s.pcPawn}`} />
      <Art name="pawn-d" eager className={`${s.pc} ${s.pcPawnD}`} />
      <Art name="knight" eager className={`${s.pc} ${s.pcKnight}`} />
    </div>
  );
}

export default function LombaCaturTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const host = data.couple.bride?.trim() || "Panitia";
  const title = data.eventLabel?.trim() || "Lomba Catur";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const d = toDate(data.date);
  const start = data.events[0]?.time?.split(/[–-]/)[0].trim() || (d ? d.toLocaleTimeString("id-ID", { timeZone: "Asia/Jakarta", hour: "2-digit", minute: "2-digit" }) : "");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#234836"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.badge}>Undangan Turnamen</p>
          <p className={s.host}>{host} mengundang</p>
          <h1 className={s.title}>{title}</h1>
          <div className={s.timeRow}>
            <Art name="clock" eager className={s.clockImg} />
            <p className={s.when}><b>{formatDate(data.date)}</b>{start && <span>Mulai {start}</span>}</p>
          </div>
          <div className={s.sheet}>
            <p className={s.sheetHead}><span>Formulir Notasi</span>{table && <span>{table}</span>}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fff6e6" />Buka Undangan</button>
          </div>
          <Board />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#fff6e6"
        dark="#1d1a17"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Halo, para pecatur dan warga!",
            title: "Ayo Adu Strategi",
            intro: "Kami mengundang warga untuk meramaikan turnamen catur antarwarga: daftar sebagai pemain di kategori umum atau pelajar, atau datang sebagai penonton. Satu papan, banyak langkah, dan semangat sportif untuk semua.",
          },
          roles: ["Penyelenggara", "Bekerja sama dengan"],
          couple: ["Di balik papan", "Panitia"],
          count: ["Jam catur sudah berjalan", "Menuju Babak Pertama"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat waktunya", "Hari Pertandingan"],
          story: ["Babak demi babak", "Jadwal Turnamen"],
          gallery: ["Dokumentasi", "Turnamen Sebelumnya"],
          wishes: ["Konfirmasi & pesan", "Daftar Hadir"],
          gifts: ["Pendaftaran & donasi", "Biaya Pendaftaran"],
          closing: {
            thanks: "Sampai Jumpa di Papan!",
            text: "Terima kasih untuk setiap pemain, penonton, dan warga yang ikut membantu. Menang, remis, atau kalah, kita tetap bertetangga.",
            salam: "Salam sportif, panitia",
          },
          sent: "Siap! Konfirmasi dan pesanmu sudah diterima panitia.",
          attend: { yes: "Pemain", maybe: "Penonton", no: "Berhalangan" },
          wishLabel: "Pesan untuk panitia",
          wishPlaceholder: "Tulis kategori (umum/pelajar), nama klub, atau pesan untuk panitia…",
          closedNote: "Pendaftaran pemain sudah ditutup. Terima kasih atas antusiasmenya, pesan semangat masih bisa dikirim lewat form ini.",
          giftIntro: "Biaya pendaftaran Rp25.000 per pemain (pelajar Rp10.000) untuk formulir notasi, konsumsi, dan medali. Donasi warga untuk hadiah juga sangat kami hargai:",
          giftAddressTitle: "Donasi Hadiah",
          familyLabel: null,
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{host} mempersembahkan</p>
            <h1 className={s.heroTitle}>{title}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.chips} aria-hidden>
              <span>Rapid 15+5</span>
              <span>Sistem Swiss</span>
              <span>Umum & Pelajar</span>
            </div>
            <Board />
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="pawn-d" /></span>,
          node: <Art name="pawn" />,
          portrait: <Art name="knight-l" className={s.guard} />,
          countDecor: <Art name="clock" className={s.countClock} />,
          closingDecor: (
            <div className={s.closingBoard} aria-hidden>
              <Art name="board" className={s.boardImg} />
              <Art name="king" className={s.kingW} />
              <Art name="king-d" className={s.kingB} />
            </div>
          ),
          sentArt: <Art name="knight" />,
        }}
      />
    </ThemeShell>
  );
}
