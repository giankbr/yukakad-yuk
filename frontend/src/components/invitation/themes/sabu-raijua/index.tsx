"use client";
// Theme "Sabu Raijua" — adat NTT dari Rai Hawu (Sabu): sampul seperti sarung tenun ikat Sabu (pita bunga putih dan
// merah mengkudu di atas nila gelap) dengan jendela bundar ke laut Sawu, pulau karang, rumah adat dan pohon lontar
// yang dilukis tangan. Foto pembuka dalam bingkai belah ketupat diapit dua lontar; potret bundar berbingkai tenun.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Gloock", "Literata:ital,wght@0,400;0,500;0,600;1,400"];
// Painted by /tmp/pen/art/themes/sabu-raijua.py (the ikat field is a CSS background tile)
const Art = makeArt("sabu-raijua", { scene: [600, 600], lontar: [220, 635], flower: [120, 123] } as const);

const Band = () => <span className={s.band} aria-hidden />;

export default function SabuRaijuaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const heroSrc = data.gallery[0] || data.couple.bridePhoto || data.couple.groomPhoto;
  const note = data.couple.note?.trim();
  const label = data.eventLabel ?? "Pernikahan";

  return (
    <ThemeShell
      fonts={FONTS}
      background="#1e1b2a"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Band />
          <div className={s.window}><Art name="scene" eager /></div>
          <Art name="flower" eager className={s.windowFlower} />
          <div className={s.coverText}>
            <p className={s.kicker}>Undangan {label}</p>
            <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fff8ec" />Buka Undangan</button>
          </div>
          <Band />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ebc98a"
        dark="#1e1b2a"
        demoWishes={[
          { id: "w1", name: "Bapa Mama Djara Wadu", attendance: "yes", message: "Selamat menempuh hidup baru, Ance dan Yermi. Tuhan Yesus memberkati rumah tangga kalian, rukun dan setia seperti lontar yang tetap berdiri di musim kering." },
          { id: "w2", name: "Teman-teman PMK Undana", attendance: "yes", message: "Dari persekutuan Jumat malam sampai pelaminan. Kami datang dari Kupang, siap ikut menari Pado'a sampai pagi." },
          { id: "w3", name: "Ibu Yohana Rohi", attendance: "maybe", message: "Doa mama dari Rote menyertai kalian berdua. Semoga keluarga kalian menjadi berkat bagi banyak orang." },
        ]}
        copy={{
          opening: {
            kicker: "Shalom",
            title: "Dalam Kasih-Nya",
            sub: "Dari Rai Hawu, pulau Sabu",
            intro: "Atas kasih karunia Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan turut mendoakan pemberkatan nikah putra-putri kami. Kehadiran Anda adalah sukacita bagi kedua keluarga besar.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Benang Lungsin & Pakan", "Kedua Mempelai"],
          count: ["Menanti Harinya", "Hitung Mundur"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & Tempat", "Rangkaian Acara"],
          story: ["Perjalanan Kami", "Kisah Kami"],
          gallery: ["Galeri", "Potongan Kenangan"],
          wishes: ["Doa & Ucapan", "Ucapan & Kehadiran"],
          gifts: ["Tanda Kasih", "Amplop Digital"],
          closing: {
            thanks: "Terima Kasih",
            text: "Kehadiran dan doa Bapak/Ibu/Saudara/i merupakan kehormatan dan sukacita bagi kami sekeluarga. Tuhan memberkati.",
            salam: "Salam damai dalam kasih Kristus",
          },
          sent: "Terima kasih, doa dan ucapan Anda sudah terkirim.",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tuliskan doa dan ucapan untuk kedua mempelai…",
          giftIntro: "Doa dan kehadiran Anda adalah hadiah terindah bagi kami. Jika ingin memberi tanda kasih, dapat melalui:",
          familyLabel: "Keluarga Besar",
        }}
        hero={(
          <header className={s.hero}>
            <Band />
            <p className={s.heroKicker}>Kami akan menikah</p>
            <div className={s.heroStage}>
              <Art name="lontar" className={s.lontarL} />
              <div className={s.lozenge}>
                <div className={s.heroPhoto}>{heroSrc ? <Photo src={heroSrc} alt={`${bride} & ${groom}`} /> : <div />}</div>
              </div>
              <Art name="lontar" className={s.lontarR} />
            </div>
            <h1 className={s.heroNames}>{bride} <i>&amp;</i> {groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="flower" /></span>,
          node: <Art name="flower" />,
          amp: <Art name="flower" />,
          portrait: <Art name="flower" className={s.portraitArt} />,
          countDecor: <Band />,
          closingDecor: <Band />,
          closingEmblem: <div className={s.closingEmblem} aria-hidden><Art name="scene" /></div>,
          sentArt: <Art name="flower" />,
        }}
      />
    </ThemeShell>
  );
}
