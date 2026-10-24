"use client";
// Theme "Malam Keakraban" — undangan makrab mahasiswa bergaya poster risograf: biru, merah muda neon, kuning, dan toska
// bertumpuk di atas kertas krem dengan raster titik. Sampul berupa poster: judul besar, villa di gunung, api unggun yang
// berkedip dengan lingkaran siluet mahasiswa dan gitar, untaian lampion, dan tiket masuk. Panitia sebagai tuan rumah,
// susunan acara sebagai rundown, iuran sebagai patungan. Bukan undangan pernikahan.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Rubik Mono One", "Space Grotesk:wght@400;500;700", "Gochi Hand"];
// Printed (riso simulation) by /tmp/pen/art/themes/malam-keakraban.py; the lantern string is also a CSS background.
const Art = makeArt("malam-keakraban", { scene: [560, 589], fire: [120, 243], guitar: [110, 103], lantern: [90, 167], divider: [240, 24], sticks: [100, 92] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, angkatan baru!",
    title: "Satu Malam, Satu Angkatan",
    sub: "Kenalan dulu, tugas studio belakangan",
    intro: "Sebelum semester berjalan kencang, ayo naik ke gunung sebentar. Kita nyalakan api unggun, kenalan satu per satu, main games kelompok, dan nyanyi bareng diiringi gitar sampai larut. Kakak tingkat, dosen pembimbing, dan teman seangkatan sudah menunggu.",
  },
  roles: ["Penyelenggara", "Bersama"],
  couple: ["Yang ngajak", "Panitia"],
  count: ["Api unggun dinyalakan dalam", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat ya", "Waktu & Tempat"],
  story: ["Biar nggak ketinggalan", "Rundown Acara"],
  gallery: ["Dokumentasi", "Foto-foto"],
  wishes: ["Daftar ulang", "Konfirmasi & Pesan"],
  gifts: ["Patungan", "Iuran Makrab"],
  closing: { thanks: "Sampai Ketemu di Api Unggun!", text: "Bawa jaket, bawa suara, dan bawa rasa penasaranmu. Satu malam ini bakal jadi cerita angkatan kita bertahun-tahun ke depan." },
  sent: "Sip, kamu sudah terdaftar! Sampai ketemu di bus.",
  attend: { yes: "Ikut!", maybe: "Belum pasti", no: "Absen" },
  wishPlaceholder: "Tulis pesan buat panitia atau request lagu buat sesi gitar…",
  wishLabel: "Pesan & Request Lagu",
  closedNote: "Pendaftaran makrab sudah ditutup. Pesan untuk panitia masih bisa dikirim lewat form ini.",
  giftIntro: "Iuran Rp175.000 per orang sudah termasuk bus pulang-pergi, villa, tiga kali makan, dan kaos angkatan. Transfer ke bendahara:",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Rizky (Maba, Kelompok Cemara)", attendance: "yes" as const, message: "Ikut! Request lagu Kangen Band buat sesi gitar, biar kakak tingkat ikut nyanyi juga." },
  { id: "w2", name: "Kak Dinda, Angkatan 2025", attendance: "yes" as const, message: "Siap jadi mentor kelompok. Maba, jangan lupa bawa jaket, Cangar dinginnya nggak main-main." },
  { id: "w3", name: "Bagus Pratama", attendance: "maybe" as const, message: "Masih nunggu jadwal kerja part-time. Kalau bisa tukar sif, aku nyusul naik motor." },
];

export default function MalamKeakrabanTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Malam Keakraban";
  const words = label.split(/\s+/);
  const title = words.length > 1 ? [words.slice(0, -1).join(" "), words[words.length - 1]] : [label];
  const groom = data.couple.groom?.trim();
  const hosts = [data.couple.bride, groom].filter(Boolean).join(" & ");
  const org = data.couple.brideFull?.trim() || hosts;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const year = (data.date ?? "").slice(0, 4);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1f3478"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverLights} aria-hidden />
          {org && <p className={s.org}>{org}</p>}
          <h1 className={s.title}>
            {title.map(word => <span key={word}>{word}</span>)}
            {/^\d{4}$/.test(year) && <span className={s.year} aria-hidden>{year}</span>}
          </h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.poster} aria-hidden>
            <Art name="scene" eager />
            <Art name="fire" eager className={s.fire} />
          </div>
          <div className={s.ticket}>
            <div className={s.guest}>
              <small>Tiket untuk</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <p className={s.stub} aria-hidden>Tiket<b>01</b>Masuk</p>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
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
        light="#ffffff"
        dark="#2f4fa2"
        hero={(
          <header className={s.hero}>
            {org && <p className={s.heroOrg}>{org}</p>}
            <h1 className={s.heroTitle}>{label}</h1>
            {hosts && <p className={s.heroHosts}>bareng {hosts}</p>}
            <div className={s.dateBlock}><Art name="lantern" /><p>{formatDate(data.date)}</p></div>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.props} aria-hidden><Art name="guitar" /><Art name="lantern" /><Art name="sticks" /></div>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="lantern" />,
          portrait: <Art name="guitar" className={s.portraitArt} />,
          closingEmblem: <div className={s.campfire} aria-hidden><Art name="fire" /><Art name="lantern" /></div>,
          sentArt: <Art name="lantern" />,
        }}
      />
    </ThemeShell>
  );
}
