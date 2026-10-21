"use client";
// Theme "Telaga Kabut" — telaga pegunungan berkabut yang dilukis cat air basah: punggung bukit berlapis, pinus, pantulan
// air, dermaga kayu dan perahu kecil. Palet sage & abu kebiruan, tata letak editorial rata kiri dengan garis tipis bernomor.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Italiana", "Cormorant Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500", "Jost:wght@400;500"];
// Painted by /tmp/pen/art/themes/telaga-kabut.py (tools/art/themes in the repo).
const Art = makeArt("telaga-kabut", { telaga: [680, 574], pinus: [260, 268], perahu: [300, 41] } as const);
// Lucide "arrow-right" (ISC license).
const ARROW = "<path d=\"M5 12h14\" /> <path d=\"m12 5 7 7-7 7\" />";

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  attend: { maybe: "Mungkin" },
  opening: {
    kicker: "Salam Hangat",
    title: "Di Tepi Telaga",
    intro: "Dengan sukacita dan rasa syukur, kami mengundang Bapak/Ibu/Saudara/i untuk menjadi saksi hari bahagia kami, di tepi telaga yang tenang di antara kabut dan pinus.",
  },
  roles: ["Mempelai Wanita", "Mempelai Pria"],
  couple: ["Kedua Mempelai", "Kami Berdua"],
  count: ["Hitung Mundur", "Menuju Hari Bahagia"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Agenda", "Waktu & Tempat"],
  story: ["Catatan Perjalanan", "Kisah Kami"],
  gallery: ["Album", "Potret Kabut"],
  wishes: ["Buku Tamu", "Ucapan & Konfirmasi"],
  gifts: ["Tanda Kasih", "Amplop Digital"],
  closing: { thanks: "Terima Kasih", text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i adalah hadiah paling berharga bagi kami.", salam: "Sampai jumpa di tepi telaga" },
  sent: "Terima kasih, ucapan Anda sudah kami terima.",
};

export default function TelagaKabutTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Pernikahan";
  const table = tableLabel(data.guestTable);
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const note = data.couple.note?.trim();
  const year = data.date?.slice(0, 4);

  return (
    <ThemeShell
      fonts={FONTS}
      background="#dfe4e0"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverArt}>
            <Art name="telaga" eager />
            <span className={`${s.mist} ${s.mistA}`} aria-hidden />
            <span className={`${s.mist} ${s.mistB}`} aria-hidden />
            {photo && <div className={s.plate}><Photo src={photo} alt="" /></div>}
          </div>
          <p className={s.masthead}>Undangan {label}{year && /^\d{4}$/.test(year) ? ` · ${year}` : ""}</p>
          <h1 className={s.coverNames}><span>{data.couple.bride}</span><em>dan</em><span>{data.couple.groom}</span></h1>
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}>
              <Lucide icon={ic.mailOpen} size={16} color="#eef0ec" />Buka Undangan<Lucide icon={ARROW} size={16} color="#eef0ec" />
            </button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        light="#eef0ec"
        dark="#2f414a"
        hero={(
          <header className={s.hero}>
            {photo ? <div className={s.heroPhoto}><Photo src={photo} alt="" /></div> : <Art name="telaga" className={s.heroArt} />}
            {data.place && <p className={s.caption}>{data.place}</p>}
            <p className={s.kickerDark}>Undangan {label}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="perahu" className={s.divider} />,
          countDecor: <Art name="pinus" className={s.countPines} />,
          closingDecor: <Art name="telaga" className={s.closingArt} />,
          closingEmblem: <Art name="perahu" className={s.closingBoat} />,
          sentArt: <Art name="perahu" />,
        }}
      />
    </ThemeShell>
  );
}
