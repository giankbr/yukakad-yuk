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
  checked_in_at?: string;
};

export default function GuestsDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [guests, setGuests] = useState<Guest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [name, setName] = useState("");
  const [qrGuestId, setQrGuestId] = useState<string | null>(null);
  const [phone, setPhone] = useState("");
  const [category, setCategory] = useState("family");
  const [submitting, setSubmitting] = useState(false);
  const [importing, setImporting] = useState(false);

  const invitationId = routeParams?.id;

  const load = useCallback(() => {
    if (!token || !invitationId) return;
    apiFetch(`/api/invitations/${invitationId}/guests`, token)
      .then((response) => response.json())
      .then((body: { items?: Guest[] }) => setGuests(body.items ?? []))
      .catch(() => setError("Could not load guests"))
      .finally(() => setLoading(false));
  }, [token, invitationId]);

  useEffect(() => {
    if (!ready) return;
    load();
  }, [ready, load]);

  async function handleAddGuest(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !invitationId) return;
    setSubmitting(true);
    setError("");
    try {
      const response = await apiFetch(`/api/invitations/${invitationId}/guests`, token, {
        method: "POST",
        body: JSON.stringify({ name, phone, category }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Could not add guest");
      setName("");
      setPhone("");
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not add guest");
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
      if (!response.ok) throw new Error(body.error ?? "Import failed");
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Import failed");
    } finally {
      setImporting(false);
      event.target.value = "";
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
          <p className="dashboard-kicker">Invitation guests</p>
          <h1>Guest list</h1>
          <p className="dashboard-subtitle">{guests.length} guests invited</p>
        </div>
        <a className="secondary-action" href={`/dashboard/invitations/${invitationId}/checkin`}>
          Scan for check-in →
        </a>
      </header>

      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      <form className="dashboard-form" onSubmit={handleAddGuest} style={{ maxWidth: "none" }}>
        <div className="form-row" style={{ gridTemplateColumns: "2fr 1fr 1fr auto" }}>
          <FormField label="Name" value={name} onChange={(e) => setName(e.target.value)} required />
          <FormField label="Phone" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="0812..." />
          <FormField label="Category" value={category} onChange={(e) => setCategory(e.target.value)} />
          <div className="form-actions">
            <Button type="submit" disabled={submitting} className="bg-[#173c3a] text-white">
              {submitting ? "Adding..." : "Add"}
            </Button>
          </div>
        </div>
      </form>

      <label className="upload-drop" style={{ marginTop: "1rem" }}>
        <span>{importing ? "Importing..." : "Click to import guests from CSV (name, phone, category)"}</span>
        <input type="file" accept=".csv,text/csv" onChange={handleImportCSV} disabled={importing} hidden />
      </label>

      {loading && <p className="dashboard-state">Loading guest list...</p>}
      {!loading && !error && guests.length === 0 && <p className="dashboard-state">No guests yet. Add your first guest to begin.</p>}
      {!loading && guests.length > 0 && (
        <div className="dashboard-table-wrap" style={{ marginTop: "1.5rem" }}>
          <table className="dashboard-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Category</th>
                <th>Phone</th>
                <th>Check-in</th>
                <th>QR</th>
                <th><span className="sr-only">Actions</span></th>
              </tr>
            </thead>
            <tbody>
              {guests.map((guest) => (
                <tr key={guest.id}>
                  <td><strong>{guest.name}</strong></td>
                  <td>{guest.category}</td>
                  <td>{guest.phone || "—"}</td>
                  <td>
                    {guest.checked_in_at ? (
                      <span className="status status-published">Checked in</span>
                    ) : (
                      <span className="status status-draft">Not yet</span>
                    )}
                  </td>
                  <td>
                    {qrGuestId === guest.id ? <GuestQRCode guestId={guest.id} /> : (
                      <button className="table-action" onClick={() => setQrGuestId(guest.id)}>Show QR</button>
                    )}
                  </td>
                  <td style={{ display: "flex", gap: ".5rem" }}>
                    {!guest.checked_in_at && (
                      <button className="table-action" onClick={() => handleCheckIn(guest.id)}>Check in</button>
                    )}
                    <button className="table-action" onClick={() => handleDelete(guest.id)}>Remove</button>
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
