"use client";
// Theme "Ultah Panda" — ulang tahun anak di hutan bambu: panda lucu orisinal bergaya gouache buku cerita, papan nama
// bambu yang digantung di antara rumpun bambu dengan panda mengintip di atasnya, kue bertingkat berbalut bambu dengan
// lilin, hitung mundur berwajah panda dan kartu bertelinga panda. Gerak riang: papan berayun, panda mengintip dan memantul.
import { Lucide, ThemeShell, formatDate, guestLabel, toDate, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Lilita One", "Nunito:wght@500;600;700;800"];
// Painted by /tmp/pen/art/themes/ultah-panda.py.
const Art = makeArt("ultah-panda", { panda: [360, 552], peek: [220, 166], face: [120, 112], cake: [300, 343], sprig: [300, 52] } as const);

const WISHES = [
  { id: "w1", name: "Kenzo & Mama", attendance: "yes" as const, message: "Selamat ulang tahun, Alya! Kenzo sudah siap pakai bando panda. Semoga sehat, ceria, dan makin pintar ya." },
  { id: "w2", name: "Keluarga Om Bima", attendance: "yes" as const, message: "Selamat empat tahun, panda kecil kesayangan. Semoga harimu semanis kue dan seceria hutan bambu." },
  { id: "w3", name: "Tante Laras", attendance: "maybe" as const, message: "Maaf belum tentu bisa datang, Sayang. Kadonya sudah Tante siapkan, peluk jauh dari Bandung!" },
];

function ageAt(birth?: string, at?: string) {
  const b = toDate(birth);
  const d = toDate(at);
  if (!b || !d) return undefined;
  let age = d.getFullYear() - b.getFullYear();
  if (d.getMonth() < b.getMonth() || (d.getMonth() === b.getMonth() && d.getDate() < b.getDate())) age -= 1;
  return age > 0 && age < 30 ? age : undefined;
}

export default function UltahPandaTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Ulang Tahun";
  const child = data.extras?.child?.enabled !== false && data.extras?.child?.name?.trim() ? data.extras.child : undefined;
  const nick = child?.nickname?.trim() || child?.name.trim() || data.couple.bride;
  const names = child ? nick : [data.couple.bride, data.couple.groom?.trim()].filter(Boolean).join(" & ");
  const age = ageAt(child?.birthDate, data.date);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e6f4d9"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <span className={s.ropes} aria-hidden />
          <div className={s.signWrap}>
            <Art name="peek" eager className={s.peek} />
            <div className={s.sign}>
              <p className={s.kicker}>Undangan {label}</p>
              <h1 className={s.coverNames}>{names}</h1>
              {age && <p className={s.age}><b>{age}</b>tahun</p>}
              <p className={s.coverDate}>{formatDate(data.date)}</p>
            </div>
          </div>
          <div className={s.coverFoot}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={18} color="#ffffff" />Buka Undangan</button>
          </div>
          <div className={s.coverBank} aria-hidden>
            <Art name="panda" eager className={s.coverPanda} />
            <Art name="cake" eager className={s.coverCake} />
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        noPhotos={!child?.photo && !data.couple.bridePhoto}
        light="#ffffff"
        dark="#25262a"
        demoWishes={WISHES}
        copy={{
          opening: {
            kicker: "Halo, teman-teman panda!",
            title: "Ayo ke Hutan Bambu",
            intro: `Dengan penuh sukacita, kami mengundang teman-teman dan keluarga untuk merayakan ${label.toLowerCase()} ${names}${age ? ` yang ke-${age}` : ""}. Kita main bersama, makan kue, lalu tiup lilin ramai-ramai!`,
          },
          roles: ["Yang Berulang Tahun", "Bersama"],
          couple: ["Kenalan yuk", child ? "Si Panda Kecil" : "Yang Merayakan"],
          count: ["Sebentar lagi", "Menuju Hari Pesta"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Catat tanggalnya", "Waktu & Tempat"],
          story: ["Ruas demi ruas", `Cerita ${nick}`],
          gallery: ["Album", "Foto Ceria"],
          wishes: ["Kirim doa terbaik", "Ucapan & Kehadiran"],
          gifts: ["Tanda sayang", "Kado & Amplop Digital"],
          closing: { thanks: "Terima Kasih!", text: `Kehadiran dan doa teman-teman membuat hari ${names} makin ceria. Sampai jumpa di hutan bambu!` },
          sent: "Hore! Ucapanmu sudah terkirim. Terima kasih!",
          attend: { maybe: "Mungkin" },
          wishPlaceholder: "Tulis ucapan dan doa untuk si kecil…",
          closedNote: "Terima kasih sudah ikut merayakan! Ucapan masih bisa dikirim lewat form ini.",
          giftIntro: "Kehadiran teman-teman sudah jadi hadiah paling indah. Bila ingin memberi tanda sayang, dapat melalui:",
          familyLabel: "Dengan sayang,",
        }}
        hero={(
          <header className={s.hero}>
            <div className={s.heroRing}>
              <Art name="peek" className={s.heroPeek} />
              <div className={s.heroInner}>
                <p className={s.heroKicker}>Pesta {label}</p>
                <h1 className={s.heroNames}>{names}</h1>
                {age && <span className={s.heroAge} aria-hidden>{age}</span>}
              </div>
            </div>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <Art name="sprig" className={s.divider} />,
          node: <Art name="face" />,
          amp: <Art name="face" />,
          portrait: <Art name="peek" />,
          closingDecor: <span className={s.closingBank} aria-hidden><Art name="panda" /><Art name="cake" /></span>,
          closingEmblem: <Art name="face" className={s.closingEmblem} />,
          sentArt: <Art name="face" />,
        }}
      />
    </ThemeShell>
  );
}
