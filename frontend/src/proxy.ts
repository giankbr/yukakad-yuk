import { NextResponse, type NextRequest } from "next/server";

/**
 * 1. Security headers for every page (next.config.ts is left untouched on purpose). The CSP only restricts
 *    what is safe without nonces: who may frame Rawuh, <base>, plugins and form targets.
 * 2. Couples' own domains: a request whose Host isn't one of Rawuh's hosts shows that couple's invitation
 *    (`/` is rewritten to `/domain/<host>`); any other path there is sent to the main site.
 */
const CSP = ["frame-ancestors 'self'", "base-uri 'self'", "object-src 'none'", "form-action 'self'"].join("; ");

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://rawuh.id";

/** Rawuh's own hostnames: the site URL (+ www), APP_HOSTS (comma separated) and local development hosts. */
function appHosts() {
  const hosts = new Set(["localhost", "127.0.0.1", "[::1]"]);
  try {
    const site = new URL(SITE_URL).hostname;
    hosts.add(site);
    hosts.add(site.startsWith("www.") ? site.slice(4) : `www.${site}`);
  } catch { /* invalid NEXT_PUBLIC_SITE_URL: only local hosts */ }
  for (const host of (process.env.APP_HOSTS ?? "").split(",")) if (host.trim()) hosts.add(host.trim().toLowerCase());
  return hosts;
}
const APP_HOSTS = appHosts();

function isAppHost(host: string) {
  return APP_HOSTS.has(host) || host.endsWith(".localhost") || /^\d+\.\d+\.\d+\.\d+$/.test(host);
}

function withHeaders(response: NextResponse, request: NextRequest) {
  const headers = response.headers;
  headers.set("Content-Security-Policy", CSP);
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("X-Frame-Options", "SAMEORIGIN");
  // Reset links carry a secret token in the URL: never leak it to other sites.
  headers.set("Referrer-Policy", request.nextUrl.pathname.startsWith("/auth/reset-password") ? "no-referrer" : "strict-origin-when-cross-origin");
  // Camera is needed for the QR check-in scanner; nothing else needs device features.
  headers.set("Permissions-Policy", "camera=(self), microphone=(), geolocation=(), payment=(), usb=()");
  if (request.nextUrl.protocol === "https:" || request.headers.get("x-forwarded-proto") === "https") {
    headers.set("Strict-Transport-Security", "max-age=31536000");
  }
  return response;
}

export function proxy(request: NextRequest) {
  const host = (request.headers.get("x-forwarded-host") ?? request.headers.get("host") ?? "").split(",")[0].trim().toLowerCase().replace(/:\d+$/, "");
  if (host && !isAppHost(host)) {
    const { pathname } = request.nextUrl;
    if (pathname === "/") {
      const url = request.nextUrl.clone();
      url.pathname = `/domain/${encodeURIComponent(host)}`;
      return withHeaders(NextResponse.rewrite(url), request);
    }
    // Next's own internals keep working on the custom domain; everything else lives on the main site.
    if (!pathname.startsWith("/domain/") && !pathname.startsWith("/_next/")) {
      return NextResponse.redirect(new URL(pathname + request.nextUrl.search, SITE_URL), 308);
    }
  }
  return withHeaders(NextResponse.next(), request);
}

export const config = {
  // Skip static assets and image optimisation; they don't need page headers or domain routing.
  matcher: ["/((?!_next/static|_next/image|favicon.ico|robots.txt|sitemap.xml|.*\\.(?:png|jpg|jpeg|webp|svg|gif|ico|mp3|woff2?|css|js|json|txt)$).*)"],
};
