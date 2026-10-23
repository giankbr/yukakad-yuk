"use client";
// Theme "Malam Tahun Baru" — undangan pesta malam tahun baru (bukan pernikahan). Sampul: langit malam yang dilukis
// dengan kembang api di atas siluet kota, konfeti yang terus berjatuhan, jam emas yang jarumnya bergerak ke tengah
// malam, angka 31.12 raksasa, dan tiket masuk bersobekan untuk tamu. Hero berupa poster pesta (selamat tinggal tahun
// lama, halo tahun baru) dengan keterangan waktu dan tempat; hitung mundur berupa ubin jam lipat menuju 00.00,
// acara sebagai tiket, iuran patungan, dan dua gelas yang berdenting di penutup.
import { Lucide, ThemeShell, dateParts, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Big Shoulders Display:wght@600;800", "Outfit:wght@400;500;600;700", "Parisienne"];
// Painted by /tmp/pen/art/themes/malam-tahun-baru.py (tools/art/themes in the repo).
const Art = makeArt("malam-tahun-baru", {
  clock: [150, 150], "hand-h": [150, 150], "hand-m": [150, 150], "burst-gold": [105, 105], "burst-coral": [105, 105], "burst-mint": [105, 105],
  coupes: [150, 145], streamer: [160, 26],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Hai, kamu!",
    title: "Ayo tutup tahun bareng",
    intro: "Setahun penuh kerja, cerita, dan kejutan sudah kita lewati. Sebelum kalender berganti, mari berkumpul di atap: makan bersama, tukar kado kecil, lalu menghitung mundur dan menyambut tahun baru di bawah langit yang penuh kembang api.",
  },
  // Hosts, not a couple; the trailing space keeps the two role labels distinct as list keys.
  roles: ["Tuan Rumah", "Tuan Rumah "] as [string, string],
  couple: ["Yang ngajak", "Tuan Rumah"] as [string, string],
  count: ["Menuju 00.00", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Catat jamnya", "Susunan Malam"] as [string, string],
  story: ["Dari tahun ke tahun", "Tradisi Kami"] as [string, string],
  gallery: ["Tahun-tahun lalu", "Galeri"] as [string, string],
  wishes: ["Kabari kami", "Konfirmasi & Pesan"] as [string, string],
  gifts: ["Patungan", "Iuran Pesta"] as [string, string],
  closing: {
    thanks: "Selamat Tahun Baru!",
    text: "Terima kasih sudah jadi bagian dari tahun ini. Sampai jumpa di atap, dan sampai jumpa di tahun yang baru!",
    salam: "Semoga tahun depan lebih baik",
  },
  attend: { yes: "Datang!", maybe: "Mungkin", no: "Absen dulu" } as Partial<Record<Attendance, string>>,
  sent: "Sip! Pesanmu sudah masuk. Sampai ketemu di hitung mundur!",
  wishPlaceholder: "Tulis pesan, harapan tahun depan, atau request lagu…",
  closedNote: "Pendataan tamu sudah ditutup. Pesan dan harapan tahun baru masih bisa dikirim lewat form ini.",
  giftIntro: "Pesta ini patungan: Rp150.000 per orang, sudah termasuk makan, minuman, dan terompet. Bisa dibayar di tempat atau ditransfer ke:",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Bimo & Partner", attendance: "yes" as Attendance, message: "Gas! Kami bawa terompet dan satu kotak martabak manis. Semoga tahun depan kita makin sering kumpul." },
  { id: "w2", name: "Dinda (lantai 2)", attendance: "yes" as Attendance, message: "Request lagu buat hitung mundur ya. Patungan sudah aku transfer ke Sasha." },
  { id: "w3", name: "Mas Yoga", attendance: "maybe" as Attendance, message: "Mungkin nyusul setelah jaga toko. Sisakan jagung bakar satu, dan selamat tahun baru semuanya!" },
];

export default function MalamTahunBaruTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Malam Tahun Baru";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const hosts = [data.couple.bride?.trim(), data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const d = dateParts(data.date);
  const when = toDate(data.date);
  const year = when ? Number(d.year) : undefined;
  const dayMonth = when ? new Intl.DateTimeFormat("id-ID", { timeZone: "Asia/Jakarta", day: "2-digit", month: "2-digit" }).format(when).replace("/", ".") : "";
  const firstEvent = data.events[0];

  return (
    <ThemeShell
      fonts={FONTS}
      background="#03100f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.confetti} aria-hidden />
          <Art name="burst-gold" eager className={`${s.pop} ${s.popA}`} />
          <Art name="burst-coral" eager className={`${s.pop} ${s.popB}`} />
          <Art name="burst-mint" eager className={`${s.pop} ${s.popC}`} />
          <div className={s.clock} aria-hidden>
            <Art name="clock" eager />
            <Art name="hand-h" eager className={s.hh} />
            <Art name="hand-m" eager className={s.hm} />
          </div>
          <p className={s.kicker}>Undangan {label}</p>
          {dayMonth ? <h1 className={s.coverDate}>{dayMonth}<small>{d.year}</small></h1> : <h1 className={s.coverDate}><small>{formatDate(data.date)}</small></h1>}
          <p className={s.coverTitle}>{label}</p>
          {hosts && <p className={s.coverHost}>bersama <b>{hosts}</b></p>}
          <div className={s.ticket}>
            <div className={s.guest}>
              <small>Tiket masuk untuk</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <div className={s.stub} aria-hidden>{d.year ? <><b>{d.day}</b>{d.monthShort}</> : "Admit"}</div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="currentColor" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#fff0c4"
        dark="#061a21"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="burst-gold" className={`${s.heroBurst} ${s.heroBurstA}`} />
            <Art name="burst-coral" className={`${s.heroBurst} ${s.heroBurstB}`} />
            <p className={s.heroKicker}>{label}</p>
            {year ? (
              <h1 className={s.heroBig}>Dadah <s>{year}</s><span>Halo {year + 1}</span></h1>
            ) : <h1 className={s.heroBig}>Sampai Jumpa<span>Tahun Baru</span></h1>}
            {hosts && <p className={s.heroHost}>Diundang oleh <b>{hosts}</b></p>}
            <div className={s.facts}>
              <div><small>Kapan</small><strong>{formatDate(data.date)}{firstEvent?.time ? <><br />{firstEvent.time}</> : null}</strong></div>
              <div><small>Di mana</small><strong>{firstEvent?.venue || data.place}</strong></div>
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="coupes" className={s.heroCoupes} />
          </header>
        )}
        slots={{
          divider: <Art name="streamer" className={s.divider} />,
          node: <Art name="burst-gold" />,
          portrait: <span className={s.hostBurst} aria-hidden><Art name="burst-gold" /></span>,
          countDecor: <><Art name="burst-coral" className={`${s.countPop} ${s.countPopA}`} /><Art name="burst-mint" className={`${s.countPop} ${s.countPopB}`} /></>,
          closingEmblem: <Art name="coupes" className={s.closeCoupes} />,
          sentArt: <Art name="burst-gold" />,
        }}
      />
    </ThemeShell>
  );
}
