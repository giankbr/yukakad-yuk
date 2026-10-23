"use client";
// Theme "Bakti Sosial" — undangan bakti sosial, donor darah dan cek kesehatan gratis dari sebuah komunitas, bergaya gouache
// hangat: dua tangan membentuk hati berisi palang putih, tenda pos kesehatan bergaris dengan relawan berompi oranye,
// kardus sembako dan papan tetes darah, bendera untai. Sampulnya selebaran dengan papan klip formulir pendaftaran untuk
// tamu. Penyelenggara adalah panitia (bride = komunitas, groom = mitra), kisah berisi alur program, amplop menjadi donasi,
// dan konfirmasi kehadiran berupa pendaftaran relawan atau peserta.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One:wght@400", "Nunito:wght@400;600;700;800", "Patrick Hand:wght@400"];
// Painted by /tmp/pen/art/themes/bakti-sosial.py (paper tile and bunting strip are also CSS backgrounds)
const Art = makeArt("bakti-sosial", { hands: [440, 342], scene: [780, 324], box: [130, 133], drop: [100, 138], person: [140, 279], bunting: [780, 61] } as const);

export default function BaktiSosialTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const host = data.couple.bride?.trim() || "Panitia";
  const title = data.eventLabel?.trim() || "Bakti Sosial";
  const table = tableLabel(data.guestTable);
  const venue = data.events[0]?.venue || data.place;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fff4e4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="bunting" eager className={s.bunting} />
          <p className={s.org}>{host}</p>
          <Art name="hands" eager className={s.hands} />
          <h1 className={s.title}>{title}</h1>
          <div className={s.clip}>
            <div className={s.sheet}>
              <h2>Formulir Undangan</h2>
              <p className={s.line}><small>Untuk</small><strong>{guestLabel(data)}</strong></p>
              {table && <p className={s.line}><small>Pos</small><strong>{table}</strong></p>}
              <p className={s.line}><small>Tanggal</small><strong>{formatDate(data.date)}</strong></p>
              {venue && <p className={s.line}><small>Tempat</small><strong>{venue}</strong></p>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff6ea" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#ffe2a3"
        dark="#4a2219"
        demoWishes={[
          { id: "w1", name: "Dinda (relawan pos registrasi)", attendance: "yes", message: "Siap jaga meja registrasi dari pagi! Tahun lalu antreannya panjang, semoga tahun ini makin banyak yang datang." },
          { id: "w2", name: "Pak Asep, Ketua RT 03", attendance: "yes", message: "Terima kasih sudah memikirkan warga kami. Data penerima sembako RT 03 sudah saya serahkan ke panitia." },
          { id: "w3", name: "Bayu & teman kampus", attendance: "maybe", message: "Kami berlima ingin ikut donor. Kalau jadwal kuliah aman, kami datang pagi-pagi. Semangat panitia!" },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Halo, Orang Baik!",
            title: "Satu Hari untuk Berbagi",
            intro: "Kami mengajak Bapak/Ibu/Saudara/i untuk ikut dalam kegiatan bakti sosial: donor darah, cek kesehatan gratis, dan pembagian sembako bagi warga. Datang sebagai relawan atau peserta, setiap tangan yang hadir sangat berarti.",
          },
          roles: ["Penyelenggara", "Mitra Kegiatan"],
          couple: ["Dari Kami", "Penyelenggara"],
          count: ["Kegiatan dimulai dalam", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat Jadwalnya", "Pos Kegiatan"],
          story: ["Alur Kegiatan", "Program Hari Itu"],
          gallery: ["Dokumentasi", "Kegiatan Sebelumnya"],
          wishes: ["Daftar Sekarang", "Pendaftaran & Pesan"],
          gifts: ["Ikut Berdonasi", "Salurkan Donasi"],
          closing: {
            thanks: "Terima Kasih, Orang Baik!",
            text: "Setiap kantong darah, setiap paket sembako, dan setiap jam yang Anda berikan adalah harapan baru bagi sesama. Sampai jumpa di lokasi!",
            salam: "Salam hangat dari seluruh panitia",
          },
          sent: "Terima kasih! Pendaftaran dan pesanmu sudah kami terima.",
          attend: { yes: "Relawan", maybe: "Peserta", no: "Berhalangan" },
          wishPlaceholder: "Tulis pesan semangat atau pertanyaanmu untuk panitia…",
          closedNote: "Pendaftaran sudah ditutup. Terima kasih atas kepeduliannya, pesan semangat masih bisa dikirim lewat form ini.",
          giftIntro: "Donasi disalurkan untuk paket sembako, kebutuhan pos kesehatan, dan konsumsi pendonor. Berapa pun nilainya, terima kasih sudah ikut berbagi:",
          giftAddressTitle: "Donasi Barang",
          familyLabel: null,
        }}
        hero={(
          <header className={s.hero}>
            <Art name="bunting" className={s.heroBunting} />
            <p className={s.heroOrg}>{host} mengundang</p>
            <h1 className={s.heroTitle}>{title}</h1>
            <Art name="scene" className={s.scene} />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.stickers} aria-label="Kegiatan">
              <span><Art name="drop" />Donor Darah</span>
              <span><Art name="hands" />Cek Kesehatan</span>
              <span><Art name="box" />Sembako</span>
            </div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="drop" /></span>,
          node: <Art name="box" />,
          portrait: <Art name="person" className={s.portraitPerson} />,
          countDecor: <span className={s.countBunting} aria-hidden />,
          closingEmblem: <Art name="hands" className={s.emblem} />,
          sentArt: <Art name="drop" />,
        }}
      />
    </ThemeShell>
  );
}
