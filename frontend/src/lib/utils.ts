/** Joins class names, filtering out falsy values. Shadcn-style cn() utility. */
export function cn(...classes: (string | undefined | false | null)[]): string {
  return classes.filter(Boolean).join(' ');
}
