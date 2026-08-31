"use client";

/* eslint-disable @typescript-eslint/no-explicit-any -- Leaflet is loaded dynamically from its browser bundle. */

import { useEffect, useMemo, useRef } from "react";
import type { Property } from "@/lib/types";

function escapeHtml(value: string): string {
  return value.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[character] as string);
}

// Price bands come from the result set itself, not fixed VND thresholds — the
// same map has to read correctly for a 5 triệu/tháng rental and a 5 tỷ sale.
const BANDS = [
  { color: "#2f9e63", label: "Rẻ nhất nhóm" },
  { color: "#c8a02c", label: "Dưới trung vị" },
  { color: "#e07a3c", label: "Trên trung vị" },
  { color: "#c8453c", label: "Cao nhất nhóm" },
] as const;

function quartileCuts(prices: number[]): [number, number, number] {
  const sorted = [...prices].sort((a, b) => a - b);
  const at = (fraction: number) => sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * fraction))];
  return [at(0.25), at(0.5), at(0.75)];
}

function bandIndex(price: number | null | undefined, cuts: [number, number, number]): number {
  if (price == null) return 1;
  if (price <= cuts[0]) return 0;
  if (price <= cuts[1]) return 1;
  if (price <= cuts[2]) return 2;
  return 3;
}

