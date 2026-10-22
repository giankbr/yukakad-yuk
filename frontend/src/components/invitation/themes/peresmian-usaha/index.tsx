"use client";
// Theme "Peresmian Usaha" — undangan grand opening toko, kedai, atau kantor baru saat senja: fasad toko gouache dengan
// papan nama kayu (nama usaha = nama tempat acara, diketik di atasnya), kanopi bergaris hijau toska-krem, pita satin merah
// dengan gunting emas yang siap memotong, papan bunga khas Indonesia berteks ucapan umum, konfeti. Pemilik usaha tampil
// sebagai "yang merayakan" (data mempelai), kartu acara berbentuk label harga, hitung mundur papan gantung.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["DM Serif Display", "Outfit:wght@400;500;600;700", "Anton"];
// Painted by /tmp/pen/art/themes/peresmian-usaha.py (tools/art/themes in the repo).
const Art = makeArt("peresmian-usaha", { shop: [520, 520], ribbon: [640, 143], scissors: [180, 194], "board-a": [190, 280], "board-b": [190, 280] } as const);

const WISHES = [
  { id: "w1", name: "Bapak Yudhistira & Rekan", attendance: "yes" as const, message: "Selamat dan sukses atas pembukaannya! Semoga laris manis, jadi tempat pulang favorit warga, dan terus tumbuh membuka cabang." },
  { id: "w2", name: "Komunitas Pesepeda Malang", attendance: "yes" as const, message: "Akhirnya ada titik kumpul baru! Kami datang satu rombongan selepas gowes sore. Sukses selalu untuk tim di balik bar." },
  { id: "w3", name: "Mbak Sekar", attendance: "maybe" as const, message: "Ikut bangga lihat perjalanan dari gerobak sampai punya kedai sendiri. Semoga penuh berkah dan pelanggannya setia." },
];

function Board({ name, className, title, line, by }: { name: "board-a" | "board-b"; className: string; title: string; line: string; by?: string }) {
  return (
    <span className={className} aria-hidden>
      <Art name={name} />
      <span className={s.boardText}><small>{line}</small><b>{title}</b>{by && <i>{by}</i>}</span>
    </span>
  );
}

export default function PeresmianUsahaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Grand Opening";
  const business = data.events[0]?.venue?.trim() || data.place?.trim() || data.couple.bride;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Kabar Gembira",
      title: "Pintu Kami Segera Dibuka",
      intro: `Dengan penuh syukur dan semangat, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam peresmian ${business}. Mari bersama menggunting pita, mencicipi sajian perdana, dan merayakan awal perjalanan baru kami.`,
    },
    roles: ["Pemilik", "Rekan Pemilik"] as [string, string],
    couple: ["Di Balik Usaha", data.couple.groom?.trim() ? "Para Pemilik" : "Pemilik"] as [string, string],
    count: ["Segera Buka", "Hitung Mundur Peresmian"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Agenda", "Waktu & Tempat"] as [string, string],
    story: ["Perjalanan Kami", `Cerita ${business}`] as [string, string],
    gallery: ["Intip Dapur", "Galeri"] as [string, string],
    wishes: ["Ucapan Selamat", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["Tanda Dukungan", "Kirim Hadiah"] as [string, string],
    closing: { thanks: "Terima Kasih", text: "Dukungan dan kehadiran Anda adalah modal terbesar bagi langkah pertama kami. Sampai jumpa di depan pintu!" },
    sent: "Terima kasih! Ucapan selamat Anda sudah kami terima.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: "Tulis ucapan selamat dan doa untuk usaha baru ini…",
    closedNote: "Konfirmasi kehadiran sudah ditutup. Terima kasih atas dukungannya, ucapan selamat masih bisa dikirim.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf4e8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.coverKicker}>Undangan Peresmian</p>
          <h1 className={s.coverTitle}>{label}</h1>
          <div className={s.store}>
            <Art name="shop" eager className={s.shop} />
            <span className={s.sign}>{business}</span>
            <span className={`${s.miniBoard} ${s.boardL}`} aria-hidden><Art name="board-a" eager /><span className={s.boardText}><small>Selamat</small><b>& Sukses</b></span></span>
            <span className={`${s.miniBoard} ${s.boardR}`} aria-hidden><Art name="board-b" eager /><span className={s.boardText}><small>Turut</small><b>Bahagia</b></span></span>
            <div className={s.ribbonWrap} aria-hidden>
              <Art name="ribbon" eager className={s.ribbon} />
              <Art name="scissors" eager className={s.scissors} />
            </div>
          </div>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          {data.address && <p className={s.coverPlace}>{data.address}</p>}
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fffaf1" />Buka Undangan</button>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        light="#fbe6a6"
        dark="#3a2620"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.boards}>
              <Board name="board-a" className={s.bigBoard} line="Selamat & Sukses" title={label} by={business} />
              <Board name="board-b" className={s.bigBoard} line="Turut Berbahagia" title="Laris Manis" by="Semoga penuh berkah" />
            </div>
            <p className={s.heroKicker}>Dengan bangga kami persembahkan</p>
            <h1 className={s.heroName}>{business}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="scissors" /><i /></span>,
          node: <Art name="scissors" />,
          closingDecor: <Art name="ribbon" className={s.closingRibbon} />,
          closingEmblem: <div className={s.emblem} aria-hidden><Art name="shop" /><span className={s.emblemSign}>{business}</span></div>,
          sentArt: <Art name="scissors" />,
        }}
      />
    </ThemeShell>
  );
}
