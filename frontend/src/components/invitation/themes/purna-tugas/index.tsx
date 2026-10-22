"use client";
// Theme "Purna Tugas" — syukuran pensiun dalam biru tua dan krem: buku kenangan terbuka bersampul kain biru dengan bunga
// kering, selotip washi, tulisan tangan dan pita pembatas, pena tinta yang bergerak pelan seperti sedang menulis, garis
// waktu karier di kertas bergaris bermargin, foto tempel bertali selotip, kartu indeks untuk acara.
import { Lucide, ThemeShell, formatDate, guestLabel, storyItems, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bodoni Moda:ital,wght@0,400;0,500;1,400;1,500", "Figtree:wght@400;500;600", "Homemade Apple"];
// Painted by /tmp/pen/art/themes/purna-tugas.py
const Art = makeArt("purna-tugas", { journal: [560, 402], pen: [300, 42], pressed: [213, 386], bloom: [72, 72] } as const);

export default function PurnaTugasTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Syukuran Purna Tugas";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const full = child?.name.trim() || data.couple.brideFull || "";
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const firstYear = /\d{4}/.exec(storyItems(data)[0]?.date ?? "")?.[0];
  const lastYear = toDate(data.date)?.getFullYear();
  const span = firstYear && lastYear && lastYear > Number(firstYear) ? lastYear - Number(firstYear) : undefined;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#22345a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.book} aria-hidden>
            <Art name="journal" eager />
            <Art name="pen" eager className={s.coverPen} />
          </div>
          <p className={s.kicker}>{label}</p>
          <h1 className={s.coverName}>{names}</h1>
          {full && full !== names && <p className={s.coverFull}>{full}</p>}
          {span && <p className={s.coverHand}>terima kasih untuk {span} tahun pengabdian</p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#1d2a45" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#f3dfb2"
        dark="#22345a"
        demoWishes={[
          { id: "w1", name: "Hendra, alumni angkatan 2003", attendance: "yes", message: "Terima kasih, Pak, sudah sabar mengajari saya pecahan sampai paham. Selamat menikmati masa purnabakti, sehat selalu!" },
          { id: "w2", name: "Rekan guru SMP Negeri Klojen", attendance: "yes", message: "Selamat purna tugas, Pak Bambang. Teladan dan kehangatan Bapak akan selalu kami ingat di ruang guru." },
          { id: "w3", name: "Keluarga Bapak Wiryo", attendance: "maybe", message: "Mohon maaf kalau berhalangan. Semoga masa pensiun penuh berkah, banyak waktu untuk cucu dan kebun." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Dengan penuh syukur",
            title: "Terima Kasih untuk Perjalanan Panjang Ini",
            intro: `Setelah ${span ? `${span} tahun ` : ""}mengabdi, ${names} kini memasuki masa purna tugas. Bersama keluarga, kami mengundang Bapak/Ibu/Saudara/i, rekan kerja, murid dan sahabat, untuk hadir dalam ${label.toLowerCase()} dan berbagi kenangan di babak baru ini.`,
          },
          roles: ["Purna Tugas", "Bersama"],
          couple: ["Sosok yang Kami Syukuri", "Sang Purnabakti"],
          count: ["Menuju Malam Syukuran", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat Tanggalnya", "Waktu & Tempat"],
          story: ["Jejak Pengabdian", "Perjalanan Karier"],
          gallery: ["Album", "Lembar Kenangan"],
          wishes: ["Buku Tamu", "Kesan, Pesan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Terima Kasih",
            text: `Untuk setiap doa, kerja sama dan persahabatan yang menyertai perjalanan ${names}. Sampai jumpa di malam syukuran.`,
            salam: "dengan hormat dan hangat,",
          },
          attend: { maybe: "Mungkin" },
          sent: "Terima kasih, kesan dan pesan Anda sudah tercatat di buku kenangan.",
          wishPlaceholder: `Tuliskan kesan, pesan atau kenangan bersama ${names}…`,
          closedNote: "Terima kasih atas perhatiannya. Kesan dan pesan masih bisa ditulis lewat form ini.",
        }}
        hero={(
          <header className={s.hero}>
            {firstYear && lastYear && <p className={s.years} aria-label={`${firstYear} sampai ${lastYear}`}>{firstYear}<i aria-hidden />{lastYear}</p>}
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroName}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="pressed" className={s.heroPressed} />
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="pen" /></span>,
          node: <Art name="bloom" />,
          portrait: <Art name="pen" className={s.portraitPen} />,
          countDecor: <><Art name="pressed" className={`${s.countPressed} ${s.countPressedL}`} /><Art name="pressed" className={`${s.countPressed} ${s.countPressedR}`} /></>,
          closingEmblem: <Art name="journal" className={s.closingJournal} />,
          sentArt: <Art name="pressed" />,
        }}
      />
    </ThemeShell>
  );
}