// Handles both sale prices (tỷ) and rents (triệu) — and the k/m² range a
// per-square-metre rent falls into, which would otherwise round to "0 tr".
function shortPrice(value: number | null | undefined): string {
  if (value == null) return "—";
  if (value >= 1_000_000_000) return `${(value / 1_000_000_000).toFixed(1).replace(/\.0$/, "")} tỷ`;
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1).replace(/\.0$/, "")} tr`;
  if (value >= 1_000) return `${Math.round(value / 1_000)}k`;
  return `${Math.round(value)}đ`;
}

function median(values: number[]): number | null {
  if (values.length === 0) return null;
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.floor(sorted.length / 2)];
}

export default function PropertiesMap({ properties }: { properties: Property[] }) {
  const mapRef = useRef<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Context strip: what the customer is actually looking at right now.
  const summary = useMemo(() => {
    const withPrice = properties.filter((p) => p.list_price != null);
    const districts = new Map<string, number>();
    properties.forEach((p) => {
      if (p.district) districts.set(p.district, (districts.get(p.district) ?? 0) + 1);
    });
    const topDistrict = [...districts.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];
    const perSqm = withPrice
      .filter((p) => p.area_sqm > 0)
      .map((p) => (p.list_price as number) / p.area_sqm);
    const focus = properties.find((p) => p.distance_evidence?.destination);
    return {
      count: properties.length,
      district: topDistrict,
      medianPrice: median(withPrice.map((p) => p.list_price as number)),
      medianPerSqm: median(perSqm),
      destination: focus?.distance_evidence?.destination,
      nearestKm: focus ? Math.min(...properties.filter((p) => p.distance_evidence).map((p) => p.distance_evidence!.distance_km)) : null,
    };
  }, [properties]);

  useEffect(() => {
    if (!document.getElementById("leaflet-css")) {
      const link = document.createElement("link");
      link.id = "leaflet-css";
      link.rel = "stylesheet";
      link.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
      document.head.appendChild(link);
    }

    let isCancelled = false;

    function initMap() {
      if (isCancelled || !containerRef.current) return;
      const L = (window as any).L;
      if (!L) {
        setTimeout(initMap, 50);
        return;
      }

      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }

      const validProps = properties.filter((p) => p.latitude && p.longitude);

      const center =
        validProps.length > 0
          ? [validProps[0].latitude, validProps[0].longitude]
          : [21.028511, 105.804817]; // Hanoi default

      const map = L.map(containerRef.current).setView(center, 12);
      mapRef.current = map;

      L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png", {
        attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
        maxZoom: 19,
        subdomains: "abcd",
      }).addTo(map);

      const prices = validProps.map((p) => p.list_price).filter((v): v is number => v != null);
      const cuts = prices.length > 0 ? quartileCuts(prices) : ([0, 0, 0] as [number, number, number]);
      const bounds: [number, number][] = [];

      // Search radius around the place the customer named, so "gần" is visible.
      const withDestination = validProps.find(
        (p) => p.distance_evidence?.destination_lat != null && p.distance_evidence?.destination_lng != null,
      );
      const destination = withDestination?.distance_evidence;
      if (destination?.destination_lat != null && destination.destination_lng != null) {
        const target: [number, number] = [destination.destination_lat, destination.destination_lng];
        const radiusKm = Math.max(
          ...validProps.filter((p) => p.distance_evidence).map((p) => p.distance_evidence!.distance_km),
          0.5,
        );
        L.circle(target, {
          radius: radiusKm * 1000,
          color: "#e07a3c",
          weight: 1.5,
          dashArray: "6 6",
          fillColor: "#e07a3c",
          fillOpacity: 0.06,
        }).addTo(map);
        L.marker(target, {
          icon: L.divIcon({
            className: "",
            html: `<div style="background:#1f3d34;color:#fff;font:600 11px/1 system-ui,sans-serif;padding:6px 10px;border-radius:999px;white-space:nowrap;box-shadow:0 2px 8px rgba(0,0,0,.25)">📍 ${escapeHtml(destination.destination)}</div>`,
            iconAnchor: [0, 10],
          }),
        }).addTo(map);
        bounds.push(target);
      }

      validProps.forEach((p) => {
        const point: [number, number] = [p.latitude as number, p.longitude as number];
        bounds.push(point);
        const band = BANDS[bandIndex(p.list_price, cuts)];
        const marker = L.marker(point, {
          icon: L.divIcon({
            className: "",
            html: `<div style="background:${band.color};color:#fff;font:700 11px/1 system-ui,sans-serif;padding:5px 9px;border-radius:999px;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,.28);border:1.5px solid rgba(255,255,255,.85)">${escapeHtml(shortPrice(p.list_price))}</div>`,
            iconAnchor: [22, 12],
          }),
        }).addTo(map);
        const distance = p.distance_evidence
          ? `<br/><span style="color:#2f9e63;">${p.distance_evidence.distance_km} km · ${p.distance_evidence.duration_minutes} phút</span>`
          : "";
        marker.bindPopup(
          `<div style="font-family: sans-serif; font-size: 13px;"><b>${escapeHtml(p.title)}</b><br/><span style="color: #666;">${escapeHtml(p.district ?? "")}, ${escapeHtml(p.province ?? "")}</span><br/><b style="color: #c86843;">${escapeHtml(shortPrice(p.list_price))}</b>${distance}</div>`,
        );
      });

      if (bounds.length > 1) {
        map.fitBounds(L.latLngBounds(bounds).pad(0.15));
      }

      setTimeout(() => {
        if (!isCancelled && mapRef.current) {
          mapRef.current.invalidateSize();
        }
      }, 150);
    }

    if (!document.getElementById("leaflet-js")) {
      const script = document.createElement("script");
      script.id = "leaflet-js";
      script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
      script.onload = initMap;
      document.head.appendChild(script);
    } else {
      setTimeout(initMap, 50);
    }

    return () => {
      isCancelled = true;
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, [properties]);

  return (
    <div className="relative h-full w-full">
      {/* No id: the chat renders one map per result turn, so it cannot be unique. */}
      <div
        ref={containerRef}
        className="w-full h-full rounded-[1.5rem] border border-black/5 bg-[#f7f5ef] z-0 shadow-inner overflow-hidden"
      />

      {/* Context chips */}
      <div className="pointer-events-none absolute left-4 top-4 z-[400] flex flex-wrap gap-2">
        <span className="rounded-full bg-white/95 px-3 py-1.5 text-xs font-semibold text-[var(--ink)] shadow-sm ring-1 ring-black/5">
          {summary.count} căn phù hợp{summary.district ? ` · ${summary.district}` : ""}
        </span>
        {summary.medianPerSqm != null && (
          <span className="rounded-full bg-white/95 px-3 py-1.5 text-xs font-semibold text-[var(--muted)] shadow-sm ring-1 ring-black/5">
            Phổ biến ~{shortPrice(summary.medianPrice)} · ~{shortPrice(summary.medianPerSqm)}/m²
          </span>
        )}
        {summary.destination && summary.nearestKm != null && Number.isFinite(summary.nearestKm) && (
          <span className="rounded-full bg-white/95 px-3 py-1.5 text-xs font-semibold text-[var(--forest)] shadow-sm ring-1 ring-black/5">
            Gần {summary.destination} ~{summary.nearestKm} km
          </span>
        )}
      </div>

      {/* Price legend */}
      <div className="pointer-events-none absolute bottom-4 left-4 z-[400] rounded-xl bg-white/95 px-3 py-2.5 shadow-sm ring-1 ring-black/5">
        <p className="mb-1.5 text-[11px] font-bold uppercase tracking-wide text-[var(--muted)]">Giá so với nhóm</p>
        <div className="space-y-1">
          {BANDS.map((band) => (
            <p key={band.label} className="flex items-center gap-2 text-[11px] font-medium text-[var(--ink)]">
              <span className="h-2.5 w-2.5 rounded-full" style={{ background: band.color }} />
              {band.label}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}
