"use client";
// Theme "Lomba Masak" — undangan lomba masak warga (komunitas rekaan) dalam guas ceria: sampul biru kobalt dengan judul
// kuning kunyit, meja masak bertaplak kotak-kotak berisi panci enamel berasap, wajan nasi goreng, talenan dan tumpukan
// sayur, kartu tamu berupa kartu nilai juri. Halaman: celemek tergantung dan kategori lomba, panitia & juri dalam
// bingkai piring, hitung mundur di pengatur waktu dapur, aturan lomba sebagai garis waktu sendok, meja juri di penutup.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Shrikhand", "Nunito:wght@600;700;800;900", "Caveat Brush"];
// Painted by /tmp/pen/art/themes/lomba-masak.py
const Art = makeArt("lomba-masak", {
  dapur: [841, 402], asap: [136, 282], juri: [832, 330], celemek: [220, 328], sayur: [400, 52], sendok: [140, 147],
} as const);

const WISHES = [
  { id: "w1", name: "Tim Dapur Melati (Meja 5)", attendance: "yes" as const, message: "Bumbu nasi goreng rahasia keluarga sudah siap sejak semalam. Tahun ini piala harus mampir ke gang kami!" },
  { id: "w2", name: "Bu Yanti & cucu-cucu", attendance: "maybe" as const, message: "Kami datang menonton dan ikut mencicipi. Semoga semua tim kompak dan masakannya lezat-lezat." },
  { id: "w3", name: "Pak Joko, peserta pemula", attendance: "yes" as const, message: "Pertama kali ikut lomba masak, satu tim dengan anak dan menantu. Doakan tumpengnya tidak miring ya!" },
];

export default function LombaMasakTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const host = data.couple.bride?.trim() || "Panitia";
  const title = data.eventLabel?.trim() || "Lomba Masak";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2c4fa3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.top}>
            <p className={s.tag}>Undangan Lomba</p>
            <p className={s.host}>{host} mengundang</p>
            <h1 className={s.title}>{title}</h1>
            <p className={s.when}>{formatDate(data.date)}</p>
          </div>
          <div className={s.scene} aria-hidden>
            <Art name="dapur" eager />
            <Art name="asap" eager className={s.steam} />
            <Art name="asap" eager className={`${s.steam} ${s.steam2}`} />
          </div>
          <div className={s.score}>
            <p className={s.scoreHead}><span>Kartu Undangan</span>{table && <span>{table}</span>}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
            </div>
            <p className={s.marks} aria-hidden><span>Rasa <b>✓</b></span><span>Tampilan <b>✓</b></span><span>Kreasi <b>✓</b></span></p>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#ffffff"
        dark="#2c4fa3"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Halo, para jago dapur!",
            title: "Nyalakan Kompor, Tunjukkan Masakanmu",
            intro: "Kami mengundang warga, keluarga, dan tetangga untuk ikut lomba masak bersama: daftar sebagai tim peserta, atau datang menonton, menyemangati, lalu ikut mencicipi hidangan di akhir acara.",
          },
          roles: ["Penyelenggara", "Dewan Juri"],
          couple: ["Di balik lomba", "Panitia & Juri"],
          count: ["Siapkan celemekmu", "Menuju Hari Lomba"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat tanggalnya", "Jadwal Kegiatan"],
          story: ["Wajib dibaca peserta", "Aturan & Babak Lomba"],
          gallery: ["Dokumentasi", "Lomba Tahun Lalu"],
          wishes: ["Daftar & pesan", "Konfirmasi Kehadiran"],
          gifts: ["Pendaftaran & donasi", "Biaya Pendaftaran"],
          closing: {
            thanks: "Sampai Jumpa di Dapur!",
            text: "Terima kasih untuk setiap peserta, penonton, juri, dan relawan. Siapa pun juaranya, yang paling penting kita masak dan makan bersama.",
            salam: "Salam hangat, panitia",
          },
          sent: "Siap! Konfirmasi dan pesanmu sudah diterima panitia.",
          attend: { yes: "Peserta", maybe: "Penonton", no: "Berhalangan" },
          wishLabel: "Pesan untuk panitia",
          wishPlaceholder: "Tulis nama tim, kategori lomba, atau pesan untuk panitia…",
          closedNote: "Pendaftaran peserta sudah ditutup. Terima kasih atas antusiasmenya, pesan semangat masih bisa dikirim lewat form ini.",
          giftIntro: "Biaya pendaftaran Rp25.000 per tim, sudah termasuk celemek, paket bahan wajib, dan sertifikat. Sumbangan hadiah atau bahan masakan juga sangat kami hargai:",
          giftAddressTitle: "Sumbangan Hadiah & Bahan",
          guestsLabel: "Jumlah orang",
          familyLabel: null,
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroBand} aria-hidden />
            <p className={s.heroKicker}>{host} mempersembahkan</p>
            <h1 className={s.heroTitle}>{title}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroRow}>
              <Art name="celemek" className={s.heroApron} />
              <div className={s.chips} aria-hidden>
                <span>Nasi Goreng Kreasi</span>
                <span>Tumpeng Mini</span>
                <span>Makan Bersama</span>
              </div>
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sayur" className={s.divider} />,
          node: <Art name="sendok" />,
          portrait: <Art name="sendok" className={s.portraitArt} />,
          closingDecor: <Art name="juri" className={s.closingTable} />,
          closingEmblem: <Art name="celemek" className={s.closingEmblem} />,
          sentArt: <Art name="celemek" />,
        }}
      />
    </ThemeShell>
  );
}
