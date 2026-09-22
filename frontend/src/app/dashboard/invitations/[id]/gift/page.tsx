"use client";

import { useCallback, useEffect, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FormField, FormSelect } from "@/components/dashboard/FormField";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Gift = {
  id: string;
  type: string;
  bank_name?: string;
  account_number?: string;
  account_name?: string;
  ewallet_provider?: string;
  ewallet_number?: string;
  qris_image_url?: string;
  address?: string;
  is_active: boolean;
};

const emptyForm = { type: "bank", bank_name: "", account_number: "", account_name: "", ewallet_provider: "gopay", ewallet_number: "", qris_image_url: "", address: "" };

export default function GiftPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [gifts, setGifts] = useState<Gift[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [form, setForm] = useState(emptyForm);
  const [submitting, setSubmitting] = useState(false);
  const [uploadingQris, setUploadingQris] = useState(false);

  const invitationId = routeParams?.id;

  const load = useCallback(() => {
    if (!token || !invitationId) return;
    apiFetch(`/api/invitations/${invitationId}/gifts`, token)
      .then((response) => response.json())
      .then((body: { items?: Gift[] }) => setGifts(body.items ?? []))
      .catch(() => setError("Could not load gift methods"))
      .finally(() => setLoading(false));
  }, [token, invitationId]);

  useEffect(() => {
    if (!ready) return;
    load();
  }, [ready, load]);

  async function toggleActive(gift: Gift) {
    if (!token || !invitationId) return;
    await apiFetch(`/api/invitations/${invitationId}/gifts/${gift.id}`, token, {
      method: "PATCH",
      body: JSON.stringify({ is_active: !gift.is_active }),
    });
    load();
  }

  async function handleQrisUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file || !token || !invitationId) return;
    setUploadingQris(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("type", "qris");
      const response = await apiFetch(`/api/invitations/${invitationId}/media`, token, { method: "POST", body: formData });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Upload failed");
      setForm((prev) => ({ ...prev, qris_image_url: body.path }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "QRIS upload failed");
    } finally {
      setUploadingQris(false);
    }
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !invitationId) return;
    setSubmitting(true);
    setError("");
    try {
      const response = await apiFetch(`/api/invitations/${invitationId}/gifts`, token, {
        method: "POST",
        body: JSON.stringify(form),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error ?? "Could not add gift method");
      setForm(emptyForm);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not add gift method");
    } finally {
      setSubmitting(false);
    }
  }

  if (!ready || !invitationId) return null;

  return (
    <DashboardShell active="gift" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Invitation</p>
          <h1>Gift / Amplop digital</h1>
          <p className="dashboard-subtitle">Bank, QRIS, or e-wallet — guests pick whichever is easiest for them.</p>
        </div>
      </header>

      {loading && <p className="dashboard-state">Loading gift methods...</p>}
      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      {!loading && gifts.length > 0 && (
        <div className="dashboard-table-wrap">
          <table className="dashboard-table">
            <thead><tr><th>Type</th><th>Details</th><th>Status</th><th><span className="sr-only">Actions</span></th></tr></thead>
            <tbody>
              {gifts.map((gift) => (
                <tr key={gift.id}>
                  <td><strong>{gift.type}</strong></td>
                  <td>
                    {gift.type === "bank" && `${gift.bank_name} · ${gift.account_number} · ${gift.account_name}`}
                    {gift.type === "ewallet" && `${gift.ewallet_provider} · ${gift.ewallet_number}`}
                    {gift.type === "qris" && "QRIS image"}
                    {gift.type === "address" && gift.address}
                  </td>
                  <td><span className={`status ${gift.is_active ? "status-published" : "status-draft"}`}>{gift.is_active ? "Active" : "Inactive"}</span></td>
                  <td><button className="table-action" onClick={() => toggleActive(gift)}>{gift.is_active ? "Deactivate" : "Activate"}</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <form className="dashboard-form" onSubmit={handleSubmit}>
        <h2 style={{ margin: "1rem 0 0", color: "#173c3a" }}>Add a method</h2>
        <FormSelect label="Type" value={form.type} onChange={(e) => setForm({ ...emptyForm, type: e.target.value })}>
          <option value="bank">Bank transfer</option>
          <option value="ewallet">E-wallet</option>
          <option value="qris">QRIS</option>
          <option value="address">Address</option>
        </FormSelect>

        {form.type === "bank" && (
          <>
            <FormField label="Bank name" value={form.bank_name} onChange={(e) => setForm({ ...form, bank_name: e.target.value })} placeholder="BCA" required />
            <div className="form-row">
              <FormField label="Account number" value={form.account_number} onChange={(e) => setForm({ ...form, account_number: e.target.value })} placeholder="1234567890" required />
              <FormField label="Account name" value={form.account_name} onChange={(e) => setForm({ ...form, account_name: e.target.value })} required />
            </div>
          </>
        )}

        {form.type === "ewallet" && (
          <div className="form-row">
            <FormSelect label="Provider" value={form.ewallet_provider} onChange={(e) => setForm({ ...form, ewallet_provider: e.target.value })}>
              <option value="gopay">GoPay</option>
              <option value="ovo">OVO</option>
              <option value="dana">DANA</option>
              <option value="shopeepay">ShopeePay</option>
            </FormSelect>
            <FormField label="Number" value={form.ewallet_number} onChange={(e) => setForm({ ...form, ewallet_number: e.target.value })} placeholder="081234567890" required />
          </div>
        )}

        {form.type === "qris" && (
          <label className="upload-drop">
            <span>{uploadingQris ? "Uploading..." : form.qris_image_url ? "QRIS image uploaded — click to replace" : "Click to upload QRIS image"}</span>
            <input type="file" accept="image/jpeg,image/png,image/webp" onChange={handleQrisUpload} disabled={uploadingQris} hidden />
          </label>
        )}

        {form.type === "address" && (
          <FormField label="Address" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} required />
        )}

        <div className="form-actions">
          <Button type="submit" disabled={submitting} className="bg-[#173c3a] text-white">
            {submitting ? "Adding..." : "Add gift method"}
          </Button>
        </div>
      </form>
    </DashboardShell>
  );
}
