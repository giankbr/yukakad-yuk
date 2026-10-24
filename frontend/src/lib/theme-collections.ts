// Theme collections (the gallery's first filter level) and the "variety" order every theme list uses.
// Plain module (no "use client") so server pages and client components share it.

export const COLLECTIONS = [
  { id: "pernikahan", label: "Pernikahan" },
  { id: "adat", label: "Adat Nusantara" },
  { id: "islami", label: "Islami & Syari" },
  { id: "unik", label: "Kekinian" },
  { id: "acara", label: "Acara lain" },
] as const;
export type CollectionId = (typeof COLLECTIONS)[number]["id"];

const UNIK = new Set(["Aplikasi", "Hiburan", "Sosial Media", "Perjalanan", "Keuangan", "Belanja", "Unik", "Retro"]);

export function collectionOf(category: string, eventType?: string): CollectionId {
  if (eventType && eventType !== "wedding") return "acara";
  if (category.startsWith("Adat ") || category === "Peranakan") return "adat";
  if (category === "Islami" || category === "Syari") return "islami";
  if (UNIK.has(category)) return "unik";
  return "pernikahan";
}

// How collections take turns: weddings lead, adat and islami follow closely, then other events and the app-style ones.
const RHYTHM: CollectionId[] = ["pernikahan", "adat", "islami", "pernikahan", "acara", "adat", "unik", "islami", "pernikahan", "acara"];

/** Takes one item from each list in turn until all are empty. */
function roundRobin<T>(lists: T[][]): T[] {
  const queues = lists.map(list => [...list]);
  const out: T[] = [];
  while (queues.some(queue => queue.length)) for (const queue of queues) if (queue.length) out.push(queue.shift()!);
  return out;
}

/**
 * Orders themes so any page of the gallery looks varied: collections alternate following RHYTHM, and inside a
 * collection its categories take turns (Jawa, Minang, Bali, … rather than all Jawa first). Within a category the
 * newest theme (highest position in the input, which comes sorted by sort_order) goes first.
 */
export function varietyOrder<T>(items: T[], meta: (item: T) => { category: string; eventType?: string }): T[] {
  const byCollection = new Map<CollectionId, Map<string, T[]>>();
  for (const item of [...items].reverse()) {
    const { category, eventType } = meta(item);
    const collection = collectionOf(category, eventType);
    const categories = byCollection.get(collection) ?? new Map<string, T[]>();
    byCollection.set(collection, categories);
    categories.set(category, [...(categories.get(category) ?? []), item]);
  }
  const queues = new Map<CollectionId, T[]>();
  for (const [collection, categories] of byCollection) queues.set(collection, roundRobin([...categories.values()]));
  const out: T[] = [];
  while (out.length < items.length) {
    let took = false;
    for (const collection of RHYTHM) {
      const next = queues.get(collection)?.shift();
      if (next !== undefined) { out.push(next); took = true; }
    }
    if (!took) break;
  }
  return out;
}
