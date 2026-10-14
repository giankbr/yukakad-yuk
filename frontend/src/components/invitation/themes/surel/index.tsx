"use client";
// Theme "Surel" — undangan bergaya kotak masuk email (design: Undangan — Tema Surel (Sinta & Haris)).
import { useState } from "react";
import {
  Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, dateParts, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, timeAgo, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Roboto:wght@400;500;600;700"];
const tint: ThemeTint = {
  "--t-accent": "#1a73e8", "--t-bg": "#ffffff", "--t-ink": "#202124", "--t-muted": "#5f6368", "--t-line": "#e0e0e0",
  "--t-field": "#f1f3f4", "--t-radius": "12px", "--t-font": "Roboto, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Bu Dewi (HRD)", message: "Wah akhirnya resmi! Satu kantor hadir semua ya. Selamat!", created_at: new Date(Date.now() - 3 * 3600e3).toISOString() },
  { id: "w2", name: "Pak Anto", message: "Approved tanpa revisi. Samawa Sinta & Haris!", created_at: new Date(Date.now() - 6 * 3600e3).toISOString() },
];
const DEMO_FILES = ["prewed_01.jpg", "prewed_02.jpg", "akad_sneak.jpg"];
const DEMO_WISHLIST = [["Stand mixer", "Rp2.150.000"], ["Rak buku kayu", "Rp980.000"], ["Smart TV 43\"", "Rp3.400.000"]];
// Decorative inbox rows around the invitation email (flavour only, not invitation data).
const INBOX_BEFORE = [{ from: "Kantor", time: "08.12", subject: "Re: Laporan bulanan", snippet: "Baik, akan saya kirim hari ini…" }];
const INBOX_AFTER = [
  { from: "Promo Belanja", time: "09.41", subject: "Diskon 9.9 menanti!", snippet: "Jangan lewatkan penawaran…" },
  { from: "Newsletter", time: "Kemarin", subject: "5 resep minggu ini", snippet: "Tumis kangkung ala restoran…" },
];

function Status() {
  return (
    <div className={s.status} aria-hidden>
      10:10
      <span><Lucide icon={ic.signal} color="#202124" /><Lucide icon={ic.wifi} color="#202124" /><Lucide icon={ic.batteryFull} color="#202124" /></span>
    </div>
  );
}

function initial(name: string) {
  return name.trim().slice(0, 1).toUpperCase() || "?";
}

/** Account-avatar letter for the guest, skipping honorifics ("Bapak Taufik" → "T"). */
function guestInitial(name: string) {
  const words = name.replace(/[^\p{L}\s]/gu, " ").split(/\s+/).filter(Boolean);
  const skip = /^(bapak|bpk|ibu|bu|pak|sdr|sdri|saudara|saudari|tn|ny|nn|dr|drs|ir|prof|h|hj|kel|keluarga|mr|mrs|ms)$/i;
  return initial(words.find(word => !skip.test(word)) ?? name);
}

function slugPart(name: string) {
  return name.normalize("NFD").replace(/[^a-zA-Z]/g, "").toLowerCase();
}

function InboxRow({ from, time, subject, snippet }: { from: string; time: string; subject: string; snippet: string }) {
  return (
    <div className={s.row} aria-hidden>
      <span className={s.avatar}>{initial(from)}</span>
      <div className={s.rowText}>
        <div className={s.rowHead}><span>{from}</span><small>{time}</small></div>
        <span className={s.rowSubject}>{subject}</span>
        <span className={s.rowSnippet}>{snippet}</span>
      </div>
      <Lucide icon={ic.star} color="#e0e0e0" />
    </div>
  );
}

