"use client";
// Theme "Paskah Keluarga" — ibadah subuh dan brunch Paskah keluarga jemaat: kubur batu yang kosong di bawah langit
// fajar bercat air (batu penutup sudah terguling), lili putih yang bergoyang pelan, telur hias dalam keranjang anyam,
// ranting musim semi; kartu dan bingkai berbentuk jendela kapel lengkung, lilac lembut dan krem.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import type { Attendance } from "../kit";
import s from "./styles.module.css";

const FONTS = ["Libre Caslon Display", "Libre Caslon Text:ital,wght@0,400;0,700;1,400", "Imperial Script"];
// Painted by /tmp/pen/art/themes/paskah-keluarga.py (tools/art/themes in the repo).
const Art = makeArt("paskah-keluarga", {
  lilies: [480, 548], lily: [150, 201], eggs: [360, 158], egg: [80, 88], sprig: [440, 55],
} as const);

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Latuheru", attendance: "yes" as Attendance, message: "Selamat Paskah! Kristus bangkit, pengharapan kita hidup. Sampai jumpa di ibadah subuh, kami bawa nasi kuning untuk brunch." },
  { id: "w2", name: "Ibu Ester Wattimena", attendance: "yes" as Attendance, message: "Puji Tuhan untuk tradisi yang indah ini. Kiranya sukacita kebangkitan memenuhi setiap keluarga yang hadir." },
  { id: "w3", name: "Kak Mario & Sekolah Minggu", attendance: "maybe" as Attendance, message: "Telur hias sedang dicat anak-anak. Kami usahakan datang lebih pagi untuk menyembunyikannya di taman." },
];

export default function PaskahKeluargaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Perayaan Paskah";
  const hosts = [data.couple.bride?.trim(), data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const note = data.couple.note?.trim();
  const table = tableLabel(data.guestTable);
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Salam Paskah",
      title: "Kristus Telah Bangkit",
      sub: "Ia sungguh telah bangkit",
      intro: `Dengan sukacita kebangkitan, ${hosts || "kami"} mengundang Bapak/Ibu/Saudara/i sekeluarga untuk beribadah bersama di pagi Paskah, lalu bersantap dan bersukacita di taman.`,
    },
    // Both hosts carry their own visible role; the labels double as list keys.
    roles: ["Penyelenggara", "Tuan Rumah"] as [string, string],
    couple: ["yang mengundang", "Tuan Rumah Paskah"] as [string, string],
    count: ["menanti fajar", "Menuju Minggu Paskah"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["waktu & tempat", "Rangkaian Acara"] as [string, string],
    story: ["dari tahun ke tahun", "Tradisi Paskah Kami"] as [string, string],
    gallery: ["galeri", "Pagi yang Cerah"] as [string, string],
    wishes: ["salam paskah", "Ucapan & Kehadiran"] as [string, string],
    gifts: ["persembahan kasih", "Persembahan & Diakonia"] as [string, string],
    closing: {
      thanks: "Selamat Paskah",
      text: "Terima kasih telah merayakan pagi kebangkitan bersama kami. Kiranya damai dan pengharapan Kristus yang bangkit menyertai Bapak/Ibu/Saudara/i sekeluarga.",
      salam: "Tuhan memberkati",
    },
    sent: "Terima kasih, salam Paskah Anda sudah kami terima. Tuhan memberkati.",
    attend: { maybe: "Mungkin" },
    wishPlaceholder: "Tuliskan salam dan doa Paskah Anda…",
    closedNote: "Terima kasih atas perhatiannya. Salam Paskah masih bisa dikirim lewat form ini.",
    giftIntro: "Kehadiran Anda adalah sukacita kami. Bila tergerak memberi, persembahan akan disalurkan melalui diakonia untuk keluarga yang membutuhkan:",
    giftAddressTitle: "Bingkisan Diakonia",
    familyLabel: null,
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9e2cf"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverSun} aria-hidden />
          <p className={s.kicker}>{label}</p>
          <p className={s.greet}>Selamat Paskah</p>
          <h1 className={s.coverTitle}>Kristus Telah Bangkit</h1>
          {hosts && <p className={s.coverHosts}>bersama {hosts}</p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="currentColor" />Buka Undangan</button>
          </div>
          <Art name="lilies" eager className={s.coverLilies} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos
        light="#fbf7ec"
        dark="#4a3c6c"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="eggs" className={s.heroEggs} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroTitle}>Selamat Paskah</h1>
            {hosts && <p className={s.heroHosts}>{hosts}</p>}
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="egg" />,
          portrait: <><Art name="lilies" className={s.hostArt} /><Art name="eggs" className={s.hostArt} /></>,
          countDecor: <Art name="eggs" className={s.countEggs} />,
          closingEmblem: <Art name="lilies" className={s.closingLilies} />,
          sentArt: <Art name="lily" />,
        }}
      />
    </ThemeShell>
  );
}
