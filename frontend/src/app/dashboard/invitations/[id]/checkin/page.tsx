"use client";

import { useEffect, useRef, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Result = { kind: "success" | "error"; message: string } | null;
type Checked = { id: string; name: string };

export default function CheckInPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [result, setResult] = useState<Result>(null);
  const [scanning, setScanning] = useState(false);
  const [checked, setChecked] = useState<Checked | null>(null);
  const [gift, setGift] = useState({ kind: "cash", amount: "", item: "" });
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState("");
  const scannerRef = useRef<import("html5-qrcode").Html5QrcodeScanner | null>(null);
  const busyRef = useRef(false);

  const invitationId = routeParams?.id;

  useEffect(() => {
    if (!ready || !token || !invitationId) return;
    let cancelled = false;

    import("html5-qrcode").then(({ Html5QrcodeScanner }) => {
      if (cancelled) return;
      const scanner = new Html5QrcodeScanner("qr-reader", { fps: 10, qrbox: 240 }, false);
      scanner.render(
        async (decoded) => {
          if (busyRef.current) return;
          busyRef.current = true;
          try {
            // Dashboard QR codes carry the guest ID; the guest's own invitation shows "rawuh:<invitation token>".
            let guestId = decoded.trim();
            if (guestId.startsWith("rawuh:")) {
              const guestToken = guestId.slice("rawuh:".length);
              const list = await apiFetch(`/api/invitations/${invitationId}/guests`, token).then(r => r.json()) as { items?: Array<{ id: string; token?: string }> } | Array<{ id: string; token?: string }>;
              const guests = Array.isArray(list) ? list : list.items ?? [];
              const match = guests.find(guest => guest.token === guestToken);
              if (!match) throw new Error("QR tidak dikenali untuk undangan ini.");
              guestId = match.id;
            }
            const response = await apiFetch(`/api/invitations/${invitationId}/guests/${encodeURIComponent(guestId)}/check-in`, token, { method: "POST" });
            const body = await response.json();
            if (!response.ok) throw new Error(body.error ?? "Check-in gagal");
            setChecked({ id: body.id, name: body.name });
            setGift({ kind: "cash", amount: "", item: "" });
            setSaved("");
            setResult({ kind: "success", message: `${body.name} berhasil check-in.${body.table ? ` Arahkan ke ${/^\d/.test(body.table) ? `meja ${body.table}` : body.table}.` : ""}` });
          } catch (err) {
            setResult({ kind: "error", message: err instanceof Error ? err.message : "Check-in gagal" });
          } finally {
            setTimeout(() => { busyRef.current = false; }, 1500);
          }
        },
        () => {}
      );
      scannerRef.current = scanner;
      setScanning(true);
    });

    return () => {
      cancelled = true;
      scannerRef.current?.clear().catch(() => {});
    };
  }, [ready, token, invitationId]);

  async function recordGift(event: React.FormEvent) {
    event.preventDefault();
    if (!token || !invitationId || !checked) return;
    setSaving(true);
    try {
      const response = await apiFetch(`/api/invitations/${invitationId}/ledger`, token, {
        method: "POST",
        body: JSON.stringify({ guest_id: checked.id, name: checked.name, kind: gift.kind, amount: Number(gift.amount) || 0, item: gift.item, note: gift.kind === "cash" && !gift.amount ? "Amplop belum dibuka — isi nominal nanti" : "Dicatat saat check-in" }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.error);
      setSaved(`Tercatat di buku buwuh: ${checked.name}.`);
      setChecked(null);
    } catch (err) {
      setSaved(err instanceof Error && err.message ? err.message : "Belum tercatat.");
    } finally {
      setSaving(false);
    }
  }

  if (!ready || !invitationId) return null;

  return (
    <DashboardShell active="checkin" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Undangan</p>
          <h1>Scan check-in</h1>
          <p className="dashboard-subtitle">Arahkan kamera ke kode QR tamu untuk check-in.</p>
        </div>
      </header>

      <div className="checkin-scan">
        <div id="qr-reader" />
        {!scanning && <p className="dashboard-state">Menyalakan kamera...</p>}
        {result && (
          <p className={`checkin-result ${result.kind === "error" ? "error" : ""}`}>{result.message}</p>
        )}
        {checked && (
          <form className="checkin-gift" onSubmit={recordGift} aria-label="Catat amplop atau kado">
            <strong>Catat amplop / kado dari {checked.name}</strong>
            <div>
              <select value={gift.kind} onChange={(e) => setGift({ ...gift, kind: e.target.value })} aria-label="Jenis">
                <option value="cash">Amplop</option>
                <option value="kado">Kado</option>
              </select>
              {gift.kind === "kado"
                ? <input value={gift.item} onChange={(e) => setGift({ ...gift, item: e.target.value })} placeholder="Nama barang" required aria-label="Barang" />
                : <input inputMode="numeric" value={gift.amount} onChange={(e) => setGift({ ...gift, amount: e.target.value.replace(/\D/g, "") })} placeholder="Nominal (kosongkan bila amplop belum dibuka)" aria-label="Nominal" />}
              <button type="submit" className="dashboard-action" disabled={saving}>{saving ? "…" : "Catat"}</button>
              <button type="button" className="table-action" onClick={() => setChecked(null)}>Lewati</button>
            </div>
          </form>
        )}
        {saved && <p className="dashboard-state" role="status">{saved}</p>}
      </div>
    </DashboardShell>
  );
}
