"use client";
// Theme "Kawin Emas" — syukuran 50 tahun pernikahan yang diadakan anak, cucu, dan cicit (desain orisinal): album foto
// keluarga bersampul kulit dengan cap emas, cetakan foto sepia bersudut hitam, keterangan mesin ketik, krisan cat air
// emas-krem-karat, dan karangan daun berlapis emas untuk angka 50.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Playfair Display:ital,wght@0,400;0,600;1,400", "EB Garamond:ital,wght@0,400;0,600;1,400", "Pinyon Script", "Special Elite", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/kawin-emas.py (tools/art/themes in the repo).
const Art = makeArt("kawin-emas", { bouquet: [520, 471], krisan: [150, 131], wreath: [320, 316], divider: [300, 29] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Lima Puluh Tahun Bersama",
    intro: "Dengan memanjatkan puji syukur ke hadirat Allah SWT, kami putra-putri, cucu, dan cicit bermaksud menyelenggarakan syukuran 50 tahun pernikahan Eyang Kakung dan Eyang Putri. Merupakan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan turut mendoakan.",
  },
  roles: ["Eyang Putri", "Eyang Kakung"],
  couple: ["yang kami syukuri", "Eyang Berdua"],
  count: ["menghitung hari", "Menuju Hari Syukuran"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["waktu & tempat", "Rangkaian Acara"],
  story: ["halaman demi halaman", "Album Perjalanan"],
  gallery: ["foto-foto lama", "Kenangan Keluarga"],
  wishes: ["doa untuk Eyang", "Ucapan & Konfirmasi"],
  gifts: ["berbagi kebahagiaan", "Tanda Kasih"],
  closing: {
    thanks: "Terima Kasih",
    text: "Atas kehadiran dan doa Bapak/Ibu/Saudara/i untuk Eyang, kami sekeluarga mengucapkan terima kasih. Semoga Allah memberi Eyang berdua umur yang berkah, sehat, dan bahagia.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Matur suwun, doa untuk Eyang sudah terkirim.",
  wishPlaceholder: "Tuliskan doa dan kenangan bersama Eyang…",
  closedNote: "Terima kasih atas doa dan perhatiannya untuk Eyang. Ucapan masih bisa dikirim lewat form ini.",
  giftIntro: "Kehadiran dan doa untuk Eyang sudah lebih dari cukup. Bila berkenan berbagi, tanda kasih akan kami salurkan ke panti wreda di Klaten atas nama Eyang berdua.",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Cucu-cucu di Yogyakarta", attendance: "yes" as Attendance, message: "Selamat ulang tahun pernikahan emas, Eyang Kakung dan Eyang Putri! Terima kasih sudah jadi teladan bagaimana saling setia. Kami sayang Eyang." },
  { id: "w2", name: "Bu Darmini, teman mengajar SD 2", attendance: "yes" as Attendance, message: "Bu Sri dan Pak Harjono, lima puluh tahun dan masih selalu berdua ke pasar. Semoga sehat terus dan panjang umur." },
  { id: "w3", name: "Keluarga Pakde Sumarno, Solo", attendance: "maybe" as Attendance, message: "Insyaallah kami datang. Doa kami: semoga Mas Harjono dan Mbak Sri diberi umur berkah dan selalu rukun." },
];

export default function KawinEmasTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Syukuran 50 Tahun Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const names = <>{data.couple.bride}{data.couple.groom?.trim() && <><em>&amp;</em>{data.couple.groom}</>}</>;

  return (
    <ThemeShell
      fonts={FONTS}
      background="#4b2a19"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <p className={s.kicker}>Album Kenangan Keluarga</p>
          <div className={s.wreath}>
            <Art name="wreath" eager />
            <b>50</b>
            <small>TAHUN</small>
          </div>
          <p className={s.coverLabel}>{label}</p>
          <h1 className={s.coverNames}>{names}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.plate}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#3a2410" />Buka Undangan</button>
          </div>
          <Art name="bouquet" eager className={s.coverBouquet} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ecd08a"
        dark="#6e3f1c"
        copy={COPY}
        demoWishes={WISHES}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{names}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.print}>
                <div className={s.heroPhoto}><Photo src={hero} alt="" /></div>
                <p>masih berdua, setelah lima puluh tahun</p>
                <Art name="krisan" className={s.heroKrisan} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="krisan" />,
          amp: <Art name="krisan" />,
          portrait: <span className={s.pCap} aria-hidden>kenangan</span>,
          closingEmblem: <div className={s.seal} aria-hidden><Art name="wreath" /><b>50</b></div>,
          sentArt: <Art name="krisan" />,
        }}
      />
    </ThemeShell>
  );
}
