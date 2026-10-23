"use client";
// Theme "Pentas Seni" — undangan pentas seni sekolah: panggung aula dilukis gouache (tirai toska diikat pita kuning,
// valans koral berumbai, lampu sorot, bendera segitiga) dengan tiga murid yang tampil, poster buatan tangan yang
// ditempel selotip, gambar krayon anak-anak, kartu acara bergaris, dan susunan acara sebagai urutan penampilan.
// Tuan rumah: kepala sekolah & panitia.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Titan One", "Baloo 2:wght@400;500;600;700;800", "Patrick Hand"];
// Painted by /tmp/pen/art/themes/pentas-seni.py (bendera, rebana and angklung are also CSS backgrounds).
const Art = makeArt("pentas-seni", {
  panggung: [780, 655], matahari: [220, 233], pelangi: [230, 206], rumah: [230, 218], angklung: [120, 145], rebana: [110, 109], kipas: [150, 86], bintang: [64, 62],
} as const);

const WISHES = [
  { id: "w1", name: "Bunda Kirana (4B)", attendance: "yes" as const, message: "Kirana sudah latihan angklung tiap sore di teras rumah. Terima kasih Pak Bagus dan para guru, kami sekeluarga pasti datang!" },
  { id: "w2", name: "Ayah Raka (2A)", attendance: "yes" as const, message: "Semangat para penari kipas kelas 2! Semoga lancar dan anak-anak makin percaya diri tampil di depan banyak orang." },
  { id: "w3", name: "Eyang Putri Danu (5C)", attendance: "maybe" as const, message: "Eyang menonton dari siaran langsung saja ya, Cucu. Semoga drama Kancil-nya sukses, tepuk tangan dari Klaten!" },
];

export default function PentasSeniTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pentas Seni";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const storyTitle = data.story?.title?.trim();
  const title = storyTitle && !/^kisah|^cerita|^tentang/i.test(storyTitle) ? storyTitle : label;
  const host = data.place?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf3e1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.stage}>
            <Art name="panggung" eager />
            <span className={s.spot} aria-hidden />
          </div>
          <Art name="matahari" eager className={s.drawL} />
          <Art name="pelangi" eager className={s.drawR} />
          <div className={s.poster}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverTitle}>{title}</h1>
            {host && <p className={s.coverHost}>{host}</p>}
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth.</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff8e8" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#fff8e8"
        dark="#2b2230"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Halo, Bapak/Ibu dan Keluarga!",
            title: "Tirai Segera Dibuka",
            sub: "Anak-anak kami siap tampil",
            intro: "Dengan gembira kami mengundang Bapak/Ibu wali murid, keluarga, dan sahabat sekolah untuk menyaksikan penampilan putra-putri kita. Tepuk tangan Anda adalah hadiah terbesar bagi para penampil cilik.",
          },
          roles: ["Kepala Sekolah", "Ketua Panitia"],
          couple: ["Yang mengundang", "Sekolah & Panitia"],
          count: ["Tirai dibuka dalam", "Menuju Pentas"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat tanggalnya", "Waktu & Tempat"],
          story: ["Urutan penampilan", "Susunan Acara"],
          gallery: ["Dipajang di koridor", "Karya Murid"],
          wishes: ["Pesan untuk penampil", "Dukungan & Kehadiran"],
          gifts: ["Donasi sukarela", "Dukung Ekskul Seni"],
          closing: {
            thanks: "Sampai Jumpa di Panggung!",
            text: "Terima kasih atas dukungan Bapak/Ibu. Mari datang lebih awal, duduk di depan, dan beri tepuk tangan paling meriah untuk anak-anak kita.",
            salam: "Salam budaya, keluarga besar sekolah",
          },
          sent: "Terima kasih! Pesanmu akan kami bacakan untuk para penampil.",
          attend: { yes: "Hadir", maybe: "Mungkin", no: "Berhalangan" },
          wishPlaceholder: "Tulis pesan semangat untuk para penampil…",
          closedNote: "Terima kasih sudah menonton dan mendukung. Pesan semangat masih bisa dikirim lewat form ini.",
          giftIntro: "Pentas ini gratis untuk semua. Bila berkenan, donasi sukarela akan dipakai untuk membeli alat musik dan kostum ekstrakurikuler seni.",
          familyLabel: null,
        }}
        hero={(
          <header className={s.hero}>
            <Art name="panggung" className={s.heroStage} />
            <p className={s.kickerDark}>{label}</p>
            <h1 className={s.heroTitle}>{title}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="bintang" className={s.divider} />,
          node: <Art name="bintang" />,
          portrait: <Art name="bintang" />,
          closingEmblem: (
            <div className={s.closingProps} aria-hidden>
              <Art name="kipas" />
              <Art name="angklung" />
              <Art name="rebana" />
            </div>
          ),
          sentArt: <Art name="kipas" />,
        }}
      />
    </ThemeShell>
  );
}
