"use client";
// Theme "Pulang Haji" — tasyakuran menyambut keluarga yang pulang dari ibadah haji, putih dan hijau lembut: sepasang
// payung putih berumbai hijau yang bergoyang pelan, untaian tasbih, lukisan cat air kurma dan air zamzam, bintang
// khatam di sudut, dan doa penyambutan haji (teks Arab diketik). Tanpa foto, tanpa makhluk bernyawa, tanpa gambar
// Ka'bah atau tempat suci.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["El Messiri:wght@400;500;600", "Gentium Book Plus:ital,wght@0,400;0,700;1,400", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/pulang-haji.py.
const Art = makeArt("pulang-haji", { payung: [260, 327], still: [560, 228], tasbih: [600, 170], corner: [220, 220], divider: [300, 28], star: [70, 71] } as const);
const MABRUR = "حَجًّا مَبْرُوْرًا، وَسَعْيًا مَشْكُوْرًا، وَذَنْبًا مَغْفُوْرًا";
const DOA = "تَقَبَّلَ اللّٰهُ حَجَّكَ، وَغَفَرَ ذَنْبَكَ، وَأَخْلَفَ نَفَقَتَكَ";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: MABRUR,
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Alhamdulillah",
    sub: "Haji yang mabrur, sa'i yang diterima, dosa yang diampuni",
    intro: "Puji syukur ke hadirat Allah SWT yang telah memanggil, menjaga, dan memulangkan keluarga kami dari Tanah Suci dalam keadaan sehat. Dengan penuh rasa syukur, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dalam tasyakuran dan doa bersama.",
  },
  roles: ["Bapak Haji", "Ibu Hajjah"],
  couple: ["Telah Kembali dari Tanah Suci", "Yang Kami Sambut"],
  count: ["Menuju Tasyakuran", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Waktu & Tempat", "Rangkaian Acara"],
  story: ["Perjalanan Ibadah", "Dari Niat hingga Pulang"],
  gallery: ["Galeri", "Kenangan"],
  wishes: ["Doa & Kehadiran", "Doa untuk Haji Mabrur"],
  gifts: ["Sedekah", "Santunan Anak Yatim"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Terima kasih atas doa, kunjungan, dan perhatian Bapak/Ibu/Saudara/i selama kami di Tanah Suci. Mohon maaf lahir dan batin atas segala khilaf. Semoga kita semua kelak dipanggil ke sana.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa Anda sudah kami terima. Semoga Allah membalas dengan kebaikan yang sama.",
  wishPlaceholder: "Tuliskan doa dan ucapan untuk keluarga yang baru pulang…",
  giftIntro: "Tidak ada amplop untuk kami. Bila berkenan bersedekah, titipan Anda akan kami salurkan sebagai santunan anak yatim di lingkungan kami.",
  familyLabel: null,
  closedNote: "Terima kasih atas doa dan kunjungannya. Ucapan masih bisa dikirim lewat form ini.",
};

const WISHES = [
  { id: "w1", name: "Keluarga H. Fahrurrazi", attendance: "yes" as const, message: "Taqabbalallahu hajjakum. Semoga menjadi haji mabrur, sehat selalu, dan keberkahannya menular ke seluruh keluarga." },
  { id: "w2", name: "Ibu-ibu Majelis Taklim Al-Ikhlas", attendance: "yes" as const, message: "Alhamdulillah sudah pulang dengan selamat. Semoga menjadi haji mabrur, kami tunggu ceritanya di pengajian." },
  { id: "w3", name: "Rahmadi & Keluarga, Martapura", attendance: "maybe" as const, message: "Insyaallah menyusul sore hari. Semoga hajinya mabrur dan kita semua dimampukan berangkat ke Tanah Suci." },
];

export default function PulangHajiTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Tasyakuran Kepulangan Haji";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const first = child ? child.name.trim() : (data.couple.brideFull?.trim() || data.couple.bride);
  const second = child ? "" : (data.couple.groomFull?.trim() || data.couple.groom?.trim() || "");
  const names = <>{first && <span>{first}</span>}{second && <><em>&amp;</em><span>{second}</span></>}</>;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e8efe7"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="corner" eager className={s.cornerTL} />
          <Art name="corner" eager className={s.cornerBR} />
          <div className={s.payungs} aria-hidden>
            <Art name="payung" eager className={`${s.payung} ${s.payungL}`} />
            <Art name="payung" eager className={`${s.payung} ${s.payungR}`} />
          </div>
          <p className={s.coverKicker}>Walimatul Hajj</p>
          <p className={s.coverLabel}>{label}</p>
          <h1 className={s.coverNames}>{names}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <Art name="tasbih" eager className={s.coverTasbih} />
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        celebrant
        demoWishes={WISHES}
        light="#ffffff"
        dark="#3d6650"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <Art name="corner" className={s.heroCorner} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <Art name="still" className={s.heroStill} />
            {note && <p className={s.heroNote}>{note}</p>}
            <section className={s.doa} aria-labelledby="ph-doa">
              <Art name="star" />
              <h2 id="ph-doa">Doa Menyambut Haji</h2>
              <p className={s.doaAr} lang="ar" dir="rtl">{DOA}</p>
              <p className={s.doaId}>&ldquo;Semoga Allah menerima hajimu, mengampuni dosamu, dan mengganti biaya yang telah engkau keluarkan.&rdquo;</p>
              <p className={s.doaSrc}>Doa para sahabat untuk jamaah yang pulang</p>
            </section>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="star" />,
          countDecor: <Art name="tasbih" className={s.countTasbih} />,
          closingEmblem: <div className={s.closingPayung} aria-hidden><Art name="payung" /><Art name="payung" /></div>,
          sentArt: <Art name="star" />,
        }}
      />
    </ThemeShell>
  );
}
