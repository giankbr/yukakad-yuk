"use client";
// Theme "Gala Dinner" — undangan gala dinner tahunan perusahaan, black tie: biru malam dan hitam dengan emas. Sampul
// berupa lukisan panggung (panel latar bergaris emas, podium, meja trofi, sorot lampu yang menyapu pelan) di atas ruang
// meja bundar, lalu kartu program dengan segel nomor meja. Tuan rumah adalah direksi dan panitia, susunan acara tampil
// sebagai program malam, tanpa amplop. Dilukis oleh /tmp/pen/art/themes/gala-dinner.py. Bukan undangan pernikahan.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Playfair Display:ital,wght@0,500;0,700;1,400;1,500", "Manrope:wght@400;500;600;700;800"];
const Art = makeArt("gala-dinner", { trophy: [260, 316], divider: [320, 29] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan hormat",
    title: "Satu Malam untuk Merayakan Kerja Bersama",
    sub: "Anda diundang sebagai tamu kehormatan",
    intro: "Terima kasih atas dedikasi sepanjang tahun ini. Direksi dan panitia mengundang Bapak/Ibu/Saudara/i untuk hadir dalam jamuan makan malam tahunan, malam penghargaan, dan undian doorprize bersama seluruh keluarga besar perusahaan.",
  },
  roles: ["Tuan Rumah", "Bersama"],
  couple: ["Tuan rumah", "Direksi & Panitia"],
  count: ["Tirai dibuka dalam", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat tanggalnya", "Waktu & Tempat"],
  story: ["Program malam", "Susunan Acara"],
  gallery: ["Dokumentasi", "Momen Gala"],
  wishes: ["RSVP", "Konfirmasi Kehadiran"],
  gifts: ["Doorprize", "Informasi Doorprize"],
  closing: { thanks: "Sampai Jumpa di Ballroom", text: "Kehadiran Anda melengkapi malam penghargaan ini. Mari rayakan pencapaian kita bersama." },
  sent: "Terima kasih, konfirmasi dan pesan Anda sudah diterima panitia.",
  attend: { yes: "Hadir", maybe: "Belum pasti", no: "Tidak hadir" },
  wishLabel: "Pesan untuk Panitia",
  wishPlaceholder: "Tulis pesan, ucapan untuk rekan yang menerima penghargaan, atau pertanyaan untuk panitia…",
  closedNote: "Konfirmasi kehadiran sudah ditutup. Pesan untuk panitia masih bisa dikirim lewat form ini.",
  giftIntro: "Setiap karyawan yang hadir mendapat satu kupon undian saat registrasi.",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Andini, Divisi Keuangan", attendance: "yes" as Attendance, message: "Siap hadir! Selamat untuk tim Operasional yang jadi nominasi Tim Terbaik, kalian layak banget." },
  { id: "w2", name: "Pak Joko, Gudang Cikarang", attendance: "yes" as Attendance, message: "Dua puluh tahun bersama Arkana, terima kasih untuk penghargaannya. Saya datang dengan istri." },
  { id: "w3", name: "Rizal, Tim IT", attendance: "maybe" as Attendance, message: "Masih menunggu jadwal migrasi server. Kalau aman, saya menyusul setelah sesi makan malam." },
];

export default function GalaDinnerTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Gala Dinner";
  const org = data.couple.bride?.trim();
  const note = data.couple.note?.trim();
  const seat = data.guestTable?.trim().replace(/^meja\s*/i, "");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#04060c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.stageWrap} aria-hidden>
            <span className={`${s.beam} ${s.beamL}`} />
            <span className={`${s.beam} ${s.beamR}`} />
          </div>
          <div className={s.programme}>
            {org && <p className={s.org}>{org}</p>}
            <h1 className={s.title}>{label}</h1>
            <p className={s.sub}>Black tie · Jamuan malam</p>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            {data.place && <p className={s.coverPlace}>{data.place}</p>}
          </div>
          <div className={s.invite}>
            <div className={s.guest}>
              <small>Kepada Yth.</small>
              <strong>{guestLabel(data)}</strong>
            </div>
            {seat && <p className={s.seal}><small>Meja</small><b>{seat}</b></p>}
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#06080f" />Buka Undangan</button>
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
        light="#e9cf8e"
        dark="#06080f"
        hero={(
          <header className={s.hero}>
            <Art name="trophy" className={s.heroTrophy} />
            {org && <p className={s.heroOrg}>{org}</p>}
            <h1 className={s.heroTitle}>{label}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="trophy" />,
          portrait: <Art name="trophy" className={s.portraitArt} />,
          closingEmblem: <Art name="trophy" className={s.closeTrophy} />,
          sentArt: <Art name="trophy" />,
        }}
      />
    </ThemeShell>
  );
}
