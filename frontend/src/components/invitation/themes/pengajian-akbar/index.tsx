"use client";
// Theme "Pengajian Akbar" — undangan majelis taklim / pengajian di pelataran masjid saat senja biru: lukisan gouache serambi
// berlengkung runcing yang membingkai kolam pantul, fasad berlengkung yang menyala, kubah hijau sage dan dua menara;
// lentera kuningan bergoyang, roset bintang delapan dari foil emas, pita geometris hijau-emas. Penceramah tampil sebagai
// "yang diundang" (data mempelai / extras.child), tema kajian dari catatan pembuka, sesi acara dari daftar acara.
// Tanpa figur makhluk hidup dan tanpa kaligrafi yang digambar: bismillah diketik dengan huruf Amiri.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Reem Kufi:wght@400;500;600", "Lora:ital,wght@0,400;0,500;0,600;1,400", "Amiri:wght@400;700"];
// Painted by /tmp/pen/art/themes/pengajian-akbar.py (tools/art/themes in the repo).
const Art = makeArt("pengajian-akbar", { scene: [600, 754], lantern: [100, 224], rosette: [120, 121], skyline: [420, 203] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const WISHES = [
  { id: "w1", name: "Majelis Taklim Al-Ikhlas Cimanggu", attendance: "yes" as const, message: "Insyaallah kami hadir bersama rombongan 25 jamaah. Semoga majelisnya penuh berkah dan ilmunya bermanfaat untuk kita semua." },
  { id: "w2", name: "Ibu Hj. Nurhasanah", attendance: "yes" as const, message: "Barakallahu fiikum. Semoga acara berjalan lancar dan Ustadz senantiasa diberi kesehatan untuk terus berdakwah." },
  { id: "w3", name: "Keluarga Bapak Hendra", attendance: "no" as const, message: "Mohon maaf belum bisa hadir karena tugas ke luar kota. Insyaallah kami simak lewat siaran langsung. Jazakumullahu khairan." },
];

export default function PengajianAkbarTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Pengajian Akbar";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const speaker = child?.name.trim() || data.couple.brideFull?.trim() || data.couple.bride;
  const second = !child && data.couple.groom?.trim() ? (data.couple.groomFull?.trim() || data.couple.groom) : undefined;
  const topic = data.couple.note?.trim();
  const table = tableLabel(data.guestTable);
  const place = data.place?.trim();
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      arabic: BISMILLAH,
      kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
      title: "Undangan Majelis Ilmu",
      intro: `Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami mengundang Bapak/Ibu/Saudara/i kaum muslimin dan muslimat untuk menghadiri ${label}${place ? ` yang insyaallah diselenggarakan di ${place}` : ""}. Mari bersama menuntut ilmu, menguatkan iman, dan mempererat ukhuwah.`,
    },
    roles: ["Penceramah", "Qari' & Pembaca Doa"] as [string, string],
    couple: ["Pengisi Majelis", second ? "Penceramah & Qari'" : "Penceramah"] as [string, string],
    count: ["Menuju Majelis", "Hitung Mundur Kajian"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Susunan Acara", "Sesi Majelis"] as [string, string],
    story: ["Profil Majelis", "Perjalanan Kami"] as [string, string],
    gallery: ["Dokumentasi", "Majelis Sebelumnya"] as [string, string],
    wishes: ["Doa & Pesan", "Konfirmasi Kehadiran"] as [string, string],
    gifts: ["Infaq & Sedekah", "Salurkan Infaq"] as [string, string],
    closing: {
      thanks: "Jazakumullahu Khairan",
      text: "Atas perhatian dan kehadiran Bapak/Ibu/Saudara/i, kami haturkan terima kasih. Semoga majelis ini menjadi taman surga yang mempertemukan kita dalam kebaikan.",
      salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
    },
    sent: "Jazakumullahu khairan, doa dan konfirmasi Anda sudah kami terima.",
    wishPlaceholder: "Tuliskan doa atau pesan untuk majelis…",
    closedNote: "Konfirmasi kehadiran sudah ditutup. Jazakumullahu khairan atas doa dan perhatiannya, pesan masih bisa dikirim.",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6f0e1"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.scene} aria-hidden>
            <Art name="scene" eager className={s.sceneImg} />
            <div className={s.coverLamps}><Art name="lantern" eager /><Art name="lantern" eager /></div>
          </div>
          <div className={s.coverBody}>
            <p className={s.coverArabic} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.coverSalam}>Assalamu&apos;alaikum Warahmatullahi Wabarakatuh</p>
            <p className={s.coverKicker}>Undangan</p>
            <h1 className={s.coverTitle}>{label}</h1>
            {topic && <p className={s.coverTopic}>&ldquo;{topic}&rdquo;</p>}
            <p className={s.coverWith}>bersama <b>{speaker}</b></p>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestBox}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#f3dc9c" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#f3dc9c"
        dark="#1f4d3f"
        copy={copy}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <Art name="rosette" className={s.heroRosette} />
            <p className={s.heroKicker}>{topic ? "Tema Kajian" : label}</p>
            <h1 className={s.heroTopic}>{topic || label}</h1>
            {topic && <p className={s.heroLabel}>{label}</p>}
            <p className={s.heroWith}>bersama {speaker}{second ? ` dan ${second}` : ""}</p>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="scene" className={s.heroScene} />
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><i /><Art name="rosette" /><i /></span>,
          node: <Art name="rosette" />,
          portrait: <Art name="rosette" />,
          countDecor: <div className={s.lamps} aria-hidden><Art name="lantern" /><Art name="lantern" /><Art name="lantern" /></div>,
          closingEmblem: <div className={s.skyWrap} aria-hidden><Art name="skyline" className={s.skyline} /></div>,
          sentArt: <Art name="rosette" />,
        }}
      />
    </ThemeShell>
  );
}
