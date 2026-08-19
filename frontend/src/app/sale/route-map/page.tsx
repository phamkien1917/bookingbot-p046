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
    if (!document.getElementById("routing-css")) {
      const link = document.createElement("link");
      link.id = "routing-css";
      link.rel = "stylesheet";
      link.href = "https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.css";
      document.head.appendChild(link);
    }
    
    let isCancelled = false;
    let map: any = null;
    let routingControl: any = null;

    function loadScripts() {
      if (!document.getElementById("leaflet-js")) {
        const script = document.createElement("script");
        script.id = "leaflet-js";
        script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
        script.onload = () => {
          if (!document.getElementById("routing-js")) {
            const rScript = document.createElement("script");
            rScript.id = "routing-js";
            rScript.src = "https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.js";
            rScript.onload = initMap;
            document.head.appendChild(rScript);
          } else {
            initMap();
          }
        };
        document.head.appendChild(script);
      } else {
        if (!document.getElementById("routing-js")) {
            const rScript = document.createElement("script");
            rScript.id = "routing-js";
            rScript.src = "https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.js";
            rScript.onload = initMap;
            document.head.appendChild(rScript);
        } else {
            setTimeout(initMap, 50);
        }
      }
    }

    function initMap() {
      if (isCancelled) return;
      
      const L = (window as any).L;
      if (!L || !L.Routing) {
        setTimeout(initMap, 50);
        return;
      }
      
      const container = document.getElementById("route-map");
      if (!container) return;
      
      // Clean up previous map if it exists
      if ((container as any)._leaflet_id) {
          (container as any).outerHTML = '<div id="route-map" class="w-full h-full rounded-[1.5rem] border border-black/5 bg-[#f7f5ef] z-0 shadow-inner min-h-[400px]"></div>';
      }
      
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

      setTimeout(() => { if (map && !isCancelled) map.invalidateSize(); }, 500);

      if (validPoints.length === 0) return;

      const waypoints = validPoints.map(p => L.latLng(p.property!.latitude, p.property!.longitude));
      
      const groupedPoints: Record<string, { apts: CalendarAppointment[], indices: number[] }> = {};
      validPoints.forEach((apt, i) => {
        const key = `${apt.property!.latitude},${apt.property!.longitude}`;
        if (!groupedPoints[key]) groupedPoints[key] = { apts: [], indices: [] };
        groupedPoints[key].apts.push(apt);
        groupedPoints[key].indices.push(i + 1);
      });

      Object.values(groupedPoints).forEach(group => {
        const label = group.indices.join(', ');
        const width = 24 + (group.indices.length - 1) * 8;
        const iconHtml = `<div style="background:var(--forest);color:white;width:${width}px;height:24px;border-radius:12px;text-align:center;line-height:24px;font-weight:bold;border:2px solid white;box-shadow:0 2px 4px rgba(0,0,0,0.3);font-size:11px;">${label}</div>`;
        const customIcon = L.divIcon({
          html: iconHtml,
          className: '',
          iconSize: [width, 24],
          iconAnchor: [width / 2, 12]
        });

        const popupContent = group.apts.map(apt => {
          const timeString = new Date(apt.starts_at).toLocaleTimeString('vi-VN', {hour: '2-digit', minute: '2-digit'});
          return `<b>${apt.property!.title}</b><br/>${timeString} - ${apt.status}`;
        }).join('<hr style="margin:8px 0; border-color:#eee;" />');

        L.marker([group.apts[0].property!.latitude, group.apts[0].property!.longitude], {icon: customIcon})
          .addTo(map)
          .bindPopup(popupContent);
      });

      if (waypoints.length > 1) {
        routingControl = L.Routing.control({
          waypoints: waypoints,
          lineOptions: {
            styles: [{color: 'var(--coral)', weight: 4, opacity: 0.8}],
            extendToWaypoints: true,
            missingRouteTolerance: 10
          },
          show: false,
          addWaypoints: false,
          draggableWaypoints: false,
          fitSelectedRoutes: true,
          showAlternatives: false,
          createMarker: function() { return null; }
        }).addTo(map);
      } else if (waypoints.length === 1) {
        map.setView(waypoints[0], 15);
      }
    }

    loadScripts();

    return () => {
      isCancelled = true;
      if (routingControl && map) {
        map.removeControl(routingControl);
      }
      if (map) {
        map.remove();
      }
    };
  }, [appointments]);

  return <div id="route-map" className="w-full h-full rounded-[1.5rem] border border-black/5 bg-[#f7f5ef] z-0 shadow-inner min-h-[400px]"></div>;
}

