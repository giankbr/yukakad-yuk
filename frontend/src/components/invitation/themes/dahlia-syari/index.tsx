"use client";
// Theme "Dahlia Syari" — undangan syar'i tanpa foto. Dahlia cat air terakota, merah muda pudar dan krem dengan daun
// zaitun dan rumput kering: buket tumpah dari sudut kanan atas sampul, panel lengkung terakota naik dari kiri bawah
// berisi nama. Monogram dalam karangan dahlia menggantikan foto, kartu acara berpuncak lengkung, dahlia berputar pelan.
import { Lucide, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import s from "./styles.module.css";

const FONTS = ["Italiana", "EB Garamond:ital,wght@0,400;0,600;1,400", "Pinyon Script", "Amiri:wght@400"];
// Painted by /tmp/pen/art/themes/dahlia-syari.py
const Art = makeArt("dahlia-syari", { bouquet: [560, 571], spray: [400, 311], bloom: [220, 225], wreath: [300, 300], divider: [300, 39] } as const);
const BISMILLAH = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ";

const WISHES = [
  { id: "w1", name: "Ibu Hj. Nurhasanah & Keluarga", attendance: "yes" as const, message: "Barakallahu lakuma wa baraka 'alaikuma wa jama'a bainakuma fi khair. Semoga menjadi keluarga sakinah, mawaddah, wa rahmah." },
  { id: "w2", name: "Teh Fitri", attendance: "yes" as const, message: "MasyaAllah, ikut bahagia, Bila! Semoga Allah mudahkan setiap langkah kalian berdua." },
  { id: "w3", name: "Rekan kajian Salman", attendance: "maybe" as const, message: "Insyaallah hadir bila tidak ada halangan. Doa terbaik untuk Umar dan Salsabila." },
];

function initial(name?: string) {
  return name?.trim().slice(0, 1).toUpperCase() ?? "";
}

export default function DahliaSyariTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const { bride, groom } = data.couple;
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const mono = [initial(bride), initial(groom)].filter(Boolean).join("&");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f8f0e5"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Art name="bouquet" eager className={s.coverBouquet} />
          <p className={s.bism} lang="ar" dir="rtl">{BISMILLAH}</p>
          <p className={s.bismSub}>Assalamu&apos;alaikum Wr. Wb.</p>
          <div className={s.arch}>
            <Art name="spray" eager className={s.coverSpray} />
            <p className={s.kicker}>{data.eventLabel ?? "Walimatul 'Ursy"}</p>
            <h1 className={s.coverNames}><span>{bride}</span><i>&amp;</i><span>{groom}</span></h1>
            <p className={s.coverDate}>{formatDate(data.date)}</p>
            <div className={s.guestBox}>
              <div className={s.guest}>
                <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                <strong>{guestLabel(data)}</strong>
                {table && <span className={s.table}>{table}</span>}
              </div>
              <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={16} color="#7f3520" />Buka Undangan</button>
            </div>
          </div>
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        noPhotos
        light="#fbefe2"
        dark="#7f3520"
        demoWishes={WISHES}
        copy={{
          ...DEFAULT_COPY,
          opening: {
            arabic: BISMILLAH,
            kicker: "Assalamu'alaikum Warahmatullahi Wabarakatuh",
            title: "Dengan Rahmat Allah",
            intro: "Dengan memohon rahmat dan rida Allah Subhanahu wa Ta'ala, kami bermaksud menyelenggarakan walimah pernikahan putra-putri kami. Merupakan kehormatan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.",
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
            thanks: "Jazakumullah Khairan",
            text: "Kehadiran dan doa restu Bapak/Ibu/Saudara/i merupakan kehormatan dan kebahagiaan bagi kami sekeluarga.",
            salam: "Wassalamu'alaikum Warahmatullahi Wabarakatuh",
          },
          sent: "Jazakumullah khairan, doa dan ucapan Anda sudah terkirim.",
        }}
        hero={(
          <header className={s.hero}>
            <p className={s.heroKicker}>Walimatul &apos;Ursy</p>
            <div className={s.medal} aria-hidden>
              <Art name="wreath" />
              <Art name="wreath" />
              <span className={s.medalMono}><span>{mono}</span></span>
            </div>
            <h1 className={s.heroNames}>{bride}<i>&amp;</i>{groom}</h1>
            <p className={s.heroDate}>{formatDate(data.date)}</p>
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="spray" className={`${s.heroSpray} ${s.heroSprayL}`} />
            <Art name="spray" className={`${s.heroSpray} ${s.heroSprayR}`} />
          </header>
        )}
        slots={{
          divider: <span className={s.divider} aria-hidden><Art name="divider" /></span>,
          node: <Art name="bloom" />,
          amp: <Art name="divider" />,
          portrait: <Art name="wreath" className={s.wreath} />,
          countDecor: <><Art name="spray" className={`${s.countSpray} ${s.countSprayL}`} /><Art name="spray" className={`${s.countSpray} ${s.countSprayR}`} /></>,
          closingEmblem: <Art name="bloom" className={s.closingBloom} />,
          sentArt: <Art name="bloom" />,
        }}
      />
    </ThemeShell>
  );
}
