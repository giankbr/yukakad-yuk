"use client";
// Theme "Asmat Ukir" — adat Asmat (Papua Selatan), pasangan Kristiani. Papan ukir kayu gelap terinspirasi relief Asmat:
// kait berparuh enggang, kaki belalang sembah, spiral ganda dan alur sungai berwarna putih kapur, merah oker dan arang
// (gouache), sungai rawa berkabut dengan perahu lesung panjang dan akar bakau (cat air). Bingkai foto daun dayung,
// kartu acara berlis papan ukir, garis gerigi, dan medali ukir sebagai simpul cerita.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Big Shoulders Display:wght@700;800", "Alegreya:ital,wght@0,400;0,500;0,700;1,400;1,500"];
// Painted by /tmp/pen/art/themes/asmat-ukir.py
const Art = makeArt("asmat-ukir", { river: [780, 760], band: [320, 28], medal: [200, 197] } as const);

const WISHES = [
  { id: "w1", name: "Bapak Paulus Tamot & Keluarga", attendance: "yes" as const, message: "Syalom! Tuhan Yesus memberkati rumah tangga kalian. Semoga kokoh seperti kayu besi dan selalu seiring seperti dayung dalam satu perahu." },
  { id: "w2", name: "Suster Veronika", attendance: "yes" as const, message: "Selamat Agustina dan Natalis. Kami berdoa agar kasih kalian terus mengalir seperti sungai yang tak pernah kering." },
  { id: "w3", name: "Teman-teman guru SD Inpres", attendance: "maybe" as const, message: "Belum tentu bisa turun ke Agats karena air surut, tapi doa kami ikut mendayung bersama kalian. Tuhan memberkati!" },
];

export default function AsmatUkirTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();
  const label = data.eventLabel ?? "Pernikahan";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1f130c"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={`${s.coverPanel} ${s.coverPanelL}`} aria-hidden />
          <span className={`${s.coverPanel} ${s.coverPanelR}`} aria-hidden />
          <div className={s.coverTop}>
            <Art name="medal" eager className={s.coverMedal} />
            <p className={s.kicker}>Syalom · Undangan {label}</p>
            <h1 className={s.coverNames}><span>{bride}</span><i>dan</i><span>{groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.river} aria-hidden>
            <Art name="river" eager />
            <span className={s.mist} />
          </div>
          <div className={s.plank}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#efe7d6" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#efe7d6"
        dark="#3a2416"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Salam damai dalam kasih Kristus",
            title: "Syalom",
            sub: "Tuhan yang mempertemukan, Tuhan pula yang mempersatukan",
            intro: "Dengan penuh syukur atas kasih karunia Tuhan, kami bermaksud melangsungkan pemberkatan nikah putra-putri kami. Merupakan sukacita bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
          },
          roles: ["Mempelai Perempuan", "Mempelai Laki-laki"],
          couple: ["Dua keluarga, satu perahu", "Kedua Mempelai"],
          count: ["Air pasang menuju hari bahagia", "Menghitung Hari"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & tempat", "Rangkaian Acara"],
          story: ["Menyusuri sungai", "Kisah Kami"],
          gallery: ["Kenangan", "Galeri"],
          wishes: ["Doa & ucapan", "Kirim Doa"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: {
            thanks: "Terima Kasih",
            text: "Kehadiran dan doa Bapak/Ibu/Saudara/i adalah berkat yang tak ternilai bagi kami sekeluarga.",
            salam: "Tuhan Yesus memberkati",
          },
          attend: { maybe: "Mungkin" },
          sent: "Terima kasih, doa dan ucapan Anda sudah kami terima. Tuhan memberkati.",
          wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
          giftIntro: "Doa Anda adalah hadiah terindah bagi kami. Bila ingin memberi tanda kasih, dapat melalui:",
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroRiver} aria-hidden><Art name="river" /></div>
            <p className={s.heroKicker}>Atas berkat Tuhan, kami menikah</p>
            <div className={s.heroBlade}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
            <span className={s.heroBand} aria-hidden><Art name="band" /></span>
            <h1 className={s.heroNames}>{bride}<i>dan</i>{groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="band" /></span>,
          node: <Art name="medal" />,
          amp: <Art name="band" />,
          portrait: <Art name="medal" className={s.portraitMedal} />,
          countDecor: <><span className={`${s.countPanel} ${s.countPanelL}`} aria-hidden /><span className={`${s.countPanel} ${s.countPanelR}`} aria-hidden /></>,
          closingDecor: <><span className={`${s.closingPanel} ${s.closingPanelL}`} aria-hidden /><span className={`${s.closingPanel} ${s.closingPanelR}`} aria-hidden /></>,
          closingEmblem: <Art name="medal" className={s.closingMedal} />,
          sentArt: <Art name="medal" />,
        }}
      />
    </ThemeShell>
  );
}
