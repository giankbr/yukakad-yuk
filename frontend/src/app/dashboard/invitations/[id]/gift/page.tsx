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

const giftTypeLabels: Record<string, string> = { bank: "Transfer bank", ewallet: "E-wallet", qris: "QRIS", address: "Alamat" };

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
      .catch(() => setError("Gagal memuat metode amplop digital"))
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
      if (!response.ok) throw new Error(body.error ?? "Gagal mengunggah");
      setForm((prev) => ({ ...prev, qris_image_url: body.path }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Gagal mengunggah QRIS");
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
      if (!response.ok) throw new Error(body.error ?? "Gagal menambahkan metode amplop digital");
      setForm(emptyForm);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Gagal menambahkan metode amplop digital");
    } finally {
      setSubmitting(false);
    }
  }

  if (!ready || !invitationId) return null;

  return (
    <DashboardShell active="gift" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Amplop digital / Hadiah</h1>
          <p className="dashboard-subtitle">Transfer bank, QRIS, atau e-wallet — tamu bisa pilih yang paling mudah buat mereka.</p>
        </div>
      </header>

      {loading && <p className="dashboard-state">Memuat metode amplop digital...</p>}
      {error && <p className="dashboard-state dashboard-state-error">{error}</p>}

      {!loading && gifts.length > 0 && (
        <div className="dashboard-table-wrap">
          <table className="dashboard-table">
            <thead><tr><th>Jenis</th><th>Detail</th><th>Status</th><th><span className="sr-only">Aksi</span></th></tr></thead>
            <tbody>
              {gifts.map((gift) => (
                <tr key={gift.id}>
                  <td><strong>{giftTypeLabels[gift.type] ?? gift.type}</strong></td>
                  <td>
                    {gift.type === "bank" && `${gift.bank_name} · ${gift.account_number} · ${gift.account_name}`}
                    {gift.type === "ewallet" && `${gift.ewallet_provider} · ${gift.ewallet_number}`}
                    {gift.type === "qris" && "Gambar QRIS"}
                    {gift.type === "address" && gift.address}
                  </td>
                  <td><span className={`status ${gift.is_active ? "status-published" : "status-draft"}`}>{gift.is_active ? "Aktif" : "Nonaktif"}</span></td>
                  <td><button className="table-action" onClick={() => toggleActive(gift)}>{gift.is_active ? "Nonaktifkan" : "Aktifkan"}</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <form className="dashboard-form" onSubmit={handleSubmit}>
        <h2 style={{ margin: "1rem 0 0", color: "#173c3a" }}>Tambah metode</h2>
        <FormSelect label="Jenis" value={form.type} onChange={(e) => setForm({ ...emptyForm, type: e.target.value })}>
          <option value="bank">Transfer bank</option>
          <option value="ewallet">E-wallet</option>
          <option value="qris">QRIS</option>
          <option value="address">Alamat</option>
        </FormSelect>

        {form.type === "bank" && (
          <>
            <FormField label="Nama bank" value={form.bank_name} onChange={(e) => setForm({ ...form, bank_name: e.target.value })} placeholder="BCA" required />
            <div className="form-row">
              <FormField label="Nomor rekening" value={form.account_number} onChange={(e) => setForm({ ...form, account_number: e.target.value })} placeholder="1234567890" required />
              <FormField label="Nama pemilik rekening" value={form.account_name} onChange={(e) => setForm({ ...form, account_name: e.target.value })} required />
            </div>
          </>
        )}

        {form.type === "ewallet" && (
          <div className="form-row">
            <FormSelect label="Penyedia" value={form.ewallet_provider} onChange={(e) => setForm({ ...form, ewallet_provider: e.target.value })}>
              <option value="gopay">GoPay</option>
              <option value="ovo">OVO</option>
              <option value="dana">DANA</option>
              <option value="shopeepay">ShopeePay</option>
            </FormSelect>
            <FormField label="Nomor" value={form.ewallet_number} onChange={(e) => setForm({ ...form, ewallet_number: e.target.value })} placeholder="081234567890" required />
          </div>
        )}

        {form.type === "qris" && (
          <label className="upload-drop">
            <span>{uploadingQris ? "Mengunggah..." : form.qris_image_url ? "Gambar QRIS sudah terunggah — klik untuk mengganti" : "Klik untuk mengunggah gambar QRIS"}</span>
            <input type="file" accept="image/jpeg,image/png,image/webp" onChange={handleQrisUpload} disabled={uploadingQris} hidden />
          </label>
        )}

        {form.type === "address" && (
          <FormField label="Alamat" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} required />
        )}

        <div className="form-actions">
          <Button type="submit" disabled={submitting} className="bg-[#173c3a] text-white">
            {submitting ? "Menambahkan..." : "Tambah metode"}
          </Button>
        </div>
      </form>
    </DashboardShell>
  );
}
