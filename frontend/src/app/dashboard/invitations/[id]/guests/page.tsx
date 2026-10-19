"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField } from "@/components/dashboard/FormField";
import { GuestQRCode } from "@/components/dashboard/GuestQRCode";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";
import Link from "next/link";
import { friendly, GateNotice, getJson, lostAccess, usePageGate, type ApiBody } from "../_lib";

type Guest = {
  id: string;
  name: string;
  phone?: string;
  category: string;
  token: string;
  table?: string;
  checked_in_at?: string;
};

/** Friendly message for the plan's guest quota (409 code guest_limit, or the older 422 text). */
function quotaMessage(status: number, body: ApiBody): string | null {
  const isQuota = body.code === "guest_limit" || ((status === 409 || status === 422) && /guest limit/i.test(String(body.error ?? "")));
  if (!isQuota) return null;
  const limit = typeof body.limit === "number" ? body.limit : null;
  const remaining = typeof body.remaining === "number" ? Math.max(0, body.remaining) : null;
  if (limit !== null && remaining !== null) return `Kuota tamu paketmu tinggal ${remaining} dari ${limit}. Kurangi isi file atau upgrade paket.`;
  if (limit !== null) return `Kuota tamu paketmu (${limit} tamu) sudah penuh. Upgrade paket untuk menambah tamu.`;
  return "Kuota tamu paketmu sudah penuh. Upgrade paket untuk menambah tamu.";
}

const categoryLabels: Record<string, string> = { family: "Keluarga", friend: "Teman", friends: "Teman", colleague: "Rekan kerja", vip: "VIP" };

