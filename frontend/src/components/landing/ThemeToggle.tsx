"use client";
// Light / dark switch for the marketing site. The choice lives in localStorage ("rawuh-theme") and on
// <html data-theme>; without a choice the site follows the device (prefers-color-scheme). THEME_SCRIPT runs in
// <head> before paint so a returning dark-mode visitor never sees a white flash.
import { useEffect, useState } from "react";
import { IconMoon, IconSun } from "@/components/brand/icons";
import styles from "@/app/landing.module.css";

const KEY = "rawuh-theme";

export const THEME_SCRIPT = `try{var t=localStorage.getItem("${KEY}");if(t==="dark"||t==="light")document.documentElement.dataset.theme=t}catch(e){}`;

function currentTheme(): "light" | "dark" {
  const stored = document.documentElement.dataset.theme;
  if (stored === "dark" || stored === "light") return stored;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function ThemeToggle({ className }: { className?: string }) {
  const [theme, setTheme] = useState<"light" | "dark" | null>(null);
  useEffect(() => {
    const timer = setTimeout(() => setTheme(currentTheme()), 0);
    const media = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = () => setTheme(currentTheme());
    media.addEventListener("change", onChange);
    return () => { clearTimeout(timer); media.removeEventListener("change", onChange); };
  }, []);

  function toggle() {
    const next = currentTheme() === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem(KEY, next); } catch { /* storage unavailable: the choice lasts this visit */ }
    setTheme(next);
  }

  const dark = theme === "dark";
  return (
    <button type="button" className={`${styles.themeToggle} ${className ?? ""}`} onClick={toggle} aria-pressed={dark}
      aria-label={dark ? "Pakai mode terang" : "Pakai mode gelap"} title={dark ? "Mode terang" : "Mode gelap"}>
      {dark ? <IconSun size={18} /> : <IconMoon size={18} />}
    </button>
  );
}
