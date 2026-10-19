"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";
import { EVENT_TYPES } from "@/lib/event-types";
import styles from "@/components/dashboard/editor.module.css";
import { friendly, GateNotice, getJson, lostAccess, usePageGate } from "../_lib";

type MainEvent = { title?: string; type?: string; date?: string; start_time?: string; end_time?: string; venue?: string; address?: string; maps_url?: string };
type Invitation = { id: string; slug: string; title: string; event?: MainEvent };
type EventItem = { id: string; title: string; type?: string; date: string; start_time?: string; end_time?: string; venue: string; address?: string; maps_url?: string; sort_order?: number };
type Draft = Omit<EventItem, "id"> & { id?: string };

const EMPTY_DRAFT: Draft = { title: "", date: "", start_time: "", end_time: "", venue: "", address: "", maps_url: "" };

const DATE_RE = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;
const TIME_RE = /^([01]\d|2[0-3]):[0-5]\d$/;

/** Mirrors the backend rules (YYYY-MM-DD, HH:MM); returns an Indonesian message or "". */
function validateSchedule(value: { date?: string; start_time?: string; end_time?: string }, dateRequired: boolean) {
  const date = value.date?.slice(0, 10) ?? "";
  if (!date) return dateRequired ? "Tanggal acara wajib diisi." : "";
  if (!DATE_RE.test(date) || Number.isNaN(new Date(`${date}T00:00:00Z`).getTime()) || new Date(`${date}T00:00:00Z`).toISOString().slice(0, 10) !== date) {
    return "Tanggal belum benar. Pilih tanggal dari kalender (format TTTT-BB-HH).";
  }
  for (const [label, time] of [["Jam mulai", value.start_time], ["Jam selesai", value.end_time]] as const) {
    if (time && !TIME_RE.test(time.slice(0, 5))) return `${label} belum benar. Gunakan format JJ:MM, misalnya 09:30.`;
  }
  if (value.start_time && value.end_time && value.end_time.slice(0, 5) < value.start_time.slice(0, 5)) return "Jam selesai tidak boleh lebih awal dari jam mulai.";
  return "";
}

/** Normalises date/time to exactly what the backend accepts. */
function cleanSchedule<T extends { date?: string; start_time?: string; end_time?: string }>(value: T): T {
  return { ...value, date: value.date?.slice(0, 10) ?? "", start_time: value.start_time?.slice(0, 5) ?? "", end_time: value.end_time?.slice(0, 5) ?? "" };
}

function dateLabel(value?: string) {
  if (!value) return "Tanggal belum diisi";
  const date = new Date(`${value.slice(0, 10)}T00:00:00+07:00`);
  return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat("id-ID", { weekday: "long", day: "numeric", month: "long", year: "numeric", timeZone: "Asia/Jakarta" }).format(date);
}

