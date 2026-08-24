import type { Property } from "@/lib/types";

type AddressProperty = Pick<Property, "address_full" | "address_line" | "ward" | "district" | "province">;

function normalizePart(value: string): string {
  return value.toLocaleLowerCase("vi-VN").replace(/[.,]/g, " ").replace(/\s+/g, " ").trim();
}

export function formatPropertyAddress(property: AddressProperty): string {
  if (property.address_full?.trim()) return property.address_full.trim();

  const parts: string[] = [];
  for (const rawPart of [property.address_line, property.ward, property.district, property.province]) {
    const part = rawPart?.trim();
    if (!part) continue;
    const normalized = normalizePart(part);
    const alreadyIncluded = parts.some((existing) => {
      const normalizedExisting = normalizePart(existing);
      return normalizedExisting.includes(normalized) || normalized.includes(normalizedExisting);
    });
    if (!alreadyIncluded) parts.push(part);
  }
  return parts.join(", ") || "Đang cập nhật địa chỉ";
}

export function formatPropertyTitle(title?: string | null): string {
  if (!title) return "Căn hộ bất động sản";
  let clean = title.trim();

  // Remove common junk/marketing prefixes
  clean = clean.replace(/^\s*gi[oỏ]\s*h[aà]ng\s*m[oớ]i\s*\|\|\s*/i, "");
  clean = clean.replace(/^\s*\[(?:hot|si[eê]u\s*ph[aẩ]m|g[aấ]p|ch[ií]nh\s*ch[uủ]|b[aá]n\s*g[aấ]p)\]\s*/i, "");
  clean = clean.replace(/^\s*(?:g[dđ]|gia\s*đ[iì]nh)\s*(?:c[aầ]n\s*b[aá]n|chuy[eể]n\s*nh[aà]|chuy[eể]n\s*v[eề]\s*qu[eê]\s*c[aầ]n\s*b[aá]n)\s+/i, "");
  clean = clean.replace(/^\s*(?:ch[ií]nh\s*ch[uủ]\s*c[aầ]n\s*b[aá]n|ch[ií]nh\s*ch[uủ]\s*b[aá]n\s*g[aấ]p|ch[ií]nh\s*ch[uủ]\s*b[aá]n|c[aầ]n\s*b[aá]n\s*g[aấ]p|b[aá]n\s*g[aấ]p|b[aá]n\s*nhanh|c[aắ]t\s*l[oỗ])\s+/i, "");
  clean = clean.replace(/^\s*b[aá]n\s+(?=(?:c[aă]n\s*h[oộ]|ch\b|cc\b|nh[aà]|chung\s*c[uư]|t[aậ]p\s*th[eể]|bi[eệ]t\s*th[uự]|shophouse|penthouse|duplex|đ[aấ]t))/i, "");
  clean = clean.replace(/^\s*b[aá]n\s+/i, "");

  // Expand abbreviations
  clean = clean.replace(/\bch\s*(\d+[a-zA-Z]?)\b/gi, "Căn hộ $1");
  clean = clean.replace(/\bcc\s*([a-zA-Z]\d+[a-zA-Z]?)\b/gi, "Chung cư $1");
  clean = clean.replace(/\bch\b/gi, "Căn hộ");
  clean = clean.replace(/\bcc\b/gi, "Chung cư");
  clean = clean.replace(/\bk[dđ]tm\b/gi, "Khu đô thị mới");
  clean = clean.replace(/\bk[dđ]t\b/gi, "Khu đô thị");
  clean = clean.replace(/\btttm\b/gi, "TTTM");
  clean = clean.replace(/\b(\d+)\s*pn\b/gi, "$1PN");
  clean = clean.replace(/\b(\d+)\s*wc\b/gi, "$1WC");
  clean = clean.replace(/\b(\d+(?:[.,]\d+)?)\s*m2\b/gi, "$1m²");

  // Uppercase building codes: "b10a" -> "B10A", "ct2a" -> "CT2A"
  clean = clean.replace(/\b([a-zA-Z]{1,3}\d+[a-zA-Z]{0,2})\b/g, (match) => match.toUpperCase());

  // Spacing after commas (ignoring decimals)
  clean = clean.replace(/,([^\s\d])/g, ", $1");
  clean = clean.replace(/\.([^\s\d])/g, ". $1");
  clean = clean.replace(/,\s*([a-zà-ỹ])/g, (_m, p1) => ", " + p1.toUpperCase());
  clean = clean.replace(/\s+/g, " ").trim();

  // Ensure first character capitalized
  if (clean.length > 0) {
    clean = clean.charAt(0).toUpperCase() + clean.slice(1);
  }
  return clean;
}
