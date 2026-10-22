"use client";
// Theme "Lomba 17-an" — undangan warga untuk lomba Agustusan, bergaya poster kampung dengan cat gouache: bendera
// segitiga merah-putih yang berkibar, panjat pinang berhadiah, anak-anak balap karung yang melompat dan makan kerupuk,
// deretan rumah kampung dengan gapura merah-putih. Kartu bergaris tebal dengan bayangan offset, nomor dada peserta
// untuk hitung mundur. Bendera Merah Putih selalu merah di atas. Pengundang adalah panitia, bukan pasangan.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import type { CSSProperties } from "react";
import type { InvitationData } from "../../types";
import s from "./styles.module.css";

const FONTS = ["Bowlby One", "Baloo 2:wght@400;500;600;700;800", "Caveat Brush"];
// Painted by /tmp/pen/art/themes/lomba-17an.py (tools/art/themes in the repo).
const Art = makeArt("lomba-17an", {
  pinang: [260, 918], kampung: [680, 170], bendera: [640, 122], karung: [220, 379], kerupuk: [230, 255], tambang: [360, 25], flag: [90, 85], awan: [200, 87],
} as const);

/** "HUT ke-82 RI" from the event year (17 Agustus 1945 = HUT ke-0). */
function hutLabel(data: InvitationData) {
  const year = toDate(data.date)?.getFullYear();
  return year && year > 1945 ? `HUT ke-${year - 1945} Republik Indonesia` : "HUT Kemerdekaan Republik Indonesia";
}

function Title({ label, className }: { label: string; className: string }) {
  const [first, ...rest] = label.trim().split(/\s+/);
  const longest = Math.max(...label.trim().split(/\s+/).map(word => word.length), 4);
  return (
    <h1 className={className} style={{ "--n": longest } as CSSProperties}>
      <span>{first}</span>{rest.length > 0 && <>{" "}<span>{rest.join(" ")}</span></>}
    </h1>
  );
}

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Salam Merdeka!",
    title: "Ayo ramaikan Agustusan di kampung kita",
    intro: "Dalam rangka memperingati Hari Ulang Tahun Kemerdekaan Republik Indonesia, panitia mengundang seluruh warga beserta keluarga untuk ikut serta dan meramaikan rangkaian lomba 17-an. Tua, muda, anak-anak, semua boleh ikut!",
  },
  roles: ["Yang Mengundang", "Bersama"],
  couple: ["Panitia", "Yang Mengundang"],
  count: ["Hitung mundur!", "Menuju Hari Lomba"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat jadwalnya", "Susunan Lomba"],
  story: ["Dari tahun ke tahun", "Cerita Agustusan Kita"],
  gallery: ["Album kampung", "Foto Kegiatan"],
  wishes: ["Daftar & semangat", "Konfirmasi Kehadiran"],
  gifts: ["Iuran & donasi", "Dukung Hadiah Lomba"],
  closing: {
    thanks: "Merdeka!",
    text: "Terima kasih untuk seluruh warga yang sudah bergotong royong. Sampai jumpa di lapangan, siapkan tenaga dan sorakan terbaik!",
  },
  sent: "Siap! Kehadiran dan semangatmu sudah tercatat. Merdeka!",
  attend: { yes: "Ikut", maybe: "Mungkin", no: "Belum Bisa" },
  wishPlaceholder: "Tulis semangat untuk peserta, atau lomba yang ingin kamu ikuti…",
  closedNote: "Terima kasih sudah meramaikan! Pesan dan semangat masih bisa dikirim lewat form ini.",
  giftIntro: "Warga yang ingin ikut iuran konsumsi atau menyumbang hadiah lomba dapat menyalurkannya melalui panitia:",
  giftAddressTitle: "Antar Hadiah Lomba",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Bu Tini (Warung Gang Melati)", attendance: "yes" as Attendance, message: "Siap jualan es teh di pinggir lapangan! Semangat buat anak-anak, jangan lupa minum ya." },
  { id: "w2", name: "Dimas, kelas 4", attendance: "yes" as Attendance, message: "Aku ikut balap karung lagi. Mau juara empat kali berturut-turut!" },
  { id: "w3", name: "Keluarga Pak Hasan, Blok D", attendance: "maybe" as Attendance, message: "Pagi masih di jalan pulang kampung, insyaallah sore sudah sampai buat lihat panjat pinang." },
];

export default function Lomba17anTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Lomba 17-an";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const host = data.couple.brideFull?.trim() || data.couple.bride;
  const hut = hutLabel(data);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6e9cf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="bendera" eager className={s.coverBunting} />
          <Art name="awan" eager className={s.cloudA} />
          <Art name="awan" eager className={s.cloudB} />
          <Art name="pinang" eager className={s.pinang} />
          <p className={s.tag}>Undangan Warga</p>
          <Title label={label} className={s.coverTitle} />
          <p className={s.hut}>{hut}</p>
          {host && <p className={s.host}>{host}</p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestCard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#ffffff" />Buka Undangan</button>
          </div>
          <Art name="kampung" eager className={s.kampung} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#ffffff"
        dark="#2a1d17"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="bendera" className={s.coverBunting} />
            <Title label={label} className={s.heroTitle} />
            <p className={s.hut}>{hut}</p>
            {host && <p className={s.host}>{host}</p>}
            {note && <p className={s.heroNote}>{note}</p>}
            <div className={s.heroRow}>
              <Art name="karung" className={s.karung} />
              <Art name="kerupuk" className={s.kerupuk} />
            </div>
            <Art name="kampung" className={s.heroGrass} />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
          </header>
        )}
        slots={{
          divider: <Art name="tambang" className={s.divider} />,
          node: <Art name="flag" />,
          amp: <Art name="flag" />,
          portrait: <Art name="flag" className={s.pFlag} />,
          countDecor: <Art name="bendera" className={s.countFlags} />,
          closingDecor: <Art name="kampung" className={s.closingKampung} />,
          closingEmblem: <Art name="flag" className={s.closingFlag} />,
          sentArt: <Art name="karung" />,
        }}
      />
    </ThemeShell>
  );
}
