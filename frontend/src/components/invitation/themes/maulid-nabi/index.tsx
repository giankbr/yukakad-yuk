"use client";
// Theme "Maulid Nabi" — undangan peringatan Maulid Nabi Muhammad SAW dari DKM / majelis taklim (desain orisinal): malam
// hijau zamrud, untaian janur dengan rumbai menjuntai, lentera kuningan yang menyala, kembang endog kertas dalam pot
// kuningan, dan bintang delapan dari foil emas. Pengisi acara tampil dari data mempelai (penceramah + grup shalawat),
// tema tausiyah dari catatan pembuka, sesi dari daftar acara, rangkaian kegiatan dari cerita. Tanpa figur makhluk
// bernyawa, tanpa kaligrafi yang digambar (teks Arab diketik dengan Amiri), dan tidak menggambarkan Nabi dalam bentuk apa pun.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Prata", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Marcellus SC", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/maulid-nabi.py (tools/art/themes in the repo).
const Art = makeArt("maulid-nabi", {
  lantern: [130, 298], lantern2: [130, 264], janur: [780, 186], kembang: [300, 394], star: [120, 120],
} as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";
const SHALAWAT = "اللّٰهُمَّ صَلِّ عَلٰى سَيِّدِنَا مُحَمَّدٍ";

const WISHES = [
  { id: "w1", name: "Majelis Taklim Al-Hidayah Kalimalang", attendance: "yes" as Attendance, message: "Insyaallah kami hadir bersama 30 jamaah ibu-ibu. Semoga peringatan Maulid ini menambah cinta kita kepada Rasulullah dan membawa keberkahan." },
  { id: "w2", name: "Ibu Hj. Maryam", attendance: "yes" as Attendance, message: "Allahumma shalli 'ala Sayyidina Muhammad. Terima kasih undangannya, semoga santunan untuk anak-anak yatim berjalan lancar." },
  { id: "w3", name: "Keluarga Bapak Junaedi", attendance: "no" as Attendance, message: "Mohon maaf belum bisa hadir karena sedang di luar kota. Kami titipkan infaq lewat rekening panitia. Jazakumullahu khairan." },
];

export default function MaulidNabiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Peringatan Maulid Nabi Muhammad SAW";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const speaker = child?.name.trim() || data.couple.brideFull?.trim() || data.couple.bride;
  const second = !child && data.couple.groom?.trim() ? (data.couple.groomFull?.trim() || data.couple.groom) : undefined;
  const topic = data.couple.note?.trim();
  const table = tableLabel(data.guestTable);
  const place = data.place?.trim();
  const host = data.extras?.family?.enabled !== false ? data.extras?.family?.names?.find(name => name.trim())?.trim() : undefined;
  const hosts = host || place;
  const copy: ThemeCopy = {
    opening: {
      arabic: BISMILLAH,
      kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
      title: "Menyambut Bulan Kelahiran Rasulullah",
      sub: "Allahumma shalli 'ala Sayyidina Muhammad",
      intro: `Dengan memohon rahmat dan ridha Allah SWT, kami mengundang Bapak/Ibu/Saudara/i kaum muslimin dan muslimat untuk menghadiri ${label}${place ? ` yang insyaallah diselenggarakan di ${place}` : ""}. Mari bersama memperbanyak shalawat, meneladani akhlak Rasulullah, dan berbagi kebahagiaan dengan anak-anak yatim.`,
    },
    roles: ["Penceramah", "Lantunan Shalawat"],
    couple: ["Pengisi Acara", second ? "Tausiyah & Shalawat" : "Penceramah"],
    count: ["Menuju Majelis", "Hitung Mundur Peringatan"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Susunan Acara", "Sesi Peringatan"],
    story: ["Menyambut Maulid", "Rangkaian Kegiatan"],
    gallery: ["Dokumentasi", "Peringatan Sebelumnya"],
    wishes: ["Doa & Pesan", "Konfirmasi Kehadiran"],
    gifts: ["Infaq & Santunan", "Salurkan Kepedulian"],
    closing: {
      thanks: "Jazakumullahu Khairan",
      text: "Atas perhatian dan kehadiran Bapak/Ibu/Saudara/i, kami haturkan terima kasih. Semoga Allah mengumpulkan kita bersama Rasulullah dalam kebaikan.",
      salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
    },
    sent: "Jazakumullahu khairan, doa dan konfirmasi Anda sudah kami terima.",
    wishPlaceholder: "Tuliskan doa atau pesan untuk panitia dan jamaah…",
    closedNote: "Konfirmasi kehadiran sudah ditutup. Jazakumullahu khairan atas doa dan perhatiannya, pesan masih bisa dikirim.",
    giftIntro: "Bagi jamaah yang ingin berpartisipasi dalam infaq penyelenggaraan dan santunan anak yatim, dapat disalurkan melalui:",
    giftAddressTitle: "Antar Donasi Sembako",
    familyLabel: null,
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#123d2f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.garland} aria-hidden><Art name="janur" eager /></div>
          <span className={`${s.hang} ${s.hang1}`} aria-hidden><Art name="lantern" eager /></span>
          <span className={`${s.hang} ${s.hang2}`} aria-hidden><Art name="lantern2" eager /></span>
          <span className={`${s.hang} ${s.hang3}`} aria-hidden><Art name="lantern2" eager /></span>
          <span className={`${s.hang} ${s.hang4}`} aria-hidden><Art name="lantern" eager /></span>
          <div className={s.coverBody}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{SHALAWAT}</p>
            <p className={s.coverSalam}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
            <p className={s.coverKicker}>Undangan</p>
            <h1 className={s.coverTitle}>{label}</h1>
            <Art name="star" eager className={s.coverStar} />
            {topic && <p className={s.coverTopic}>&ldquo;{topic}&rdquo;</p>}
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guestBox}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#123d2f" />Buka Undangan</button>
          </div>
          <Art name="kembang" eager className={s.kembangL} />
          <Art name="kembang" eager className={s.kembangR} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#f0d58e"
        dark="#1f6b4e"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{topic ? "Tema Tausiyah" : "Undangan"}</p>
            <h1 className={s.heroTopic}>{topic || label}</h1>
            {topic && <p className={s.heroLabel}>{label}</p>}
            <p className={s.heroWith}>bersama {speaker}{second ? ` dan ${second}` : ""}</p>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroStage} aria-hidden>
              <Art name="lantern" className={s.heroLamp} />
              <Art name="kembang" className={s.heroKembang} />
              <Art name="lantern2" className={s.heroLamp} />
            </div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="star" /><i /></span>,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          portrait: <Art name="star" className={s.pStar} />,
          countDecor: <div className={s.lamps} aria-hidden><Art name="lantern" /><Art name="lantern2" /><Art name="lantern" /></div>,
          closingDecor: <div className={s.closingJanur} aria-hidden><Art name="janur" /></div>,
          closingEmblem: (
            <>
              <div className={s.closingStage} aria-hidden><Art name="kembang" /><Art name="star" /><Art name="kembang" /></div>
              {hosts && <p className={s.closingHost}>Hormat kami, Panitia Peringatan<br />{hosts}</p>}
            </>
          ),
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
