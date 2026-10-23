"use client";
// Theme "Isra Mi'raj" — undangan peringatan Isra Mi'raj Nabi Muhammad SAW dari DKM / majelis taklim (desain orisinal):
// langit malam nila yang dilukis dengan pita bintang yang naik dan bulan sabit, siluet masjid berkubah dan bermenara
// dengan serambi yang menyala hangat, lentera kuningan berlubang bintang yang berayun, dan bintang delapan dari foil.
// Pengisi acara tampil dari data mempelai (penceramah + pembaca doa), tema tausiyah dari catatan, sesi dari daftar
// acara, susunan acara malam itu dari cerita. Tanpa figur makhluk bernyawa, tanpa penggambaran Buraq maupun Nabi dalam
// bentuk apa pun, tanpa kaligrafi yang digambar (teks Arab diketik dengan Amiri).
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Reem Kufi:wght@400;500", "Spectral:ital,wght@0,400;0,600;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/isra-miraj.py.
const Art = makeArt("isra-miraj", {
  masjid: [360, 203], lantern: [65, 132], star: [55, 55],
} as const);
const BISMILLAH = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ";
const TASBIH = "سُبْحَانَ الَّذِيْٓ اَسْرٰى بِعَبْدِهٖ لَيْلًا";

const WISHES = [
  { id: "w1", name: "Majelis Taklim Al-Mubarak", attendance: "yes" as Attendance, message: "Insyaallah kami hadir bersama 25 jamaah ibu-ibu. Semoga peringatan ini menguatkan shalat kita dan membawa keberkahan bagi seluruh jamaah." },
  { id: "w2", name: "Bapak H. Asep Saepudin", attendance: "yes" as Attendance, message: "Jazakumullahu khairan atas undangannya. Semoga Allah memudahkan seluruh panitia dan menjadikan majelis ini penuh rahmat." },
  { id: "w3", name: "Keluarga Ibu Neneng", attendance: "no" as Attendance, message: "Mohon maaf belum bisa hadir karena sedang di luar kota. Infaq kami titipkan lewat rekening panitia. Semoga lancar dan berkah." },
];

export default function IsraMirajTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Peringatan Isra Mi'raj Nabi Muhammad SAW";
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
      title: "Mengenang Perjalanan Malam yang Agung",
      sub: "Subhanalladzi asra bi'abdihi lailan",
      intro: `Dengan memohon rahmat dan ridha Allah SWT, kami mengundang Bapak/Ibu/Saudara/i kaum muslimin dan muslimat untuk menghadiri ${label}${place ? ` yang insyaallah diselenggarakan di ${place}` : ""}. Mari bersama mengambil hikmah perjalanan Isra Mi'raj dan menguatkan kembali shalat kita.`,
    },
    roles: ["Penceramah", "Tilawah & Doa"],
    couple: ["Pengisi Acara", second ? "Tausiyah & Doa" : "Penceramah"],
    count: ["Menuju Malam Peringatan", "Hitung Mundur"],
    units: ["Hari", "Jam", "Menit", "Detik"],
    events: ["Waktu & Tempat", "Sesi Peringatan"],
    story: ["Malam Itu", "Susunan Acara"],
    gallery: ["Dokumentasi", "Peringatan Sebelumnya"],
    wishes: ["Doa & Pesan", "Konfirmasi Kehadiran"],
    gifts: ["Infaq & Santunan", "Salurkan Kepedulian"],
    closing: {
      thanks: "Jazakumullahu Khairan",
      text: "Atas perhatian dan kehadiran Bapak/Ibu/Saudara/i, kami haturkan terima kasih. Semoga Allah menerima amal kita dan menjaga shalat kita hingga akhir hayat.",
      salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
    },
    sent: "Jazakumullahu khairan, doa dan konfirmasi Anda sudah kami terima.",
    wishPlaceholder: "Tuliskan doa atau pesan untuk panitia dan jamaah…",
    closedNote: "Konfirmasi kehadiran sudah ditutup. Jazakumullahu khairan atas doa dan perhatiannya, pesan masih bisa dikirim.",
    giftIntro: "Bagi jamaah yang ingin berinfaq untuk penyelenggaraan peringatan dan santunan anak yatim, dapat disalurkan melalui:",
    giftAddressTitle: "Antar Donasi",
    familyLabel: null,
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#15173d"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.sky} aria-hidden />
          <Art name="lantern" eager className={`${s.lamp} ${s.lamp1}`} />
          <Art name="lantern" eager className={`${s.lamp} ${s.lamp2}`} />
          <Art name="lantern" eager className={`${s.lamp} ${s.lamp3}`} />
          <p className={s.coverArabic} lang="ar" dir="rtl">{TASBIH}</p>
          <p className={s.coverSalam}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
          <p className={s.coverKicker}>Undangan</p>
          <h1 className={s.coverTitle}>{label}</h1>
          <Art name="star" eager className={s.coverStar} />
          {topic && <p className={s.coverTopic}>&ldquo;{topic}&rdquo;</p>}
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.coverFoot}>
            <div className={s.guestBox}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#15173d" />Buka Undangan</button>
          </div>
          <Art name="masjid" eager className={s.masjid} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ecd59b"
        dark="#26296a"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <div className={s.heroArch}>
              <div className={s.heroLamps} aria-hidden><Art name="lantern" /><Art name="lantern" /></div>
              <Art name="star" className={s.heroStar} />
              <p className={s.heroKicker}>{topic ? "Tema Tausiyah" : "Undangan"}</p>
              <h1 className={s.heroTopic}>{topic || label}</h1>
              {topic && <p className={s.heroLabel}>{label}</p>}
              <p className={s.heroWith}>bersama {speaker}{second ? ` dan ${second}` : ""}</p>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
            </div>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="star" /><i /></span>,
          node: <Art name="star" />,
          amp: <Art name="star" />,
          portrait: <Art name="star" />,
          countDecor: <div className={s.countLamps} aria-hidden><Art name="lantern" /><Art name="lantern" /></div>,
          closingDecor: <Art name="masjid" className={s.closingMasjid} />,
          closingEmblem: (
            <>
              <Art name="star" className={s.closingStar} />
              {hosts && <p className={s.closingHost}>{/^panitia/i.test(hosts) ? "Hormat kami," : "Hormat kami, Panitia Peringatan"}<br />{hosts}</p>}
            </>
          ),
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
