"use client";
// Theme "Seminar Ilmiah" — undangan seminar & diskusi ilmiah bergaya poster konferensi modern: kertas berpetak halus,
// bilah atas bergaya kop acara, molekul bola-batang yang dilukis guas, judul topik sans tebal rata kiri, tabel fakta
// (tanggal, waktu, tempat) bergaya data, dan dua kartu pembicara. Di dalam: ruang kuliah dengan layar grafik, kartu
// narasumber/moderator horizontal, sesi bertanda warna, hitung mundur sebagai panel data. Tuan rumah = bride (+ groom)
// dengan peran dari copy, atau extras.child bila diisi.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Plus Jakarta Sans:wght@400;500;600;700;800", "Petrona:ital,wght@0,500;1,400;1,500", "Geist Mono:wght@400;500"];
// Painted by /tmp/pen/art/themes/seminar-ilmiah.py.
const Art = makeArt("seminar-ilmiah", { molecule: [420, 355], hall: [700, 422], chart: [412, 49], atom: [120, 81] } as const);

const ROLES: [string, string] = ["Narasumber", "Moderator"];

const WISHES = [
  { id: "w1", name: "Nadia Putri, Teknik Sipil", attendance: "yes" as const, message: "Apakah beton geopolimer sudah diuji untuk iklim pesisir dengan kadar garam tinggi? Ingin tahu data ketahanannya." },
  { id: "w2", name: "Bambang Setiadi, Dinas PUPR", attendance: "yes" as const, message: "Kami tertarik pada skema uji coba di proyek pemerintah daerah. Mohon dibahas juga soal standar SNI-nya." },
  { id: "w3", name: "Kelompok Studi Material Hijau", attendance: "maybe" as const, message: "Kami ikut daring dari Makassar. Semoga sesi poster juga direkam, terima kasih panitia." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Undangan Terbuka",
    title: "Ruang untuk bertanya, berbagi data, dan berdiskusi.",
    intro: "Dengan hormat, kami mengundang Bapak/Ibu/Saudara/i, para akademisi, peneliti, mahasiswa, dan praktisi, untuk hadir dalam seminar dan diskusi ilmiah kami. Mari bertukar temuan, menguji gagasan, dan membuka kolaborasi baru.",
  },
  roles: ROLES,
  couple: ["Pembicara", "Narasumber & Moderator"],
  count: ["Hitung Mundur", "Menuju Hari Seminar"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Jadwal", "Waktu & Tempat"],
  story: ["Tentang Seminar", "Latar & Agenda"],
  gallery: ["Dokumentasi", "Seminar Sebelumnya"],
  wishes: ["Registrasi", "Konfirmasi & Pertanyaan"],
  gifts: ["Registrasi", "Biaya Pendaftaran"],
  closing: { thanks: "Sampai jumpa di ruang seminar.", text: "Terima kasih atas minat dan partisipasi Anda. Setiap pertanyaan yang Anda bawa adalah bagian dari ilmu yang sedang tumbuh." },
  sent: "Terima kasih, konfirmasi dan pertanyaan Anda sudah masuk ke daftar panitia.",
  attend: { yes: "Hadir", maybe: "Ikut daring", no: "Tidak bisa" },
  wishPlaceholder: "Tulis komentar atau pertanyaan untuk narasumber…",
  closedNote: "Pendaftaran peserta sudah ditutup. Komentar dan pertanyaan masih bisa dikirim lewat form ini.",
  giftIntro: "Biaya registrasi Rp75.000 untuk mahasiswa dan Rp150.000 untuk umum, sudah termasuk e-sertifikat, seminar kit, dan makan siang. Pembayaran dapat melalui:",
  giftAddressTitle: "Alamat Panitia",
  familyLabel: null,
};

export default function SeminarIlmiahTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Seminar";
  const topic = data.couple.note?.trim() || label;
  const table = tableLabel(data.guestTable);
  const year = /^(\d{4})/.exec(data.date ?? "")?.[1];
  const first = data.events[0]?.time?.trim();
  const last = data.events[data.events.length - 1]?.time?.trim();
  const span = /^(\d{1,2}[.:]\d{2})\s*[–-]/.exec(first ?? "")?.[1];
  const end = /[–-]\s*(\d{1,2}[.:]\d{2})\s*(\w*)$/.exec(last ?? "");
  const time = span && end ? `${span} – ${end[1]}${end[2] ? ` ${end[2]}` : ""}` : first;
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const speakers = child
    ? [{ role: ROLES[0], name: child.name.trim(), photo: child.photo }]
    : [
      { role: ROLES[0], name: data.couple.brideFull?.trim() || data.couple.bride, photo: data.couple.bridePhoto },
      ...(data.couple.groom?.trim() ? [{ role: ROLES[1], name: data.couple.groomFull?.trim() || data.couple.groom, photo: data.couple.groomPhoto }] : []),
    ];
  const withLine = speakers.map(sp => sp.name).join(" & ");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6f5f0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.topbar}><Art name="atom" eager /><span>{label}</span>{year && <span>{year}</span>}</div>
          <Art name="molecule" eager className={s.coverMol} />
          <p className={s.kicker}>Undangan Seminar</p>
          <h1 className={s.coverTitle}>{topic}</h1>
          <dl className={s.facts}>
            <dt>Tanggal</dt><dd>{formatDate(data.date)}</dd>
            {time && <><dt>Waktu</dt><dd>{time}</dd></>}
            {data.place && <><dt>Tempat</dt><dd>{data.place}</dd></>}
          </dl>
          <div className={s.speakers}>
            {speakers.map(sp => (
              <div key={sp.role} className={s.speaker}>
                <span className={s.speakerPhoto}><Photo src={sp.photo} alt="" /></span>
                <span><small>{sp.role}</small><strong>{sp.name}</strong></span>
              </div>
            ))}
          </div>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}>Buka Undangan<Lucide icon={ic.mailOpen} size={16} color="#ffffff" /></button>
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
        light="#f6f5f0"
        dark="#14213d"
        hero={(
          <header className={s.hero}>
            <div className={s.heroHall}><Art name="hall" /></div>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroTitle}>{topic}</h1>
            {withLine && <p className={s.heroWith}>bersama {withLine}</p>}
            <div className={s.chips}>
              <span><Lucide icon={ic.calendarPlus} size={13} color="#14213d" />{formatDate(data.date)}</span>
              {time && <span><Lucide icon={ic.clock} size={13} color="#14213d" />{time}</span>}
              {data.place && <span><Lucide icon={ic.mapPin} size={13} color="#14213d" />{data.place}</span>}
            </div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="chart" /></span>,
          node: <Art name="atom" />,
          portrait: <Art name="atom" className={s.portraitArt} />,
          countDecor: <Art name="chart" className={s.countChart} />,
          closingDecor: <Art name="molecule" className={s.closingMol} />,
          sentArt: <Art name="atom" />,
        }}
      />
    </ThemeShell>
  );
}
