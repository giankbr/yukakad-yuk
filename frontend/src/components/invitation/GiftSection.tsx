import { CopyButton } from "@/components/ui/CopyButton";
import type { InvitationData } from "./types";

export function GiftSection({ data }: { data: InvitationData }) {
  if (data.gifts.length === 0) return null;

  return (
    <section className="invitation-section gift-section" aria-labelledby="gift-title">
      <div>
        <p className="section-label">A practical little note</p>
        <h2 id="gift-title">Your presence is enough. Truly.</h2>
        <p>If you would like to send something, here are a few ways.</p>
      </div>
      <div style={{ display: "grid", gap: "1.5rem" }}>
        {data.gifts.map((gift) => (
          <div className="gift-details" key={gift.id}>
            {gift.type === "bank" && (
              <>
                <span>{gift.bank_name}</span>
                <strong>{gift.account_number}</strong>
                <small>under {gift.account_name}</small>
                {gift.account_number && <CopyButton value={gift.account_number} />}
              </>
            )}
            {gift.type === "ewallet" && (
              <>
                <span style={{ textTransform: "capitalize" }}>{gift.ewallet_provider}</span>
                <strong>{gift.ewallet_number}</strong>
                {gift.ewallet_number && <CopyButton value={gift.ewallet_number} />}
              </>
            )}
            {gift.type === "qris" && gift.qris_image_url && (
              <>
                <span>Scan QRIS</span>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={gift.qris_image_url} alt="QRIS code" style={{ maxWidth: "14rem", marginTop: ".6rem" }} />
              </>
            )}
            {gift.type === "address" && (
              <>
                <span>Send a gift to</span>
                <strong style={{ fontSize: "1.1rem" }}>{gift.address}</strong>
              </>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
