"use client";
// Theme "Tedak Siten" — upacara turun tanah (mudhun lemah) bayi Jawa dalam pastel hangat: tangga tebu bertali janur,
// jadah tujuh warna di atas daun pisang, kurungan bambu berhias mawar dan melati, kembang setaman (gouache + cat air).
// Hero menjelaskan urutan upacara; kartu bantal membulat dengan pita tujuh warna, cincin foto tujuh warna.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Young Serif", "Nunito Sans:wght@400;600;700;800"];
// Painted by /tmp/pen/art/themes/tedak-siten.py
const Art = makeArt("tedak-siten", {
  tangga: [300, 475], jadah: [440, 138], kurungan: [320, 381], kembang: [420, 139], melati: [72, 79], petal: [44, 34],
} as const);

const RITES = [
  { art: "jadah", title: "Napak jadah tujuh warna", body: "Kaki kecilnya menapaki tujuh jadah dari merah hingga ungu: doa agar kelak ia sanggup melewati setiap tahap kehidupan." },
  { art: "tangga", title: "Naik tangga tebu", body: "Tebu, \"antebing kalbu\": dengan hati yang mantap ia belajar meniti anak tangga menuju masa depan." },
  { art: "kurungan", title: "Masuk kurungan", body: "Di dalam kurungan berhias bunga ia memilih benda yang disukai, gambaran kecil minat dan cita-citanya." },
  { art: "kembang", title: "Siraman kembang setaman", body: "Dimandikan air kembang setaman agar namanya harum, lalu udhik-udhik disebar sebagai tanda welas asih." },
] as const;

function monthsAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let m = (d.getFullYear() - b.getFullYear()) * 12 + d.getMonth() - b.getMonth();
  if (d.getDate() < b.getDate()) m -= 1;
  return m > 0 && m < 36 ? m : undefined;
}

function Scene({ eager }: { eager?: boolean }) {
  return (
    <>
      <Art name="tangga" eager={eager} className={s.stTangga} />
      <Art name="jadah" eager={eager} className={s.stJadah} />
      <Art name="kurungan" eager={eager} className={s.stKurungan} />
    </>
  );
}

export default function TedakSitenTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Tedak Siten";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const months = monthsAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#fbf1e7"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="petal" eager className={`${s.petal} ${s.petal1}`} />
          <Art name="petal" eager className={`${s.petal} ${s.petal2}`} />
          <Art name="petal" eager className={`${s.petal} ${s.petal3}`} />
          <p className={s.pill}>Undangan {label}</p>
          <span className={s.ribbon} aria-hidden />
          <h1 className={s.coverName}>{names}</h1>
          <p className={s.coverSub}>pertama kali menapak bumi{months ? <> · <b>{months} bulan</b></> : null}</p>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fffaf3" />Buka Undangan</button>
          </div>
          <div className={s.stage} aria-hidden><Scene eager /></div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fffaf3"
        dark="#4a3440"
        demoWishes={[
          { id: "w1", name: "Eyang Putri Kusumaningrum", attendance: "yes", message: "Sugeng tedak siten, cah ayu. Mugi tansah pinaringan sehat, kuat, lan saged lumampah ing dalan ingkang sae." },
          { id: "w2", name: "Tante Dewi & Om Bayu", attendance: "yes", message: "Selamat menapak bumi, Kinan! Semoga langkahmu selalu ringan, sehat terus dan jadi kebanggaan Ayah Bunda." },
          { id: "w3", name: "Keluarga Bapak Santoso", attendance: "maybe", message: "Mohon maaf bila belum bisa hadir. Doa kami, semoga Kinan tumbuh jadi anak yang mandiri dan berbudi." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Sugeng Rawuh",
            title: "Nyuwun Pangestu",
            sub: `Mudhun Lemah · ${label}`,
            intro: `Dengan penuh rasa syukur, kami mengundang Bapak/Ibu/Saudara/i untuk menyaksikan ${label.toLowerCase()} putri kami, ${names}. Tedak siten adalah upacara adat Jawa ketika bayi berusia pitung lapan pertama kali menapakkan kaki ke tanah, sebagai doa agar kelak ia kuat, mandiri, dan selalu menemukan jalan yang baik dalam hidupnya.`,
          },
          roles: ["Yang Menapak Bumi", "Bersama"],
          couple: ["Si Kecil", child ? `Kenalan dengan ${nick}` : "Yang Merayakan"],
          count: ["Ngetung Dina", "Menuju Hari Pertama Menapak"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Tumbuh Kembang", `Bulan-bulan Pertama ${nick}`],
          gallery: ["Galeri", "Momen Kecil"],
          wishes: ["Pangestu", "Doa & Kehadiran"],
          gifts: ["Tanda Sayang", "Kado & Amplop Digital"],
          closing: {
            thanks: "Matur Nuwun",
            text: `Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah bekal terindah bagi langkah pertama ${names}.`,
          },
          attend: { maybe: "Mungkin" },
          sent: "Matur nuwun, doa dan ucapan Anda sudah terkirim.",
          wishPlaceholder: `Tuliskan doa untuk langkah pertama ${names}…`,
        }}
        hero={(
          <header className={s.hero}>
            <Art name="kembang" className={s.heroKembang} />
            <p className={s.heroKicker}>{label}{months ? ` · ${months} bulan` : ""}</p>
            <h1 className={s.heroName}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <h2 className={s.ritesTitle}>Makna Upacara</h2>
            <ol className={s.rites}>
              {RITES.map(rite => (
                <li key={rite.title}>
                  <span className={s.riteArt} aria-hidden><Art name={rite.art} /></span>
                  <div><h3>{rite.title}</h3><p>{rite.body}</p></div>
                </li>
              ))}
            </ol>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="kembang" /></span>,
          node: <Art name="melati" />,
          portrait: <Art name="kembang" className={s.portraitKembang} />,
          countDecor: <Art name="jadah" className={s.countJadah} />,
          closingDecor: <div className={s.closingScene} aria-hidden><Scene /></div>,
          closingEmblem: <Art name="kembang" className={s.closingKembang} />,
          sentArt: <Art name="kembang" />,
        }}
      />
    </ThemeShell>
  );
}
