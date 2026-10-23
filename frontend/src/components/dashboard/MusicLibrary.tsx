"use client";

import { useEffect, useRef, useState } from "react";
import { Pause as PhPause, Play as PhPlay } from "@phosphor-icons/react/ssr";
import type { Mood } from "@/components/invitation/themes/mood";
import { MUSIC_LIBRARY, type LibraryTrack } from "@/lib/music-library";
import styles from "@/app/dashboard/invitations/[id]/settings/settings.module.css";

/** Built-in tracks: listen to a preview, then "Pakai" stores the track as the invitation's music. */
export function MusicLibrary({ current, recommended, disabled, onPick }: {
  current?: string; recommended?: Mood; disabled?: boolean; onPick: (track: LibraryTrack) => void;
}) {
  const audio = useRef<HTMLAudioElement | null>(null);
  const [playing, setPlaying] = useState("");
  const [showAll, setShowAll] = useState(false);

  useEffect(() => () => { audio.current?.pause(); audio.current = null; }, []);

  function preview(track: LibraryTrack) {
    if (playing === track.id) { audio.current?.pause(); setPlaying(""); return; }
    audio.current?.pause();
    const element = new Audio(track.file);
    element.onended = () => setPlaying("");
    element.onerror = () => setPlaying("");
    audio.current = element;
    setPlaying(track.id);
    void element.play().catch(() => setPlaying(""));
  }

  // Tracks that suit the invitation's theme come first; the rest wait behind "Lihat semua" (plus the one in use).
  const sorted = recommended ? [...MUSIC_LIBRARY].sort((a, b) => Number(b.mood === recommended) - Number(a.mood === recommended)) : MUSIC_LIBRARY;
  const collapsed = Boolean(recommended) && !showAll;
  const tracks = collapsed ? sorted.filter(track => track.mood === recommended || track.file === current) : sorted;

  return <>
    <div className={styles.library} role="list" aria-label="Lagu bawaan Rawuh">
      {tracks.map(track => {
        const active = current === track.file;
        return (
          <div key={track.id} role="listitem" className={styles.libraryItem} data-active={active || undefined}>
            <button type="button" className={styles.playButton} onClick={() => preview(track)} aria-pressed={playing === track.id}
              aria-label={playing === track.id ? `Jeda ${track.title}` : `Dengarkan ${track.title}`}>
              {playing === track.id ? <PhPause size={16} weight="fill" /> : <PhPlay size={16} weight="fill" />}
            </button>
            <div className={styles.libraryText}>
              <strong>
                {track.title}
                {track.mood === recommended && <span className={styles.badge}>Cocok untuk tema ini</span>}
              </strong>
              <small>{track.note}{track.credit ? ` · ${track.credit}` : ""}</small>
            </div>
            {active
              ? <span className={styles.inUse}>Dipakai</span>
              : <button type="button" className={styles.ghost} disabled={disabled} onClick={() => onPick(track)}>Pakai</button>}
          </div>
        );
      })}
    </div>
    {recommended && (
      <button type="button" className={styles.ghost} style={{ justifySelf: "start" }} onClick={() => setShowAll(open => !open)} aria-expanded={showAll}>
        {showAll ? "Tampilkan yang cocok saja" : `Lihat semua lagu (${MUSIC_LIBRARY.length})`}
      </button>
    )}
  </>;
}
