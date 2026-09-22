"use client";

import { useEffect, useState } from "react";
import QRCode from "qrcode";

// Encodes the internal guest ID, not the public invitation_token — this QR
// is only ever shown to the authenticated owner/staff for venue check-in,
// and the check-in endpoint already re-verifies invitation ownership.
export function GuestQRCode({ guestId }: { guestId: string }) {
  const [dataUrl, setDataUrl] = useState("");

  useEffect(() => {
    QRCode.toDataURL(guestId, { width: 160, margin: 1 })
      .then(setDataUrl)
      .catch(() => {});
  }, [guestId]);

  if (!dataUrl) return null;

  // eslint-disable-next-line @next/next/no-img-element
  return <img src={dataUrl} alt="Guest check-in QR code" width={80} height={80} />;
}
