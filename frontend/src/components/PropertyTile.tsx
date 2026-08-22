"use client";

import Link from "next/link";
import { FaBed, FaBookmark, FaCalendarAlt, FaMagic, FaMapMarkerAlt, FaRegBookmark, FaRulerCombined } from "react-icons/fa";
import type { Property } from "@/lib/types";
import PropertyImage from "@/components/PropertyImage";

export function formatPropertyPrice(price?: number | null) {
  if (!price) return "Liên hệ";
  if (price >= 1_000_000_000) return `${(price / 1_000_000_000).toFixed(price % 1_000_000_000 === 0 ? 0 : 1)} tỷ`;
  return `${Math.round(price / 1_000_000)} triệu`;
}

export default function PropertyTile({
  property,
  saved = false,
  onSave,
  compact = false,
}: {
  property: Property;
  saved?: boolean;
  onSave?: (property: Property) => void;
  compact?: boolean;
}) {
  const image = property.image || property.media?.[0]?.url;
  const location = [property.district, property.province].filter(Boolean).join(", ") || property.address_full || "Đang cập nhật vị trí";
  const askPrompt = encodeURIComponent(`Phân tích ưu nhược điểm và tìm căn tương tự ${property.title}`);

  return (
    <article className="group flex h-full flex-col overflow-hidden rounded-[1.65rem] border border-black/5 bg-white shadow-[0_12px_40px_rgba(22,47,42,.07)] transition duration-500 hover:-translate-y-1.5 hover:shadow-[0_28px_70px_rgba(22,47,42,.14)]">
      <div className={`relative overflow-hidden bg-stone-100 ${compact ? "h-44" : "h-56"}`}>
        <Link href={`/properties/${property.id}`} className="block h-full">
          {image ? <PropertyImage src={image} alt={property.title} className="h-full w-full object-cover transition duration-700 group-hover:scale-105" /> : <div className="grid h-full place-items-center text-5xl">🏡</div>}
        </Link>
        <span className="absolute left-3 top-3 rounded-full bg-white/90 px-3 py-1.5 text-[10px] font-bold uppercase tracking-[.12em] text-[var(--forest)] backdrop-blur">Có thể xem</span>
        {onSave && <button onClick={() => onSave(property)} aria-label={saved ? "Bỏ lưu" : "Lưu nhà"} aria-pressed={saved} className="absolute right-3 top-3 grid h-9 w-9 place-items-center rounded-full bg-white/90 text-[var(--forest)] shadow-sm transition hover:scale-105">{saved ? <FaBookmark /> : <FaRegBookmark />}</button>}
      </div>
      <div className="flex flex-1 flex-col p-5">
        <div className="flex items-start justify-between gap-4">
          <Link href={`/properties/${property.id}`} className="line-clamp-2 font-semibold leading-6 transition hover:text-[var(--forest)]">{property.title}</Link>
          <span className="shrink-0 font-semibold text-[var(--coral)]">{formatPropertyPrice(property.list_price)}</span>
        </div>
        <p className="mt-3 line-clamp-1 text-xs text-[var(--muted)]"><FaMapMarkerAlt className="mr-1 inline text-[var(--forest)]" />{location}</p>
        <div className="mt-3 flex flex-wrap gap-3 text-xs text-[var(--muted)]">
          <span><FaBed className="mr-1 inline text-[var(--forest)]" />{property.bedrooms ?? "–"} PN</span>
          <span><FaRulerCombined className="mr-1 inline text-[var(--forest)]" />{property.area_sqm ?? "–"} m²</span>
        </div>
        <div className="mt-5 grid grid-cols-2 gap-2 border-t border-black/5 pt-4">
          <Link href={`/chat?prompt=${askPrompt}`} className="rounded-full border border-black/10 px-3 py-2.5 text-center text-xs font-semibold transition hover:bg-stone-50"><FaMagic className="mr-1 inline text-[var(--coral)]" />Hỏi Nera</Link>
          <Link href={`/booking/schedule?property_id=${property.id}`} className="rounded-full bg-[var(--forest)] px-3 py-2.5 text-center text-xs font-semibold text-white transition hover:bg-[var(--ink)]"><FaCalendarAlt className="mr-1 inline" />Đặt lịch</Link>
        </div>
      </div>
    </article>
  );
}
