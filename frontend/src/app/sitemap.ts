import type { MetadataRoute } from "next";
import { defaultProducts } from "@/lib/products";
import { themeList } from "@/components/invitation/themes/list";

const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL ?? "https://rawuh.id").replace(/\/+$/, "");

const MARKETING_PAGES: Array<{ path: string; priority: number; changeFrequency: "weekly" | "monthly" | "yearly" }> = [
  { path: "", priority: 1, changeFrequency: "weekly" },
  { path: "/templates", priority: 0.9, changeFrequency: "weekly" },
  { path: "/harga", priority: 0.9, changeFrequency: "monthly" },
  { path: "/fitur", priority: 0.8, changeFrequency: "monthly" },
  { path: "/produk", priority: 0.8, changeFrequency: "monthly" },
  { path: "/tentang", priority: 0.5, changeFrequency: "yearly" },
  { path: "/syarat-ketentuan", priority: 0.2, changeFrequency: "yearly" },
  { path: "/kebijakan-privasi", priority: 0.2, changeFrequency: "yearly" },
];

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    ...MARKETING_PAGES.map(page => ({ url: `${SITE_URL}${page.path}`, changeFrequency: page.changeFrequency, priority: page.priority })),
    ...defaultProducts.map(product => ({ url: `${SITE_URL}/produk/${product.slug}`, changeFrequency: "monthly" as const, priority: 0.7 })),
    ...themeList.map(theme => ({ url: `${SITE_URL}/templates/${theme.id}`, changeFrequency: "monthly" as const, priority: 0.6 })),
  ];
}
