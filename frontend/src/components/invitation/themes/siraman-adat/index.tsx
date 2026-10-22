"use client";
// Theme "Siraman Adat" — upacara siraman calon pengantin Jawa dalam hijau pupus & gading: kendi tanah liat yang
// mengucurkan air ke jambangan kembang setaman (dilihat dari atas), anyaman janur, cengkir gading, gayung batok
// (gouache + cat air). Hero menuntun urutan siraman di sepanjang aliran air dengan penanda tetes air.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Della Respira", "Alegreya Sans:ital,wght@0,400;0,500;0,700;1,400", "Ephesis"];
// Painted by /tmp/pen/art/themes/siraman-adat.py
const Art = makeArt("siraman-adat", {
  kendi: [360, 434], setaman: [420, 420], janur: [440, 39], cengkir: [300, 214], gayung: [220, 82], sprig: [320, 368], petal: [42, 36],
} as const);

const RITES = [
  { title: "Sungkeman", body: "Sang calon pengantin bersimpuh memohon maaf dan doa restu kepada Bapak dan Ibu sebelum melangkah ke hidup yang baru." },
  { title: "Siraman pitu pinisepuh", body: "Tujuh sesepuh menyiramkan air kembang setaman. Pitu, pitulungan: semoga pertolongan Gusti selalu menyertai." },
  { title: "Wudhu & pecah kendi", body: "Air terakhir dari kendi dipakai berwudhu, lalu kendi dipecah sebagai tanda ia siap dipinang: wis pecah pamore." },
  { title: "Dodol dawet", body: "Bapak dan Ibu berjualan dawet, dibayar tamu dengan kreweng, lambang rezeki yang kelak mengalir deras." },
] as const;

export default function SiramanAdatTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Siraman";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const full = child?.name.trim() || data.couple.brideFull || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const single = !!child || !data.couple.groom?.trim();
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f6f4ea"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="sprig" eager className={s.coverSprig} />
          <Art name="sprig" eager className={`${s.coverSprig} ${s.coverSprig2}`} />
          <Art name="petal" eager className={`${s.petal} ${s.petal1}`} />
          <Art name="petal" eager className={`${s.petal} ${s.petal2}`} />
          <Art name="petal" eager className={`${s.petal} ${s.petal3}`} />
          <div className={s.coverText}>
            <Art name="janur" eager className={s.coverJanur} />
            <p className={s.coverKicker}>Upacara {label}</p>
            <h1 className={s.coverName}>{names}</h1>
            <p className={s.coverRole}>{single ? "Calon Pengantin Putri" : "Calon Pengantin"}</p>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#fdfcf6" />Buka Undangan</button>
          </div>
          <div className={s.pool} aria-hidden>
            <Art name="setaman" eager className={s.poolSetaman} />
            <Art name="cengkir" eager className={s.poolCengkir} />
            <Art name="kendi" eager className={s.poolKendi} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#fdfcf6"
        dark="#2f4237"
        demoWishes={[
          { id: "w1", name: "Eyang Putri Atmojo", attendance: "yes", message: "Sugeng siraman, nduk. Mugi resik lahir lan batinipun, lancar ngantos ijab, lan tansah pinaringan berkah." },
          { id: "w2", name: "Mbak Ratih & Mas Yoga", attendance: "yes", message: "Laras, semoga segala gugup luruh bersama air kembang setaman. Besok tinggal melangkah dengan hati yang lapang." },
          { id: "w3", name: "Teman-teman Psikologi 2017", attendance: "maybe", message: "Maaf belum bisa ikut dodol dawet. Doa kami menyertaimu, sampai jumpa di resepsi!" },
        ]}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            kicker: "Sugeng Rawuh",
            title: "Nyuwun Pangestu",
            sub: `Upacara ${label}`,
            intro: `Dengan memohon rahmat Tuhan Yang Maha Esa, kami mengundang Bapak/Ibu/Saudara/i untuk menyaksikan upacara ${label.toLowerCase()} putri kami, ${names}. Siraman adalah doa yang dituangkan lewat air kembang setaman, agar ia suci lahir dan batin menjelang ijab.`,
          },
          roles: [single ? "Calon Pengantin Putri" : "Calon Pengantin", "Calon Pengantin"],
          couple: ["Ingkang Dipun Siram", single ? "Calon Pengantin" : "Calon Pengantin"],
          count: ["Ngetung Dina", `Menuju ${label}`],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Wekdal & Papan", "Rangkaian Acara"],
          story: ["Lelampahan", "Perjalanan"],
          gallery: ["Galeri", "Kenangan"],
          wishes: ["Pangestu", "Doa & Kehadiran"],
          gifts: ["Tanda Katresnan", "Amplop & Kado"],
          closing: {
            thanks: "Matur Nuwun",
            text: `Rawuh dan pangestu Bapak/Ibu/Saudara/i menjadi air yang menyejukkan langkah ${names} menuju hari bahagia.`,
            salam: "Rahayu ingkang sami pinanggih",
          },
          attend: { maybe: "Mungkin" },
          sent: "Matur nuwun, doa dan ucapan Anda sudah terkirim.",
          wishPlaceholder: `Tuliskan doa untuk ${names} menjelang ijab…`,
          giftIntro: "Pangestu Bapak/Ibu/Saudara/i sudah lebih dari cukup. Bila berkenan memberi tanda kasih, dapat melalui:",
          familyLabel: "Kami yang berbahagia, Keluarga",
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroTop}>
              <Art name="kendi" className={s.heroKendi} />
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroName}>{names}</h1>
              {child && full !== nick && <p className={s.heroFull}>{full}</p>}
              <p className={s.heroDate}>{formatDate(data.date)}</p>
            </div>
            {note && <p className={s.heroNote}>{note}</p>}
            <h2 className={s.ritesTitle}>Urutan Siraman</h2>
            <p className={s.ritesSub}>mengalir seperti air, satu demi satu</p>
            <ol className={s.rites}>
              {RITES.map((rite, i) => (
                <li key={rite.title}>
                  <span className={s.drop} aria-hidden><b>{i + 1}</b></span>
                  <div><h3>{rite.title}</h3><p>{rite.body}</p></div>
                </li>
              ))}
            </ol>
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="janur" /></span>,
          node: <Art name="petal" />,
          portrait: <Art name="setaman" className={s.portraitSetaman} />,
          countDecor: <Art name="cengkir" className={s.countCengkir} />,
          closingDecor: <div className={s.closingPool} aria-hidden><Art name="setaman" /></div>,
          closingEmblem: <Art name="gayung" className={s.closingGayung} />,
          sentArt: <Art name="gayung" />,
        }}
      />
    </ThemeShell>
  );
}
