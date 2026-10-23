"use client";
// Theme "Turnamen Futsal" — undangan turnamen futsal antarwarga bergaya poster olahraga gouache. Sampul dibuka dengan papan
// skor LED berisi tanggal dan jam kick-off, judul turnamen bertipe kondensasi tebal, lapangan indoor berperspektif
// (permukaan biru, area luar oranye, garis putih, gawang) dengan bola yang memantul di titik tengah, dan kartu ID tamu
// bertali. Penyelenggara tampil di jersey, jadwal menjadi bagan pertandingan, acara menjadi tiket laga, amplop menjadi
// biaya pendaftaran/donasi, penutupnya piala emas di depan gawang.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Big Shoulders Display:wght@700;800;900", "Barlow:wght@400;500;600;700;800", "VT323:wght@400"];
// Painted by /tmp/pen/art/themes/turnamen-futsal.py
const Art = makeArt("turnamen-futsal", { court: [780, 561], ball: [180, 181], goal: [360, 219], trophy: [200, 236], whistle: [120, 92], jersey: [220, 231] } as const);

const WISHES = [
  { id: "w1", name: "Tim RT 03 Garuda Gang", attendance: "yes" as const, message: "Siap tempur! Tahun ini kami bawa suporter satu gang lengkap dengan galon buat ditabuh. Salam sportif buat semua tim." },
  { id: "w2", name: "Pak Darto, Ketua RT 01", attendance: "yes" as const, message: "Terima kasih panitia sudah mengadakan lagi. Anak-anak RT 01 sudah latihan tiap sore di lapangan masjid." },
  { id: "w3", name: "Ibu-ibu PKK RW 07", attendance: "maybe" as const, message: "Kami bantu jualan es teh dan gorengan di pinggir lapangan, hasilnya untuk kas RW. Semangat semuanya!" },
];

export default function TurnamenFutsalTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const host = data.couple.bride?.trim() || "Panitia";
  const title = data.eventLabel?.trim() || "Turnamen Futsal";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const d = toDate(data.date);
  const parts = d ? d.toLocaleDateString("en-GB", { timeZone: "Asia/Jakarta", day: "2-digit", month: "2-digit", year: "2-digit" }).split("/") : [];
  const digits = parts.length === 3 ? parts : ["--", "--", "--"];
  const kick = data.events[0]?.time?.split(/[–-]/)[0].trim() || (d ? d.toLocaleTimeString("id-ID", { timeZone: "Asia/Jakarta", hour: "2-digit", minute: "2-digit" }) : "--.--");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#070c16"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="court" eager className={s.court} />
          <span className={s.ballShadow} aria-hidden />
          <Art name="ball" eager className={s.ball} />
          <div className={s.board} aria-label={`Kick-off ${formatDate(data.date)} pukul ${kick}`}>
            <p className={s.boardTop}><span>Kick-off {kick}</span><i aria-hidden /></p>
            <div className={s.boardDigits} aria-hidden>
              <span><b>{digits[0]}</b><small>Tgl</small></span>
              <span><b>{digits[1]}</b><small>Bln</small></span>
              <span><b>{digits[2]}</b><small>Thn</small></span>
            </div>
          </div>
          <p className={s.host}>{host}</p>
          <h1 className={s.title}>{title}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.pass}>
            <span className={s.passLabel}>Undangan Resmi</span>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#16233f" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#ffffff"
        dark="#16233f"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Halo, warga dan para pemain!",
            title: "Ayo Turun ke Lapangan",
            intro: "Kami mengundang seluruh warga untuk meramaikan turnamen futsal antarwarga: daftarkan tim RT-mu, atau datang sebagai penonton dan pendukung. Satu lapangan, banyak tawa, dan semangat sportif untuk semua.",
          },
          roles: ["Penyelenggara", "Didukung oleh"],
          couple: ["Di balik turnamen", "Panitia"],
          count: ["Menuju peluit pertama", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat jadwalnya", "Hari Pertandingan"],
          story: ["Bagan & jadwal", "Jadwal Laga"],
          gallery: ["Dokumentasi", "Turnamen Sebelumnya"],
          wishes: ["Konfirmasi & pesan", "Daftar Hadir"],
          gifts: ["Biaya & donasi", "Pendaftaran Tim"],
          closing: {
            thanks: "Sampai Jumpa di Lapangan!",
            text: "Terima kasih untuk setiap tim, penonton, dan warga yang ikut membantu. Menang atau kalah, kita tetap satu RW.",
            salam: "Salam sportif, panitia",
          },
          sent: "Mantap! Konfirmasi dan pesanmu sudah masuk ke panitia.",
          attend: { yes: "Ikut Tim", maybe: "Penonton", no: "Berhalangan" },
          wishPlaceholder: "Tulis nama tim, yel-yel, atau pesan untuk panitia…",
          closedNote: "Pendaftaran sudah ditutup. Terima kasih atas antusiasmenya, pesan semangat masih bisa dikirim lewat form ini.",
          giftIntro: "Biaya pendaftaran Rp150.000 per tim untuk sewa lapangan, wasit, dan konsumsi. Donasi warga untuk hadiah dan doorprize juga sangat kami hargai:",
          giftAddressTitle: "Donasi Barang",
          familyLabel: null,
        }}
        hero={(
          <header className={s.hero}>
            <Art name="court" className={s.heroCourt} />
            <p className={s.heroKicker}>{host} mempersembahkan</p>
            <h1 className={s.heroTitle}>{title}</h1>
            <Art name="ball" className={s.heroBall} />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.chips} aria-hidden>
              <span><Art name="whistle" />Fair Play</span>
              <span><Art name="ball" />Kompak</span>
              <span><Art name="trophy" />Juara</span>
            </div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="ball" /></span>,
          node: <Art name="ball" />,
          portrait: <Art name="jersey" className={s.jersey} />,
          closingDecor: <Art name="goal" className={s.closingGoal} />,
          closingEmblem: <Art name="trophy" className={s.trophy} />,
          sentArt: <Art name="trophy" />,
        }}
      />
    </ThemeShell>
  );
}
