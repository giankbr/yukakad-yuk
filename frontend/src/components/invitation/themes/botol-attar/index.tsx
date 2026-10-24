"use client";
// Theme "Botol Attar" — toko attar di kampung Arab: rak kayu berukir berisi botol kaca zamrud, delima, nila, dan
// kecubung bertutup filigri emas, diterangi lampu hangat di atas beludru ungu tua. Sampulnya label parfum bersudut
// potong di bawah rak, mabkhara kuningan berasap di kaki kiri dan kelopak mawar di kanan. Monogram mempelai berada
// di dalam botol kaca, hitung mundur berbentuk empat botol kecil, kartu acara seperti label parfum. Tanpa figur dan
// tanpa kaligrafi lukis (Arab hanya teks). Dilukis oleh /tmp/pen/art/themes/botol-attar.py.
import { Lucide, ThemeShell, formatDate, guestLabel, type Attendance, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cinzel Decorative:wght@700", "Cormorant Garamond:ital,wght@0,500;0,600;0,700;1,500", "El Messiri:wght@600;700", "Amiri"];
const Art = makeArt("botol-attar", {
  rak: [780, 429], mabkhara: [208, 276], asap: [117, 401], botol: [160, 291], kelopak: [353, 140], filigri: [403, 42],
} as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
    title: "Undangan Walimah",
    sub: "Seharum doa yang dititipkan",
    intro: "Dengan memohon rahmat dan ridha Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimatul 'ursy putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Dua Racikan", "Kedua Mempelai"],
  count: ["Menanti Hari", "Menuju Akad"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat Tanggalnya", "Waktu & Tempat"],
  story: ["Racikan Perjalanan", "Kisah Kami"],
  gallery: ["Galeri", "Momen Bahagia"],
  wishes: ["Doa & Kehadiran", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: {
    thanks: "Jazakumullah Khairan",
    text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah wangi yang akan kami kenang selamanya. Atas perhatiannya, kami ucapkan terima kasih.",
    salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
  },
  sent: "Jazakumullah khairan, doa dan ucapan Anda sudah kami terima.",
  wishPlaceholder: "Tuliskan doa untuk kedua mempelai…",
  giftIntro: "Doa Anda adalah hadiah yang paling harum bagi kami. Bila berkenan memberi tanda kasih, dapat melalui:",
};

const WISHES = [
  { id: "w1", name: "Ammi Hasan & Keluarga, Ampel", attendance: "yes" as Attendance, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga rumah tangganya harum seperti gaharu terbaik." },
  { id: "w2", name: "Teman Apotek Aisyah", attendance: "yes" as Attendance, message: "Masya Allah, selamat Aisyah & Rayyan! Semoga sakinah, mawaddah, warahmah, dan racikan cintanya awet sampai jannah." },
  { id: "w3", name: "Keluarga Baraja, Gresik", attendance: "maybe" as Attendance, message: "Insyaallah kami usahakan hadir. Doa terbaik dari Gresik untuk kalian berdua." },
];

export default function BotolAttarTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const groom = data.couple.groom?.trim();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#23091c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.shelf} aria-hidden><Art name="rak" eager /></div>
          <div className={s.label}>
            <div className={s.labelIn}>
              <p className={s.coverArabic} lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
              <p className={s.kicker}>{label}</p>
              <h1 className={s.coverNames}><span>{data.couple.bride}</span>{groom && <><em>&amp;</em><span>{groom}</span></>}</h1>
              <p className={s.coverDate}>{formatDate(data.date)}</p>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#23091c" />Buka Undangan</button>
          <span className={s.burner} aria-hidden><Art name="mabkhara" eager /><Art name="asap" eager /></span>
          <Art name="kelopak" eager className={s.petals} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        demoWishes={WISHES}
        light="#f1d99c"
        dark="#34122b"
        copy={COPY}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}{groom && <><em>dan</em>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            <div className={s.heroStill} aria-hidden>
              <Art name="botol" className={s.heroBottle} />
              <Art name="mabkhara" className={s.heroBurner} />
              <Art name="asap" className={s.heroSmoke} />
              <Art name="kelopak" className={s.heroPetals} />
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="filigri" className={s.divider} />,
          node: <Art name="botol" />,
          amp: <Art name="botol" />,
          portrait: <Art name="kelopak" className={s.portraitArt} />,
          countDecor: <Art name="asap" className={s.smoke} />,
          closingDecor: <Art name="rak" className={s.closingScene} />,
          closingEmblem: <span className={s.closingEmblem} aria-hidden><Art name="mabkhara" /><Art name="asap" /></span>,
          sentArt: <Art name="botol" />,
        }}
      />
    </ThemeShell>
  );
}
