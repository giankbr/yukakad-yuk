"use client";
// Theme "Chat Hijau" — undangan bergaya ruang obrolan aplikasi pesan (design: Tema Chat Hijau (Fitri & Andra)).
import { useState, type ReactNode } from "react";
import {
  Extras, Lucide, Photo, RsvpForm, Sheet, ThemeShell, WishForm, coupleLabel, formatDate, giftInfo, guestLabel,
  mapsHref, storyItems, useCopy, useRsvp, useSheets, useWishes, type ThemeProps, type ThemeTint,
} from "../kit";
import { ic } from "./icons";
import s from "./styles.module.css";

const FONTS = ["Inter:wght@400;600;700;800"];
const tint: ThemeTint = {
  "--t-accent": "#008069", "--t-ink": "#111b21", "--t-muted": "#667781", "--t-line": "#d1d7db", "--t-field": "#f0f2f5",
  "--t-radius": "12px", "--t-font": "Inter, system-ui, sans-serif",
};
const DEMO_WISHES = [
  { id: "w1", name: "Keluarga Pak RT", message: "Barakallah Fitri & Andra! Samawa yaa, kami sekeluarga hadir insyaAllah.", created_at: "2026-10-15T14:02:00+07:00" },
  { id: "w2", name: "Teman KKN", message: "Selamat! Dari grup KKN sampai KUA keren kalian.", created_at: "2026-10-15T14:02:00+07:00" },
];

/** "Fitri Handayani, S.Pd." → "Fitri Handayani" */
function plainName(name: string) {
  return name.split(",")[0].trim();
}

function city(address: string) {
  const parts = address.split(",").map(part => part.trim()).filter(Boolean);
  return parts[parts.length - 1] ?? "";
}

function Bubble({ out, time = "14:02", read, className, children }: { out?: boolean; time?: string; read?: boolean; className?: string; children: ReactNode }) {
  return (
    <div className={`${s.row} ${out ? s.rowOut : ""}`}>
      <div className={`${s.bubble} ${out ? s.out : ""} ${className ?? ""}`}>
        {children}
        {time && <span className={s.stamp}>{time}{read && <Lucide icon={ic.checkCheck} size={13} color="#53bdeb" />}</span>}
      </div>
    </div>
  );
}

function Day({ children }: { children: ReactNode }) {
  return <div className={s.day}><span>{children}</span></div>;
}

function ChatHeader({ title, avatar }: { title: string; avatar?: string }) {
  return (
    <header className={s.header}>
      <div className={s.contact}>
        <Lucide icon={ic.arrowLeft} size={20} color="#fff" />
        <Photo src={avatar} alt="" className={s.avatar} />
        <div><strong>{title}</strong><small>online</small></div>
        <span className={s.headIcons} aria-hidden>
          <Lucide icon={ic.video} size={19} color="#fff" /><Lucide icon={ic.phone} size={19} color="#fff" /><Lucide icon={ic.ellipsisVertical} size={19} color="#fff" />
        </span>
      </div>
    </header>
  );
}

