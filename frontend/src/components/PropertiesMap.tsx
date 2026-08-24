"use client";

/* eslint-disable @typescript-eslint/no-explicit-any -- Leaflet is loaded dynamically from its browser bundle. */

import { useEffect, useRef } from "react";
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

export default function PropertiesMap({ properties }: { properties: Property[] }) {
  const mapRef = useRef<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);

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

      validProps.forEach((p) => {
        const marker = L.marker([p.latitude, p.longitude]).addTo(map);
        const price = p.list_price == null ? "Liên hệ" : `${(p.list_price / 1000000000).toFixed(2)} tỷ`;
        marker.bindPopup(
          `<div style="font-family: sans-serif; font-size: 13px;"><b>${escapeHtml(p.title)}</b><br/><span style="color: #666;">${escapeHtml(p.district ?? "")}, ${escapeHtml(p.province ?? "")}</span><br/><b style="color: #c86843;">${price}</b></div>`,
        );
      });

      if (validProps.length > 1) {
        const group = new L.featureGroup(validProps.map((p) => L.marker([p.latitude, p.longitude])));
        map.fitBounds(group.getBounds().pad(0.1));
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
    <div
      ref={containerRef}
      id="properties-map-container"
      className="w-full h-full rounded-[1.5rem] border border-black/5 bg-[#f7f5ef] z-0 shadow-inner overflow-hidden"
    />
  );
}
