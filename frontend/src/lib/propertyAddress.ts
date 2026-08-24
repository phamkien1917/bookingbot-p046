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

const PROPER_NOUNS: Array<[RegExp, string]> = [
  [/(?<!\p{L})b[aã]i\s+ch[aá]y(?!\p{L})/gui, "Bãi Cháy"],
  [/(?<!\p{L})nam\s+trung\s+y[eê]n(?!\p{L})/gui, "Nam Trung Yên"],
  [/(?<!\p{L})ho[aà]ng\s+c[aầ]u(?!\p{L})/gui, "Hoàng Cầu"],
  [/(?<!\p{L})c[aầ]u\s+gi[aấ]y(?!\p{L})/gui, "Cầu Giấy"],
  [/(?<!\p{L})m[yỹ]\s+[dđ][iì]nh(?!\p{L})/gui, "Mỹ Đình"],
  [/(?<!\p{L})y[eê]n\s+ho[aà](?!\p{L})/gui, "Yên Hòa"],
  [/(?<!\p{L})thanh\s+xu[aâ]n(?!\p{L})/gui, "Thanh Xuân"],
  [/(?<!\p{L})[dđ][oố]ng\s+[dđ]a(?!\p{L})/gui, "Đống Đa"],
  [/(?<!\p{L})h[aà]\s+[dđ][oô]ng(?!\p{L})/gui, "Hà Đông"],
  [/(?<!\p{L})ba\s+[dđ][iì]nh(?!\p{L})/gui, "Ba Đình"],
  [/(?<!\p{L})hai\s+b[aà]\s+tr[uư]ng(?!\p{L})/gui, "Hai Bà Trưng"],
  [/(?<!\p{L})long\s+bi[eê]n(?!\p{L})/gui, "Long Biên"],
  [/(?<!\p{L})t[aâ]y\s+h[oồ](?!\p{L})/gui, "Tây Hồ"],
  [/(?<!\p{L})ho[aà]n\s+ki[eế]m(?!\p{L})/gui, "Hoàn Kiếm"],
  [/(?<!\p{L})b[aắ]c\s+t[uừ]\s+li[eê]m(?!\p{L})/gui, "Bắc Từ Liêm"],
  [/(?<!\p{L})nam\s+t[uừ]\s+li[eê]m(?!\p{L})/gui, "Nam Từ Liêm"],
  [/(?<!\p{L})ho[aà]ng\s+mai(?!\p{L})/gui, "Hoàng Mai"],
  [/(?<!\p{L})b[iì]nh\s+th[aạ]nh(?!\p{L})/gui, "Bình Thạnh"],
  [/(?<!\p{L})th[uủ]\s+[dđ][uứ]c(?!\p{L})/gui, "Thủ Đức"],
  [/(?<!\p{L})g[oò]\s+v[aấ]p(?!\p{L})/gui, "Gò Vấp"],
  [/(?<!\p{L})m[oỗ]\s+lao(?!\p{L})/gui, "Mỗ Lao"],
  [/(?<!\p{L})b[aắ]c\s+h[aà](?!\p{L})/gui, "Bắc Hà"],
  [/(?<!\p{L})fodacon(?!\p{L})/gui, "Fodacon"],
  [/(?<!\p{L})vinhomes(?!\p{L})/gui, "Vinhomes"],
  [/(?<!\p{L})smart\s+city(?!\p{L})/gui, "Smart City"],
  [/(?<!\p{L})ocean\s+park(?!\p{L})/gui, "Ocean Park"],
  [/(?<!\p{L})times\s+city(?!\p{L})/gui, "Times City"],
  [/(?<!\p{L})royal\s+city(?!\p{L})/gui, "Royal City"],
  [/(?<!\p{L})goldmark\s+city(?!\p{L})/gui, "Goldmark City"],
  [/(?<!\p{L})bcons(?!\p{L})/gui, "Bcons"],
  [/(?<!\p{L})newsky(?!\p{L})/gui, "Newsky"],
];

