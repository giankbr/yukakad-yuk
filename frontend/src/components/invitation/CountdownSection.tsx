"use client";

import { useEffect, useState } from "react";
import type { InvitationData } from "./types";

function timeLeft(target: number) {
  const diff = Math.max(0, target - Date.now());
  return {
    days: Math.floor(diff / 86400000),
    hours: Math.floor((diff / 3600000) % 24),
    minutes: Math.floor((diff / 60000) % 60),
    seconds: Math.floor((diff / 1000) % 60),
  };
}

export function CountdownSection({ data }: { data: InvitationData }) {
  const targetDate = data.events[0]?.date ?? data.date;
  const target = Date.parse(targetDate);
  const [remaining, setRemaining] = useState<ReturnType<typeof timeLeft> | null>(null);

  useEffect(() => {
    if (Number.isNaN(target)) return;
    // Set on mount rather than in the initializer to avoid an SSR/client
    // hydration mismatch, since "now" differs between render and mount.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setRemaining(timeLeft(target));
    const id = setInterval(() => setRemaining(timeLeft(target)), 1000);
    return () => clearInterval(id);
  }, [target]);

  if (Number.isNaN(target) || !remaining) return null;

  return (
    <section className="invitation-section countdown-section" aria-labelledby="countdown-title">
      <p className="section-label">Counting the days</p>
      <h2 id="countdown-title">Almost there.</h2>
      <div style={{ display: "flex", gap: "1.5rem", marginTop: "1.5rem", flexWrap: "wrap" }}>
        {(["days", "hours", "minutes", "seconds"] as const).map((unit) => (
          <div key={unit} style={{ textAlign: "center" }}>
            <strong style={{ display: "block", fontFamily: "var(--font-cormorant), serif", fontSize: "2.5rem", color: "var(--accent)" }}>
              {remaining[unit]}
            </strong>
            <span style={{ fontSize: ".75rem", textTransform: "uppercase", letterSpacing: ".06em", color: "var(--muted)" }}>{unit}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
