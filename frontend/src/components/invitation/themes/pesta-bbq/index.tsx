"use client";
// Theme "Pesta BBQ" — pesta barbeku di halaman belakang bersama keluarga dan teman: lukisan gouache orisinal panggangan
// dengan sate dan jagung, asap yang mengepul, lampu gantung, meja piknik kayu dengan es jeruk, kotak pendingin, dan
// papan lempar karung. Kartu bergaya stiker, susunan acara sebagai jadwal; bukan undangan pernikahan.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt, type ThemeCopy } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Bowlby One", "Bricolage Grotesque:wght@400;600;700;800", "Caveat Brush"];
// Painted by /tmp/pen/art/themes/pesta-bbq.py (the string lights are also a CSS background).
const Art = makeArt("pesta-bbq", { scene: [760, 490], asap: [73, 349], sate: [150, 105], jagung: [130, 73], divider: [360, 24], es: [120, 196] } as const);

const COPY: ThemeCopy = {
  ...DEFAULT_COPY,
  opening: {
    kicker: "Halo, kawan!",
    title: "Ayo Bakar-bakar!",
    sub: "Pesta barbeku santai di halaman belakang",
    intro: "Arang sudah siap, lampu sudah digantung, es jeruk sudah didinginkan. Kami mengajak kamu dan keluarga untuk kumpul, makan sate dan jagung bakar, main lempar karung, dan ngobrol sampai malam.",
  },
  roles: ["Tuan Rumah", "Bareng"],
  couple: ["Yang ngundang", "Tuan Rumah"],
  count: ["Arang dinyalakan dalam", "Hitung Mundur"],
  units: ["Hari", "Jam", "Menit", "Detik"],
  events: ["Catat tanggalnya", "Waktu & Tempat"],
  story: ["Biar nggak ketinggalan", "Susunan Acara"],
  gallery: ["Kenangan", "Foto-foto"],
  wishes: ["Konfirmasi", "Datang & Titip Pesan"],
  gifts: ["Nggak wajib", "Ikut Patungan"],
  closing: {
    thanks: "Sampai Ketemu!",
    text: "Terima kasih sudah mau datang. Siapkan perut kosong dan baju yang boleh bau asap.",
  },
  sent: "Sip, pesanmu sudah masuk! Sampai ketemu di halaman belakang.",
  attend: { yes: "Datang!", maybe: "Diusahakan", no: "Absen dulu" },
  wishPlaceholder: "Tulis pesan, salam, atau request menu…",
  closedNote: "Pendaftaran sudah ditutup. Pesan dan salam masih boleh dikirim lewat form ini.",
  giftIntro: "Tidak perlu bawa kado. Kalau mau ikut patungan arang dan es batu, boleh lewat sini:",
  familyLabel: null,
};

const WISHES = [
  { id: "w1", name: "Mas Dimas & Mbak Sarah", attendance: "yes" as const, message: "Datang! Kami bawa kursi lipat dan sambal matah. Siap jadi juri sate terbaik." },
  { id: "w2", name: "Pak RT Hendra", attendance: "yes" as const, message: "Mantap, warga Blok C kompak. Saya bawa speaker kecil buat lagu-lagu lawas." },
  { id: "w3", name: "Tante Lusi & anak-anak", attendance: "maybe" as const, message: "Diusahakan mampir habis les renang anak-anak. Sisakan jagung bakar ya!" },
];

export default function PestaBbqTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel?.trim() || "Pesta BBQ";
  const words = label.split(/\s+/);
  const title = words.length > 1 ? [words.slice(0, -1).join(" "), words[words.length - 1]] : [label];
  const groom = data.couple.groom?.trim();
  const hosts = [data.couple.bride, groom].filter(Boolean).join(" & ");
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#232c47"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.coverLights} aria-hidden />
          <div className={s.sign}>
            <p className={s.kicker}>Kamu diundang ke</p>
            <h1 className={s.coverTitle}>{title.map(word => <span key={word}>{word}</span>)}</h1>
            {hosts && <p className={s.hosts}>bareng {hosts}</p>}
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guestBox}>
            <div className={s.guest}>
              <small>Kepada Yth.</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
          </div>
          <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#ffffff" />Buka Undangan</button>
          <div className={s.yard} aria-hidden>
            <Art name="asap" eager className={`${s.smoke} ${s.smoke1}`} />
            <Art name="asap" eager className={`${s.smoke} ${s.smoke2}`} />
            <Art name="scene" eager className={s.yardImg} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        copy={COPY}
        demoWishes={WISHES}
        celebrant
        noPhotos
        light="#ffffff"
        dark="#2b2a2e"
        hero={(
          <header className={s.hero}>
            <div className={s.ticket}>
              <p className={s.heroKicker}>{label}</p>
              <h1 className={s.heroNames}><span>{data.couple.bride}</span>{groom && <><em>bareng</em><span>{groom}</span></>}</h1>
              <p className={s.heroDate}>{formatDate(data.date)}</p>
              {note && <p className={s.heroNote}>{note}</p>}
            </div>
            <ul className={s.menu} aria-label="Menu">
              <li><Art name="sate" /><span>Sate</span></li>
              <li><Art name="jagung" /><span>Jagung bakar</span></li>
              <li><Art name="es" /><span>Es jeruk</span></li>
            </ul>
          </header>
        )}
        slots={{
          divider: <Art name="divider" className={s.divider} />,
          node: <Art name="sate" />,
          amp: <Art name="jagung" />,
          portrait: <Art name="sate" className={s.portraitArt} />,
          closingEmblem: <Art name="es" className={s.closingEmblem} />,
          closingDecor: <Art name="scene" className={s.closingScene} />,
          sentArt: <Art name="es" />,
        }}
      />
    </ThemeShell>
  );
}
