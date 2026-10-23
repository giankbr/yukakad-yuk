"use client";
// Theme "Kabin Danau" — lukisan gouache pagi: kabin kayu berjendela hangat, dermaga dan kano merah, pinus berlapis, dan
// kabut yang melayang di atas danau. Sampul: lukisan penuh di atas, panel hijau pinus melengkung dengan lentera berayun.
// Foto pembuka dilihat "dari jendela kabin", potret di cincin flanel kotak merah-hitam.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Fraunces:ital,wght@0,400;0,500;0,600;1,400;1,500", "Alegreya Sans:ital,wght@0,400;0,500;0,700;1,400", "Caveat:wght@400;600"];
// Painted by /tmp/pen/art/themes/kabin-danau.py (scene and mist are CSS backgrounds)
const Art = makeArt("kabin-danau", { lantern: [160, 263], canoe: [300, 78], pine: [67, 199] } as const);

const WISHES = [
  { id: "w1", name: "Tim Pendaki Jalur Barat", attendance: "yes" as const, message: "Dari pos dua sampai ujung dermaga! Kami datang lengkap, termos teh sudah disiapkan. Selamat menempuh perjalanan baru." },
  { id: "w2", name: "Tante Ratih & Om Gunawan", attendance: "yes" as const, message: "Selamat ya, Kirana dan Bastian. Semoga rumah kalian selalu hangat seperti kabin di pagi hari." },
  { id: "w3", name: "Nadia (Jakarta)", attendance: "maybe" as const, message: "Masih menunggu kepastian cuti, tapi doa dan peluk dari jauh sudah dikirim duluan. Bahagia selalu!" },
];

export default function KabinDanauTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const hero = data.gallery[0] || data.couple.bridePhoto;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#14251f"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <div className={s.coverScene} aria-hidden>
            <span className={s.mist} />
            <span className={s.mist} />
            <Art name="lantern" eager className={s.lantern} />
          </div>
          <div className={s.panel}>
            <p className={s.kicker}>kami akan menikah</p>
            <h1 className={s.coverNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#1d2a24" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        light="#ffd98a"
        dark="#1d332c"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Salam hangat dari tepi danau",
            title: "Mari Pulang ke Kabin",
            intro: "Dengan penuh syukur dan sukacita, kami mengundang Bapak/Ibu/Saudara/i untuk hadir dan merayakan hari pernikahan kami. Kehadiran dan doa Anda akan membuat pagi itu semakin hangat.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["yang akan menikah", "Kedua Mempelai"],
          count: ["sebentar lagi", "Menuju Pagi Itu"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["catat tanggalnya", "Waktu & Tempat"],
          story: ["dari jalur pendakian", "Cerita Kami"],
          gallery: ["kenangan", "Galeri"],
          wishes: ["kabari kami", "Ucapan & Kehadiran"],
          gifts: ["tanda kasih", "Hadiah Pernikahan"],
          closing: {
            thanks: "Sampai Jumpa di Dermaga",
            text: "Terima kasih atas doa, kehadiran, dan kehangatan yang Anda bawa. Kami tidak sabar merayakan pagi itu bersama Anda.",
          },
          sent: "Terima kasih, ucapan Anda sudah sampai di kabin kami.",
          attend: { yes: "Hadir", maybe: "Mungkin", no: "Berhalangan" },
          wishPlaceholder: "Tuliskan ucapan dan doa untuk kami berdua…",
          familyLabel: "Bersama keluarga",
        }}
        hero={(
          <header className={s.hero}>
            {hero && (
              <>
                <div className={s.window}><div className={s.heroPhoto}><Photo src={hero} alt={`${data.couple.bride} dan ${data.couple.groom}`} /></div></div>
                <span className={s.sill} aria-hidden />
              </>
            )}
            <p className={s.heroKicker}>{data.eventLabel?.trim() || "Pernikahan"}</p>
            <h1 className={s.heroNames}>{data.couple.bride}<em>&amp;</em>{data.couple.groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="canoe" /></span>,
          node: <Art name="pine" />,
          amp: <Art name="pine" />,
          portrait: <Art name="pine" className={s.portraitPine} />,
          countDecor: <span className={s.mist} aria-hidden />,
          closingDecor: <span className={s.mist} aria-hidden />,
          closingEmblem: <Art name="lantern" className={s.closingLantern} />,
          sentArt: <Art name="canoe" />,
        }}
      />
    </ThemeShell>
  );
}
