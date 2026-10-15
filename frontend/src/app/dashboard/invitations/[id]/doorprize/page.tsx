"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Prize = { id: string; name: string; qty: number };
type Winner = { guest_id: string; name: string; table?: string; prize_id: string; prize: string; at: string };
type State = { prizes: Prize[]; winners: Winner[] };

export default function DoorprizePage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const invitationId = routeParams?.id;
  const [state, setState] = useState<State>({ prizes: [], winners: [] });
  const [draft, setDraft] = useState<Prize[]>([]);
  const [present, setPresent] = useState<string[]>([]);
  const [presentCount, setPresentCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string | null>(null);
  const [rolling, setRolling] = useState("");
  const [reveal, setReveal] = useState<Winner | null>(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const spin = useRef<ReturnType<typeof setInterval> | null>(null);

  const load = useCallback(async () => {
    if (!token || !invitationId) return;
    const [d, live] = await Promise.all([
      apiFetch(`/api/invitations/${invitationId}/doorprize`, token).then((r) => r.json()),
      apiFetch(`/api/invitations/${invitationId}/live`, token).then((r) => r.json()).catch(() => ({ checkins: [] })),
    ]);
    setState(d);
    setDraft(d.prizes.length ? d.prizes : [{ id: "", name: "", qty: 1 }]);
    setPresent((live.checkins ?? []).map((c: { name: string }) => c.name));
    setPresentCount(live.stats?.checked_in ?? 0);
  }, [token, invitationId]);

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    const timer = setTimeout(() => { load().catch(() => setError("Gagal memuat doorprize")).finally(() => setLoading(false)); }, 0);
    return () => { clearTimeout(timer); if (spin.current) clearInterval(spin.current); };
  }, [ready, token, invitationId, load]);

  async function savePrizes(reset = false) {
    if (!token || !invitationId) return;
    setBusy("save");
    setError("");
    setNotice("");
    try {
      const response = await apiFetch(`/api/invitations/${invitationId}/doorprize`, token, { method: "PUT", body: JSON.stringify({ prizes: draft, reset_winners: reset }) });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error);
      setState(body);
      setDraft(body.prizes.length ? body.prizes : [{ id: "", name: "", qty: 1 }]);
      setNotice(reset ? "Daftar pemenang dikosongkan." : "Hadiah tersimpan.");
    } catch (err) {
      setError(err instanceof Error && err.message ? err.message : "Belum tersimpan.");
    } finally {
      setBusy(null);
    }
  }

  async function draw(prize: Prize) {
    if (!token || !invitationId) return;
    setBusy(prize.id);
    setError("");
    setNotice("");
    setReveal(null);
    // Shuffle names for suspense while the server picks the winner.
    const names = present.length ? present : ["…"];
    let i = 0;
    spin.current = setInterval(() => { setRolling(names[i++ % names.length]); }, 70);
    try {
      const [response] = await Promise.all([
        apiFetch(`/api/invitations/${invitationId}/doorprize/draw`, token, { method: "POST", body: JSON.stringify({ prize_id: prize.id }) }),
        new Promise((resolve) => setTimeout(resolve, 2600)),
      ]);
      const body = await response.json();
      if (!response.ok) throw new Error(body.error);
      setState(body.state);
      setReveal(body.winner);
    } catch (err) {
      setError(err instanceof Error && err.message ? err.message : "Undian gagal.");
    } finally {
      if (spin.current) clearInterval(spin.current);
      setRolling("");
      setBusy(null);
    }
  }

  if (!ready || !invitationId) return null;
  const given = (id: string) => state.winners.filter((w) => w.prize_id === id).length;
  const dirty = JSON.stringify(draft.filter((p) => p.name.trim())) !== JSON.stringify(state.prizes);

  return (
    <DashboardShell active="doorprize" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Hari-H</p>
          <h1>Undian doorprize</h1>
          <p className="dashboard-subtitle">Diundi acak dari tamu yang sudah check-in ({presentCount} hadir). Setiap tamu hanya bisa menang sekali. Pemenang langsung tampil di Layar sapa.</p>
        </div>
        <a className="secondary-action" href={`/layar/${invitationId}`} target="_blank" rel="noreferrer">Buka layar sapa ↗</a>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {notice && <p role="status" className={styles.ok} style={{ margin: "0 0 12px" }}>{notice}</p>}

      {loading ? <p className="dashboard-state">Memuat…</p> : (
        <div className={styles.form}>
          {(rolling || reveal) && (
            <section className={styles.panel} aria-live="assertive" style={{ textAlign: "center", borderColor: "var(--rw-primary-border)", background: "var(--rw-primary-soft)" }}>
              <p className={styles.hint} style={{ fontFamily: "var(--rw-font-mono)", letterSpacing: ".2em", textTransform: "uppercase" }}>{rolling ? "Mengundi…" : `Pemenang ${reveal?.prize}`}</p>
              <p style={{ margin: 0, fontSize: "clamp(28px, 5vw, 48px)", fontWeight: 700, color: rolling ? "var(--rw-ink-2)" : "var(--rw-primary)" }}>{rolling || reveal?.name}</p>
              {!rolling && reveal?.table && <p className={styles.hint}>{/^\d/.test(reveal.table) ? `Meja ${reveal.table}` : reveal.table}</p>}
            </section>
          )}

          <section className={styles.panel} aria-label="Hadiah">
            <div className={styles.panelHead}><div><h2>Hadiah</h2><p>Urutkan dari hadiah hiburan sampai hadiah utama.</p></div></div>
            <ul className={styles.list}>
              {draft.map((prize, index) => {
                const saved = state.prizes.find((p) => p.id === prize.id);
                const left = saved ? saved.qty - given(saved.id) : 0;
                return (
                  <li key={prize.id || `new-${index}`} className={styles.item}>
                    <div className={`${styles.cells} ${styles.nameQty}`}>
                      <label className={styles.field}><span>Nama hadiah</span><input value={prize.name} maxLength={80} onChange={(e) => setDraft(draft.map((p, i) => (i === index ? { ...p, name: e.target.value } : p)))} placeholder="Voucher belanja Rp200.000" /></label>
                      <label className={styles.field}><span>Jumlah</span><input type="number" min={1} max={500} value={prize.qty} onChange={(e) => setDraft(draft.map((p, i) => (i === index ? { ...p, qty: Number(e.target.value) || 1 } : p)))} /></label>
                    </div>
                    <div className={styles.itemActions} style={{ alignSelf: "end" }}>
                      {saved && !dirty && (
                        <button type="button" className="dashboard-action" disabled={busy !== null || left <= 0 || presentCount === 0} onClick={() => draw(saved)}>
                          {busy === saved.id ? "Mengundi…" : left > 0 ? `Undi (${left} lagi)` : "Habis"}
                        </button>
                      )}
                      <button type="button" className="table-action table-action-danger" onClick={() => setDraft(draft.filter((_, i) => i !== index))}>Hapus</button>
                    </div>
                  </li>
                );
              })}
            </ul>
            <div className={styles.actions}>
              <button type="button" className={styles.ghost} onClick={() => setDraft([...draft, { id: "", name: "", qty: 1 }])}>+ Tambah hadiah</button>
              <button type="button" className="dashboard-action" disabled={busy !== null || !dirty} onClick={() => savePrizes()}>{busy === "save" ? "Menyimpan…" : "Simpan hadiah"}</button>
              {dirty && <span className={styles.hint}>Simpan dulu sebelum mengundi.</span>}
            </div>
          </section>

          <section className={styles.panel} aria-label="Pemenang">
            <div className={styles.panelHead}>
              <div><h2>Pemenang</h2><p>{state.winners.length} pemenang</p></div>
              {state.winners.length > 0 && <button type="button" className={styles.ghost} onClick={() => { if (window.confirm("Kosongkan semua pemenang? Undian bisa diulang dari awal.")) void savePrizes(true); }}>Ulang undian</button>}
            </div>
            {state.winners.length === 0 ? <p className={styles.empty}>Belum ada yang diundi.</p> : (
              <ol className={styles.list}>
                {state.winners.slice().reverse().map((w) => (
                  <li key={w.guest_id + w.at} className={styles.item}>
                    <div className={styles.itemBody}><strong>{w.name}</strong><small>{w.prize}{w.table ? ` · ${/^\d/.test(w.table) ? `meja ${w.table}` : w.table}` : ""} · {new Date(w.at).toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" })}</small></div>
                  </li>
                ))}
              </ol>
            )}
          </section>
        </div>
      )}
    </DashboardShell>
  );
}
