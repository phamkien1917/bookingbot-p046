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
