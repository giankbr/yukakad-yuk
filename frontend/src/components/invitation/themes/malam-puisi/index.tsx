"use client";
// Theme "Malam Puisi" — undangan malam puisi komunitas sastra (bukan pernikahan): panggung kecil kedai-teater dalam
// gouache hangat (tirai marun, untaian bohlam, sorot lampu pada mikrofon antik, kursi kayu, buku catatan, lilin).
// Sampul seperti selebaran acara dengan karcis bergerigi; halaman berganti antara kertas buku bergaris dan panggung
// gelap. Tuan rumah: penyair tamu & komunitas, susunan acara tampil sebagai urutan pembaca, kado menjadi donasi.
// Dilukis oleh /tmp/pen/art/themes/malam-puisi.py.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["IM Fell English:ital@0;1", "Crimson Pro:ital,wght@0,400;0,600;1,400", "Courier Prime:wght@400;700"];
const Art = makeArt("malam-puisi", { mik: [150, 225], lilin: [100, 150], api: [100, 150], buku: [360, 255], garis: [380, 22] } as const);

const WISHES = [
  { id: "w1", name: "Dimas, mahasiswa Sastra", attendance: "yes" as Attendance, message: "Sudah siapkan dua puisi untuk panggung terbuka. Semoga gemetarnya hilang setelah bait pertama." },
  { id: "w2", name: "Bu Ratih, pembaca setia", attendance: "yes" as Attendance, message: "Malam puisi selalu jadi alasan saya keluar rumah di hari Sabtu. Terima kasih sudah menjaga ruang ini tetap hangat." },
  { id: "w3", name: "Kolektif Kata Pinggir, Solo", attendance: "maybe" as Attendance, message: "Kami usahakan datang beramai-ramai. Kalau terlambat, sisakan satu kursi kayu di belakang ya." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Selamat datang",
    title: "Mari Mendengar, Mari Membaca",
    intro: "Kami mengundang Anda untuk satu malam yang pelan: lampu redup, kopi hangat, dan kata-kata yang dibacakan dengan suara sendiri. Datanglah sebagai pendengar, atau bawa puisimu ke panggung terbuka.",
  },
  roles: ["Penyair Tamu", "Komunitas"],
  couple: ["Di atas panggung", "Penyair & Tuan Rumah"],
  count: ["Lampu panggung menyala dalam", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Simpan karcismu", "Waktu & Tempat"],
  story: ["Urutan pembaca", "Susunan Acara"],
  gallery: ["Dokumentasi", "Malam-malam Sebelumnya"],
  wishes: ["Buku tamu", "Konfirmasi & Pesan"],
  gifts: ["Saweran", "Donasi Pustaka Jalanan"],
  closing: { thanks: "Sampai Bertemu di Panggung", text: "Terima kasih telah menjaga puisi tetap dibacakan. Kursi kayu kami menunggu Anda." },
  sent: "Terima kasih, pesan Anda sudah kami selipkan di buku tamu.",
  attend: { yes: "Datang", maybe: "Mungkin", no: "Tidak bisa" },
  wishLabel: "Pesan atau Sebait Puisi",
  wishPlaceholder: "Tulis pesan, harapan, atau sebait puisi pendekmu…",
  guestsLabel: "Jumlah orang",
  closedNote: "Konfirmasi kehadiran sudah ditutup. Pesan dan puisi pendek masih bisa dititipkan lewat form ini.",
  giftIntro: "Acara ini gratis dan terbuka. Bila berkenan, donasi untuk perpustakaan jalanan komunitas dapat dikirim ke:",
  familyLabel: null,
};

export default function MalamPuisiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Malam Puisi";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const poet = data.couple.bride?.trim();
  const host = data.couple.groomFull?.trim() || data.couple.groom?.trim();
  const time = data.events[data.events.length - 1]?.time?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1d1210"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.beam} aria-hidden />
          <div className={s.stageGap} aria-hidden />
          <div className={s.flyer}>
            {host && <p className={s.presents}>{host} mempersembahkan</p>}
            <h1 className={s.title}>{label}</h1>
            {poet && <p className={s.with}>bersama <b>{poet}</b></p>}
            <p className={s.meta}><span>{formatDate(data.date)}</span>{time && <span>{time}</span>}</p>
            <div className={s.ticket}>
              <div className={s.guest}>
                <small>Karcis untuk</small>
                <strong>{guestLabel(data)}</strong>
              </div>
              <p className={s.stub}>{table ? <>{table}</> : <>Masuk<b>Gratis</b></>}</p>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#2b1a14" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        celebrant
        noPhotos
        light="#f0cf8e"
        dark="#2b1a14"
        hero={(
          <header className={s.hero}>
            <Art name="buku" className={s.heroBook} eager />
            <p className={s.heroLabel}>Undangan terbuka</p>
            <h1 className={s.heroTitle}>{label}</h1>
            {poet && <p className={s.heroWith}>bersama <b>{poet}</b>{host && <> &amp; {host}</>}</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="garis" className={s.divider} />,
          node: <Art name="mik" />,
          portrait: <Art name="mik" className={s.portraitArt} />,
          closingEmblem: <span className={s.candle} aria-hidden><Art name="lilin" /><Art name="api" /></span>,
          sentArt: <Art name="lilin" />,
        }}
      />
    </ThemeShell>
  );
}
