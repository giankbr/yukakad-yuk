"use client";
// Theme "Arisan Keluarga" — undangan arisan keluarga bulanan (bukan pernikahan). Sampul taplak renda di atas hijau mint:
// gelas kocokan penuh gulungan kertas yang sesekali digoyang dan satu gulungan yang meloncat keluar, nama tamu tertulis
// di kertas undian bergerigi, nampan teh manis dengan teko blirik dan piring klepon, kue lapis, risoles di bawahnya.
// Hero: ruang tamu tuan rumah (jendela bertirai renda, kursi rotan, lantai tegel kunci) dengan meja arisan yang sudah
// tertata. Tuan rumah bulan ini di atas nampan rotan, hitung mundur di atas gulungan kertas, acara seperti buku arisan,
// ucapan berupa kertas tempel, dan iuran arisan sebagai amplop.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One", "Nunito:wght@400;600;800", "Gochi Hand"];
// Painted by /tmp/pen/art/themes/arisan-keluarga.py (tools/art/themes in the repo).
const Art = makeArt("arisan-keluarga", {
  kocokan: [100, 162], slip: [50, 23], teh: [150, 86], kue: [150, 45], teras: [390, 320], divider: [90, 15],
} as const);

const COPY = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, keluarga besar!",
    title: "Waktunya Arisan Lagi!",
    sub: "Kumpul sebulan sekali, kangen setiap hari",
    intro: "Sudah sebulan kita sibuk masing-masing. Hari Minggu ini, mari berkumpul lagi di ruang tamu kami: bertukar kabar, menikmati teh manis dan kue-kue, lalu bersama-sama menunggu nama siapa yang keluar dari gelas kocokan.",
  },
  // A family hosts; the trailing space keeps the two role labels distinct as list keys.
  roles: ["Tuan Rumah Bulan Ini", "Tuan Rumah "] as [string, string],
  couple: ["Yang menjamu", "Tuan Rumah"] as [string, string],
  count: ["Kocokan dimulai dalam", "Hitung Mundur"] as [string, string],
  units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
  events: ["Catat di buku arisan", "Jadwal Arisan"] as [string, string],
  story: ["Dari putaran ke putaran", "Cerita Arisan Kita"] as [string, string],
  gallery: ["Foto-foto", "Kenangan Arisan"] as [string, string],
  wishes: ["Kabari tuan rumah", "Konfirmasi & Pesan"] as [string, string],
  gifts: ["Setor iuran", "Iuran Arisan"] as [string, string],
  closing: {
    thanks: "Sampai Jumpa!",
    text: "Terima kasih sudah meluangkan waktu untuk keluarga. Kehadiran Bapak/Ibu/Saudara/i yang membuat arisan ini selalu hangat dan ramai.",
    salam: "Jangan lupa bawa iuran dan cerita terbaru, ya.",
  },
  attend: { yes: "Hadir", maybe: "Diusahakan", no: "Absen dulu" } as Partial<Record<Attendance, string>>,
  sent: "Sip, pesan Anda sudah sampai ke tuan rumah. Sampai ketemu hari Minggu!",
  wishPlaceholder: "Tulis kabar atau pesan untuk keluarga arisan…",
  closedNote: "Pendataan kehadiran sudah ditutup. Pesan untuk keluarga masih bisa dikirim lewat form ini.",
  giftIntro: "Iuran bulan ini Rp200.000 per keluarga. Bagi yang berhalangan hadir, iuran dapat ditransfer ke bendahara arisan:",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Keluarga Om Bambang & Tante Wati", attendance: "yes" as Attendance, message: "Siap hadir! Kami bawa lemper satu tampah. Semoga bulan ini nama kami yang keluar, hehe." },
  { id: "w2", name: "Mbak Dewi (Semarang)", attendance: "maybe" as Attendance, message: "Diusahakan datang kalau kereta pagi masih ada. Iuran sudah aku transfer ke Bu Rini ya." },
  { id: "w3", name: "Pakde Joko sekeluarga", attendance: "no" as Attendance, message: "Bulan ini absen dulu, ada hajatan di kampung. Titip salam untuk Eyang Putri, sisakan klepon satu!" },
];

export default function ArisanKeluargaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Arisan Keluarga";
  const hosts = [data.couple.bride?.trim(), data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const host = /^keluarga/i.test(hosts) ? hosts : `Keluarga ${hosts}`;
  const note = data.couple.note?.trim();
  const table = tableLabel(data.guestTable);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#2a7f7a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.pill}>Undangan untuk keluarga</p>
          <h1 className={s.coverTitle}>{label}</h1>
          <p className={s.coverHost}>Tuan rumah: {host}</p>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.jar} aria-hidden>
            <span className={s.popSlip}><Art name="slip" eager /></span>
            <Art name="kocokan" eager />
          </div>
          <div className={s.ticket}>
            <div className={s.guest}>
              <small>Kertas undian untuk:</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fffaf0" />Buka Undangan</button>
          <Art name="teh" eager className={s.coverTeh} />
          <Art name="kue" eager className={s.coverKue} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#fff1c4"
        dark="#3a2a22"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.room} aria-hidden>
              <Art name="teras" />
              <Art name="kue" className={s.roomKue} />
              <span className={s.roomGlass}><Art name="kocokan" /></span>
              <Art name="teh" className={s.roomTeh} />
            </div>
            <div className={s.heroCard}>
              <p className={s.heroKicker}>{label} bulan ini di rumah</p>
              <h1 className={s.heroName}>{host}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="slip" />,
          portrait: <span className={s.hostArt} aria-hidden><Art name="teh" /></span>,
          closingEmblem: <div className={s.closeSet} aria-hidden><Art name="teh" className={s.closeTeh} /><span className={s.closeGlass}><Art name="kocokan" /></span></div>,
          sentArt: <Art name="kocokan" />,
        }}
      />
    </ThemeShell>
  );
}
