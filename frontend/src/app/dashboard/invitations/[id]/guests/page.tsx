"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField } from "@/components/dashboard/FormField";
import { GuestQRCode } from "@/components/dashboard/GuestQRCode";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Guest = {
  id: string;
  name: string;
  phone?: string;
  category: string;
  token: string;
  table?: string;
  checked_in_at?: string;
};

const categoryLabels: Record<string, string> = { family: "Keluarga", friend: "Teman", friends: "Teman", colleague: "Rekan kerja", vip: "VIP" };

export default function GuestsDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [guests, setGuests] = useState<Guest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [name, setName] = useState("");
  const [qrGuestId, setQrGuestId] = useState<string | null>(null);
  const [phone, setPhone] = useState("");
  const [table, setTable] = useState("");
  const [savingTable, setSavingTable] = useState<string | null>(null);
  const [category, setCategory] = useState("family");
  const [submitting, setSubmitting] = useState(false);
  const [importing, setImporting] = useState(false);
  const [slug, setSlug] = useState("");
  const [copied, setCopied] = useState<string | null>(null);

  const invitationId = routeParams?.id;

  const load = useCallback(() => {
    if (!token || !invitationId) return;
    apiFetch(`/api/invitations/${invitationId}/guests`, token)
      .then((response) => response.json())
      .then((body: { items?: Guest[] }) => setGuests(body.items ?? []))
      .catch(() => setError("Gagal memuat daftar tamu"))
      .finally(() => setLoading(false));
  }, [token, invitationId]);

  useEffect(() => {
    if (!ready) return;
    load();
  }, [ready, load]);

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    apiFetch(`/api/invitations/${invitationId}`, token)
      .then((response) => response.json())
      .then((body: { slug?: string }) => setSlug(body.slug ?? ""))
      .catch(() => undefined);
  }, [ready, token, invitationId]);

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
    try {
      const response = await apiFetch(`/api/invitations/${invitationId}/guests`, token, {
        method: "POST",
        body: JSON.stringify({ name, phone, category, table }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Gagal menambahkan tamu");
      setName("");
      setPhone("");
      setTable("");
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Gagal menambahkan tamu");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleImportCSV(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file || !token || !invitationId) return;
    setImporting(true);
    setError("");
    try {
      const text = await file.text();
      const response = await apiFetch(`/api/invitations/${invitationId}/guests`, token, {
        method: "POST",
        headers: { "Content-Type": "text/csv" },
        body: text,
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Gagal mengimpor");
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Gagal mengimpor");
    } finally {
      setImporting(false);
      event.target.value = "";
    }
  }

  /** Saves a table/seat label; called when the inline input loses focus or Enter is pressed. */
  async function saveTable(guest: Guest, value: string) {
    const next = value.trim().slice(0, 20);
    if (!token || !invitationId || next === (guest.table ?? "")) return;
    setSavingTable(guest.id);
    setError("");
    try {
      const response = await apiFetch(`/api/invitations/${invitationId}/guests/${guest.id}`, token, {
        method: "PATCH",
        body: JSON.stringify({ name: guest.name, phone: guest.phone ?? "", category: guest.category, table: next }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Nomor meja belum tersimpan");
      setGuests(current => current.map(item => (item.id === guest.id ? { ...item, table: body.table ?? next } : item)));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Nomor meja belum tersimpan");
    } finally {
      setSavingTable(null);
    }
  }

  async function handleDelete(guestId: string) {
    if (!token || !invitationId) return;
    await apiFetch(`/api/invitations/${invitationId}/guests/${guestId}`, token, { method: "DELETE" });
    load();
  }

  async function handleCheckIn(guestId: string) {
    if (!token || !invitationId) return;
    await apiFetch(`/api/invitations/${invitationId}/guests/${guestId}/check-in`, token, { method: "POST" });
    load();
  }

  if (!ready || !invitationId) return null;

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

      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

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
        <span>{importing ? "Mengimpor..." : "Klik untuk impor tamu dari CSV (name, phone, category, table)"}</span>
        <input type="file" accept=".csv,text/csv" onChange={handleImportCSV} disabled={importing} hidden />
      </label>

      {loading && <p className="dashboard-state">Memuat daftar tamu...</p>}
      {!loading && !error && guests.length === 0 && <p className="dashboard-state">Belum ada tamu. Tambahkan tamu pertama kamu untuk mulai.</p>}
      {!loading && guests.length > 0 && (
        <div className="dashboard-table-wrap" style={{ marginTop: "1.5rem" }}>
          <table className="dashboard-table">
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
                  <td>{categoryLabels[guest.category] ?? guest.category}</td>
                  <td>{guest.phone || "—"}</td>
                  <td>
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
                  <td>
                    {guest.checked_in_at ? (
                      <span className="status status-published">Sudah check-in</span>
                    ) : (
                      <span className="status status-draft">Belum</span>
                    )}
                  </td>
                  <td>
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
