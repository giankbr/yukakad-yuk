"use client";

import { useEffect, useRef, useState } from "react";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { apiFetch } from "@/lib/api";
import { useAuthToken, useRouteParams } from "@/lib/useAuthToken";

type Result = { kind: "success" | "error"; message: string } | null;

export default function CheckInPage({ params }: { params: Promise<{ id: string }> }) {
  const routeParams = useRouteParams(params);
  const { token, ready } = useAuthToken();
  const [result, setResult] = useState<Result>(null);
  const [scanning, setScanning] = useState(false);
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
        async (decodedGuestId) => {
          if (busyRef.current) return;
          busyRef.current = true;
          try {
            const response = await apiFetch(`/api/invitations/${invitationId}/guests/${decodedGuestId}/check-in`, token, { method: "POST" });
            const body = await response.json();
            if (!response.ok) throw new Error(body.error ?? "Check-in failed");
            setResult({ kind: "success", message: `${body.name} checked in.` });
          } catch (err) {
            setResult({ kind: "error", message: err instanceof Error ? err.message : "Check-in failed" });
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

  if (!ready || !invitationId) return null;

  return (
    <DashboardShell active="checkin" invitationId={invitationId}>
      <header className="dashboard-header">
        <div>
          <p className="dashboard-kicker">Invitation</p>
          <h1>Check-in scan</h1>
          <p className="dashboard-subtitle">Point the camera at a guest&apos;s QR code to check them in.</p>
        </div>
      </header>

      <div className="checkin-scan">
        <div id="qr-reader" />
        {!scanning && <p className="dashboard-state">Starting camera...</p>}
        {result && (
          <p className={`checkin-result ${result.kind === "error" ? "error" : ""}`}>{result.message}</p>
        )}
      </div>
    </DashboardShell>
  );
}
