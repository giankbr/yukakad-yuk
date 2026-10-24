"use client";
// Example video for a product page, in a phone frame: plays muted and loops; the visitor can turn the sound on.
// Visitors who prefer reduced motion get the poster with a play button instead of autoplay.
import { useEffect, useRef, useState } from "react";
import { IconPause, IconPlay, IconSpeaker, IconSpeakerOff } from "@/components/brand/icons";
import styles from "@/app/marketing-pages.module.css";

export function ProductVideo({ src, poster, label }: { src: string; poster: string; label: string }) {
  const video = useRef<HTMLVideoElement>(null);
  const [muted, setMuted] = useState(true);
  const [playing, setPlaying] = useState(false);
  /** The file is missing or can't play: show the product photo alone instead of an empty phone. */
  const [broken, setBroken] = useState(false);

  useEffect(() => {
    const element = video.current;
    if (!element) return;
    // The load may have failed before hydration, when onError wasn't attached yet.
    const timer = setTimeout(() => { if (element.error || element.networkState === HTMLMediaElement.NETWORK_NO_SOURCE) setBroken(true); }, 0);
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) void element.play().catch(() => undefined);
    return () => clearTimeout(timer);
  }, []);

  function toggleSound() {
    const element = video.current;
    if (!element) return;
    element.muted = !element.muted;
    setMuted(element.muted);
    if (element.paused) void element.play().catch(() => undefined);
  }
  function togglePlay() {
    const element = video.current;
    if (!element) return;
    if (element.paused) void element.play().catch(() => undefined);
    else element.pause();
  }

  if (broken) return null;
  return (
    <div className={styles.phoneVideo}>
      <video ref={video} src={src} poster={poster} muted loop playsInline preload="metadata" aria-label={label}
        onPlay={() => setPlaying(true)} onPause={() => setPlaying(false)} onError={() => setBroken(true)} />
      <div className={styles.phoneVideoControls}>
        <button type="button" onClick={togglePlay} aria-label={playing ? "Jeda video" : "Putar video"}>
          {playing ? <IconPause size={16} weight="fill" /> : <IconPlay size={16} weight="fill" />}
        </button>
        <button type="button" onClick={toggleSound} aria-pressed={!muted} aria-label={muted ? "Nyalakan suara" : "Matikan suara"}>
          {muted ? <IconSpeakerOff size={16} /> : <IconSpeaker size={16} />}
          <span>{muted ? "Suara" : "Bersuara"}</span>
        </button>
      </div>
    </div>
  );
}
