"use client";

import Link from "next/link";
import { FaBed, FaBookmark, FaCalendarAlt, FaMagic, FaMapMarkerAlt, FaRegBookmark, FaRulerCombined } from "react-icons/fa";
import type { Property } from "@/lib/types";
import { formatPropertyTitle } from "@/lib/propertyAddress";
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
  const displayTitle = formatPropertyTitle(property.title);
  const askPrompt = encodeURIComponent(`Review chi tiết căn ${displayTitle}`);

  return (
    <article className="group flex h-full flex-col overflow-hidden rounded-[1.65rem] border border-black/5 bg-white shadow-[0_12px_35px_rgba(22,47,42,.06)] transition-all duration-500 hover:-translate-y-2 hover:shadow-[0_24px_55px_rgba(22,47,42,.13)] hover:border-black/10">
      <div className={`relative overflow-hidden bg-stone-100 ${compact ? "h-44" : "h-56"}`}>
        <Link href={`/properties/${property.id}`} className="block h-full">
          {image ? (
            <PropertyImage
              src={image}
              alt={displayTitle}
              className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
            />
          ) : (
            <div className="grid h-full place-items-center text-5xl">🏡</div>
          )}
        </Link>
        
        {/* Pulsing Live Badge */}
        <div className="absolute left-3 top-3 inline-flex items-center gap-1.5 rounded-full bg-white/95 px-3 py-1.5 text-[10px] font-bold uppercase tracking-[.12em] text-[var(--forest)] shadow-xs backdrop-blur-md border border-emerald-100/80">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          Có thể xem
        </div>

        {onSave && (
          <button
            onClick={() => onSave(property)}
            aria-label={saved ? "Bỏ lưu" : "Lưu nhà"}
            aria-pressed={saved}
            className="absolute right-3 top-3 grid h-9 w-9 place-items-center rounded-full bg-white/90 text-[var(--forest)] shadow-sm backdrop-blur-md transition-transform duration-300 hover:scale-110 active:scale-95"
          >
            {saved ? <FaBookmark className="text-emerald-700" /> : <FaRegBookmark />}
          </button>
        )}
      </div>

      <div className="flex flex-1 flex-col p-5 sm:p-6">
        <div className="flex items-start justify-between gap-4">
          <Link
            href={`/properties/${property.id}`}
            className="line-clamp-2 font-semibold leading-6 text-stone-900 transition-colors duration-200 hover:text-[var(--forest)]"
          >
            {displayTitle}
          </Link>
          <span className="shrink-0 text-base font-bold text-[var(--coral)] sm:text-lg">
            {formatPropertyPrice(property.list_price)}
          </span>
        </div>

        <p className="mt-2.5 line-clamp-1 text-xs text-[var(--muted)]">
          <FaMapMarkerAlt className="mr-1.5 inline text-[var(--forest)]" />
          {location}
        </p>

        <div className="mt-3.5 flex flex-wrap items-center gap-3 text-xs font-medium text-stone-600">
          <span className="inline-flex items-center rounded-md bg-stone-50 px-2.5 py-1 border border-black/5">
            <FaBed className="mr-1.5 inline text-[var(--forest)]" />
            {property.bedrooms ?? "–"} PN
          </span>
          <span className="inline-flex items-center rounded-md bg-stone-50 px-2.5 py-1 border border-black/5">
            <FaRulerCombined className="mr-1.5 inline text-[var(--forest)]" />
            {property.area_sqm ?? "–"} m²
          </span>
        </div>

        <div className="mt-5 grid grid-cols-2 gap-2.5 border-t border-black/5 pt-4">
          <Link
            href={`/chat?property_id=${property.id}&prompt=${askPrompt}`}
            className="inline-flex items-center justify-center rounded-full border border-black/10 bg-white px-3 py-2.5 text-center text-xs font-semibold text-stone-700 transition-all duration-200 hover:bg-stone-50 hover:border-[var(--sage)] hover:text-[var(--forest)] shadow-xs"
          >
            <FaMagic className="mr-1.5 inline text-[var(--coral)]" />
            Hỏi Nera
          </Link>
          <Link
            href={`/booking/schedule?property_id=${property.id}`}
            className="inline-flex items-center justify-center rounded-full bg-[var(--forest)] px-3 py-2.5 text-center text-xs font-semibold text-white shadow-[0_4px_12px_rgba(22,47,42,0.18)] transition-all duration-200 hover:shadow-[0_6px_18px_rgba(22,47,42,0.28)] hover:bg-[var(--ink)] hover:scale-[1.02] active:scale-[0.98]"
          >
            <FaCalendarAlt className="mr-1.5 inline" />
            Đặt lịch
          </Link>
        </div>
      </div>
    </article>
  );
}
