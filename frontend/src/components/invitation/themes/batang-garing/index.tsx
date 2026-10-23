"use client";
// Theme "Batang Garing" — pohon kehidupan Dayak Ngaju sebagai ornamen lukisan rakyat (terinspirasi, dekoratif): batang
// tombak di atas balanga, cabang bertingkat yang ujungnya bergulung, daun merah-kuning kunyit berlis hitam dan burung
// kecil di puncak; Sungai Kahayan saat fajar; bingkai bersudut potong di atas kain kulit kayu.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Federant", "Literata:ital,wght@0,400;0,600;0,700;1,400"];
// Painted by /tmp/pen/art/themes/batang-garing.py.
const Art = makeArt("batang-garing", { tree: [497, 800], river: [860, 334], curl: [240, 213], bird: [200, 111], band: [570, 63] } as const);

const WISHES = [
  { id: "w1", name: "Keluarga Bapak Yulianus Nyahu", attendance: "yes" as const, message: "Selamat menempuh hidup baru, Hana dan Andre. Kiranya Tuhan memberkati rumah tangga kalian, tumbuh kokoh seperti batang garing." },
  { id: "w2", name: "Pemuda GKE Imanuel", attendance: "yes" as const, message: "Akhirnya! Dari satu perahu di Kahayan sampai ke pelaminan. Tuhan Yesus memberkati, sampai jumpa di Betang Hapakat." },
  { id: "w3", name: "Ibu Marta Pandong", attendance: "maybe" as const, message: "Maaf belum tentu bisa hadir karena masih di Kuala Kapuas. Doa terbaik dari kami sekeluarga." },
];

export default function BatangGaringTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const hero = data.gallery[0] ?? data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1f2c28"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverBand} aria-hidden />
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.treeWrap}>
            <Art name="tree" eager className={s.tree} />
          </div>
          <div className={s.coverFoot}>
            <Art name="river" eager className={s.coverRiver} />
            <div className={s.guestPanel}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#1c1612" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1c867"
        dark="#1c1612"
        noPhotos={!data.couple.bridePhoto && !data.couple.groomPhoto}
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Tabe, Salam Sejahtera",
            title: "Kasih yang Bertumbuh",
            sub: "Isen mulang, bersama dalam semangat huma betang",
            intro: "Dengan sukacita dan atas kasih karunia Tuhan, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan memberikan doa restu pada pernikahan kami.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dua keluarga, satu betang", "Kedua Mempelai"],
          count: ["Menghitung hari", "Menuju Hari Bahagia"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu dan tempat", "Rangkaian Acara"],
          story: ["Akar dan tunas", "Perjalanan Kami"],
          gallery: ["Kenangan", "Galeri Foto"],
          wishes: ["Doa dan ucapan", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang tak ternilai bagi kami dan kedua keluarga besar.", salam: "Tuhan memberkati" },
          sent: "Terima kasih, doa dan ucapan Anda sudah kami terima.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
          giftIntro: "Doa restu Anda adalah kado terindah. Bila ingin memberi tanda kasih, dapat melalui:",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="bird" className={s.heroBird} />
            <p className={s.heroKicker}>{label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {hero && (
              <div className={s.heroFrame}>
                <div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div>
                <Art name="curl" className={s.heroCurlL} />
                <Art name="curl" className={s.heroCurlR} />
              </div>
            )}
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="band" className={s.divider} />,
          node: <Art name="bird" />,
          amp: <Art name="curl" />,
          portrait: <Art name="curl" />,
          countDecor: <span className={s.countDecor} aria-hidden><Art name="river" /></span>,
          closingEmblem: <Art name="tree" className={s.closingEmblem} />,
          closingDecor: <span className={s.closingRiver} aria-hidden><Art name="river" /></span>,
          sentArt: <Art name="bird" />,
        }}
      />
    </ThemeShell>
  );
}
