/** A same-site path from ?next= (e.g. /gabung/abc), or null — never an external URL. */
export function safeNext(value: string | null | undefined): string | null {
  if (!value || !value.startsWith("/") || value.startsWith("//") || value.startsWith("/\\")) return null;
  return value;
}
