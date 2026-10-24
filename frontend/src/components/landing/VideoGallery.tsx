"use client";
// Grid of example videos: each plays muted while it's on screen and pauses when it isn't; "Suara" turns the sound
// on for one video at a time. Reduced-motion visitors get posters and start a video themselves.
import { useEffect, useRef, useState } from "react";
import { IconPause, IconPlay, IconSpeaker, IconSpeakerOff } from "@/components/brand/icons";
import styles from "@/app/marketing-pages.module.css";

export type GalleryVideo = { slug: string; title: string; note: string };

const SOUND_EVENT = "rawuh:gallery-sound";

function Tile({ video, base }: { video: GalleryVideo; base: string }) {
  const ref = useRef<HTMLVideoElement>(null);
  const [playing, setPlaying] = useState(false);
  const [muted, setMuted] = useState(true);
  const [broken, setBroken] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    const failed = setTimeout(() => { if (element.error || element.networkState === HTMLMediaElement.NETWORK_NO_SOURCE) setBroken(true); }, 0);
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const observer = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) element.pause();
      else if (!reduce && element.muted) void element.play().catch(() => undefined);
    }, { threshold: 0.5 });
    observer.observe(element);
    // Only one tile plays with sound: the others go quiet when one is unmuted.
    const onSound = (event: Event) => {
      if ((event as CustomEvent<string>).detail !== video.slug && !element.muted) { element.muted = true; setMuted(true); }
    };
    window.addEventListener(SOUND_EVENT, onSound);
    return () => { clearTimeout(failed); observer.disconnect(); window.removeEventListener(SOUND_EVENT, onSound); };
  }, [video.slug]);

  function toggleSound() {
    const element = ref.current;
    if (!element) return;
    element.muted = !element.muted;
    setMuted(element.muted);
    if (!element.muted) {
      window.dispatchEvent(new CustomEvent(SOUND_EVENT, { detail: video.slug }));
      if (element.paused) void element.play().catch(() => undefined);
    }
  }
  function togglePlay() {
    const element = ref.current;
    if (!element) return;
    if (element.paused) void element.play().catch(() => undefined);
    else element.pause();
  }

  if (broken) return null;
  return (
    <figure className={styles.videoTile}>
      <div className={styles.videoTileFrame}>
        <video ref={ref} src={`${base}/${video.slug}.mp4`} poster={`${base}/${video.slug}-poster.webp`} muted loop playsInline preload="none"
          aria-label={`Contoh video ${video.title}`} onPlay={() => setPlaying(true)} onPause={() => setPlaying(false)} onError={() => setBroken(true)} />
        <div className={styles.phoneVideoControls}>
          <button type="button" onClick={togglePlay} aria-label={playing ? `Jeda ${video.title}` : `Putar ${video.title}`}>
            {playing ? <IconPause size={16} weight="fill" /> : <IconPlay size={16} weight="fill" />}
          </button>
          <button type="button" onClick={toggleSound} aria-pressed={!muted} aria-label={muted ? `Nyalakan suara ${video.title}` : `Matikan suara ${video.title}`}>
            {muted ? <IconSpeakerOff size={16} /> : <IconSpeaker size={16} />}
            <span>{muted ? "Suara" : "Bersuara"}</span>
          </button>
        </div>
      </div>
      <figcaption><strong>{video.title}</strong><small>{video.note}</small></figcaption>
    </figure>
  );
}

export function VideoGallery({ videos, base = "/rawuh/video-contoh" }: { videos: GalleryVideo[]; base?: string }) {
  return <div className={styles.videoGrid}>{videos.map(video => <Tile key={video.slug} video={video} base={base} />)}</div>;
}
