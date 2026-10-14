"use client";

import { useEffect, useRef, useState } from "react";
import { autoReveal } from "@/lib/reveal";

/** Scroll reveal for marketing pages: staggers every section's content in as it enters the viewport. */
export function MotionInit({ root = "#konten" }: { root?: string }) {
  useEffect(() => {
    const element = document.querySelector<HTMLElement>(root);
    if (!element) return;
    // Wait a frame so layout (fonts, images with fixed sizes) has settled.
    let cleanup = () => undefined as void;
    const frame = requestAnimationFrame(() => { cleanup = autoReveal(element); });
    return () => { cancelAnimationFrame(frame); cleanup(); };
  }, [root]);
  return null;
}

/** Counts the leading number of a stat ("120rb+", "4.9/5", "10 mnt") up from 0 when it scrolls into view. */
export function CountUp({ value, duration = 1400 }: { value: string; duration?: number }) {
  const match = value.match(/^(\d+(?:[.,]\d+)?)(.*)$/);
  const ref = useRef<HTMLSpanElement>(null);
  const [display, setDisplay] = useState(value);
  useEffect(() => {
    if (!match || !ref.current) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const [, raw, suffix] = match;
    const decimals = raw.includes(".") || raw.includes(",") ? raw.split(/[.,]/)[1].length : 0;
    const separator = raw.includes(",") ? "," : ".";
    const target = Number(raw.replace(",", "."));
    const format = (n: number) => n.toFixed(decimals).replace(".", separator) + suffix;
    let frame = 0;
    const observer = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return;
      observer.disconnect();
      const start = performance.now();
      const tick = (now: number) => {
        const t = Math.min(1, (now - start) / duration);
        const eased = 1 - Math.pow(1 - t, 3);
        setDisplay(format(target * eased));
        if (t < 1) frame = requestAnimationFrame(tick);
      };
      frame = requestAnimationFrame(tick);
    }, { threshold: 0.4 });
    observer.observe(ref.current);
    return () => { observer.disconnect(); cancelAnimationFrame(frame); };
    // eslint-disable-next-line react-hooks/exhaustive-deps -- value drives everything
  }, [value, duration]);
  return <span ref={ref} aria-label={value}><span aria-hidden>{display}</span></span>;
}