export default function EventsPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const invitationId = routeParams?.id;
  const [invitation, setInvitation] = useState<Invitation | null>(null);
  const [main, setMain] = useState<MainEvent>({});
  const [items, setItems] = useState<EventItem[]>([]);
  const [draft, setDraft] = useState<Draft | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState<"" | "main" | "item">("");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  const gate = usePageGate(invitationId, token, "events");
  const { lose } = gate;
  const allowed = gate.status === "ok";

  const loadItems = useCallback(async () => {
    if (!token || !invitationId) return;
    const list = await getJson<{ items?: EventItem[] }>(`/api/invitations/${invitationId}/events`, token);
    if (lostAccess(list.status)) { lose(); return; }
    if (!list.ok) { setError("Rangkaian acara gagal dimuat. Coba muat ulang halaman."); return; }
    setItems((list.data?.items ?? []).slice().sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0)));
  }, [token, invitationId, lose]);

  useEffect(() => {
    if (!ready || !token || !invitationId || !allowed) return;
    Promise.all([
      getJson<Invitation>(`/api/invitations/${invitationId}`, token),
      getJson<{ items?: EventItem[] }>(`/api/invitations/${invitationId}/events`, token),
    ])
      .then(([body, list]) => {
        if (lostAccess(body.status) || lostAccess(list.status)) { lose(); return; }
        if (!body.ok || !body.data || !list.ok) { setError("Gagal memuat detail acara. Coba muat ulang halaman."); return; }
        setInvitation(body.data);
        setMain(body.data.event ?? {});
        setItems((list.data?.items ?? []).slice().sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0)));
      })
      .finally(() => setLoading(false));
  }, [ready, token, invitationId, allowed, lose]);

  const setMainField = (key: keyof MainEvent, value: string) => { setMain((m) => ({ ...m, [key]: value })); setNotice(""); };

  async function saveMain(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !invitation) return;
    setError("");
    setNotice("");
    const invalid = validateSchedule(main, false);
    if (invalid) { setError(invalid); return; }
    setSaving("main");
    try {
      const response = await apiFetch(`/api/invitations/${invitation.id}`, token, {
        method: "PUT",
        // `published` is left out on purpose: the backend keeps the current publish state.
        body: JSON.stringify({ slug: invitation.slug, title: invitation.title, event: cleanSchedule(main) }),
      });
      if (lostAccess(response.status)) { lose(); return; }
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body.error ?? "");
      setNotice("Info utama tersimpan.");
    } catch (err) {
      const message = friendly(err, "");
      setError(message ? `Info utama belum tersimpan: ${message}` : "Info utama belum tersimpan.");
    } finally {
      setSaving("");
    }
  }

  async function saveItem(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !invitationId || !draft) return;
    setError("");
    const invalid = validateSchedule(draft, true);
    if (invalid) { setError(invalid); return; }
    setSaving("item");
    try {
      const payload = { ...cleanSchedule(draft), type: draft.type || main.type || "pernikahan", sort_order: draft.sort_order ?? items.length };
      const response = draft.id
        ? await apiFetch(`/api/invitations/${invitationId}/events/${draft.id}`, token, { method: "PUT", body: JSON.stringify(payload) })
        : await apiFetch(`/api/invitations/${invitationId}/events`, token, { method: "POST", body: JSON.stringify(payload) });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body.error);
      setDraft(null);
      await loadItems();
      setNotice("Rangkaian acara tersimpan.");
    } catch (err) {
      const message = friendly(err, "");
      setError(message ? `Acara belum tersimpan: ${message}` : "Acara belum tersimpan.");
    } finally {
      setSaving("");
    }
  }

  async function removeItem(item: EventItem) {
    if (!token || !invitationId || !window.confirm(`Hapus "${item.title}" dari rangkaian acara?`)) return;
    const response = await apiFetch(`/api/invitations/${invitationId}/events/${item.id}`, token, { method: "DELETE" });
    if (!response.ok) { setError("Acara belum terhapus."); return; }
    await loadItems();
  }

  async function move(index: number, direction: -1 | 1) {
    if (!token || !invitationId) return;
    const next = items.slice();
    const target = index + direction;
    if (target < 0 || target >= next.length) return;
    [next[index], next[target]] = [next[target], next[index]];
    setItems(next);
    const results = await Promise.all(next.map((item, order) => apiFetch(`/api/invitations/${invitationId}/events/${item.id}`, token, { method: "PUT", body: JSON.stringify({ ...cleanSchedule(item), sort_order: order }) }).catch(() => null)));
    if (results.some((r) => !r?.ok)) { setError("Urutan acara belum tersimpan semua."); await loadItems(); }
  }

  if (!ready || !invitationId) return null;

  if (!allowed) {
    return (
      <DashboardShell active="events" invitationId={invitationId}>
        <GateNotice gate={gate} invitationId={invitationId} />
      </DashboardShell>
    );
  }

  const fields = (value: Draft | MainEvent, change: (key: keyof Draft & keyof MainEvent, v: string) => void, withTitle: boolean) => (
    <>
      {withTitle && (
        <label className={styles.field}><span>Nama acara</span>
          <input value={value.title ?? ""} onChange={(e) => change("title", e.target.value)} required placeholder="Akad Nikah" />
        </label>
      )}
      <div className={styles.row3}>
        <label className={styles.field}><span>Tanggal</span><input type="date" min="1900-01-01" max="2100-12-31" value={value.date?.slice(0, 10) ?? ""} onChange={(e) => change("date", e.target.value)} required={withTitle} /></label>
        <label className={styles.field}><span>Jam mulai</span><input type="time" step={60} pattern="[0-2][0-9]:[0-5][0-9]" value={value.start_time?.slice(0, 5) ?? ""} onChange={(e) => change("start_time", e.target.value)} /></label>
        <label className={styles.field}><span>Jam selesai</span><input type="time" step={60} pattern="[0-2][0-9]:[0-5][0-9]" value={value.end_time?.slice(0, 5) ?? ""} onChange={(e) => change("end_time", e.target.value)} /></label>
      </div>
      <div className={styles.row}>
        <label className={styles.field}><span>Tempat</span><input value={value.venue ?? ""} onChange={(e) => change("venue", e.target.value)} required={withTitle} placeholder="Gedung Graha Sarana" /></label>
        <label className={styles.field}><span>Link Google Maps</span><input type="url" value={value.maps_url ?? ""} onChange={(e) => change("maps_url", e.target.value)} placeholder="https://maps.app.goo.gl/…" /></label>
      </div>
      <label className={styles.field}><span>Alamat lengkap</span><input value={value.address ?? ""} onChange={(e) => change("address", e.target.value)} placeholder="Jl. Gatot Subroto Kav. 12, Jakarta" /></label>
    </>
  );

  return (
    <DashboardShell active="events" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Acara</h1>
          <p className="dashboard-subtitle">Jenis acara, tanggal utama untuk hitung mundur, dan rangkaian acara seperti akad dan resepsi.</p>
        </div>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {notice && <p role="status" className={styles.ok} style={{ margin: "0 0 12px" }}>{notice}</p>}

      {loading ? <p className="dashboard-state">Memuat...</p> : (
        <div className={styles.form}>
          <form className={styles.panel} onSubmit={saveMain} aria-label="Info utama">
            <div className={styles.panelHead}>
              <div><h2>Info utama</h2><p>Dipakai untuk hitung mundur, sampul, dan jika rangkaian acara masih kosong.</p></div>
            </div>
            <div className={styles.row}>
              <label className={styles.field}><span>Jenis acara</span>
                <select value={main.type ?? ""} onChange={(e) => setMainField("type", e.target.value)}>
                  <option value="">Pilih jenis acara</option>
                  {EVENT_TYPES.map((type) => <option key={type.value} value={type.value}>{type.label}</option>)}
                </select>
              </label>
              <label className={styles.field}><span>Judul acara</span>
                <input value={main.title ?? ""} onChange={(e) => setMainField("title", e.target.value)} placeholder="Resepsi Pernikahan" />
              </label>
            </div>
            {fields(main, (key, value) => setMainField(key, value), false)}
            <div className={styles.actions}>
              <button type="submit" className="dashboard-action" disabled={saving !== ""}>{saving === "main" ? "Menyimpan..." : "Simpan info utama"}</button>
            </div>
          </form>

          <section className={styles.panel} aria-label="Rangkaian acara">
            <div className={styles.panelHead}>
              <div><h2>Rangkaian acara</h2><p>Tambahkan setiap sesi, misalnya akad lalu resepsi. Urutan di sini sama dengan di undangan.</p></div>
              {!draft && <button type="button" className={styles.ghost} onClick={() => setDraft({ ...EMPTY_DRAFT, date: main.date?.slice(0, 10) ?? "", venue: main.venue ?? "", address: main.address ?? "", maps_url: main.maps_url ?? "" })}>+ Tambah acara</button>}
            </div>

            {items.length === 0 && !draft && <p className={styles.empty}>Belum ada rangkaian acara. Undangan memakai info utama di atas.</p>}

            <ul className={styles.list}>
              {items.map((item, index) => draft?.id === item.id ? null : (
                <li key={item.id} className={styles.item}>
                  <span className={styles.badge}>{item.start_time || "—"}</span>
                  <div className={styles.itemBody}>
                    <strong>{item.title}</strong>
                    <small>{dateLabel(item.date)}{item.start_time ? ` · ${item.start_time}${item.end_time ? `–${item.end_time}` : ""} WIB` : ""}</small>
                    <small>{[item.venue, item.address].filter(Boolean).join(" · ")}</small>
                  </div>
                  <div className={styles.itemActions}>
                    <button type="button" className="table-action" onClick={() => move(index, -1)} disabled={index === 0} aria-label="Naikkan">↑</button>
                    <button type="button" className="table-action" onClick={() => move(index, 1)} disabled={index === items.length - 1} aria-label="Turunkan">↓</button>
                    <button type="button" className="table-action" onClick={() => setDraft({ ...item })}>Ubah</button>
                    <button type="button" className="table-action table-action-danger" onClick={() => removeItem(item)}>Hapus</button>
                  </div>
                </li>
              ))}
            </ul>

            {draft && (
              <form className={styles.editor} onSubmit={saveItem} aria-label={draft.id ? "Ubah acara" : "Tambah acara"}>
                {fields(draft, (key, value) => setDraft((d) => (d ? { ...d, [key]: value } : d)), true)}
                <div className={styles.actions}>
                  <button type="submit" className="dashboard-action" disabled={saving !== ""}>{saving === "item" ? "Menyimpan..." : draft.id ? "Simpan acara" : "Tambah ke rangkaian"}</button>
                  <button type="button" className={styles.ghost} onClick={() => setDraft(null)}>Batal</button>
                </div>
              </form>
            )}
          </section>
        </div>
      )}
    </DashboardShell>
  );
}
