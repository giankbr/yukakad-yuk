"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import styles from "@/components/dashboard/editor.module.css";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Entry = { id: string; guest_id?: string; name: string; kind: string; amount: number; item?: string; note?: string; created_at: string; source: "manual" | "online" };
type Ledger = { items: Entry[]; totals: { cash: number; transfer: number; online: number; total: number }; kado_count: number };
type Guest = { id: string; name: string; table?: string };

const KINDS: Record<string, string> = { cash: "Amplop tunai", transfer: "Transfer", kado: "Kado / barang", online: "Amplop online" };
const empty = { id: "", guest_id: "", name: "", kind: "cash", amount: "", item: "", note: "" };
const rupiah = (value: number) => `Rp${Math.round(value).toLocaleString("id-ID")}`;
const when = (value: string) => new Date(value).toLocaleString("id-ID", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });

function downloadCsv(filename: string, rows: (string | number)[][]) {
  const escape = (cell: string | number) => `"${String(cell).replace(/"/g, '""')}"`;
  const csv = "﻿" + rows.map((row) => row.map(escape).join(",")).join("\r\n");
  const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
  const link = Object.assign(document.createElement("a"), { href: url, download: filename });
  link.click();
  URL.revokeObjectURL(url);
}

export default function BuwuhPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const invitationId = routeParams?.id;
  const [ledger, setLedger] = useState<Ledger | null>(null);
  const [guests, setGuests] = useState<Guest[]>([]);
  const [form, setForm] = useState(empty);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    if (!token || !invitationId) return;
    const [l, g] = await Promise.all([
      apiFetch(`/api/invitations/${invitationId}/ledger`, token).then((r) => r.json()),
      apiFetch(`/api/invitations/${invitationId}/guests`, token).then((r) => r.json()).catch(() => ({})),
    ]);
    setLedger(l);
    setGuests(Array.isArray(g) ? g : g.items ?? []);
  }, [token, invitationId]);

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    const timer = setTimeout(() => { load().catch(() => setError("Gagal memuat buku buwuh")).finally(() => setLoading(false)); }, 0);
    return () => clearTimeout(timer);
  }, [ready, token, invitationId, load]);

  const pickName = (name: string) => {
    const guest = guests.find((g) => g.name.toLowerCase() === name.trim().toLowerCase());
    setForm((f) => ({ ...f, name, guest_id: guest?.id ?? "" }));
  };

  async function save(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !invitationId) return;
    setBusy(true);
    setError("");
    setNotice("");
    try {
      const payload = { guest_id: form.guest_id, name: form.name, kind: form.kind, amount: Number(form.amount.replace(/\D/g, "")) || 0, item: form.item, note: form.note };
      const response = await apiFetch(`/api/invitations/${invitationId}/ledger${form.id ? `/${form.id}` : ""}`, token, { method: form.id ? "PATCH" : "POST", body: JSON.stringify(payload) });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error);
      setNotice(form.id ? "Catatan diperbarui." : `${form.name} tercatat.`);
      setForm(empty);
      await load();
    } catch (err) {
      setError(err instanceof Error && err.message ? err.message : "Belum tersimpan.");
    } finally {
      setBusy(false);
    }
  }

  async function remove(entry: Entry) {
    if (!token || !invitationId || !window.confirm(`Hapus catatan dari ${entry.name}?`)) return;
    await apiFetch(`/api/invitations/${invitationId}/ledger/${entry.id}`, token, { method: "DELETE" });
    await load();
  }

  const visible = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return (ledger?.items ?? []).filter((e) => !needle || `${e.name} ${e.item ?? ""} ${e.note ?? ""}`.toLowerCase().includes(needle));
  }, [ledger, query]);

  function exportCsv() {
    const rows: (string | number)[][] = [["Tanggal", "Nama", "Meja", "Jenis", "Nominal", "Barang", "Catatan"]];
    for (const e of ledger?.items ?? []) {
      const table = guests.find((g) => g.id === e.guest_id)?.table ?? "";
      rows.push([when(e.created_at), e.name, table, KINDS[e.kind] ?? e.kind, e.amount || "", e.item ?? "", e.note ?? ""]);
    }
    downloadCsv("buku-buwuh.csv", rows);
  }

  if (!ready || !invitationId) return null;
  const t = ledger?.totals;

  return (
    <DashboardShell active="ledger" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Tamu &amp; amplop</p>
          <h1>Buku buwuh</h1>
          <p className="dashboard-subtitle">Catatan siapa memberi apa, supaya keluarga bisa membalas saat mereka punya hajat. Amplop online masuk otomatis; amplop tunai dan kado dicatat di sini atau saat check-in.</p>
        </div>
        <button type="button" className="secondary-action" onClick={exportCsv} disabled={!ledger?.items.length}>Unduh Excel (CSV)</button>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {notice && <p role="status" className={styles.ok} style={{ margin: "0 0 12px" }}>{notice}</p>}

      {loading ? <p className="dashboard-state">Memuat…</p> : (
        <div className={styles.form} style={{ maxWidth: "none" }}>
          <div className={styles.row3} style={{ gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))" }}>
            {[["Total uang", t?.total ?? 0], ["Amplop tunai", t?.cash ?? 0], ["Transfer", t?.transfer ?? 0], ["Amplop online", t?.online ?? 0]].map(([label, value]) => (
              <div key={label} className={styles.item} style={{ display: "grid", gap: 2 }}><small className={styles.hint}>{label}</small><strong style={{ fontSize: 20 }}>{rupiah(Number(value))}</strong></div>
            ))}
            <div className={styles.item} style={{ display: "grid", gap: 2 }}><small className={styles.hint}>Kado / barang</small><strong style={{ fontSize: 20 }}>{ledger?.kado_count ?? 0}</strong></div>
          </div>

          <form className={styles.panel} onSubmit={save} aria-label={form.id ? "Ubah catatan" : "Catat pemberian"}>
            <div className={styles.panelHead}><div><h2>{form.id ? "Ubah catatan" : "Catat pemberian"}</h2><p>Nama tamu dari daftar tamu akan terhubung otomatis.</p></div></div>
            <div className={styles.row}>
              <label className={styles.field}><span>Nama pemberi</span>
                <input list="buwuh-guests" value={form.name} onChange={(e) => pickName(e.target.value)} placeholder="Keluarga Bpk. Hadi" required maxLength={120} />
                <datalist id="buwuh-guests">{guests.map((g) => <option key={g.id} value={g.name} />)}</datalist>
              </label>
              <label className={styles.field}><span>Jenis</span>
                <select value={form.kind} onChange={(e) => setForm({ ...form, kind: e.target.value })}>
                  <option value="cash">Amplop tunai</option><option value="transfer">Transfer</option><option value="kado">Kado / barang</option>
                </select>
              </label>
              <label className={styles.field}><span>{form.kind === "kado" ? "Perkiraan nilai (opsional)" : "Nominal (Rp)"}</span>
                <input inputMode="numeric" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value.replace(/[^\d]/g, "") })} required={form.kind === "transfer"} placeholder={form.kind === "cash" ? "Kosongkan bila belum dibuka" : "100000"} />
              </label>
              {form.kind === "kado" ? (
                <label className={styles.field}><span>Barang</span><input value={form.item} onChange={(e) => setForm({ ...form, item: e.target.value })} placeholder="Rice cooker" required /></label>
              ) : (
                <label className={styles.field}><span>Catatan (opsional)</span><input value={form.note} onChange={(e) => setForm({ ...form, note: e.target.value })} placeholder="Titipan dari Pak RT" /></label>
              )}
            </div>
            <div className={styles.actions}>
              <button type="submit" className="dashboard-action" disabled={busy}>{busy ? "Menyimpan…" : form.id ? "Simpan perubahan" : "Catat"}</button>
              {form.id && <button type="button" className={styles.ghost} onClick={() => setForm(empty)}>Batal</button>}
            </div>
          </form>

          <section className={styles.panel} aria-label="Daftar pemberian">
            <div className={styles.panelHead}>
              <div><h2>Daftar pemberian</h2><p>{ledger?.items.length ?? 0} catatan</p></div>
              <label className={styles.field} style={{ width: 260 }}><span className="sr-only">Cari</span><input type="search" placeholder="Cari nama atau barang…" value={query} onChange={(e) => setQuery(e.target.value)} /></label>
            </div>
            {visible.length === 0 ? <p className={styles.empty}>Belum ada catatan.</p> : (
              <div className="dashboard-table-wrap">
                <table className="dashboard-table" style={{ minWidth: 720 }}>
                  <thead><tr><th>Nama</th><th>Jenis</th><th>Nominal / barang</th><th>Waktu</th><th><span className="sr-only">Aksi</span></th></tr></thead>
                  <tbody>
                    {visible.map((e) => (
                      <tr key={e.id}>
                        <td><strong>{e.name}</strong>{e.note && <span>{e.note}</span>}</td>
                        <td><span className={`status ${e.source === "online" ? "status-published" : "status-draft"}`}>{KINDS[e.kind] ?? e.kind}</span></td>
                        <td><strong>{e.amount ? rupiah(e.amount) : e.kind === "cash" ? "Belum dihitung" : "—"}</strong>{e.item && <span>{e.item}</span>}</td>
                        <td>{when(e.created_at)}</td>
                        <td>
                          {e.source === "manual" && (
                            <div style={{ display: "flex", gap: 6 }}>
                              <button type="button" className="table-action" onClick={() => { setForm({ id: e.id, guest_id: e.guest_id ?? "", name: e.name, kind: e.kind, amount: e.amount ? String(e.amount) : "", item: e.item ?? "", note: e.note ?? "" }); window.scrollTo({ top: 0, behavior: "smooth" }); }}>Ubah</button>
                              <button type="button" className="table-action table-action-danger" onClick={() => remove(e)}>Hapus</button>
                            </div>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </div>
      )}
    </DashboardShell>
  );
}
