"use client";
// Theme "Wayang Golek" — panggung wayang golek Sunda. Sampul adalah kelir hijau tua di bawah rumbai beludru merah:
// nama besar, papan lakon untuk tamu, lalu panggung dengan sepasang golek kayu orisinal (putra bermakuta, putri bersiger)
// yang tertancap di gedebog dan bergoyang pelan di depan gong degung. Halaman dibuka dengan foto dalam bingkai panggung
// dan kendang; potret berumbai, acara jadi papan lakon kayu, kisah ditulis di atas kelir, penutup kembali ke panggung.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Yeseva One", "Alegreya:ital,wght@0,400;0,500;0,700;1,400", "Federant"];
// Painted by /tmp/pen/art/themes/wayang-golek.py
const Art = makeArt("wayang-golek", { putra: [198, 777], putri: [178, 735], gedebog: [800, 105], gong: [360, 313], kendang: [300, 131], valance: [480, 150] } as const);

const WISHES = [
  { id: "w1", name: "Ceu Imas & Kang Asep", attendance: "yes" as const, message: "Wilujeng nikah Resti sareng Gilang! Mugia janten kulawarga sakinah, mawaddah, warahmah, sauyunan dugi ka pupus." },
  { id: "w2", name: "Sanggar Degung Pakuan", attendance: "yes" as const, message: "Barudak sanggar siap ngiringan ku degung. Bahagia selalu, semoga lakon kalian panjang dan penuh berkah." },
  { id: "w3", name: "Keluarga Bapak Tatang", attendance: "maybe" as const, message: "Hapunten upami teu tiasa hadir. Doa kami menyertai, semoga Allah memberkahi pernikahan kalian." },
];

function Stage({ eager, className }: { eager?: boolean; className?: string }) {
  return (
    <div className={className ? `${s.stage} ${className}` : s.stage} aria-hidden>
      <Art name="gong" eager={eager} className={s.stageGong} />
      <Art name="putra" eager={eager} className={`${s.golek} ${s.golekL}`} />
      <Art name="putri" eager={eager} className={`${s.golek} ${s.golekR}`} />
      <Art name="gedebog" eager={eager} className={s.gedebog} />
      <span className={s.plank} />
    </div>
  );
}

export default function WayangGolekTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#0f2b29"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.valance} aria-hidden />
          <p className={s.sampur}>Sampurasun</p>
          <p className={s.kicker}>Undangan {label}</p>
          <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.placard}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#fff3dc" />Buka Undangan</button>
          </div>
          <Stage eager />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#f1d491"
        dark="#173f3c"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ",
            kicker: "Assalamu'alaikum Wr. Wb.",
            title: "Sampurasun",
            intro: "Dengan memohon rahmat dan ridho Allah SWT, kami bermaksud menyelenggarakan pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
          },
          roles: ["Mempelai Istri", "Mempelai Pameget"],
          couple: ["Panganten", "Kedua Mempelai"],
          count: ["Ngitung Poé", "Menuju Hari Bahagia"],
          units: ["Poé", "Jam", "Menit", "Detik"],
          events: ["Runtuyan Acara", "Rangkaian Acara"],
          story: ["Lalakon Urang", "Kisah Kami"],
          gallery: ["Galeri", "Momen Bahagia"],
          wishes: ["Du'a & Wawarti", "Ucapan & Konfirmasi"],
          gifts: ["Tanda Asih", "Amplop Digital"],
          closing: {
            thanks: "Hatur Nuhun",
            text: "Kehadiran serta doa restu Bapak/Ibu/Saudara/i merupakan kebahagiaan yang tak ternilai bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Wr. Wb.",
          },
          sent: "Hatur nuhun, doa dan ucapan Anda sudah kami terima.",
          wishPlaceholder: "Tuliskan doa restu untuk kedua mempelai…",
        }}
        hero={(
          <header className={s.hero}>
            <span className={s.valance} aria-hidden />
            <div className={s.heroFrame}>
              {data.gallery[0] ? <div className={s.heroPhoto}><Photo src={data.gallery[0]} alt="" /></div> : <Stage className={s.heroStage} />}
            </div>
            <Art name="kendang" className={s.heroKendang} />
            <p className={s.heroKicker}>Pagelaran {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride} <em>&amp;</em> {data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="gong" /></span>,
          node: <Art name="gong" />,
          portrait: <span className={s.portraitValance} aria-hidden />,
          countDecor: <><Art name="gong" className={s.countGong} /><Art name="kendang" className={s.countKendang} /></>,
          closingEmblem: <Stage className={s.closingStage} />,
          sentArt: <Art name="gong" />,
        }}
      />
    </ThemeShell>
  );
}
