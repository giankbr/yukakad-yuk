"use client";

import { useState } from "react";

export function CopyButton({ value }: { value: string }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // clipboard access denied — silently ignore, the value is still visible to copy manually
    }
  }

  return (
    <button type="button" onClick={handleCopy} className="cover-link" style={{ marginTop: ".35rem" }}>
      {copied ? "Copied ✓" : "Copy"}
    </button>
  );
}
