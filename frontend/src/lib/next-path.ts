/**
 * A same-origin relative path from ?next= (e.g. /gabung/abc), or null — never an external URL.
 * Control characters and backslashes are rejected up front because browsers strip/normalise them
 * (`/\tevil.com`, `/\evil.com` would otherwise become protocol-relative `//evil.com`).
 */
export function safeNext(value: string | null | undefined): string | null {
  if (!value || !value.startsWith("/") || /[\x00-\x1f\\]/.test(value)) return null;
  let url: URL;
  try {
    url = new URL(value, "http://x");
  } catch {
    return null;
  }
  if (url.origin !== "http://x") return null;
  const path = `${url.pathname}${url.search}${url.hash}`;
  if (path.startsWith("//")) return null;
  // Encoded tricks ("/%09/evil.com", "/%2F/evil.com", "/%5Cevil.com") turn into the raw forms above once
  // something downstream decodes the path, so check the decoded form with the same rules.
  let decoded: string;
  try {
    decoded = decodeURIComponent(url.pathname);
  } catch {
    return null;
  }
  if (/[\x00-\x1f\\]/.test(decoded) || decoded.startsWith("//")) return null;
  return path;
}
