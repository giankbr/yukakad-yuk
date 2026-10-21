"use client";
// Theme "Reuni Sekolah" — buku tulis retro untuk reuni akbar: kertas bergaris dengan margin merah, coretan pulpen biru
// (gedung sekolah, pesawat kertas), papan kapur berbingkai kayu dengan lonceng kapur, polaroid berselotip, lencana angkatan.
import { Lucide, Photo, ThemeShell, formatDate, guestLabel, type ThemeProps } from "../kit";
import { tableLabel } from "../extras";
import { DEFAULT_COPY, ThemeBody, ic, makeArt } from "../_base/body";
import type { InvitationData } from "../../types";
import s from "./styles.module.css";

const FONTS = ["Caveat:wght@500;700", "Patrick Hand", "Cabin Sketch:wght@400;700", "Special Elite"];
// Painted by /tmp/pen/art/themes/reuni-sekolah.py (tools/art/themes in the repo).
const Art = makeArt("reuni-sekolah", {
  school: [420, 187], plane: [240, 114], doodles: [110, 523], chalk: [180, 137], badge: [200, 268], tape: [140, 33], pencil: [180, 17], node: [60, 56],
} as const);

/** "Angkatan 2007" (or a lone 4-digit year) from the note/label, for the badge. */
function angkatan(data: InvitationData) {
  const text = [data.eventLabel, data.couple.note, data.place].filter(Boolean).join(" ");
  return /angkatan\s+(\d{4})/i.exec(text)?.[1] ?? /\b(19[5-9]\d|20[0-4]\d)\b/.exec(data.couple.note ?? "")?.[1];
}

function Badge({ year, className, eager }: { year?: string; className: string; eager?: boolean }) {
  return (
    <div className={className} aria-hidden>
      <Art name="badge" eager={eager} />
      <b>{year ? "Angkatan" : "Reuni"}<span>{year ?? "Akbar"}</span></b>
    </div>
  );
}

function Board({ label, school, eager }: { label: string; school?: string; eager?: boolean }) {
  return (
    <div className={s.board}>
      <Art name="chalk" eager={eager} className={s.boardChalk} />
      <p className={s.boardKicker}>Undangan</p>
      <h1 className={s.boardTitle}>{label}</h1>
      {school && <p className={s.boardSchool}>{school}</p>}
    </div>
  );
}

export default function ReuniSekolahTheme(props: ThemeProps) {
  const { data, skipCover } = props;
  const label = data.eventLabel ?? "Reuni Akbar";
  const year = angkatan(data);
  const table = tableLabel(data.guestTable);
  const note = data.couple.note?.trim();
  const photo = data.gallery[0] ?? data.couple.bridePhoto;
  const school = data.place?.trim();
  const committee = [data.couple.brideFull ?? data.couple.bride, data.couple.groom?.trim() ? data.couple.groomFull ?? data.couple.groom : ""].filter(Boolean);
  const copy = {
    ...DEFAULT_COPY,
    opening: {
      kicker: "Halo, Kawan Lama!",
      title: "Ayo Kembali ke Kelas",
      intro: `Bel sudah berbunyi lagi. Kami mengundang seluruh alumni${year ? ` angkatan ${year}` : ""} beserta bapak/ibu guru untuk berkumpul, bernostalgia, dan menyambung lagi cerita yang sempat tertunda.`,
    },
    roles: ["Ketua Panitia", "Sekretaris"] as [string, string],
    couple: ["Panitia", "Yang Mengundang"] as [string, string],
    count: ["Hitung Mundur", "Sebelum Bel Masuk"] as [string, string],
    units: ["Hari", "Jam", "Menit", "Detik"] as [string, string, string, string],
    events: ["Jadwal Pelajaran", "Acara Reuni"] as [string, string],
    story: ["Buku Kenangan", "Dulu & Sekarang"] as [string, string],
    gallery: ["Album Kelas", "Foto-foto Kita"] as [string, string],
    wishes: ["Daftar Hadir", "Absen Dulu, Yuk!"] as [string, string],
    gifts: ["Iuran Sukarela", "Patungan & Donasi"] as [string, string],
    closing: { thanks: "Sampai Jumpa!", text: "Terima kasih sudah membaca undangan ini sampai halaman terakhir. Kursi kalian masih kami simpan, jangan bolos, ya." },
    sent: "Terima kasih, absen dan pesanmu sudah tercatat!",
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#e9e4d4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Board label={label} school={school} eager />
          <div className={s.pinRow}>
            <Art name="plane" eager className={s.plane} />
            {photo && (
              <div className={s.polaroid}>
                <Art name="tape" eager className={s.tapeTop} />
                <Photo src={photo} alt="" />
              </div>
            )}
            <Badge year={year} eager className={s.badge} />
          </div>
          <Art name="doodles" eager className={s.marginDoodles} />
          <p className={s.coverDate}>{formatDate(data.date)}</p>
          <div className={s.guestWrap}>
            <div className={s.label}>
              <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
              <strong>{guestLabel(data)}</strong>
              {table && <span className={s.table}>{table}</span>}
            </div>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={17} color="#2a2f45" />Buka Undangan</button>
          </div>
          <Art name="pencil" eager className={s.pencil} />
          <Art name="school" eager className={s.coverSchool} />
        </section>
      )}
    >
      <ThemeBody
        {...props}
        s={s}
        celebrant
        light="#f4f1e6"
        dark="#23377e"
        copy={copy}
        hero={(
          <header className={s.hero}>
            <Board label={label} school={school} />
            {note && <p className={s.heroNote}>{note}</p>}
            <Art name="school" className={s.heroSchool} />
            <p className={s.heroDate}>{formatDate(data.date)}</p>
          </header>
        )}
        slots={{
          divider: <Art name="pencil" className={s.divider} />,
          node: <Art name="node" />,
          portrait: <Art name="tape" className={s.tapeTop} />,
          countDecor: <Art name="chalk" className={s.chalkBell} />,
          closingEmblem: (
            <>
              <Badge year={year} className={s.closingBadge} />
              {committee.length > 0 && <p className={s.closingSign}>Salam hangat, panitia: {committee.join(" & ")}</p>}
            </>
          ),
          sentArt: <Art name="plane" />,
        }}
      />
    </ThemeShell>
  );
}
