// A couple's own domain (e.g. rinadanbima.com). src/proxy.ts rewrites `/` on any non-Rawuh host to
// /domain/<host>; this page resolves the verified domain to its invitation and renders it like /invitation/<slug>.
import type { Metadata } from "next";
import { headers } from "next/headers";
import { notFound } from "next/navigation";
import PublicInvitationPage, { generateMetadata as invitationMetadata } from "../../invitation/[slug]/page";
import { getDomainSlug } from "../../invitation/[slug]/data";

type Props = { params: Promise<{ host: string }>; searchParams: Promise<Record<string, string | string[] | undefined>> };

/** Only serve the domain the guest actually visited (so rawuh.id/domain/<x> can't mirror someone's invitation). */
async function resolve(params: Props["params"]) {
  const host = decodeURIComponent((await params).host).toLowerCase();
  const list = await headers();
  const visited = (list.get("x-forwarded-host") ?? list.get("host") ?? "").split(",")[0].trim().toLowerCase().replace(/:\d+$/, "");
  if (visited !== host) notFound();
  return { host, slug: await getDomainSlug(host) };
}

export async function generateMetadata({ params, searchParams }: Props): Promise<Metadata> {
  const { host, slug } = await resolve(params);
  const metadata = await invitationMetadata({ params: Promise.resolve({ slug }), searchParams });
  const url = `https://${host}/`;
  return { ...metadata, alternates: { canonical: url }, openGraph: { ...metadata.openGraph, url } };
}

export default async function CustomDomainPage({ params, searchParams }: Props) {
  const { slug } = await resolve(params);
  return <PublicInvitationPage params={Promise.resolve({ slug })} searchParams={searchParams} />;
}
