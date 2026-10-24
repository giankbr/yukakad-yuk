"use client";
// Theme "Stasiun Tua" — stasiun kereta tua dalam guas sepia dan besi tempa teal: kanopi berpapan valance dan siku besi,
// jam stasiun besar yang jarumnya menunjuk jam acara (jarum detik berputar), papan nama stasiun dari pelat email
// berisi nama mempelai, karcis karton berlubang untuk tamu, lokomotif uap berkepul di peron kayu. Halaman: jendela
// gerbong untuk foto, papan keberangkatan, hitung mundur papan huruf-balik, kartu acara bergaya karcis, garis waktu rel.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Big Shoulders Display:wght@700;800", "Libre Caslon Text:ital,wght@0,400;0,700;1,400", "IM Fell English:ital@0;1"];
// Painted by /tmp/pen/art/themes/stasiun-tua.py
const Art = makeArt("stasiun-tua", {
  kanopi: [860, 250], jam: [460, 540], lokomotif: [860, 339], uap: [400, 219], koper: [320, 256], ulir: [390, 44],
} as const);

const WISHES = [
  { id: "w1", name: "Om Yohanes & Tante Maria", attendance: "yes" as Attendance, message: "Selamat menempuh perjalanan baru, Sekar dan Arga. Semoga rumah tangga kalian selalu tepat waktu dalam saling mengasihi." },
  { id: "w2", name: "Komunitas Pecinta Kereta Semarang", attendance: "yes" as Attendance, message: "Dari peron Tawang sampai pelaminan! Kami datang lengkap dengan karcis koleksi kalian." },
  { id: "w3", name: "Rina & Bayu, Bandung", attendance: "maybe" as Attendance, message: "Semoga bisa menyusul naik kereta malam. Kalau belum sempat, doa terbaik kami ikut dalam gerbong kalian." },
];

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Dengan penuh sukacita",
    title: "Satu Perjalanan Baru",
    sub: "kami mengundang Anda ke peron kebahagiaan kami",
    intro: "Dengan penuh syukur, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua penumpang, satu tujuan", "Kedua Mempelai"],
  count: ["Kereta segera berangkat", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Jadwal keberangkatan", "Rangkaian Acara"],
  story: ["Catatan perjalanan", "Kisah Kami"],
  gallery: ["Dari jendela gerbong", "Galeri"],
  wishes: ["Telegram untuk mempelai", "Ucapan & Konfirmasi"],
  gifts: ["Bekal perjalanan", "Tanda Kasih"],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas kehadiran dan doa restu Bapak/Ibu/Saudara/i, kami ucapkan terima kasih. Sampai jumpa di peron kebahagiaan kami.",
    salam: "Salam hangat dari kami sekeluarga",
  },
  sent: "Telegram diterima! Terima kasih atas doa dan ucapan Anda.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan ucapan dan doa untuk kedua mempelai…",
};

/** Clock hand angles for the event time ("…T10:00…"), read from the ISO string so SSR and client agree. */
function hands(iso: string) {
  const match = /T(\d{2}):(\d{2})/.exec(iso);
  const h = match ? Number(match[1]) % 12 : 10;
  const m = match ? Number(match[2]) : 0;
  return { hour: h * 30 + m * 0.5, minute: m * 6 };
}

export default function StasiunTuaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const heroPhoto = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const angle = hands(data.date);
  const serial = (data.date.replace(/\D/g, "").slice(2, 8) || "000000");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1f4445"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="kanopi" eager className={s.canopy} />
          <div className={s.clock} aria-hidden>
            <Art name="jam" eager />
            <span className={`${s.hand} ${s.hHour}`} style={{ rotate: `${angle.hour}deg` }} />
            <span className={`${s.hand} ${s.hMin}`} style={{ rotate: `${angle.minute}deg` }} />
            <span className={`${s.hand} ${s.hSec}`} />
            <span className={s.pin} />
          </div>
          <div className={s.board}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.ticket}>
            <p className={s.ticketHead}><span>Karcis Undangan</span><span>No. {serial}</span></p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#2a1d0e" />Buka Undangan</button>
          <div className={s.platform} aria-hidden>
            <Art name="uap" eager className={s.steam} />
            <Art name="lokomotif" eager className={s.loco} />
            <div className={s.planks} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f4ead2"
        dark="#2f6563"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            {heroPhoto && <div className={s.heroWindow}><div className={s.heroPhoto}><Photo src={heroPhoto} alt="" /></div></div>}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.departures}>
              <p className={s.depHead}><span>Keberangkatan</span><span>{formatDate(data.date)}</span></p>
              {data.events.map((event, index) => (
                <p key={event.name + index} className={s.depRow}><span>{(event.time || "--.--").slice(0, 5)}</span><span>{event.name}</span></p>
              ))}
            </div>
          </header>
        )}
        slots={{
          divider: <Art name="ulir" className={s.divider} />,
          node: null,
          amp: <Art name="ulir" />,
          portrait: <Art name="ulir" className={s.portraitArt} />,
          closingDecor: (
            <div className={s.closingTrain} aria-hidden>
              <Art name="uap" className={s.steam} />
              <Art name="lokomotif" className={s.loco} />
              <div className={s.planks} />
            </div>
          ),
          closingEmblem: <Art name="koper" className={s.closingEmblem} />,
          sentArt: <Art name="koper" />,
        }}
      />
    </ThemeShell>
  );
}