export default function ChatHijauTheme({ data, slug, guestToken, demo, skipCover }: ThemeProps) {
  const couple = coupleLabel(data);
  const { couple: c } = data;
  const rsvp = useRsvp({ slug, guestToken, demo });
  const wishes = useWishes({ slug, guestToken, demo, seed: DEMO_WISHES });
  const sheets = useSheets();
  const { copy, copied } = useCopy();
  const stories = storyItems(data);
  const [showAll, setShowAll] = useState(false);
  const avatar = data.gallery[0];
  const cardImage = data.gallery[1] ?? data.gallery[0];
  const photos = data.gallery.length > 4 ? data.gallery.slice(2) : data.gallery;
  const visible = showAll ? photos : photos.slice(0, 4);
  const hidden = photos.length - 4;
  const fullNames = `${plainName(c.brideFull ?? c.bride)} & ${plainName(c.groomFull ?? c.groom)}`;
  const where = city(data.address);
  const wishTime = (value?: string) => (value ? formatDate(value, { hour: "2-digit", minute: "2-digit" }) : "");

  return (
    <ThemeShell
      fonts={FONTS}
      background="#d6cfc3"
      skipCover={skipCover}
      className={s.root}
      cover={open => (
        <section className={s.cover}>
          <ChatHeader title={couple} avatar={avatar} />
          <div className={s.coverChat}>
            <Day>Hari Ini</Day>
            <Bubble>Assalamualaikum! Ada kabar bahagia nih</Bubble>
            {c.note && <Bubble>{c.note}</Bubble>}
            <div className={s.row}>
              <article className={`${s.bubble} ${s.invite}`}>
                <Photo src={cardImage} alt={`Foto ${couple}`} className={s.inviteImg} />
                <div className={s.inviteText}>
                  <small>Undangan {data.eventLabel ?? "Pernikahan"}</small>
                  <h1>{fullNames}</h1>
                  <p>{[formatDate(data.date), where].filter(Boolean).join(" · ")}</p>
                  <div className={s.to}>
                    <small>Kepada Yth. Bapak/Ibu/Saudara/i</small>
                    <strong>{guestLabel(data)}</strong>
                  </div>
                </div>
                <button type="button" className={s.linkBtn} onClick={open}><Lucide icon={ic.externalLink} size={14} color="#53bdeb" />Buka Undangan</button>
              </article>
            </div>
            <Bubble>Mohon maaf bila ada salah penulisan nama &amp; gelar ya</Bubble>
            <Bubble out read className={s.short}>Wah selamat!! Pasti datang</Bubble>
          </div>
          <div className={s.inputBar}>
            <div className={s.field} aria-hidden><Lucide icon={ic.smile} size={20} color="#667781" /><span>Ketik balasan…</span><Lucide icon={ic.paperclip} size={18} color="#667781" /></div>
            <button type="button" className={s.send} onClick={open} aria-label="Buka undangan"><Lucide icon={ic.send} size={18} color="#fff" /></button>
          </div>
        </section>
      )}
    >
      <ChatHeader title={couple} avatar={avatar} />

      <main className={s.body}>
        <Day>Mempelai</Day>
        {[
          { name: c.brideFull ?? c.bride, parents: c.brideParents, photo: c.bridePhoto ?? data.gallery[2], out: false },
          { name: c.groomFull ?? c.groom, parents: c.groomParents, photo: c.groomPhoto ?? data.gallery[3], out: true },
        ].map(person => (
          <div key={person.name} className={`${s.row} ${person.out ? s.rowOut : ""}`}>
            <article className={`${s.bubble} ${s.media} ${person.out ? s.out : ""}`}>
              <Photo src={person.photo} alt={person.name} className={s.personImg} />
              <div className={s.mediaText}><strong>{person.name}</strong>{person.parents && <small>{person.parents}</small>}</div>
            </article>
          </div>
        ))}

        <Extras slot="opening" className={s.extras} />

        {stories.length > 0 && (
          <>
            <Day>Kisah Kami</Day>
            {stories.map((story, index) => (
              <Bubble key={story.title + index} out={index % 2 === 1} read={index % 2 === 1}>
                {story.title && story.body && <b className={s.sender}>{story.title}</b>}
                <p>{[story.date, story.body || story.title].filter(Boolean).join(" — ")}</p>
                {story.image && <Photo src={story.image} alt={story.title} className={s.storyImg} />}
              </Bubble>
            ))}
          </>
        )}

        <Day>Acara</Day>
        {data.events.map((event, index) => {
          const href = mapsHref(data, event);
          return (
            <div key={event.name + index} className={s.row}>
              <article className={`${s.bubble} ${s.media} ${s.event}`}>
                <div className={s.map} aria-hidden><Lucide icon={ic.mapPin} size={26} color="#008069" /></div>
                <div className={s.mediaText}>
                  <strong>{event.name} · {formatDate(event.date, { weekday: "long", day: "numeric", month: "short", year: "numeric" })}</strong>
                  <em>{event.time}</em>
                  <small>{[event.venue, event.address].filter(Boolean).join(", ")}</small>
                </div>
                {href && <a className={s.linkBtn} href={href} target="_blank" rel="noreferrer">Lihat Lokasi</a>}
              </article>
            </div>
          );
        })}

        <Extras slot="event" className={s.extras} />

        {photos.length > 0 && (
          <>
            <Day>Galeri</Day>
            <div className={`${s.row} ${s.rowOut}`}>
              <div className={`${s.bubble} ${s.out} ${s.album}`}>
                {visible.map((src, index) => {
                  const more = !showAll && index === 3 && hidden > 0;
                  const demoMore = demo && !showAll && index === 3 && hidden <= 0;
                  return (
                    <div key={src + index} className={s.tile}>
                      <Photo src={src} alt={`Foto ${index + 1}`} />
                      {more && <button type="button" className={s.more} onClick={() => setShowAll(true)} aria-label={`Lihat ${hidden} foto lainnya`}>+{hidden}</button>}
                      {demoMore && <span className={s.more} aria-hidden>+12</span>}
                    </div>
                  );
                })}
              </div>
            </div>
          </>
        )}

        <Extras slot="story" className={s.extras} />
        <Extras slot="end" className={s.extras} />

        {(demo || data.gifts.length > 0) && (
          <>
            <Day>Kado</Day>
            <div className={s.row}>
              <article className={`${s.bubble} ${s.gift}`}>
                <strong className={s.giftTitle}>{demo ? "Wishlist Kado" : "Kirim Kado"}</strong>
                {demo && [
                  { name: "Blender & Chopper", price: "Rp650.000", icon: ic.soup },
                  { name: "Air Cooler", price: "Rp980.000", icon: ic.fan },
                  { name: "Set Alat Makan", price: "Rp420.000", icon: ic.utensils },
                ].map(item => (
                  <div key={item.name} className={s.item}>
                    <span><Lucide icon={item.icon} color="#008069" /></span>
                    <div><b>{item.name}</b><small>{item.price}</small></div>
                    <Lucide icon={ic.chevronRight} size={14} color="#667781" />
                  </div>
                ))}
                {data.gifts.map(gift => {
                  const info = giftInfo(gift);
                  return (
                    <div key={gift.id} className={s.pay}>
                      <Lucide icon={ic.wallet} color="#008069" />
                      <div>
                        <b>{gift.type === "address" ? "Kirim Kado" : gift.type === "qris" ? "QRIS" : "Amplop Digital"}</b>
                        <small>{[[info.title !== "Alamat kado" && gift.type !== "qris" ? info.title : "", info.number].filter(Boolean).join(" "), info.holder ? `a.n. ${info.holder}` : ""].filter(Boolean).join(" · ")}</small>
                        {info.image && <Photo src={info.image} alt="Kode QRIS" className={s.qris} />}
                      </div>
                      {info.copy && <button type="button" onClick={() => copy(info.copy)}>{copied === info.copy ? "Tersalin" : "Salin"}</button>}
                    </div>
                  );
                })}
              </article>
            </div>
          </>
        )}

        <Day>Ucapan Tamu</Day>
        {wishes.wishes.slice(0, 10).map(wish => (
          <Bubble key={wish.id} time={wishTime(wish.created_at)}>
            <b className={s.sender}>{wish.name}</b>
            <p>{wish.message}</p>
          </Bubble>
        ))}
        <button type="button" className={`${s.field} ${s.fieldBtn}`} onClick={sheets.openWish}>
          <Lucide icon={ic.smile} size={20} color="#667781" /><span>Tulis ucapan untuk {couple}…</span><Lucide icon={ic.send} size={18} color="#008069" />
        </button>
      </main>

      <nav className={s.quick} aria-label="Konfirmasi kehadiran">
        <div className={s.chips}>
          <button type="button" className={s.chipOn} onClick={() => sheets.openRsvp("yes")}>Hadir</button>
          <button type="button" onClick={() => sheets.openRsvp("maybe")}>Masih ragu</button>
          <button type="button" onClick={() => sheets.openRsvp("no")}>Berhalangan</button>
        </div>
        <button type="button" className={s.rsvp} onClick={sheets.openRsvp}><Lucide icon={ic.send} size={15} color="#fff" />Kirim Konfirmasi &amp; Ucapan</button>
      </nav>

      <Sheet open={sheets.sheet === "rsvp"} onClose={sheets.close} title="Konfirmasi Kehadiran" tint={tint}>
        <RsvpForm key={sheets.attendance} initialAttendance={sheets.attendance} rsvp={rsvp} guestName={data.guestName} demo={demo} labels={{ maybe: "Masih ragu" }} />
      </Sheet>
      <Sheet open={sheets.sheet === "wish"} onClose={sheets.close} title="Kirim Ucapan" tint={tint}>
        <WishForm wishes={wishes} guestName={data.guestName} demo={demo} />
      </Sheet>
    </ThemeShell>
  );
}
