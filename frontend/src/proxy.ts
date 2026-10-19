import { NextResponse, type NextRequest } from "next/server";

/**
 * Security headers for every page (next.config.ts is left untouched on purpose).
 * The CSP only restricts what is safe without nonces: who may frame Rawuh, <base>, plugins and form targets.
 * Scripts/styles stay unrestricted so Next's inline bootstrap and theme fonts keep working.
 */
const CSP = ["frame-ancestors 'self'", "base-uri 'self'", "object-src 'none'", "form-action 'self'"].join("; ");

export function proxy(request: NextRequest) {
  const response = NextResponse.next();
  const headers = response.headers;
  headers.set("Content-Security-Policy", CSP);
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("X-Frame-Options", "SAMEORIGIN");
  // Reset links carry a secret token in the URL: never leak it to other sites.
  headers.set("Referrer-Policy", request.nextUrl.pathname.startsWith("/auth/reset-password") ? "no-referrer" : "strict-origin-when-cross-origin");
  // Camera is needed for the QR check-in scanner; nothing else needs device features.
  headers.set("Permissions-Policy", "camera=(self), microphone=(), geolocation=(), payment=(), usb=()");
  if (request.nextUrl.protocol === "https:") headers.set("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
  return response;
}

export const config = {
  // Skip static assets and image optimisation; they don't need page headers.
  matcher: ["/((?!_next/static|_next/image|favicon.ico|robots.txt|sitemap.xml|.*\\.(?:png|jpg|jpeg|webp|svg|gif|ico|mp3|woff2?)$).*)"],
};
