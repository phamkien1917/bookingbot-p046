"use client";

import { useEffect, useRef } from "react";
import type { Property } from "@/lib/types";

export default function PropertiesMap({ properties }: { properties: Property[] }) {
  const mapRef = useRef<any>(null);

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
      if (isCancelled) return;
      const L = (window as any).L;
      if (!L) {
        setTimeout(initMap, 50);
        return;
      }
      
      const container = document.getElementById("properties-map-container");
      if (!container) return;

      if ((container as any)._leaflet_id) {
          (container as any).outerHTML = '<div id="properties-map-container" class="w-full h-full rounded-[1.5rem] border border-black/5 bg-[#f7f5ef] z-0 shadow-inner"></div>';
      }

      const validProps = properties.filter(p => p.latitude && p.longitude);
      
      const center = validProps.length > 0 
        ? [validProps[0].latitude, validProps[0].longitude]
        : [10.762622, 106.660172];

      const map = L.map("properties-map-container").setView(center, 13);
      mapRef.current = map;

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
      }).addTo(map);

      validProps.forEach(p => {
        const marker = L.marker([p.latitude, p.longitude]).addTo(map);
        marker.bindPopup(`<b>${p.title}</b><br/>${p.district}, ${p.province}<br/>${(p.list_price / 1000000000).toFixed(2)} tỷ`);
      });
      
      if (validProps.length > 1) {
          const group = new L.featureGroup(validProps.map(p => L.marker([p.latitude, p.longitude])));
          map.fitBounds(group.getBounds().pad(0.1));
      }
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

  return <div id="properties-map-container" className="w-full h-full rounded-[1.5rem] border border-black/5 bg-[#f7f5ef] z-0 shadow-inner"></div>;
}
