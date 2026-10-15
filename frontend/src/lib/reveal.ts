/**
 * Automatic scroll-reveal for long pages (landing + invitation themes).
 *
 * Finds top-level blocks (section / footer / article) inside `root`, descends through single-child wrappers,
 * and staggers the block's items in as they enter the viewport. Uses the independent CSS `translate`
 * property via a keyframe animation (see globals.css `[data-reveal]`), so it never fights a component's own
 * `transform` or `transition`. Elements that already run their own animation, fixed/sticky bars and anything
 * marked `data-noreveal` are left alone. No-op under prefers-reduced-motion.
 */
const BLOCKS = "section, footer, article, [data-reveal-block]";

function isSkippable(element: HTMLElement) {
  if (element.closest("[data-noreveal]")) return true;
  const style = getComputedStyle(element);
  if (style.position === "fixed" || style.position === "sticky") return true;
  if (style.display === "none" || style.visibility === "hidden") return true;
  if (style.animationName && style.animationName !== "none") return true;
  return false;
}

const MEDIA = new Set(["IMG", "PICTURE", "VIDEO", "FIGURE", "IFRAME", "CANVAS"]);

/** Reveal flavour: images settle in, headings blur/pop in, everything else rises (see globals.css). */
function variantOf(item: HTMLElement): string {
  if (getComputedStyle(item).position === "absolute") return "fade";
  if (MEDIA.has(item.tagName)) return "media";
  if (/^H[1-3]$/.test(item.tagName)) return "title";
  const text = item.textContent?.trim() ?? "";
  if (!text && item.querySelector("img, video, picture")) return "media";
  const first = item.firstElementChild;
  if (first && /^H[1-3]$/.test(first.tagName) && item.children.length <= 2 && text.length < 90) return "title";
  return "";
}

function itemsOf(block: HTMLElement, depth = 0): HTMLElement[] {
  let container: HTMLElement = block;
  for (let i = 0; i < 3; i++) {
    const kids = Array.from(container.children).filter((el): el is HTMLElement => el instanceof HTMLElement);
    if (kids.length !== 1) break;
    container = kids[0];
  }
  const kids = Array.from(container.children).filter((el): el is HTMLElement => el instanceof HTMLElement);
  if (!kids.length) return [block];
  // Very tall items (long chat lists, whole-page wrappers) are split into their own children.
  const tall = window.innerHeight * 1.2;
  return kids.flatMap(kid => (depth < 3 && kid.offsetHeight > tall && kid.children.length > 1 && !isSkippable(kid)) ? itemsOf(kid, depth + 1) : [kid]);
}

export function autoReveal(root: HTMLElement, { stagger = 70, maxStagger = 6 }: { stagger?: number; maxStagger?: number } = {}) {
  if (typeof window === "undefined" || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return () => undefined;
  if (!("IntersectionObserver" in window)) return () => undefined;

  const all = Array.from(root.querySelectorAll<HTMLElement>(BLOCKS));
  let blocks = all.filter(block => !all.some(other => other !== block && other.contains(block)) && !isSkippable(block));
  // Pages built without section/article blocks (e.g. chat-style themes): reveal the root's own items.
  if (blocks.length === 0) blocks = [root];
  const targets: HTMLElement[] = [];
  for (const block of blocks) {
    itemsOf(block).forEach((item, index) => {
      if (item.hasAttribute("data-reveal") || isSkippable(item) || item.offsetHeight === 0) return;
      item.setAttribute("data-reveal", variantOf(item));
      item.style.setProperty("--rd", `${Math.min(index, maxStagger) * stagger}ms`);
      targets.push(item);
    });
  }

  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      // Reveal when visible, or when it's already above the viewport (anchor jumps).
      if (entry.isIntersecting || entry.boundingClientRect.bottom < 0) {
        (entry.target as HTMLElement).setAttribute("data-revealed", "");
        observer.unobserve(entry.target);
      }
    }
  }, { rootMargin: "0px 0px -6% 0px", threshold: 0.08 });
  targets.forEach(target => observer.observe(target));

  return () => {
    observer.disconnect();
    targets.forEach(target => { target.removeAttribute("data-reveal"); target.removeAttribute("data-revealed"); });
  };
}

/** Stagger the direct children of `container` in right away (used for invitation covers). */
export function revealChildren(container: HTMLElement, { stagger = 90, delay = 120 }: { stagger?: number; delay?: number } = {}) {
  if (typeof window === "undefined" || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  let index = 0;
  for (const child of Array.from(container.children)) {
    if (!(child instanceof HTMLElement) || isSkippable(child)) continue;
    const position = getComputedStyle(child).position;
    child.setAttribute("data-reveal", position === "absolute" || position === "fixed" ? "fade" : "");
    child.style.setProperty("--rd", `${delay + Math.min(index, 8) * stagger}ms`);
    index += 1;
  }
  requestAnimationFrame(() => container.querySelectorAll(":scope > [data-reveal]").forEach(el => el.setAttribute("data-revealed", "")));
}
