"use client";

import { use, useEffect, useMemo, useRef, useState } from "react";
import QRCode from "qrcode";
import { apiFetch, getToken } from "@/lib/api";
import s from "./layar.module.css";

type Checkin = { id: string; name: string; table?: string; checked_in_at: string };
type Wish = { id: string; name: string; message: string };
type Photo = { id: string; url: string };
type Winner = { guest_id: string; name: string; table?: string; prize: string; at: string };
type Feed = {
  invitation: { slug: string; title: string; couple?: { bride_name?: string; groom_name?: string; bride_nickname?: string; groom_nickname?: string } };
  stats: { checked_in: number; guests: number };
  checkins: Checkin[];
  wishes: Wish[];
  photos: Photo[];
  doorprize: { winners: Winner[] };
};

const POLL = 3000;
const WELCOME_MS = 9000;
const WISH_MS = 8000;
const WINNER_MS = 15000;
const tableLabel = (table?: string) => (table ? (/^\d/.test(table) ? `Meja ${table}` : table) : "");
const COLORS = ["#ffd76a", "#9fb0ff", "#ff8fa3", "#7be0c3", "#ffffff"];

export default function VenueScreen({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [feed, setFeed] = useState<Feed | null>(null);
  const [error, setError] = useState("");
  // Conditions polling can't fix by itself: show a full-screen state and stop polling.
  const [blocked, setBlocked] = useState<"login" | "forbidden" | null>(null);
  const [queue, setQueue] = useState<Checkin[]>([]);
  const [current, setCurrent] = useState<Checkin | null>(null);
  const [wishIndex, setWishIndex] = useState(0);
  const [winner, setWinner] = useState<Winner | null>(null);
  const [qr, setQr] = useState("");
  const seen = useRef<Set<string> | null>(null);
  const seenWinners = useRef<Set<string> | null>(null);

  // Poll the feed; new check-ins are queued so every guest gets their moment on screen.
  useEffect(() => {
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout>;
    const tick = async () => {
      const token = getToken();
      if (!token) { setBlocked("login"); return; }
      try {
        const response = await apiFetch(`/api/invitations/${id}/live`, token);
        if (response.status === 401) { if (!cancelled) setBlocked("login"); return; }
        if (response.status === 403 || response.status === 404) { if (!cancelled) setBlocked("forbidden"); return; }
        if (!response.ok) throw new Error("Koneksi terputus, mencoba lagi…");
        const body: Feed = await response.json();
        if (cancelled) return;
        if (!seen.current) {
          seen.current = new Set(body.checkins.map((c) => c.id)); // don't replay arrivals from before the screen opened
          seenWinners.current = new Set(body.doorprize.winners.map((w) => w.guest_id + w.at));
        } else {
          const fresh = body.checkins.filter((c) => !seen.current!.has(c.id)).reverse();
          fresh.forEach((c) => seen.current!.add(c.id));
          if (fresh.length) setQueue((q) => [...q, ...fresh]);
          const newWinner = body.doorprize.winners.find((w) => !seenWinners.current!.has(w.guest_id + w.at));
          if (newWinner) { seenWinners.current!.add(newWinner.guest_id + newWinner.at); setWinner(newWinner); }
        }
        setFeed(body);
        setError("");
      } catch {
        if (!cancelled) setError("Koneksi terputus, mencoba lagi…");
      }
      if (!cancelled) timer = setTimeout(tick, POLL);
    };
    void tick();
    return () => { cancelled = true; clearTimeout(timer); };
  }, [id]);

  // Show queued arrivals one by one.
  useEffect(() => {
    if (current || queue.length === 0) return;
    const next = setTimeout(() => { setCurrent(queue[0]); setQueue((q) => q.slice(1)); }, 0);
    return () => clearTimeout(next);
  }, [current, queue]);
  useEffect(() => {
    if (!current) return;
    const done = setTimeout(() => setCurrent(null), queue.length > 3 ? 4000 : WELCOME_MS);
    return () => clearTimeout(done);
  }, [current, queue.length]);
  useEffect(() => {
    if (!winner) return;
    const done = setTimeout(() => setWinner(null), WINNER_MS);
    return () => clearTimeout(done);
  }, [winner]);

  const wishes = feed?.wishes ?? [];
  useEffect(() => {
    if (wishes.length < 2) return;
    const rotate = setInterval(() => setWishIndex((i) => i + 1), WISH_MS);
    return () => clearInterval(rotate);
  }, [wishes.length]);

  const slug = feed?.invitation.slug;
  useEffect(() => {
    if (!slug) return;
    QRCode.toDataURL(`${window.location.origin}/invitation/${slug}#extra-foto-tamu`, { width: 240, margin: 1 }).then(setQr).catch(() => undefined);
  }, [slug]);

  const couple = feed?.invitation.couple;
  const names = useMemo(() => {
    const bride = couple?.bride_nickname || couple?.bride_name?.split(/[ ,]/)[0];
    const groom = couple?.groom_nickname || couple?.groom_name?.split(/[ ,]/)[0];
    return bride && groom ? [bride, groom] : null;
  }, [couple]);
  const confetti = useMemo(() => Array.from({ length: 60 }, (_, i) => ({
    left: `${(i * 37) % 100}%`, delay: `${(i % 12) * 0.35}s`, duration: `${3 + (i % 5)}s`, color: COLORS[i % COLORS.length],
  })), []);

  const wish = wishes.length ? wishes[wishIndex % wishes.length] : null;
  const recent = (feed?.checkins ?? []).slice(0, 8);

  if (blocked) {
    const next = `/layar/${id}`;
    return (
      <main className={s.screen}>
        <section className={s.blocked} role="alert">
          <p className={s.eyebrow}>Layar sapa</p>
          {blocked === "login" ? (
            <>
              <h1>Layar ini perlu login dulu</h1>
              <p>Masuk dengan akun pemilik undangan atau anggota tim yang punya akses hari-H di perangkat ini. Layar akan langsung tampil setelah masuk.</p>
              <a className={s.blockedAction} href={`/auth/login?next=${encodeURIComponent(next)}`}>Masuk untuk membuka layar</a>
            </>
          ) : (
            <>
              <h1>Akunmu tidak punya akses ke layar ini</h1>
              <p>Undangan ini mungkin milik akun lain, sudah dihapus, atau peranmu di tim tidak termasuk layar sapa. Minta pemilik undangan menambahkan aksesmu, atau masuk dengan akun lain.</p>
              <div className={s.blockedRow}>
                <a className={s.blockedAction} href="/dashboard">Ke dashboard</a>
                <a className={s.blockedGhost} href={`/auth/login?next=${encodeURIComponent(next)}`}>Masuk dengan akun lain</a>
              </div>
            </>
          )}
        </section>
      </main>
    );
  }

  return (
    <main className={s.screen} aria-live="polite">
      {feed && feed.photos.length > 0 && (
        <div className={s.mosaic} aria-hidden>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          {Array.from({ length: 24 }, (_, i) => feed.photos[i % feed.photos.length]).map((p, i) => <img key={i} src={p.url} alt="" />)}
        </div>
      )}

      <header className={s.top}>
        <h1 className={s.names}>{names ? <>{names[0]} <span>&amp;</span> {names[1]}</> : feed?.invitation.title ?? "Rawuh"}</h1>
        {feed && <div className={s.count}><strong>{feed.stats.checked_in}</strong><small>tamu telah hadir</small></div>}
      </header>

      <section className={s.stage}>
        {current ? (
          <div key={current.id} className={s.welcome}>
            <p className={s.eyebrow}>Sugeng rawuh · Selamat datang</p>
            <p className={s.guest}>{current.name}</p>
            {current.table && <span className={s.table}>Silakan menuju {tableLabel(current.table)}</span>}
          </div>
        ) : wish ? (
          <div key={wish.id + wishIndex} className={s.wish}>
            <blockquote>{wish.message}</blockquote>
            <cite>— {wish.name}</cite>
          </div>
        ) : (
          <p className={s.idle}>{feed ? "Terima kasih sudah hadir. Tulis ucapanmu di undangan untuk tampil di sini." : "Menyiapkan layar…"}</p>
        )}
      </section>

      <footer className={s.bottom}>
        <ul className={s.recent} aria-label="Baru saja hadir">
          {recent.map((c) => <li key={c.id}>{c.name}</li>)}
        </ul>
        {qr && feed && feed.photos !== undefined && (
          <div className={s.qr}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={qr} alt="" />
            <span>Scan untuk kirim ucapan &amp; foto</span>
          </div>
        )}
      </footer>

      {winner && (
        <div className={s.winner} role="alert">
          <div className={s.confetti} aria-hidden>{confetti.map((c, i) => <i key={i} style={{ left: c.left, background: c.color, animationDelay: c.delay, animationDuration: c.duration }} />)}</div>
          <p className={s.eyebrow}>Pemenang doorprize</p>
          <p className={s.prize}>{winner.prize}</p>
          <p className={s.guest}>{winner.name}</p>
          {winner.table && <span className={s.table}>{tableLabel(winner.table)}</span>}
        </div>
      )}

      <div className={s.controls}>
        <button type="button" onClick={() => document.documentElement.requestFullscreen?.().catch(() => undefined)}>Layar penuh</button>
        <a href={`/dashboard/invitations/${id}/layar`}>Keluar</a>
      </div>
      {error && <p className={s.error} role="status">{error}</p>}
    </main>
  );
}