export default function SurelTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const label = data.eventLabel ?? "Pernikahan";
  const subject = `Undangan ${label} — ${couple}`;
  const sender = `${slugPart(data.couple.bride)}.${slugPart(data.couple.groom)}@menikah.id`;
  const date = new Date(data.date);
  const stamp = Number.isNaN(date.getTime()) ? "" : formatDate(data.date, { day: "2-digit", month: "2-digit" }).replace("/", ".");
  const guest = guestLabel(data);
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const [shared, setShared] = useState(false);
  const files = data.gallery.map((src, index) => ({ src, name: demo && DEMO_FILES[index] ? DEMO_FILES[index] : `foto_${String(index + 1).padStart(2, "0")}.jpg` }));
  const attachments = files.length + (demo ? 1 : 0);

  const forward = async () => {
    const url = window.location.href;
    try {
      if (navigator.share) await navigator.share({ title: subject, url });
      else { await navigator.clipboard.writeText(url); setShared(true); setTimeout(() => setShared(false), 2000); }
    } catch { /* share dismissed */ }
  };

  return (
    <ThemeShell
      fonts={FONTS}
      background="#f1f3f4"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <Status />
          <div className={s.search} aria-hidden>
            <Lucide icon={ic.menu} size={18} color="#5f6368" />
            <span>Telusuri di email</span>
            <b>{guestInitial(guest)}</b>
          </div>
          <p className={s.inboxLabel} aria-hidden>UTAMA</p>
          <div className={s.list}>
            {INBOX_BEFORE.map(row => <InboxRow key={row.from} {...row} />)}
            <button type="button" className={`${s.row} ${s.rowActive}`} onClick={open}>
              <span className={`${s.avatar} ${s.avatarRed}`} aria-hidden>{initial(data.couple.bride)}</span>
              <span className={s.rowText}>
                <span className={s.rowHead}><b>{couple}</b><small>{stamp}</small></span>
                <span className={s.rowSubject}>{subject}</span>
                <span className={s.rowSnippet}>Dengan hormat, kami mengundang Bapak/Ibu untuk hadir pada…</span>
                <span className={s.tags} aria-hidden><i>Undangan</i><i className={s.tagGold}>Penting</i></span>
              </span>
              <Lucide icon={ic.star} color="#f9ab00" />
            </button>
            {INBOX_AFTER.map(row => <InboxRow key={row.from} {...row} />)}
          </div>
          <div className={s.coverSpacer} />
          <div className={s.kepada}>
            <span className={s.kepadaHead}><Lucide icon={ic.mail} size={15} color="#d93025" />1 email penting untuk:</span>
            <h1>{guest}</h1>
            <small>dari {sender}</small>
            <button type="button" className={s.openBtn} onClick={open}><Lucide icon={ic.mailOpen} size={15} color="#fff" />Buka Email Undangan</button>
          </div>
          <div className={s.fabRow} aria-hidden><span className={s.fab}><Lucide icon={ic.pencil} color="#001d35" />Tulis</span></div>
        </section>
      )}
    >
      <Status />
      <div className={s.nav} aria-hidden>
        <Lucide icon={ic.arrowLeft} size={20} color="#5f6368" />
        <span><Lucide icon={ic.archive} size={19} color="#5f6368" /><Lucide icon={ic.trash2} size={19} color="#5f6368" /><Lucide icon={ic.ellipsisVertical} size={19} color="#5f6368" /></span>
      </div>

      <main className={s.body}>
        <div className={s.subject}>
          <h1>{subject}</h1>
          <Lucide icon={ic.star} size={18} color="#f9ab00" />
        </div>

        <div className={s.from}>
          <span className={`${s.avatar} ${s.avatarRed}`} aria-hidden>{initial(data.couple.bride)}</span>
          <div>
            <div className={s.fromHead}><strong>{couple}</strong><small>{stamp}</small></div>
            <small>kepada saya, keluarga</small>
          </div>
          <button type="button" className={s.iconBtn} onClick={sheets.openWish} aria-label="Balas dengan ucapan"><Lucide icon={ic.reply} size={18} color="#5f6368" /></button>
        </div>

        <div className={s.letter}>
          <p>Dengan hormat,<br /><br />Tanpa mengurangi rasa hormat, kami bermaksud mengundang Bapak/Ibu/Saudara/i untuk hadir pada {label.toLowerCase()} kami:</p>
          <p className={s.names}>
            {data.couple.brideFull ?? data.couple.bride}
            {data.couple.brideParents && <><br />{data.couple.brideParents}</>}
            <br />&amp;<br />
            {data.couple.groomFull ?? data.couple.groom}
            {data.couple.groomParents && <><br />{data.couple.groomParents}</>}
          </p>
        </div>

        <section className={s.invite} aria-label="Undangan kalender">
          {data.events.map((event, index) => {
            const parts = dateParts(event.date || data.date);
            const href = mapsHref(data, event);
            const where = [event.venue, event.address].filter(Boolean).join(", ");
            return (
              <div key={event.name + index} className={s.inviteEvent}>
                <div className={s.inviteHead}>
                  <span className={s.cal} aria-hidden><small>{parts.monthShort}</small><b>{parts.day}</b></span>
                  <div>
                    <strong>{event.name} — {data.couple.bride} <span className={s.heart}>{"\u2665\uFE0E"}</span> {data.couple.groom}</strong>
                    <small>{formatDate(event.date || data.date)}{event.time ? ` · ${event.time}` : ""}</small>
                  </div>
                </div>
                {where && (href
                  ? <a className={s.where} href={href} target="_blank" rel="noreferrer">Lokasi: {where}</a>
                  : <p className={s.where}>Lokasi: {where}</p>)}
              </div>
            );
          })}
          <div className={s.rsvpRow} role="group" aria-label="Konfirmasi kehadiran">
            <button type="button" className={s.rsvpYes} onClick={sheets.openRsvp}>Ya, hadir</button>
            <button type="button" onClick={sheets.openRsvp}>Mungkin</button>
            <button type="button" onClick={sheets.openRsvp}>Tidak</button>
          </div>
        </section>

        {stories.length > 0 && (
          <section className={s.thread} aria-labelledby="sr-story">
            <h2 id="sr-story">Dari thread sebelumnya (Kisah Kami):</h2>
            {stories.map((story, index) => (
              <article key={story.title + index} className={s.threadItem}>
                <Lucide icon={ic.cornerUpLeft} size={13} color="#5f6368" style={{ marginTop: 1 }} />
                <div>
                  <strong>{"date" in story && story.date ? `${story.date} — ${story.title}` : story.title}</strong>
                  <p>{story.body}</p>
                </div>
              </article>
            ))}
          </section>
        )}

        {attachments > 0 && (
          <section className={s.attach} aria-labelledby="sr-files">
            <h2 id="sr-files">{attachments} Lampiran · Galeri</h2>
            <div className={s.grid}>
              {files.map(file => (
                <a key={file.src} className={s.file} href={file.src} target="_blank" rel="noreferrer">
                  <Photo src={file.src} alt={`Foto ${couple}: ${file.name}`} className={s.fileImg} />
                  <span className={s.fileCap}><Lucide icon={ic.image} size={10} color="#5f6368" /><span>{file.name}</span></span>
                </a>
              ))}
              {demo && (
                <div className={s.file}>
                  <span className={`${s.fileImg} ${s.filePdf}`}><Lucide icon={ic.fileText} size={22} color="#d93025" /></span>
                  <span className={s.fileCap}><Lucide icon={ic.fileText} size={10} color="#5f6368" /><span>wishlist.pdf</span></span>
                </div>
              )}
            </div>
          </section>
        )}

        {(demo || data.gifts.length > 0) && (
          <section className={s.kado} aria-labelledby="sr-gift">
            <h2 id="sr-gift">{demo ? "wishlist.pdf — Pratinjau" : "Kado & Amplop Digital"}</h2>
            {demo && DEMO_WISHLIST.map(([name, price], index) => (
              <div key={name} className={s.wishItem}><span>{index + 1}. {name}</span><b>{price}</b></div>
            ))}
            {data.gifts.map(gift => {
              const info = giftInfo(gift);
              const title = gift.type === "address" ? "Kirim Kado" : `Amplop Digital — ${[info.title, info.number].filter(Boolean).join(" ")}`;
              return (
                <div key={gift.id} className={s.amplop}>
                  <Lucide icon={ic.wallet} color="#188038" />
                  <div>
                    <strong>{title}</strong>
                    {gift.type === "address" ? <small>{info.number}</small> : info.holder && <small>a.n. {info.holder}</small>}
                    {"image" in info && info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                  </div>
                  {info.copy && <button type="button" className={s.copy} onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                </div>
              );
            })}
          </section>
        )}

        <section className={s.replies} aria-labelledby="sr-wishes">
          <h2 id="sr-wishes">{wishes.wishes.length} Balasan</h2>
          {wishes.wishes.length === 0 && <p className={s.empty}>Belum ada balasan. Jadilah yang pertama mengirim ucapan!</p>}
          {wishes.wishes.slice(0, 8).map(wish => (
            <article key={wish.id} className={s.reply}>
              <span className={s.avatarSm} aria-hidden>{initial(wish.name)}</span>
              <div>
                <strong>{wish.name}{!demo && wish.created_at && <small> · {timeAgo(wish.created_at)}</small>}</strong>
                <p>{wish.message}</p>
              </div>
            </article>
          ))}
        </section>
      </main>

      <nav className={s.bottom} aria-label="Aksi undangan">
        <button type="button" className={s.replyBtn} onClick={sheets.openWish}><Lucide icon={ic.reply} size={15} color="#fff" />Balas — Kirim Ucapan</button>
        <button type="button" className={s.forwardBtn} onClick={forward}><Lucide icon={shared ? ic.check : ic.forward} size={15} color="#5f6368" />{shared ? "Tautan disalin" : "Teruskan"}</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Balas undangan kalender" tint={tint}>
        <RsvpForm rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ yes: "Ya, hadir", maybe: "Mungkin", no: "Tidak", submit: "Kirim Balasan" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Balas — Kirim Ucapan" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} submitLabel="Kirim" />
      </Sheet>
    </ThemeShell>
  );
}
