import { useMemo, useState } from "react";
import { FaBed, FaBookmark, FaBrain, FaCheckCircle, FaChevronDown, FaChevronRight, FaExclamationCircle, FaMapMarkerAlt, FaRegBookmark, FaCalendarAlt, FaTimesCircle } from "react-icons/fa";
import { formatPropertyPrice } from "@/components/PropertyTile";
import type { Property } from "@/lib/types";

// Helper: match property features vs insights for "Vì sao?"
function buildMatchReasons(property: Property, insights: Record<string, unknown>): { ok: string[]; caution: string[] } {
  const ok: string[] = [];
  const caution: string[] = [];
  const maxPrice = insights.max_price as number | undefined;
  if (maxPrice && property.list_price) {
    if (property.list_price <= maxPrice) ok.push(`Giá phù hợp ngân sách`);
    else caution.push(`Có thể hơi cao so với ngân sách`);
  }
  const beds = insights.bedrooms as number | undefined;
  if (beds && property.bedrooms != null) {
    if (property.bedrooms >= beds) ok.push(`Đủ ${property.bedrooms} phòng ngủ`);
    else caution.push(`Ít hơn yêu cầu phòng ngủ`);
  }
  const district = insights.district as string | undefined;
  if (district && property.district?.toLowerCase().includes(district.toLowerCase())) {
    ok.push(`Đúng khu vực ${district}`);
  }
  if (property.area_sqm && property.area_sqm >= 50) ok.push(`Diện tích rộng rãi (${property.area_sqm} m²)`);
  return { ok, caution };
}

// ────────────────────────────────────────────────────────────
// Property Card with AI match reasons
// ────────────────────────────────────────────────────────────
function PropertyCard({ property, insights, savedIds, onDetail, onSave, onBook, onReject, animDelay }: {
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
  const { ok, caution } = useMemo(() => buildMatchReasons(property, insights), [property, insights]);
  const hasInsights = ok.length > 0 || caution.length > 0;

  return (
    <article
      style={{ animationDelay: `${animDelay}ms` }}
      className="animate-card-rise mt-4 overflow-hidden rounded-[1.5rem] border border-black/5 bg-white shadow-[0_14px_40px_rgba(22,47,42,.08)]"
    >
      <div className="sm:flex">
        <div className="h-48 bg-stone-100 sm:h-auto sm:w-52 shrink-0">
          {(property.image || property.media?.[0]?.url)
            ? <img src={property.image || property.media[0].url} alt={property.title} className="h-full w-full object-cover" />
            : <div className="grid h-full min-h-40 place-items-center text-4xl">🏠</div>}
        </div>
        <div className="flex-1 p-5">
          <div className="flex flex-wrap justify-between gap-2">
            <h2 className="max-w-sm font-semibold leading-6">{property.title}</h2>
            <span className="font-semibold text-[var(--coral)]">{formatPropertyPrice(property.list_price)}</span>
          </div>
          <p className="mt-2 text-xs text-[var(--muted)]">
            <FaMapMarkerAlt className="mr-1 inline" />
            {property.address_full || [property.address_line, property.district, property.province].filter(Boolean).join(", ")}
          </p>
          <p className="mt-2 text-xs text-[var(--muted)]">
            <FaBed className="mr-1 inline text-[var(--forest)]" />{property.bedrooms ?? 0} phòng ngủ · {property.area_sqm} m²
          </p>

          {/* "Vì sao phù hợp?" expandable section */}
          {hasInsights && (
            <button
              onClick={() => setShowReasons(v => !v)}
              className="mt-3 flex items-center gap-1.5 text-xs font-semibold text-[var(--forest)] hover:underline"
            >
              <FaBrain className="text-[var(--sage)]" />
              Vì sao Nera gợi ý căn này?
              {showReasons ? <FaChevronDown className="text-[8px]" /> : <FaChevronRight className="text-[8px]" />}
            </button>
          )}
          {showReasons && (
            <div className="mt-2 rounded-xl bg-[#f0f5f1] px-4 py-3 space-y-1 text-xs">
              {ok.map(r => (
                <p key={r} className="flex items-start gap-1.5 text-[var(--forest)]">
                  <FaCheckCircle className="mt-0.5 shrink-0 text-emerald-500" />{r}
                </p>
              ))}
              {caution.map(r => (
                <p key={r} className="flex items-start gap-1.5 text-amber-700">
                  <FaExclamationCircle className="mt-0.5 shrink-0" />{r}
                </p>
              ))}
            </div>
          )}

          <div className="mt-4 flex flex-wrap gap-2">
            <button onClick={onDetail} className="rounded-full border border-black/10 px-4 py-2 text-xs font-semibold hover:bg-stone-50">Chi tiết</button>
            <button onClick={onSave} aria-pressed={savedIds.has(property.id)}
              className="rounded-full border border-[var(--sage)]/50 px-4 py-2 text-xs font-semibold text-[var(--forest)] hover:bg-[#edf3ed]">
              {savedIds.has(property.id) ? <FaBookmark className="mr-1 inline" /> : <FaRegBookmark className="mr-1 inline" />}
              {savedIds.has(property.id) ? "Đã lưu" : "Lưu"}
            </button>
            <button onClick={onBook} className="rounded-full bg-[var(--forest)] px-4 py-2 text-xs font-semibold text-white hover:opacity-90">
              <FaCalendarAlt className="mr-1 inline" />Đặt lịch xem
            </button>
            <button onClick={onReject}
              className="rounded-full border border-black/8 px-4 py-2 text-xs font-medium text-[var(--muted)] hover:border-red-200 hover:text-red-500">
              <FaTimesCircle className="mr-1 inline" />Không phù hợp
            </button>
          </div>
        </div>
      </div>
    </article>
  );
}