export default function GuestsDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [guests, setGuests] = useState<Guest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [quota, setQuota] = useState("");
  const [importNotice, setImportNotice] = useState("");
  const [name, setName] = useState("");
  const [qrGuestId, setQrGuestId] = useState<string | null>(null);
  const [phone, setPhone] = useState("");
  const [table, setTable] = useState("");
  const [savingTable, setSavingTable] = useState<string | null>(null);
  const [category, setCategory] = useState("family");
  const [submitting, setSubmitting] = useState(false);
  const [importing, setImporting] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);

  const invitationId = routeParams?.id;

  const gate = usePageGate<{ slug?: string }>(invitationId, token, "guests");
  const { lose } = gate;
  const allowed = gate.status === "ok";
  const slug = gate.invitation?.slug ?? "";

  const load = useCallback(async () => {
    if (!token || !invitationId) return;
    const result = await getJson<{ items?: Guest[] }>(`/api/invitations/${invitationId}/guests`, token);
    setLoading(false);
    if (lostAccess(result.status)) { lose(); return; }
    if (!result.ok) { setError(result.error || "Gagal memuat daftar tamu."); return; }
    setGuests(result.data?.items ?? []);
  }, [token, invitationId, lose]);

  useEffect(() => {
    if (!ready || !allowed) return;
    const timer = setTimeout(() => { void load(); }, 0);
    return () => clearTimeout(timer);
  }, [ready, allowed, load]);



  /** Personal link: greets the guest by name, records RSVP against them and shows their check-in QR. */
  function personalLink(guest: Guest) {
    const params = new URLSearchParams({ to: guest.name, guest: guest.token });
    return `${window.location.origin}/invitation/${slug}?${params}`;
  }

  async function copyLink(guest: Guest) {
    try {
      await navigator.clipboard.writeText(personalLink(guest));
      setCopied(guest.id);
      setTimeout(() => setCopied(current => (current === guest.id ? null : current)), 1800);
    } catch {
      window.prompt("Salin link undangan:", personalLink(guest));
    }
  }

  function whatsappHref(guest: Guest) {
    const digits = (guest.phone ?? "").replace(/[^0-9]/g, "").replace(/^0/, "62");
    const text = `Halo ${guest.name}, dengan penuh sukacita kami mengundang Anda. Buka undangan di sini: ${personalLink(guest)}`;
    return `https://wa.me/${digits}?text=${encodeURIComponent(text)}`;
  }

  async function handleAddGuest(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !invitationId) return;
    setSubmitting(true);
    setError("");
    setQuota("");
    setImportNotice("");
    try {
      const result = await getJson<Guest>(`/api/invitations/${invitationId}/guests`, token, {
        method: "POST",
        body: JSON.stringify({ name, phone, category, table }),
      });
      if (!result.ok) {
        const limit = quotaMessage(result.status, result.body);
        if (limit) { setQuota(limit.replace("Kurangi isi file atau upgrade paket.", "Upgrade paket untuk menambah tamu.")); return; }
        throw new Error(result.error || "Gagal menambahkan tamu.");
      }
      setName("");
      setPhone("");
      setTable("");
      void load();
    } catch (err) {
      setError(friendly(err, "Gagal menambahkan tamu."));
    } finally {
      setSubmitting(false);
    }
  }

  async function handleImportCSV(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file || !token || !invitationId) return;
    setImporting(true);
    setError("");
    setQuota("");
    setImportNotice("");
    try {
      const text = await file.text();
      const result = await getJson<{ items?: Guest[] }>(`/api/invitations/${invitationId}/guests`, token, {
        method: "POST",
        headers: { "Content-Type": "text/csv" },
        body: text,
      });
      if (!result.ok) {
        const limit = quotaMessage(result.status, result.body);
        if (limit) { setQuota(limit); return; }
        throw new Error(result.error || "Gagal mengimpor.");
      }
      const count = result.data?.items?.length ?? 0;
      setImportNotice(count > 0 ? `${count} tamu berhasil diimpor dari ${file.name}.` : `Tidak ada tamu baru di ${file.name}. Pastikan baris pertama berisi data atau judul kolom "name".`);
    } catch (err) {
      setError(`Impor gagal: ${friendly(err, "file belum bisa dibaca.")}`);
    } finally {
      setImporting(false);
      event.target.value = "";
      // Always refresh: part of the file may have gone in before an error.
      void load();
    }
  }

  /** Saves a table/seat label; called when the inline input loses focus or Enter is pressed. */
  async function saveTable(guest: Guest, value: string) {
    const next = value.trim().slice(0, 20);
    if (!token || !invitationId || next === (guest.table ?? "")) return;
    setSavingTable(guest.id);
    setError("");
    try {
      const result = await getJson<Guest>(`/api/invitations/${invitationId}/guests/${guest.id}`, token, {
        method: "PATCH",
        body: JSON.stringify({ name: guest.name, phone: guest.phone ?? "", category: guest.category, table: next }),
      });
      if (!result.ok) throw new Error(result.error || "Nomor meja belum tersimpan.");
      setGuests(current => current.map(item => (item.id === guest.id ? { ...item, table: result.data?.table ?? next } : item)));
    } catch (err) {
      setError(friendly(err, "Nomor meja belum tersimpan."));
    } finally {
      setSavingTable(null);
    }
  }

  async function handleDelete(guestId: string) {
    if (!token || !invitationId) return;
    const response = await apiFetch(`/api/invitations/${invitationId}/guests/${guestId}`, token, { method: "DELETE" }).catch(() => null);
    if (!response?.ok) setError("Tamu belum terhapus. Coba lagi.");
    void load();
  }

  async function handleCheckIn(guestId: string) {
    if (!token || !invitationId) return;
    const result = await getJson<Guest & { already?: boolean }>(`/api/invitations/${invitationId}/guests/${guestId}/check-in`, token, { method: "POST" });
    if (!result.ok) setError(`Check-in gagal: ${result.error}`);
    void load();
  }

  if (!ready || !invitationId) return null;

  if (!allowed) {
    return (
      <DashboardShell active="guests" invitationId={invitationId}>
        <GateNotice gate={gate} invitationId={invitationId} />
      </DashboardShell>
    );
  }

  const isOwner = gate.access?.role === "owner";

  return (
    <DashboardShell active="guests" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Tamu undangan</p>
          <h1>Daftar tamu</h1>
          <p className="dashboard-subtitle">{guests.length} tamu diundang</p>
        </div>
        <a className="secondary-action" href={`/dashboard/invitations/${invitationId}/checkin`}>
          Scan untuk check-in →
        </a>
      </header>

      {error && <p role="alert" className="dashboard-state dashboard-state-error">{error}</p>}
      {quota && (
        <p role="alert" className="dashboard-state dashboard-state-error">
          {quota}{" "}
          {isOwner ? <Link href="/dashboard/paket">Lihat paket</Link> : "Minta pemilik undangan untuk upgrade paket."}
        </p>
      )}
      {importNotice && <p role="status" className="dashboard-state">{importNotice}</p>}

      <form className="dashboard-form" onSubmit={handleAddGuest} style={{ maxWidth: "none" }}>
        <div className="form-row" style={{ gridTemplateColumns: "2fr 1fr 1fr 0.7fr auto" }}>
          <FormField label="Nama" value={name} onChange={(e) => setName(e.target.value)} required />
          <FormField label="No. HP" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="0812..." />
          <FormField label="Kategori" value={category} onChange={(e) => setCategory(e.target.value)} />
          <FormField label="Meja" value={table} onChange={(e) => setTable(e.target.value)} placeholder="12 / VIP A" maxLength={20} />
          <div className="form-actions">
            <Button type="submit" disabled={submitting}>
              {submitting ? "Menambahkan..." : "Tambah"}
            </Button>
          </div>
        </div>
      </form>

      <label className="upload-drop" style={{ marginTop: "1rem" }}>
        <span>{importing ? "Mengimpor..." : "Klik untuk impor tamu dari CSV: kolom nama, no. HP, kategori, meja. Pemisah titik koma (;) atau koma (,) sama-sama bisa, jadi file dari Excel langsung bisa dipakai."}</span>
        <input type="file" accept=".csv,text/csv" onChange={handleImportCSV} disabled={importing} hidden />
      </label>

      {loading && <p className="dashboard-state">Memuat daftar tamu...</p>}
      {!loading && !error && guests.length === 0 && <p className="dashboard-state">Belum ada tamu. Tambahkan tamu pertama kamu untuk mulai.</p>}
      {!loading && guests.length > 0 && (
        <div className="dashboard-table-wrap" style={{ marginTop: "1.5rem" }}>
          <table className="dashboard-table dashboard-table-stack">
            <thead>
              <tr>
                <th>Nama</th>
                <th>Kategori</th>
                <th>No. HP</th>
                <th>Meja</th>
                <th>Check-in</th>
                <th>QR</th>
                <th><span className="sr-only">Aksi</span></th>
              </tr>
            </thead>
            <tbody>
              {guests.map((guest) => (
                <tr key={guest.id}>
                  <td><strong>{guest.name}</strong></td>
                  <td data-label="Kategori">{categoryLabels[guest.category] ?? guest.category}</td>
                  <td data-label="No. HP">{guest.phone || "—"}</td>
                  <td data-label="Meja">
                    <input
                      className="table-input"
                      defaultValue={guest.table ?? ""}
                      key={guest.table ?? ""}
                      placeholder="—"
                      maxLength={20}
                      aria-label={`Nomor meja ${guest.name}`}
                      disabled={savingTable === guest.id}
                      onBlur={(event) => void saveTable(guest, event.target.value)}
                      onKeyDown={(event) => { if (event.key === "Enter") event.currentTarget.blur(); }}
                    />
                  </td>
                  <td data-label="Check-in">
                    {guest.checked_in_at ? (
                      <span className="status status-published">Sudah check-in</span>
                    ) : (
                      <span className="status status-draft">Belum</span>
                    )}
                  </td>
                  <td data-label="QR">
                    {qrGuestId === guest.id ? <GuestQRCode guestId={guest.id} /> : (
                      <button className="table-action" onClick={() => setQrGuestId(guest.id)}>Tampilkan QR</button>
                    )}
                  </td>
                  <td style={{ display: "flex", flexWrap: "wrap", gap: ".5rem" }}>
                    {slug && guest.token && (
                      <>
                        <button className="table-action" onClick={() => copyLink(guest)}>{copied === guest.id ? "Tersalin ✓" : "Salin link"}</button>
                        {guest.phone && <a className="table-action" href={whatsappHref(guest)} target="_blank" rel="noreferrer">Kirim WA</a>}
                      </>
                    )}
                    {!guest.checked_in_at && (
                      <button className="table-action" onClick={() => handleCheckIn(guest.id)}>Check-in</button>
                    )}
                    <button className="table-action table-action-danger" onClick={() => handleDelete(guest.id)}>Hapus</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </DashboardShell>
  );
}
