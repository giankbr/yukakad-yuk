"use client";
// Theme "Mamasa Banua" — adat Mamasa (Sulawesi Barat): lembah pinus berkabut dan sawah berundak (cat air), banua dengan
// atap perahu yang berat dan rendah dari sirap kayu, papan ukir bercat merah, kuning, hitam dan putih (gouache).
// Sampul: lembah memenuhi layar, nama di atas papan ukir hitam; hitung mundur dalam kotak belah ketupat.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Kurale", "Alegreya Sans:ital,wght@0,400;0,500;0,700;1,400"];
// Painted by /tmp/pen/art/themes/mamasa-banua.py (band.webp is also a CSS background strip)
const Art = makeArt("mamasa-banua", { valley: [780, 760], medallion: [180, 180], pines: [220, 263], divider: [260, 25] } as const);

export default function MamasaBanuaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#eef0e8"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.valley} aria-hidden><Art name="valley" eager /></div>
          <span className={s.mist} aria-hidden />
          <p className={s.kicker}>Undangan {data.eventLabel ?? "Pernikahan"}</p>
          <div className={s.board}>
            <span className={s.boardMed} aria-hidden><Art name="medallion" eager /></span>
            <h1 className={s.coverNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestWrap}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff6e0" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f0d08a"
        dark="#1f1a17"
        demoWishes={[
          { id: "w1", name: "Pdt. Markus Lebang & Keluarga", attendance: "yes", message: "Selamat menempuh hidup baru, Elsa dan Yosua. Kiranya kasih Tuhan menaungi banua kalian seperti kabut pagi menaungi lembah Mamasa." },
          { id: "w2", name: "Pemuda GTM Tawalian", attendance: "yes", message: "Turut berbahagia! Sampai jumpa di Tawalian, kami siap membantu dari pagi." },
          { id: "w3", name: "Om Daud & Tante Lea", attendance: "maybe", message: "Semoga kami bisa menyusul dari Makassar. Doa kami menyertai kalian berdua, Tuhan memberkati." },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Salam Sejahtera",
            title: "Dalam Kasih Tuhan Yesus Kristus",
            intro: "Dengan penuh syukur atas kasih karunia Tuhan, kami bermaksud melangsungkan pemberkatan nikah putra-putri kami. Merupakan sukacita bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan turut mendoakan.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dipersatukan Tuhan", "Kedua Mempelai"],
          count: ["Menanti Hari Pemberkatan", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Dari Lembah Mamasa", "Kisah Kami"],
          gallery: ["Galeri", "Momen Bersama"],
          wishes: ["Doa & Ucapan", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Terima Kasih",
            text: "Kehadiran dan doa Bapak/Ibu/Saudara/i merupakan sukacita dan berkat bagi kami sekeluarga.",
            salam: "Kurre sumanga', Tuhan memberkati.",
          },
          sent: "Terima kasih, doa dan ucapan Anda sudah terkirim. Tuhan memberkati.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroPhoto}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
            <span className={s.heroBand} aria-hidden />
            <p className={s.heroKicker}>Kami akan menikah</p>
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="divider" /></span>,
          node: <Art name="medallion" />,
          portrait: <Art name="medallion" className={s.portraitMed} />,
          countDecor: <><Art name="pines" className={`${s.countPines} ${s.countPinesL}`} /><Art name="pines" className={`${s.countPines} ${s.countPinesR}`} /></>,
          closingDecor: <><Art name="pines" className={`${s.closingPines} ${s.closingPinesL}`} /><Art name="pines" className={`${s.closingPines} ${s.closingPinesR}`} /></>,
          closingEmblem: <Art name="medallion" className={s.closingMed} />,
          sentArt: <Art name="medallion" />,
        }}
      />
    </ThemeShell>
  );
}