export default function RouteMapPage() {
  const [allAppointments, setAllAppointments] = useState<CalendarAppointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [optimizing, setOptimizing] = useState(false);
  const [error, setError] = useState("");
  const [selectedDate, setSelectedDate] = useState(() => new Date().toISOString().slice(0, 10));
  
  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await apiFetch<CalendarAppointment[]>("/sale/schedule");
      setAllAppointments(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Lỗi tải dữ liệu");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void load(); }, [load]);

  const handleOptimize = async () => {
    setOptimizing(true);
    setError("");
    try {
      await apiFetch(`/sale/optimize-route?date=${selectedDate}`, { method: "POST" });
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Lỗi tối ưu lộ trình");
    } finally {
      setOptimizing(false);
    }
  };

  const filteredAppointments = allAppointments.filter(a => {
    if (a.status === 'NO_SHOW' || a.status === 'CANCELLED') return false;
    const localDate = new Date(a.starts_at);
    const localStr = localDate.getFullYear() + "-" + 
                     String(localDate.getMonth() + 1).padStart(2, '0') + "-" + 
                     String(localDate.getDate()).padStart(2, '0');
    return localStr === selectedDate;
  });
  const sortedPoints = [...filteredAppointments].sort((a, b) => new Date(a.starts_at).getTime() - new Date(b.starts_at).getTime());

  return (
    <ProtectedPage roles={["SALE"]}>
      <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)] font-sans flex flex-col">
        <Header />
        <main className="flex-1 max-w-7xl mx-auto px-4 py-6 w-full flex flex-col h-[calc(100vh-80px)]">
          
          <div className="mb-4">
            <Link href="/sale" className="text-sm text-[var(--muted)] flex items-center mb-2 hover:text-[var(--ink)] w-fit"><FaArrowLeft className="mr-2"/> Về Dashboard</Link>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h1 className="text-2xl font-bold">Lộ trình</h1>
                <p className="text-sm text-[var(--muted)] mt-1">{sortedPoints.length} điểm đến được phân công</p>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={handleOptimize}
                  disabled={optimizing || sortedPoints.length < 2}
                  className="text-sm font-bold bg-[var(--forest)] text-white px-4 py-2 rounded-xl disabled:opacity-50"
                >
                  {optimizing ? "Đang tối ưu..." : "Tối ưu lộ trình"}
                </button>
                <input 
                  type="date" 
                  className="text-sm border border-gray-300 rounded-xl px-4 py-2 bg-white font-semibold text-[var(--ink)] outline-none focus:border-[var(--forest)] focus:ring-2 focus:ring-[var(--forest)]/20 shadow-sm"
                  value={selectedDate}
                  onChange={e => setSelectedDate(e.target.value)}
                />
              </div>
            </div>
          </div>
          
          <div className="flex-1 flex flex-col md:flex-row gap-6 min-h-0">
            <div className="w-full md:w-80 flex flex-col">
              <div className="flex-1 bg-white rounded-[1.5rem] border border-black/5 shadow-sm p-4 overflow-y-auto">
                {loading ? (
                  <div className="py-10 text-center"><FaSpinner className="animate-spin text-2xl text-[var(--forest)] mx-auto" /></div>
                ) : error ? (
                  <p className="text-red-500 text-sm">{error}</p>
                ) : sortedPoints.length === 0 ? (
                  <p className="text-center text-[var(--muted)] py-10 text-sm">Không có lịch hẹn nào vào ngày này.</p>
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
              <MapComponent appointments={filteredAppointments} />
            </div>
          </div>
          
        </main>
      </div>
    </ProtectedPage>
  );
}
