"use client";
// One background-music player per page. A theme's own music button (ThemeBody, Jawa, …) and the page's generic
// <MusicPlayer> both call useMusic(); they share this single <audio> element, so the track never plays twice and the
// generic button hides itself whenever the theme renders its own.
import { useEffect, useSyncExternalStore } from "react";
import type { InvitationData } from "../types";

export const OPEN_EVENT = "rawuh:invitation-open";

export type MusicSource = InvitationData["music"];
type State = {
  playing: boolean;
  /** The track couldn't be loaded or played (broken link, unsupported format). */
  failed: boolean;
  /** The cover was opened (or there is none), so the toggle may show. */
  opened: boolean;
  /** Theme-rendered players currently mounted (the generic one doesn't count). */
  owners: number;
  title?: string;
  bpm?: number;
  /** Bumps when playback starts for the first time, so <MusicChip> can announce the track. */
  announced: number;
};

const initial: State = { playing: false, failed: false, opened: false, owners: 0, announced: 0 };
let state = initial;
const listeners = new Set<() => void>();
function set(patch: Partial<State>) {
  state = { ...state, ...patch };
  for (const listener of listeners) listener();
}

let audio: HTMLAudioElement | null = null;
let source = "";
let autoplay = false;
let users = 0;
let everPlayed = false;
let timer: ReturnType<typeof setTimeout> | undefined;

const onPlay = () => {
  set({ playing: true, ...(everPlayed ? {} : { announced: Date.now() }) });
  everPlayed = true;
};
const onPause = () => set({ playing: false });
const onError = () => set({ failed: true, playing: false });
const onOpen = () => {
  set({ opened: true });
  if (autoplay && audio) void audio.play().catch(playFailed);
};

/** `play()` rejection: autoplay blocks (NotAllowedError) and interrupted loads (AbortError) aren't failures. */
function playFailed(error: unknown) {
  const name = error instanceof DOMException ? error.name : "";
  if (name !== "NotAllowedError" && name !== "AbortError") onError();
}

function teardown() {
  clearTimeout(timer);
  window.removeEventListener(OPEN_EVENT, onOpen);
  if (audio) {
    audio.pause();
    audio.removeEventListener("play", onPlay);
    audio.removeEventListener("pause", onPause);
    audio.removeEventListener("error", onError);
  }
  audio = null;
  source = "";
  everPlayed = false;
  document.documentElement.style.removeProperty("--music-beat");
  set({ ...initial, owners: state.owners });
}

function attach(url: string, music: NonNullable<MusicSource>) {
  autoplay = Boolean(music.autoplay);
  if (url === source) return;
  if (audio) teardown();
  source = url;
  audio = new Audio(url);
  audio.loop = true;
  audio.preload = "none";
  audio.addEventListener("play", onPlay);
  audio.addEventListener("pause", onPause);
  audio.addEventListener("error", onError);
  window.addEventListener(OPEN_EVENT, onOpen);
  // The pulse on the music button follows the track's tempo when it's known (demo tracks), else a calm default.
  document.documentElement.style.setProperty("--music-beat", `${(60 / (music.bpm || 66)).toFixed(3)}s`);
  set({ failed: false, playing: false, opened: false, title: music.title, bpm: music.bpm });
  // Rendered without a cover (?open=1): show the toggle straight away.
  timer = setTimeout(() => { if (!document.querySelector('[aria-label="Sampul undangan"]')) set({ opened: true }); }, 600);
}

export function safeMusicUrl(url?: string) {
  if (!url) return undefined;
  if (url.startsWith("/") && !url.startsWith("//")) return url;
  try {
    const parsed = new URL(url);
    return parsed.protocol === "https:" || parsed.protocol === "http:" ? parsed.href : undefined;
  } catch {
    return undefined;
  }
}

const subscribe = (listener: () => void) => { listeners.add(listener); return () => { listeners.delete(listener); }; };
const snapshot = () => state;
const serverSnapshot = () => initial;

export function useMusicState() {
  return useSyncExternalStore(subscribe, snapshot, serverSnapshot);
}

/** Background music from the dashboard (Pengaturan → musik): starts when the cover is opened if autoplay is on. */
export function useMusic(music?: MusicSource, { generic = false }: { generic?: boolean } = {}) {
  const current = useMusicState();
  const url = safeMusicUrl(music?.url);
  useEffect(() => {
    if (!url || !music) return;
    users += 1;
    if (!generic) set({ owners: state.owners + 1 });
    attach(url, music);
    return () => {
      users -= 1;
      if (!generic) set({ owners: Math.max(0, state.owners - 1) });
      if (users === 0) teardown();
    };
    // `music` is a fresh object on every render; the track is identified by its url.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url, generic, music?.autoplay, music?.title, music?.bpm]);
  const toggle = () => {
    if (!audio) return;
    if (audio.paused) void audio.play().catch(playFailed);
    else audio.pause();
  };
  const playing = current.playing && !current.failed;
  return {
    available: Boolean(url),
    visible: Boolean(url) && current.opened,
    playing,
    failed: current.failed,
    toggle,
    /** True when a theme renders its own player (the generic floating button then stays hidden). */
    ownedByTheme: current.owners > 0,
    /** Spread on the music button: drives the beat pulse in globals.css. */
    attrs: { "data-music-btn": "", "data-playing": playing ? "" : undefined },
  };
}
