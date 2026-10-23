"use client";
// Theme "Wisteria Syari" — undangan syar'i tanpa foto. Untaian wisteria cat air lilak-ungu menjuntai dari balok
// pergola di kanan atas sampul; teks rata kiri bersandar di bawah ujung-ujung untaian. Monogram dalam karangan
// wisteria menggantikan foto, pita hitung mundur ungu terong dengan untaian yang berayun pelan.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Cormorant Upright:wght@400;500;600", "Lora:ital,wght@0,400;0,500;0,600;1,400", "Monsieur La Doulaise", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/wisteria-syari.py
const Art = makeArt("wisteria-syari", { cascade: [520, 761], raceme: [180, 515], spray: [320, 121], wreath: [360, 413], petals: [480, 56] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const WISHES = [
  { id: "w1", name: "Ibu Hj. Rofi'ah & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Ustazah Laila", attendance: "yes" as const, message: "MasyaAllah, ikut berbahagia, Wardah. Semoga Allah jadikan rumah tangga kalian ladang pahala yang terus bertumbuh." },
  { id: "w3", name: "Rekan TPQ Raden Patah", attendance: "maybe" as const, message: "Insyaallah kami hadir bila tidak ada halangan. Doa terbaik untuk Hafiz dan Wardah." },
];

function initial(name?: string) {
  return name?.trim().slice(0, 1).toUpperCase() ?? "";
}

export default function WisteriaSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const label = data.eventLabel ?? "Walimatul 'Ursy";
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const mono = [initial(bride), initial(groom)].filter(Boolean).join(" ");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f7f1e6"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="cascade" eager className={s.coverCascade} />
          <div className={s.coverText}>
            <p className={s.bism} lang="ar" dir="rtl">{BISMILLAH}</p>
            <p className={s.salamCover}>Assalamu&apos;alaikum Wr. Wb.</p>
            <p className={s.coverKicker}>{label}</p>
            <h1 className={s.coverNames}><span>{bride}</span>{groom && <><i>&amp;</i><span>{groom}</span></>}</h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
          </div>
          <div className={s.guestPanel}>
            <div className={s.guest}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#efe6f7" />Buka Undangan</button>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#efe6f7"
        dark="#3a2759"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Rahmat Allah",
            intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan mendoakan.",
          },
          roles: ["Mempelai Wanita", "Mempelai Pria"],
          couple: ["Dipertemukan dalam rida-Nya", "Kedua Mempelai"],
          count: ["Menanti hari yang diberkahi", "Menghitung Hari"],
          units: ["Hari", "Jam", "Menit", "Detik"],
          events: ["Waktu & tempat", "Rangkaian Acara"],
          story: ["Perjalanan kami", "Kisah Ta'aruf"],
          gallery: ["Galeri", "Momen Bersama"],
          wishes: ["Doa restu", "Ucapan & Kehadiran"],
          gifts: ["Tanda kasih", "Amplop Digital"],
          closing: {
            thanks: "Jazakumullahu Khairan",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullahu khairan, doa dan ucapan Anda sudah terkirim.",
        }}
        hero={(
          <header className={s.hero}>
            <Art name="raceme" className={`${s.heroHang} ${s.heroHangL}`} />
            <Art name="raceme" className={`${s.heroHang} ${s.heroHangR}`} />
            <p className={s.heroKicker}>{label}</p>
            <div className={s.medal} aria-hidden>
              <Art name="wreath" />
              <span className={s.medalMono}>{mono}</span>
            </div>
            <h1 className={s.heroNames}>{bride}{groom && <><i>&amp;</i>{groom}</>}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="spray" /></span>,
          node: <Art name="raceme" />,
          amp: <Art name="spray" />,
          portrait: <Art name="wreath" className={s.wreath} />,
          countDecor: <><Art name="raceme" className={s.countHang} /><Art name="raceme" className={s.countHang} /><Art name="raceme" className={s.countHang} /><Art name="raceme" className={s.countHang} /></>,
          closingDecor: <><Art name="raceme" className={s.closingHang} /><Art name="raceme" className={s.closingHang} /><Art name="petals" className={s.closingPetals} /></>,
          closingEmblem: <Art name="spray" className={s.closingEmblem} />,
          sentArt: <Art name="spray" />,
        }}
      />
    </ThemeShell>
  );
}
