"use client";

import { useMemo, useState } from "react";
import {
  FaMap,
  FaBed,
  FaBookmark,
  FaBrain,
  FaCheckCircle,
  FaChevronDown,
  FaChevronRight,
  FaExclamationCircle,
  FaMapMarkerAlt,
  FaRegBookmark,
  FaCalendarAlt,
  FaTimesCircle,
} from "react-icons/fa";
import { formatPropertyPrice } from "@/components/PropertyTile";
import type { Property } from "@/lib/types";
import { formatPropertyAddress, formatPropertyTitle } from "@/lib/propertyAddress";
import PropertyImage from "@/components/PropertyImage";
import RoutePanel from "@/components/chat/RoutePanel";

// Helper: match property features vs insights for "Vì sao?"
function buildMatchReasons(
  property: Property,
  insights: Record<string, unknown>
): { ok: string[]; caution: string[] } {
  const ok: string[] = [];
  const caution: string[] = [];
  const maxPrice = insights.max_price as number | undefined;
  if (maxPrice && property.list_price) {
    if (property.list_price <= maxPrice) ok.push(`Giá phù hợp ngân sách`);
    else caution.push(`Có thể hơi cao so với ngân sách`);
  }
  const beds = (insights.min_bedrooms ?? insights.bedrooms) as number | undefined;
  if (beds && property.bedrooms != null) {
    if (property.bedrooms >= beds) ok.push(`Đủ ${property.bedrooms} phòng ngủ`);
    else caution.push(`Ít hơn yêu cầu phòng ngủ`);
  }
  const district = insights.district as string | undefined;
  if (district && property.district?.toLowerCase().includes(district.toLowerCase())) {
    ok.push(`Đúng khu vực ${district}`);
  }
  if (property.area_sqm && property.area_sqm >= 50) {
    ok.push(`Diện tích rộng rãi (${property.area_sqm} m²)`);
  }
  return { ok, caution };
}

// Freshness pill: a crawled listing can be let while the post stays up, so the
// card says when a human last confirmed it. Wording comes from the backend so
// chat replies and cards never drift apart.
function VerificationBadge({ property }: { property: Property }) {
  if (!property.verification_label) return null;

  const tone = property.is_stale
    ? "text-amber-700 bg-amber-50 border-amber-200"
    : "text-[var(--forest)] bg-emerald-50 border-emerald-100";

  return (
    <p className={`mt-2 flex w-fit items-center gap-1 rounded-full border px-2.5 py-1 text-xs font-semibold ${tone}`}>
      {property.is_stale ? <FaExclamationCircle /> : <FaCheckCircle />}
      {property.verification_label}
    </p>
  );
}

