"use client";

import { useEffect, useState } from "react";
import { FaBell } from "react-icons/fa";
import { useAuth } from "./AuthProvider";
import { apiFetch, API_BASE } from "@/lib/api";

type Notice = { id: string; template_key: string; payload: Record<string, unknown>; status: string };

const getNoticeText = (item: Notice) => {
  const titleMap: Record<string, string> = {
    booking_request_received: "Đã gửi yêu cầu",
    booking_confirmed: "Lịch xem đã xác nhận",
    booking_cancelled_by_customer: "Khách hàng đã hủy lịch",
    sale_booking_request: "Yêu cầu xem nhà mới",
    sale_reschedule_request: "Khách hàng muốn dời lịch",
    booking_sale_reassigned: "Đang chuyển Sale khác",
    booking_needs_new_time: "Các Sale đều đã kín lịch",
    booking_request_expired: "Yêu cầu đã hết hạn",
  };
  const title = titleMap[item.template_key] || "Cập nhật lịch xem";
  
  let desc = String(item.payload.property_title ?? "Nera");
  if (item.template_key === "booking_cancelled_by_customer" && item.payload.reason) {
    desc = `${desc} - Lý do: ${item.payload.reason}`;
  } else if (item.template_key === "sale_reschedule_request") {
    desc = `Khách hàng đề xuất dời lịch cho căn ${desc}`;
  } else if (item.template_key === "booking_sale_reassigned") {
    desc = `Sale trước đang bận. Đang tìm chuyên viên mới cho căn ${desc}`;
  }
  
  return { title, desc };
};

export default function NotificationBell() {
  const { user } = useAuth();
  const [noticeOpen, setNoticeOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notice[]>([]);

  useEffect(() => {
    let active = true;
    let ws: WebSocket | null = null;
    let timer: number | null = null;
    let retryTimeout: number | null = null;

    const load = async () => {
      if (!user) { setNotifications([]); return; }
      try {
        const data = await apiFetch<{ items: Notice[] }>("/notifications");
        if (active) setNotifications(data.items);
      } catch { if (active) setNotifications([]); }
    };

    const setupWebSocket = () => {
      if (!user || !active) return;
      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      const host = window.location.host;
      const wsUrl = `${protocol}//${host}${API_BASE}/notifications/ws`;
      
      ws = new WebSocket(wsUrl);
      
      ws.onmessage = (event) => {
        try {
          const newNotice = JSON.parse(event.data) as Notice;
          if (active) {
            setNotifications(prev => {
              if (prev.some(n => n.id === newNotice.id)) return prev;
              return [newNotice, ...prev];
            });
          }
        } catch (e) {
          console.error("Failed to parse websocket message", e);
        }
      };

      ws.onclose = () => {
        if (active) {
          if (!timer) timer = window.setInterval(() => void load(), 3000);
          retryTimeout = window.setTimeout(() => {
            if (active) setupWebSocket();
          }, 5000);
        }
      };
      
      ws.onopen = () => {
        if (timer) {
          window.clearInterval(timer);
          timer = null;
        }
      };
    };

    void load();
    setupWebSocket();

    return () => {
      active = false;
      if (timer) window.clearInterval(timer);
      if (retryTimeout) window.clearTimeout(retryTimeout);
      if (ws) {
        ws.onclose = null;
        ws.close();
      }
    };
  }, [user]);

  async function markRead(id: string) {
    try {
      await apiFetch<void>(`/notifications/${id}/read`, { method: "POST" });
      setNotifications((items) => items.map((item) => item.id === id ? { ...item, status: "DELIVERED" } : item));
    } catch { /* Keep the notification available for a retry. */ }
  }

  if (!user) return null;

  return (
    <div className="relative">
      <button 
        onClick={() => setNoticeOpen((open) => !open)} 
        className="relative grid h-10 w-10 place-items-center rounded-full text-[var(--muted)] hover:bg-black/5 transition-colors" 
        aria-label="Thông báo" 
        aria-expanded={noticeOpen}
      >
        <FaBell />
        {notifications.some((item) => item.status === "PENDING") && (
          <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-[var(--coral)] ring-2 ring-[var(--paper)]" />
        )}
      </button>
      
      {noticeOpen && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setNoticeOpen(false)} />
          <div className="absolute right-0 top-12 z-50 w-80 rounded-2xl border border-black/5 bg-white p-3 shadow-[0_20px_60px_rgba(20,40,35,.16)]">
            <p className="px-2 pb-2 text-sm font-semibold text-[var(--ink)]">Thông báo</p>
            {notifications.length === 0 ? (
              <p className="rounded-xl bg-stone-50 p-4 text-xs text-[var(--muted)]">Chưa có cập nhật mới.</p>
            ) : (
              notifications.slice(0, 5).map((item) => { 
                const text = getNoticeText(item); 
                return (
                  <button 
                    key={item.id} 
                    onClick={() => void markRead(item.id)} 
                    className={`mb-1 w-full rounded-xl p-3 text-left text-xs hover:bg-stone-50 transition-colors ${item.status === "PENDING" ? "bg-[#eef5ef]" : ""}`}
                  >
                    <span className="font-semibold text-[var(--ink)]">{text.title}</span>
                    <span className="mt-1 block text-[var(--muted)]">{text.desc}</span>
                  </button>
                );
              })
            )}
          </div>
        </>
      )}
    </div>
  );
}
