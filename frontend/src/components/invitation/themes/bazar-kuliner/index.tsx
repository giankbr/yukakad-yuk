"use client";
// Theme "Bazar Kuliner" — poster festival jajanan malam (komunitas fiktif): deretan tenda bergaris di bawah untaian
// lampu, kerumunan siluet, sate, martabak manis, dan es cendol dilukis gouache; kartu berbentuk tiket berlubang,
// papan tulis daftar lapak. Penyelenggara = panitia. Dilukis oleh /tmp/pen/art/themes/bazar-kuliner.py.
import { Lucide, Photo, ThemeShell, coupleLabel, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bowlby One", "Bricolage Grotesque:wght@400;600;700;800", "Caveat Brush"];
const Art = makeArt("bazar-kuliner", {
  stalls: [780, 676], lights: [400, 70], sate: [240, 112], martabak: [220, 105], cendol: [130, 255],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, warga dan sahabat semua!",
    title: "Ayo jajan bareng tetangga!",
    sub: "Gratis masuk, terbuka untuk umum",
    intro: "Dengan senang hati kami mengundang Bapak/Ibu/Saudara/i beserta keluarga untuk datang, mencicipi, dan meramaikan bazar kuliner kampung kita. Setiap jajanan yang dibeli ikut menghidupkan usaha kecil para tetangga.",
  },
  roles: ["Penyelenggara", "Bersama"],
  couple: ["Dari kami, untuk kampung", "Panitia"],
  count: ["Lapak dibuka dalam", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Pegang tiketnya", "Jadwal Bazar"],
  story: ["Mau jajan apa?", "Daftar Lapak"],
  gallery: ["Suasana tahun lalu", "Galeri"],
  wishes: ["Kabari panitia", "Rencana Datang & Pesan"],
  gifts: ["Ingin buka lapak?", "Pendaftaran Tenant"],
  closing: {
    thanks: "Sampai jumpa di lapak!",
    text: "Terima kasih sudah ikut meramaikan. Datang lapar, pulang senang, dan jangan lupa bawa tas belanja sendiri.",
  },
  sent: "Terima kasih, pesanmu sudah sampai ke meja panitia!",
  attend: { yes: "Datang", maybe: "Mungkin", no: "Tidak bisa" },
  wishPlaceholder: "Tulis pesan, usulan menu, atau kesan untuk panitia…",
  closedNote: "Bazar sudah selesai. Terima kasih atas kedatangan dan dukungannya, sampai jumpa tahun depan!",
  giftIntro: "Pendaftaran tenant dibuka sampai 10 Agustus 2027. Sewa lapak Rp150.000 untuk dua malam (meja, listrik, dan kebersihan). Transfer lalu kirim bukti ke panitia:",
  wishLabel: "Pesan & Kesan",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Bu Siti, RT 02", attendance: "yes" as const, message: "Sudah tidak sabar! Tahun lalu kehabisan martabak Ko Ahan, tahun ini datang lebih awal. Semangat panitia!" },
  { id: "w2", name: "Dimas & teman kos", attendance: "yes" as const, message: "Kami datang malam kedua buat lomba dan undian. Usul: tambah lapak kopi susu gula aren ya." },
  { id: "w3", name: "Keluarga Pak Joko", attendance: "maybe" as const, message: "Malam pertama ada acara keluarga, semoga bisa mampir malam kedua. Sukses bazarnya!" },
];

export default function BazarKulinerTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const title = data.eventLabel ?? "Bazar Kuliner";
  const hosts = coupleLabel(data);
  const photo = data.gallery[0];
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const time = data.events[0]?.time;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1a1430"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Undangan Bazar &amp; Festival Kuliner</p>
          <h1 className={s.coverTitle}>{title}</h1>
          <div className={s.coverChips}>
            <span>{formatDate(data.date)}</span>
            {time && <span>{time}</span>}
          </div>
          {hosts && <p className={s.coverHost}>Diselenggarakan oleh {hosts}</p>}
          <div className={s.stallsWrap}><Art name="stalls" eager className={s.stalls} /></div>
          <div className={s.coverFoot}>
            <div className={s.ticket}>
              <div className={s.guest}>
                <small>Tiket masuk untuk</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <div className={s.stub} aria-hidden><Art name="cendol" eager /></div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fdf3e0" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        celebrant
        demoWishes={WISHES}
        light="#fdf3e0"
        dark="#2a1d18"
        hero={(
          <header className={s.hero}>
            <Art name="lights" className={s.heroLights} />
            <div className={s.heroPhoto}>{photo ? <Photo src={photo} alt={`Suasana ${title}`} /> : <span className={s.heroMono} aria-hidden>{title.slice(0, 1)}</span>}</div>
            <div className={s.heroFood}><Art name="sate" /><Art name="cendol" /><Art name="martabak" /></div>
            <p className={s.heroKicker}>Undangan terbuka</p>
            <h1 className={s.heroTitle}>{title}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="lights" className={s.divider} />,
          node: <Art name="sate" />,
          amp: <Art name="sate" />,
          portrait: <Art name="cendol" className={s.portraitArt} />,
          countDecor: <Art name="lights" className={s.countLights} />,
          closingDecor: <Art name="lights" className={s.closingLights} />,
          closingEmblem: <Art name="martabak" className={s.closingEmblem} />,
          sentArt: <Art name="sate" />,
        }}
      />
    </ThemeShell>
  );
}
