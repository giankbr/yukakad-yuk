"use client";
// Theme "Minahasa Kawanua" — merah-hitam-emas: kain bentenan yang ditenun sampai ke tingkat benang (belah ketupat
// bertingkat, garis sinoi, benang emas), rumah panggung kayu Woloan dengan tangga kembar di kaki Gunung Lokon, dan
// manguni kecil sebagai lambang. Sampul: foto di atas, pita tenun, panel hitam.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cinzel Decorative:wght@400;700", "Cinzel:wght@700", "Crimson Pro:ital,wght@0,400;0,600;0,700;1,400"];
// Painted by /tmp/pen/art/themes/minahasa-kawanua.py (tools/art/themes in the repo).
const Art = makeArt("minahasa-kawanua", { rumah: [860, 567], manguni: [156, 226], divider: [303, 42] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Syalom",
    title: "Pakatuan wo Pakalawiren",
    sub: "“Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.” — Matius 19:6",
    intro: "Dengan penuh syukur kepada Tuhan Yang Maha Kasih, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam pemberkatan nikah dan resepsi putra-putri kami. Kehadiran dan doa Anda adalah sukacita bagi keluarga besar kami.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Hati, Satu Rumah", "Kedua Mempelai"],
  count: ["Menanti Hari Bahagia", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan Kami", "Kisah Cinta"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Makase Banyak", text: "Atas kehadiran, doa, dan kasih Bapak/Ibu/Saudara/i, kami sekeluarga mengucapkan terima kasih. Pakatuan wo pakalawiren.", salam: "Tuhan Yesus memberkati" },
  sent: "Makase banyak, doa dan ucapan Anda sudah terkirim.",
  attend: { maybe: "Mungkin" },
  wishPlaceholder: "Tuliskan doa dan berkat untuk kedua mempelai…",
};

export default function MinahasaKawanuaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#17100d"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          {hero ? <div className={s.coverPhoto}><Photo src={hero} alt="" /></div> : <div className={s.coverNoPhoto} aria-hidden />}
          <div className={s.coverTop}><p className={s.coverKicker}>Syalom</p></div>
          <span className={s.coverWeave} aria-hidden />
          <div className={s.coverBody}>
            <Art name="manguni" eager className={s.coverOwl} />
            <p className={s.coverLabel}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>&amp;</em><span>{data.couple.groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <Art name="divider" eager className={s.coverRule} />
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fff3dc" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f6ead4"
        dark="#17100d"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="rumah" className={s.heroHouse} />
            <span className={s.heroWeave} aria-hidden />
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          closingEmblem: <Art name="manguni" className={s.closingOwl} />,
          sentArt: <Art name="manguni" />,
        }}
      />
    </ThemeShell>
  );
}