// ────────────────────────────────────────────────────────────
// Property Card with AI match reasons and map routing
// ────────────────────────────────────────────────────────────
export default function PropertyCard({
  property,
  insights,
  savedIds,
  onDetail,
  onSave,
  onBook,
  onReject,
  animDelay,
}: {
  property: Property;
  insights: Record<string, unknown>;
  savedIds: Set<string>;
  onDetail: () => void;
  onSave: () => void;
  onBook: () => void;
  onReject: () => void;
  animDelay: number;
}) {
  const [showReasons, setShowReasons] = useState(false);
  const [showMap, setShowMap] = useState(false);
  const { ok, caution } = useMemo(() => buildMatchReasons(property, insights), [property, insights]);
  const hasInsights = ok.length > 0 || caution.length > 0;

  return (
    <article
      style={{ animationDelay: `${animDelay}ms` }}
      className="animate-card-rise mt-4 overflow-hidden rounded-[1.5rem] border border-black/5 bg-white shadow-[0_14px_40px_rgba(22,47,42,.08)] transition-all hover:shadow-[0_20px_50px_rgba(22,47,42,.12)]"
    >
      <div className="sm:flex">
        <div className="h-48 bg-stone-100 sm:h-auto sm:w-52 shrink-0 relative">
          {property.image || property.media?.[0]?.url ? (
            <PropertyImage
              src={property.image || property.media[0].url}
              alt={property.title}
              className="h-full w-full object-cover"
            />
          ) : (
            <div className="grid h-full min-h-40 place-items-center text-4xl">🏠</div>
          )}
        </div>
        <div className="flex-1 p-5">
          <div className="flex items-start justify-between gap-3">
            <h2 className="flex-1 font-semibold leading-6 text-stone-900 line-clamp-2">
              {formatPropertyTitle(property.title)}
            </h2>
            <span className="shrink-0 whitespace-nowrap text-right font-bold text-[var(--coral)] sm:text-base">
              {formatPropertyPrice(property.list_price)}
            </span>
          </div>
          <p className="mt-2 text-xs text-[var(--muted)]">
            <FaMapMarkerAlt className="mr-1 inline text-stone-400" />
            {formatPropertyAddress(property)}
          </p>
          {property.distance_evidence && (
            <p className="mt-2 text-xs font-semibold text-[var(--forest)] bg-emerald-50 border border-emerald-100 w-fit px-2.5 py-1 rounded-full flex items-center gap-1">
              <span>📍</span> Cách {property.distance_evidence.distance_km} km ({property.distance_evidence.duration_minutes} phút) đến {property.distance_evidence.destination}
            </p>
          )}
          <p className="mt-2 text-xs text-[var(--muted)]">
            <FaBed className="mr-1 inline text-[var(--forest)]" />
            {property.bedrooms ?? 0} phòng ngủ · {property.area_sqm} m²
          </p>
          <VerificationBadge property={property} />

          {/* "Vì sao phù hợp?" expandable section */}
          {hasInsights && (
            <button
              onClick={() => setShowReasons((v) => !v)}
              className="mt-3 flex cursor-pointer items-center gap-1.5 text-xs font-semibold text-[var(--forest)] hover:underline"
            >
              <FaBrain className="text-[var(--sage)]" />
              Vì sao Nera gợi ý căn này?
              {showReasons ? (
                <FaChevronDown className="text-[8px]" />
              ) : (
                <FaChevronRight className="text-[8px]" />
              )}
            </button>
          )}
          {showReasons && (
            <div className="mt-2 rounded-xl bg-[#f0f5f1] px-4 py-3 space-y-1.5 text-xs border border-emerald-100/60">
              {ok.map((r) => (
                <p key={r} className="flex items-start gap-1.5 text-[var(--forest)]">
                  <FaCheckCircle className="mt-0.5 shrink-0 text-emerald-600" />
                  {r}
                </p>
              ))}
              {caution.map((r) => (
                <p key={r} className="flex items-start gap-1.5 text-amber-700">
                  <FaExclamationCircle className="mt-0.5 shrink-0 text-amber-600" />
                  {r}
                </p>
              ))}
            </div>
          )}

          <div className="mt-4 flex flex-wrap gap-2 items-center">
            <button
              onClick={onDetail}
              className="cursor-pointer rounded-full border border-black/10 px-4 py-2 text-xs font-semibold transition hover:bg-stone-50"
            >
              Chi tiết
            </button>
            {property.latitude && property.longitude && (
              <button
                onClick={() => setShowMap(!showMap)}
                className="cursor-pointer flex items-center rounded-full border border-[var(--forest)] text-[var(--forest)] px-4 py-2 text-xs font-semibold transition hover:bg-emerald-50"
              >
                <FaMap className="inline mr-1" /> {showMap ? "Ẩn bản đồ" : "Xem bản đồ"}
              </button>
            )}
            <button
              onClick={onSave}
              aria-pressed={savedIds.has(property.id)}
              className="cursor-pointer rounded-full border border-[var(--sage)]/50 px-4 py-2 text-xs font-semibold text-[var(--forest)] transition hover:bg-[#edf3ed]"
            >
              {savedIds.has(property.id) ? (
                <FaBookmark className="mr-1 inline" />
              ) : (
                <FaRegBookmark className="mr-1 inline" />
              )}
              {savedIds.has(property.id) ? "Đã lưu" : "Lưu"}
            </button>
            <button
              onClick={onBook}
              className="cursor-pointer rounded-full bg-[var(--forest)] px-4 py-2 text-xs font-semibold text-white shadow-sm transition hover:opacity-90 hover:shadow"
            >
              <FaCalendarAlt className="mr-1 inline" />
              Đặt lịch xem
            </button>
            <button
              onClick={onReject}
              className="cursor-pointer rounded-full border border-black/10 px-3 py-2 text-xs font-semibold text-[var(--muted)] transition hover:bg-red-50 hover:text-red-600 ml-auto"
              title="Loại căn này khỏi kết quả"
            >
              <FaTimesCircle className="text-base" />
            </button>
          </div>

          {/* Lộ trình: bảng số liệu Goong trước, bản đồ sau */}
          {showMap && <RoutePanel property={property} />}
          {showMap && property.latitude && property.longitude && (
            <div className="mt-3 overflow-hidden rounded-xl border border-black/10 bg-stone-100 shadow-inner">
              <iframe
                title={`Bản đồ ${property.title}`}
                width="100%"
                height="220"
                style={{ border: 0 }}
                loading="lazy"
                allowFullScreen
                referrerPolicy="no-referrer-when-downgrade"
                src={`https://www.google.com/maps?saddr=${property.latitude},${property.longitude}&daddr=${encodeURIComponent(property.distance_evidence?.destination || property.address_line || "Hà Nội")}&hl=vi&output=embed`}
              />
            </div>
          )}
        </div>
      </div>
    </article>
  );
}
