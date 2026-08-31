"use client";

import { FaClock, FaHome, FaMapMarkerAlt, FaMotorcycle, FaRoute } from "react-icons/fa";
import type { Property } from "@/lib/types";

const TRAVEL_MODE_LABEL: Record<string, string> = {
  DRIVE: "Ô tô",
  TWO_WHEELER: "Xe máy",
  WALK: "Đi bộ",
  BICYCLE: "Xe đạp",
  TRANSIT: "Phương tiện công cộng",
};

/** Grounded route summary — every figure comes from the Goong response, none is guessed. */
export default function RoutePanel({ property }: { property: Property }) {
  const evidence = property.distance_evidence;
  if (!evidence) return null;

  const rows = [
    {
      icon: <FaHome className="text-[var(--forest)]" />,
      label: "Từ",
      value: property.district ? `${property.district}${property.province ? `, ${property.province}` : ""}` : "Vị trí căn",
    },
    { icon: <FaMapMarkerAlt className="text-[var(--coral)]" />, label: "Đến", value: evidence.destination },
    { icon: <FaRoute className="text-[var(--forest)]" />, label: "Khoảng cách", value: `${evidence.distance_km} km` },
    { icon: <FaClock className="text-[var(--forest)]" />, label: "Thời gian di chuyển", value: `~${evidence.duration_minutes} phút` },
    {
      icon: <FaMotorcycle className="text-[var(--forest)]" />,
      label: "Phương tiện",
      value: TRAVEL_MODE_LABEL[evidence.travel_mode] ?? evidence.travel_mode,
    },
  ];

  return (
    <div className="mt-3 overflow-hidden rounded-xl border border-emerald-100 bg-[#f6faf7]">
      <p className="border-b border-emerald-100 px-4 py-2 text-xs font-bold uppercase tracking-wide text-[var(--forest)]">
        Thông tin lộ trình
      </p>
      <dl className="divide-y divide-emerald-100/70">
        {rows.map((row) => (
          <div key={row.label} className="flex items-center justify-between gap-3 px-4 py-2 text-xs">
            <dt className="flex items-center gap-2 font-medium text-[var(--muted)]">
              {row.icon}
              {row.label}
            </dt>
            <dd className="text-right font-semibold text-[var(--ink)]">{row.value}</dd>
          </div>
        ))}
      </dl>
      <p className="px-4 py-2 text-[10px] text-[var(--muted)]">
        {evidence.attribution ?? evidence.provider} · thời gian thay đổi theo giao thông thực tế
      </p>
    </div>
  );
}
