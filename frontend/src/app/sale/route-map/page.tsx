"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { FaArrowLeft, FaClock, FaMapMarkerAlt, FaSpinner } from "react-icons/fa";
import ProtectedPage from "@/components/ProtectedPage";
import Header from "@/components/Header";
import { apiFetch } from "@/lib/api";

interface CalendarAppointment {
  id: string;
  booking_code: string;
  status: string;
  starts_at: string;
  ends_at: string;
  property: { id: string; title: string; address: string; latitude: number | null; longitude: number | null } | null;
}

function MapComponent({ appointments }: { appointments: CalendarAppointment[] }) {
  useEffect(() => {
    // Dynamically load leaflet css and js
    if (!document.getElementById("leaflet-css")) {
      const link = document.createElement("link");
      link.id = "leaflet-css";
      link.rel = "stylesheet";
      link.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
      document.head.appendChild(link);
    }
    
    if (!document.getElementById("leaflet-js")) {
      const script = document.createElement("script");
      script.id = "leaflet-js";
      script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
      script.onload = initMap;
      document.head.appendChild(script);
    } else {
      // If already loaded from another navigation
      // Need a small timeout to ensure DOM is ready
      setTimeout(initMap, 100);
    }

    let map: any = null;

    function initMap() {
      const L = (window as any).L;
      if (!L || !document.getElementById("route-map") || (document.getElementById("route-map") as any)._leaflet_id) return;
      
      const validPoints = appointments
        .filter(a => a.property?.latitude && a.property?.longitude)
        .sort((a, b) => new Date(a.starts_at).getTime() - new Date(b.starts_at).getTime());

      // Center around HCMC or first point
      const center = validPoints.length > 0 
        ? [validPoints[0].property!.latitude, validPoints[0].property!.longitude]
        : [10.762622, 106.660172];
        
      map = L.map('route-map').setView(center, 13);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map);

      if (validPoints.length === 0) return;

      const latlngs = validPoints.map(p => [p.property!.latitude, p.property!.longitude]);
      
      // Draw path line
      if (latlngs.length > 1) {
        L.polyline(latlngs, {color: 'var(--coral)', weight: 4, opacity: 0.7, dashArray: '10, 10'}).addTo(map);
      }

      // Add markers
      validPoints.forEach((apt, i) => {
        const iconHtml = `<div style="background:var(--forest);color:white;width:24px;height:24px;border-radius:50%;text-align:center;line-height:24px;font-weight:bold;border:2px solid white;box-shadow:0 2px 4px rgba(0,0,0,0.3);">${i + 1}</div>`;
        const customIcon = L.divIcon({
          html: iconHtml,
          className: '',
          iconSize: [24, 24],
          iconAnchor: [12, 12]
        });

        const timeString = new Date(apt.starts_at).toLocaleTimeString('vi-VN', {hour: '2-digit', minute: '2-digit'});
        L.marker([apt.property!.latitude, apt.property!.longitude], {icon: customIcon})
          .addTo(map)
          .bindPopup(`<b>${apt.property!.title}</b><br/>${timeString} - ${apt.status}`);
      });
      
      if (latlngs.length > 1) {
        map.fitBounds(L.latLngBounds(latlngs), { padding: [50, 50] });
      }
    }

    return () => {
      if (map) {
        map.remove();
      }
    };
  }, [appointments]);

  return <div id="route-map" className="w-full h-full rounded-[1.5rem] border border-black/5 bg-[#f7f5ef] z-0 shadow-inner min-h-[400px]"></div>;
}

export default function RouteMapPage() {
  const [appointments, setAppointments] = useState<CalendarAppointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await apiFetch<CalendarAppointment[]>("/sale/schedule");
      // Filter for today only
      const todayStr = new Date().toISOString().slice(0, 10);
      const todayAppointments = res.filter(a => a.starts_at.startsWith(todayStr));
      setAppointments(todayAppointments);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Lỗi tải dữ liệu");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void load(); }, [load]);

  const sortedPoints = [...appointments].sort((a, b) => new Date(a.starts_at).getTime() - new Date(b.starts_at).getTime());

  return (
    <ProtectedPage roles={["SALE"]}>
      <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)] font-sans flex flex-col">
        <Header />
        <main className="flex-1 max-w-7xl mx-auto px-4 py-6 w-full flex flex-col md:flex-row gap-6 h-[calc(100vh-80px)]">
          
          <div className="w-full md:w-80 flex flex-col gap-4">
            <div>
              <Link href="/sale" className="text-sm text-[var(--muted)] flex items-center mb-2 hover:text-[var(--ink)]"><FaArrowLeft className="mr-2"/> Về Dashboard</Link>
              <h1 className="text-2xl font-bold">Lộ trình hôm nay</h1>
              <p className="text-sm text-[var(--muted)] mt-1">
                {sortedPoints.length} điểm đến được tối ưu
              </p>
            </div>
            
            <div className="flex-1 bg-white rounded-[1.5rem] border border-black/5 shadow-sm p-4 overflow-y-auto">
              {loading ? (
                <div className="py-10 text-center"><FaSpinner className="animate-spin text-2xl text-[var(--forest)] mx-auto" /></div>
              ) : error ? (
                <p className="text-red-500 text-sm">{error}</p>
              ) : sortedPoints.length === 0 ? (
                <p className="text-center text-[var(--muted)] py-10 text-sm">Không có lịch hẹn nào hôm nay.</p>
              ) : (
                <div className="relative pl-6 border-l-2 border-[var(--forest)]/20 space-y-6 pb-2">
                  {sortedPoints.map((apt, i) => (
                    <div key={apt.id} className="relative">
                      <div className="absolute -left-[35px] top-1 w-6 h-6 rounded-full bg-[var(--forest)] text-white text-xs font-bold flex items-center justify-center shadow-sm">
                        {i + 1}
                      </div>
                      <p className="text-xs font-bold text-[var(--coral)] flex items-center gap-1.5 mb-1">
                        <FaClock /> {new Date(apt.starts_at).toLocaleTimeString('vi-VN', {hour: '2-digit', minute: '2-digit'})}
                      </p>
                      <p className="font-semibold text-sm leading-snug">{apt.property?.title || apt.booking_code}</p>
                      <p className="text-xs text-[var(--muted)] mt-1 line-clamp-2"><FaMapMarkerAlt className="inline mr-1"/>{apt.property?.address}</p>
                      <span className="inline-block mt-2 px-2 py-0.5 text-[10px] font-bold bg-[#f7f5ef] text-[var(--muted)] rounded uppercase tracking-wide">
                        {apt.status}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
          
          <div className="flex-1 min-h-[400px] h-full relative">
            <MapComponent appointments={appointments} />
          </div>
          
        </main>
      </div>
    </ProtectedPage>
  );
}
