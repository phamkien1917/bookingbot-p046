/* eslint-disable @next/next/no-img-element */
"use client";

import Link from "next/link";
import { useMemo } from "react";
import { FaBookmark, FaBrain, FaCheck, FaCompass, FaShieldAlt } from "react-icons/fa";

import { formatPropertyPrice } from "@/components/PropertyTile";
import type { Property } from "@/lib/types";

const INSIGHT_LABELS: Record<string, string> = {
  district: "Khu vực",
  province: "Tỉnh/TP",
  property_kind: "Loại nhà",
  min_bedrooms: "Phòng ngủ tối thiểu",
  min_bathrooms: "Phòng tắm tối thiểu",
  min_area: "Diện tích tối thiểu",
  min_price: "Giá từ",
  max_price: "Giá tới",
};

function formatInsightValue(key: string, value: unknown): string {
  if (key.includes("price")) {
    const amount = Number(value);
    if (amount >= 1_000_000_000) return `${(amount / 1_000_000_000).toFixed(1)} tỷ`;
    if (amount >= 1_000_000) return `${(amount / 1_000_000).toFixed(0)} triệu`;
  }
  if (key === "min_area") return `${value} m²`;
  return Array.isArray(value) ? value.join(", ") : String(value);
}

export interface InsightsSidebarProps {
  insights: Record<string, unknown>;
  memorySummary: string;
  savedProperties: Property[];
  latestMatches: Property[];
  onSelectProperty: (property: Property) => void;
  onClearMemory: () => void;
}

export default function InsightsSidebar({
  insights,
  memorySummary,
  savedProperties,
  latestMatches,
  onSelectProperty,
  onClearMemory,
}: InsightsSidebarProps) {
  const insightEntries = useMemo(
    () => Object.entries(insights).filter(([, value]) => value !== null && value !== ""),
    [insights],
  );
  const progress = Math.min(100, Math.round((insightEntries.length / 6) * 100));

  return (
    <aside className="hidden w-80 shrink-0 flex-col border-l border-black/5 bg-white xl:flex">
      <div className="border-b border-black/5 p-5">
        <p className="text-xs font-bold uppercase tracking-[.16em] text-[var(--coral)]">AI đang hiểu gì về bạn</p>
        <h2 className="mt-1 font-semibold">Hồ sơ nhu cầu</h2>
        <div className="mt-3 h-1.5 rounded-full bg-black/8">
          <div className="h-full rounded-full bg-[var(--forest)]" style={{ width: `${progress}%` }} />
        </div>
      </div>

      <div className="flex-1 space-y-5 overflow-y-auto p-5">
        {insightEntries.length > 0 && (
          <section>
            <p className="mb-2 flex items-center gap-2 text-xs font-bold uppercase tracking-[.1em] text-[var(--muted)]">
              <FaCheck className="text-emerald-500" /> Tiêu chí đã xác nhận
            </p>
            <div className="space-y-2">
              {insightEntries.map(([key, value]) => (
                <div key={key} className="flex items-center justify-between rounded-xl bg-[#f0f5f1] px-3 py-2">
                  <span className="text-[10px] font-semibold uppercase text-[var(--muted)]">{INSIGHT_LABELS[key] ?? key}</span>
                  <span className="max-w-[55%] truncate text-right text-xs font-semibold text-[var(--forest)]">
                    {formatInsightValue(key, value)}
                  </span>
                </div>
              ))}
            </div>
          </section>
        )}

        {memorySummary && (
          <section className="rounded-2xl bg-[#edf3ed] p-4">
            <p className="flex items-center gap-2 text-xs font-bold uppercase text-[var(--forest)]"><FaBrain /> Memory dài hạn</p>
            <p className="mt-2 text-xs leading-5 text-[var(--muted)]">{memorySummary}</p>
            <div className="mt-3 flex justify-between">
              <Link href="/memory" className="text-[11px] font-semibold text-[var(--forest)]">Xem và chỉnh sửa →</Link>
              <button onClick={onClearMemory} className="text-[11px] text-red-500">Xóa</button>
            </div>
          </section>
        )}

        {latestMatches.length > 0 && (
          <section>
            <h3 className="mb-2 flex items-center gap-2 text-sm font-semibold"><FaCompass /> Gợi ý gần nhất</h3>
            <div className="space-y-2">
              {latestMatches.slice(0, 3).map((property) => (
                <button key={property.id} onClick={() => onSelectProperty(property)} className="flex w-full gap-3 rounded-xl border border-black/5 p-2 text-left">
                  {property.image || property.media?.[0]?.url
                    ? <img src={property.image || property.media?.[0]?.url} alt="" className="h-14 w-14 rounded-lg object-cover" />
                    : <div className="grid h-14 w-14 place-items-center rounded-lg bg-stone-100">🏡</div>}
                  <span className="min-w-0">
                    <strong className="line-clamp-2 text-xs">{property.title}</strong>
                    <small className="text-[var(--coral)]">{formatPropertyPrice(property.list_price)}</small>
                  </span>
                </button>
              ))}
            </div>
          </section>
        )}

        {savedProperties.length > 0 && (
          <section>
            <h3 className="mb-2 flex items-center gap-2 text-sm font-semibold"><FaBookmark /> Đã lưu</h3>
            {savedProperties.slice(0, 3).map((property) => (
              <Link key={property.id} href={`/properties/${property.id}`} className="mb-1 block truncate rounded-xl bg-[#fbfaf7] px-3 py-2 text-xs">
                {property.title}
              </Link>
            ))}
          </section>
        )}

        <section className="rounded-2xl border border-black/5 p-4 text-xs text-[var(--muted)]">
          <p className="flex items-center gap-2 font-semibold text-[var(--ink)]"><FaShieldAlt /> Quy trình minh bạch</p>
          <p className="mt-2">Nera tìm căn, bạn chọn khung giờ, Sale xác nhận lịch thật.</p>
        </section>
      </div>
    </aside>
  );
}