export function formatPropertyTitle(title?: string | null): string {
  if (!title) return "Căn hộ bất động sản";
  let clean = title.trim();

  // Step 1: Remove noisy junk / seller prefixes
  clean = clean.replace(/^\s*gi[oỏ]\s*h[aà]ng\s*m[oớ]i\s*\|\|\s*/iu, "");
  clean = clean.replace(/^\s*\[(?:hot|si[eê]u\s*ph[aẩ]m|g[aấ]p|ch[ií]nh\s*ch[uủ]|b[aá]n\s*g[aấ]p)\]\s*/iu, "");
  clean = clean.replace(/^\s*(?:[🏡🏠🏢✨🔥💥⚡️🌟*]+)\s*/u, "");
  clean = clean.replace(/^\s*(?:t[oô]i\s+)?(?:ch[ií]nh\s*ch[uủ])\s*(?:c[aầ]n\s*b[aá]n|b[aá]n\s*g[aấ]p|b[aá]n)?\s*/iu, "");
  clean = clean.replace(/^\s*(?:g[dđ]|gia\s*đ[iì]nh)\s*(?:c[aầ]n\s*b[aá]n|chuy[eể]n\s*nh[aà]|chuy[eể]n\s*v[eề]\s*qu[eê]\s*c[aầ]n\s*b[aá]n)\s*/iu, "");
  clean = clean.replace(/^\s*(?:c[aầ]n\s*b[aá]n\s*g[aấ]p|b[aá]n\s*g[aấ]p|b[aá]n\s*nhanh|c[aắ]t\s*l[oỗ]|c[aầ]n\s*ti[eề]n\s*b[aá]n\s*g[aấ]p|c[aầ]n\s*b[aá]n)\s*/iu, "");
  clean = clean.replace(/^\s*b[aá]n\s+(?=(?:c[aă]n\s*h[oộ]|ch(?!\p{L})|cc(?!\p{L})|nh[aà]|chung\s*c[uư]|t[aậ]p\s*th[eể]|bi[eệ]t\s*th[uự]|shophouse|penthouse|duplex|đ[aấ]t))/iu, "");
  clean = clean.replace(/^\s*b[aá]n\s+/iu, "");

  // Step 2: Spacing after punctuation (without breaking decimals "5,8" or ellipsis "...")
  clean = clean.replace(/,([^\s\d])/g, ", $1");
  clean = clean.replace(/(?<!\.)\.(?!\.)([^\s\d])/g, ". $1");
  clean = clean.replace(/\s+/g, " ").trim();

  // Step 3: Expand abbreviations with Unicode letter lookaround
  clean = clean.replace(/(?<!\p{L})chcc(?!\p{L})/gui, "Chung cư");
  clean = clean.replace(/(?<!\p{L})ch\s*(\d+[a-zA-Z]?)(?!\p{L})/gui, "Căn hộ $1");
  clean = clean.replace(/(?<!\p{L})cc\s*([a-zA-Z]\d+[a-zA-Z]?)(?!\p{L})/gui, "Chung cư $1");
  clean = clean.replace(/(?<!\p{L})ch(?!\p{L})/gui, "Căn hộ");
  clean = clean.replace(/(?<!\p{L})cc(?!\p{L})/gui, "Chung cư");
  clean = clean.replace(/(?<!\p{L})k[dđ]tm(?!\p{L})/gui, "Khu đô thị mới");
  clean = clean.replace(/(?<!\p{L})k[dđ]t(?!\p{L})/gui, "Khu đô thị");
  clean = clean.replace(/(?<!\p{L})tttm(?!\p{L})/gui, "TTTM");
  clean = clean.replace(/(?<!\p{L})(\d+)\s*pn(?!\p{L})/gui, "$1PN");
  clean = clean.replace(/(?<!\p{L})(\d+)\s*wc(?!\p{L})/gui, "$1WC");
  clean = clean.replace(/(?<!\p{L})(\d+(?:[.,]\d+)?)\s*m2(?!\p{L})/gui, "$1m²");
  clean = clean.replace(/(?<!\p{L})(\d+(?:[.,]\d+)?)\s*m(?=\s+(?:nam|cầu|bắc|hoàng|đống|thanh|hà|hướng|tầng|view|full|giá|trung|đô)|$)/gui, "$1m²");

  // Step 4: Uppercase unit codes: "b10a" -> "B10A", "ct2a" -> "CT2A"
  clean = clean.replace(/(?<!\p{L})([a-zA-Z]{1,3}\d+[a-zA-Z]{0,2})(?!\p{L})/gu, (match) => match.toUpperCase());

  // Step 5: Proper Nouns
  for (const [pattern, proper] of PROPER_NOUNS) {
    clean = clean.replace(pattern, proper);
  }

  // Step 6: Fix duplicate words
  clean = clean.replace(/\bcăn hộ\s+căn hộ\b/giu, "Căn hộ");
  clean = clean.replace(/\bchung cư\s+chung cư\b/giu, "Chung cư");
  clean = clean.replace(/\bcăn hộ\s+chung cư\b/giu, "Căn hộ Chung cư");

  // Capitalize right after comma
  clean = clean.replace(/,\s*([a-zà-ỹ])/gu, (_m, p1) => ", " + p1.toUpperCase());
  clean = clean.replace(/\s+/g, " ").trim();

  // Ensure first character capitalized
  if (clean.length > 0) {
    clean = clean.charAt(0).toUpperCase() + clean.slice(1);
  }
  return clean;
}
