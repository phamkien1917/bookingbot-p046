"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  FaBars,
  FaBell,
  FaCalendarAlt,
  FaCheck,
  FaCheckCircle,
  FaClock,
  FaExclamationCircle,
  FaList,
  FaMapMarkerAlt,
  FaRobot,
  FaSignOutAlt,
  FaSyncAlt,
  FaTh,
  FaTimes,
  FaTimesCircle,
  FaUserCheck,
} from "react-icons/fa";
import ProtectedPage from "@/components/ProtectedPage";
import { useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";
import NotificationBell from "@/components/NotificationBell";

interface SaleOverview {
  user: { id: string; full_name: string };
  stats: { pending: number; confirmed: number };
  pending_requests: SaleBooking[];
  schedule: SaleBooking[];
}
interface SaleBooking {
  id: string;
  request_code: string;
  status: string;
  preferred_start: string;
  preferred_end: string;
  expires_at?: string;
  customer_note?: string;
  customer?: { full_name: string; phone: string; email: string };
  property: { id: string; title: string; address: string; is_stale?: boolean; verification_label?: string | null };
}
interface CalendarAppointment {
  id: string;
  booking_code: string;
  status: string;
  starts_at: string;
  ends_at: string;
  customer_user_id: string;
  customer_note?: string;
  checked_in_at: string | null;
  property: { id: string; title: string; address: string } | null;
}

const STATUS_COLORS: Record<string, { bg: string; dot: string; text: string }> = {
  WAITING_APPROVAL: { bg: "bg-amber-50 border-amber-200", dot: "bg-amber-500", text: "text-amber-700" },
  CONFIRMED: { bg: "bg-emerald-50 border-emerald-200", dot: "bg-emerald-500", text: "text-emerald-700" },
  IN_PROGRESS: { bg: "bg-blue-50 border-blue-200", dot: "bg-blue-500", text: "text-blue-700" },
  COMPLETED: { bg: "bg-stone-50 border-stone-200", dot: "bg-stone-400", text: "text-stone-600" },
  NO_SHOW: { bg: "bg-red-50 border-red-200", dot: "bg-red-500", text: "text-red-700" },
};
const STATUS_LABELS: Record<string, string> = {
  WAITING_APPROVAL: "Đang chờ",
  CONFIRMED: "Đã xác nhận",
  IN_PROGRESS: "Đang diễn ra",
  COMPLETED: "Hoàn thành",
  NO_SHOW: "Không đến",
};

const HOURS = Array.from({ length: 12 }, (_, i) => 7 + i); // 7:00 – 18:00

function WeekCalendar({
  appointments,
  onAction,
}: {
  appointments: CalendarAppointment[];
  onAction: (id: string, action: "check-in" | "no-show" | "complete" | "accept" | "reject") => void;
}) {
  const now = new Date();
  const monday = new Date(now);
  monday.setDate(now.getDate() - ((now.getDay() + 6) % 7));
  monday.setHours(0, 0, 0, 0);

  const days = Array.from({ length: 7 }, (_, i) => {
    const d = new Date(monday);
    d.setDate(d.getDate() + i);
    return d;
  });

  const dayNames = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"];

  function getBlocks(day: Date) {
    const dayStr = day.getFullYear() + "-" + String(day.getMonth() + 1).padStart(2, '0') + "-" + String(day.getDate()).padStart(2, '0');
    return appointments.filter((a) => {
      if (!a.starts_at) return false;
      const localDate = new Date(a.starts_at);
      const localStr = localDate.getFullYear() + "-" + String(localDate.getMonth() + 1).padStart(2, '0') + "-" + String(localDate.getDate()).padStart(2, '0');
      return localStr === dayStr;
    });
  }

  function getPosition(a: CalendarAppointment) {
    const start = new Date(a.starts_at);
    const end = new Date(a.ends_at);
    const topHour = start.getHours() + start.getMinutes() / 60 - 7;
    const duration = (end.getTime() - start.getTime()) / 3600000;
    return { top: `${(topHour / 12) * 100}%`, height: `${(duration / 12) * 100}%` };
  }

  const [popup, setPopup] = useState<CalendarAppointment | null>(null);

  return (
    <>
      <div className="overflow-x-auto rounded-[1.5rem] border border-black/5 bg-white shadow-sm">
        <div className="grid min-w-[700px]" style={{ gridTemplateColumns: "56px repeat(7, 1fr)" }}>
          {/* Header */}
          <div className="border-b border-r border-black/5 bg-[#f7f7f3] p-2" />
          {days.map((d, i) => {
            const isToday = d.toDateString() === now.toDateString();
            return (
              <div key={i} className={`border-b border-r border-black/5 p-3 text-center text-xs ${isToday ? "bg-[var(--forest)]/10 font-bold text-[var(--forest)]" : "bg-[#f7f7f3]"}`}>
                <div className="font-bold">{dayNames[i]}</div>
                <div>{d.getDate()}/{d.getMonth() + 1}</div>
              </div>
            );
          })}

          {/* Time column + day columns */}
          <div className="border-r border-black/5">
            {HOURS.map((h) => (
              <div key={h} className="flex h-14 items-center justify-center border-b border-black/5 text-[10px] text-[var(--muted)]">
                {h}:00
              </div>
            ))}
          </div>
          {days.map((d, di) => {
            const blocks = getBlocks(d);
            return (
              <div key={di} className="relative border-r border-black/5">
                {HOURS.map((h) => (
                  <div key={h} className="h-14 border-b border-black/5" />
                ))}
                {blocks.map((a) => {
                  const pos = getPosition(a);
                  const color = a.status === "WAITING_APPROVAL" ? "bg-amber-50 border-l-amber-400" : a.status === "CONFIRMED" ? "bg-emerald-50 border-l-emerald-500" : a.status === "IN_PROGRESS" ? "bg-blue-50 border-l-blue-500" : a.status === "COMPLETED" ? "bg-stone-50 border-l-stone-400" : "bg-red-50 border-l-red-400";
                  return (
                    <button
                      key={a.id}
                      onClick={() => setPopup(a)}
                      className={`absolute inset-x-1 rounded-lg border-l-4 ${color} p-1.5 text-left text-[10px] leading-tight shadow-sm transition hover:shadow-md cursor-pointer overflow-hidden`}
                      style={{ top: pos.top, height: pos.height, minHeight: 28 }}
                    >
                      <p className="font-semibold line-clamp-1">{a.property?.title ?? a.booking_code}</p>
                      <p className="text-[9px] text-[var(--muted)] line-clamp-1">{new Date(a.starts_at).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" })}</p>
                    </button>
                  );
                })}
              </div>
            );
          })}
        </div>
      </div>

      {/* Popup detail */}
      {popup && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" onClick={() => setPopup(null)}>
          <div className="w-full max-w-md rounded-[1.5rem] bg-white p-6 shadow-xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-xs text-[var(--muted)]">Mã booking</p>
                <p className="text-lg font-bold">{popup.booking_code}</p>
              </div>
              <button onClick={() => setPopup(null)} className="text-[var(--muted)] hover:text-[var(--ink)]"><FaTimes /></button>
            </div>
            <div className="space-y-3 text-sm">
              <p><FaCalendarAlt className="inline mr-2 text-[var(--forest)]" /><strong>Thời gian:</strong> {new Date(popup.starts_at).toLocaleString("vi-VN")} – {new Date(popup.ends_at).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" })}</p>
              <p><FaRobot className="inline mr-2 text-[var(--forest)]" /><strong>BĐS:</strong> {popup.property?.title ?? "N/A"}</p>
              <p className="text-xs text-[var(--muted)]">{popup.property?.address}</p>
              {popup.customer_note && <p className="text-xs bg-[#f7f5ef] p-3 rounded-xl italic">&quot;{popup.customer_note}&quot;</p>}
              <p className="flex items-center gap-2">
                <span className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold border ${STATUS_COLORS[popup.status]?.bg ?? "bg-stone-50 border-stone-200"} ${STATUS_COLORS[popup.status]?.text ?? "text-stone-600"}`}>
                  <span className={`h-1.5 w-1.5 rounded-full ${STATUS_COLORS[popup.status]?.dot ?? "bg-stone-400"} ${popup.status === "IN_PROGRESS" || popup.status === "WAITING_APPROVAL" ? "animate-pulse" : ""}`} />
                  {STATUS_LABELS[popup.status] ?? popup.status}
                </span>
              </p>
            </div>
            {popup.status === "WAITING_APPROVAL" && (
              <div className="mt-5 flex gap-2">
                <button onClick={() => { onAction(popup.id, "accept"); setPopup(null); }} className="flex-1 flex items-center justify-center gap-2 rounded-xl bg-[var(--forest)] py-2.5 text-sm font-semibold text-white">✓ Nhận</button>
                <button onClick={() => { onAction(popup.id, "reject"); setPopup(null); }} className="flex-1 flex items-center justify-center gap-2 rounded-xl border border-[var(--coral)] py-2.5 text-sm font-semibold text-[var(--coral)]">✗ Từ chối</button>
              </div>
            )}
            {popup.status === "CONFIRMED" && (
              <div className="mt-5 flex gap-2">
                <button onClick={() => { onAction(popup.id, "check-in"); setPopup(null); }} className="flex-1 flex items-center justify-center gap-2 rounded-xl bg-[var(--forest)] py-2.5 text-sm font-semibold text-white"><FaUserCheck /> Check-in</button>
                <button onClick={() => { onAction(popup.id, "no-show"); setPopup(null); }} className="flex-1 flex items-center justify-center gap-2 rounded-xl bg-red-500 py-2.5 text-sm font-semibold text-white"><FaTimesCircle /> No-show</button>
              </div>
            )}
            {popup.status === "IN_PROGRESS" && (
              <button onClick={() => { onAction(popup.id, "complete"); setPopup(null); }} className="mt-5 w-full flex items-center justify-center gap-2 rounded-xl bg-[var(--ink)] py-2.5 text-sm font-semibold text-white"><FaCheckCircle /> Hoàn thành</button>
            )}
          </div>
        </div>
      )}
    </>
  );
}

function SaleDashboardContent() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [overview, setOverview] = useState<SaleOverview | null>(null);
  const [appointments, setAppointments] = useState<CalendarAppointment[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [reject, setReject] = useState<{ id: string; reason: string } | null>(null);
  const [view, setView] = useState<"calendar" | "list">("calendar");
  const [verified, setVerified] = useState<Set<string>>(new Set());
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const load = useCallback(async (quiet = false) => {
    if (!quiet) setLoading(true);
    try {
      const [ov, cal] = await Promise.all([
        apiFetch<SaleOverview>("/sale/overview"),
        apiFetch<CalendarAppointment[]>("/sale/schedule"),
      ]);
      setOverview(ov);
      setAppointments(cal);
      setError("");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Lỗi tải dữ liệu");
    } finally {
      if (!quiet) setLoading(false);
    }
  }, []);

  useEffect(() => {
    const initial = window.setTimeout(() => void load(), 0);
    const interval = window.setInterval(() => void load(true), 15_000);
    return () => { window.clearTimeout(initial); window.clearInterval(interval); };
  }, [load]);

  const combinedAppointments = useMemo(() => {
    const arr: CalendarAppointment[] = [...appointments];
    if (overview?.pending_requests) {
      for (const p of overview.pending_requests) {
        arr.push({
          id: p.id,
          booking_code: p.request_code,
          status: p.status,
          starts_at: p.preferred_start,
          ends_at: p.preferred_end,
          customer_user_id: p.customer?.full_name || "",
          customer_note: p.customer_note,
          checked_in_at: null,
          property: p.property,
        });
      }
    }
    return arr.sort((a, b) => new Date(a.starts_at).getTime() - new Date(b.starts_at).getTime());
  }, [appointments, overview]);

  const nextAppointment = useMemo(() => {
    const now = new Date();
    return (overview?.schedule ?? []).find((item) => new Date(item.preferred_start) > now);
  }, [overview]);

  async function handleAccept(id: string) { try { await apiFetch(`/sale/requests/${id}/accept`, { method: "POST" }); await load(true); } catch (reason) { setError(reason instanceof Error ? reason.message : "Lỗi"); } }
  async function handleReject() { if (!reject) return; try { await apiFetch(`/sale/requests/${reject.id}/reject`, { method: "POST", body: JSON.stringify({ reason: reject.reason || null }) }); setReject(null); await load(true); } catch (reason) { setError(reason instanceof Error ? reason.message : "Lỗi"); } }
  async function handleAppointmentAction(id: string, action: "check-in" | "no-show" | "complete" | "accept" | "reject") {
    if (action === "accept") return handleAccept(id);
    if (action === "reject") { setReject({ id, reason: "" }); return; }
    try { await apiFetch(`/sale/appointments/${id}/${action}`, { method: "POST" }); await load(true); } catch (reason) { setError(reason instanceof Error ? reason.message : "Lỗi"); }
  }
  async function handleVerifyProperty(propertyId: string) { try { await apiFetch(`/sale/properties/${propertyId}/verify`, { method: "POST" }); setVerified((prev) => new Set(prev).add(propertyId)); } catch (reason) { setError(reason instanceof Error ? reason.message : "Lỗi"); } }
  async function handleLogout() { await logout(); router.replace("/login"); }

  function remaining(expiresAt: string) { const ms = new Date(expiresAt).getTime() - new Date().getTime(); if (ms <= 0) return "Hết hạn"; const m = Math.floor(ms / 60000); return `còn ${m} phút`; }

  const sidebar = (
    <aside className={`bg-[var(--ink)] p-5 text-white lg:sticky lg:top-4 lg:h-[calc(100vh-2rem)] lg:rounded-[2rem] lg:w-[280px] lg:shadow-xl lg:border lg:border-black/5 lg:overflow-y-auto ${sidebarOpen ? "fixed inset-0 z-50" : "hidden lg:block"} custom-scrollbar`}>
      <div className="flex items-center justify-between border-b border-white/10 pb-5">
        <div className="flex items-center gap-3">
          <span className="grid h-11 w-11 place-items-center rounded-2xl bg-white/10"><FaRobot className="text-[#a9c9b0]" /></span>
          <div><p className="font-semibold">Nera Sale</p><p className="text-xs text-white/40">{user?.full_name}</p></div>
        </div>
        <button onClick={() => setSidebarOpen(false)} className="lg:hidden text-white/60 hover:text-white" aria-label="Đóng menu"><FaTimes /></button>
      </div>
      <nav className="mt-6 space-y-2">
        <a href="#queue" onClick={() => setSidebarOpen(false)} className="flex items-center gap-3 rounded-xl bg-white/10 px-4 py-3 text-sm"><FaBell /> Hàng đợi</a>
        <a href="#calendar" onClick={() => setSidebarOpen(false)} className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm hover:bg-white/10"><FaCalendarAlt /> Lịch tuần</a>
        <Link href="/sale/route-map" onClick={() => setSidebarOpen(false)} className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm hover:bg-white/10"><FaMapMarkerAlt /> Lộ trình hôm nay</Link>
      </nav>
      {nextAppointment && (
        <div className="mt-8 rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs font-bold uppercase tracking-[.12em] text-[#a9c9b0]">Cuộc hẹn tiếp theo</p>
          <p className="mt-3 text-sm font-semibold">{nextAppointment.property.title}</p>
          <p className="mt-1 flex items-center gap-2 text-sm text-white/60"><FaClock />{new Date(nextAppointment.preferred_start).toLocaleString("vi-VN")}</p>
        </div>
      )}
      <button onClick={() => void handleLogout()} className="mt-6 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm text-[#e8a58d] hover:bg-white/10"><FaSignOutAlt /> Đăng xuất</button>
    </aside>
  );

  return (
    <div className="min-h-screen bg-[#f4f5f1] text-[var(--ink)] lg:flex lg:p-4 gap-4">
      {sidebar}
      {sidebarOpen && <div className="fixed inset-0 z-40 bg-black/50 lg:hidden" onClick={() => setSidebarOpen(false)} />}

      <main className="min-w-0 flex-1 p-4 sm:p-8 xl:p-10">
        <button onClick={() => setSidebarOpen(true)} className="mb-4 rounded-xl border border-black/10 bg-white p-3 lg:hidden" aria-label="Mở menu"><FaBars /></button>

        <header className="mb-8 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-xs font-bold uppercase tracking-[.18em] text-[var(--coral)]">Sale Dashboard</p>
            <h1 className="mt-2 text-3xl font-semibold tracking-[-.04em]">Xin chào {overview?.user.full_name ?? user?.full_name}</h1>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={() => void load()} disabled={loading} className="inline-flex items-center gap-2 rounded-full border border-black/10 bg-white px-4 py-2.5 text-sm font-semibold"><FaSyncAlt className={loading ? "animate-spin" : ""} /> Làm mới</button>
            <NotificationBell />
          </div>
        </header>

        {error && <div role="alert" className="mb-5 rounded-2xl border border-red-100 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

        {/* Stat cards */}
        <section className="mb-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {[
            { label: "Yêu cầu chờ", value: overview?.stats.pending ?? 0, icon: FaBell },
            { label: "Đã xác nhận", value: overview?.stats.confirmed ?? 0, icon: FaCheckCircle },
            { label: "Appointments tuần này", value: appointments.filter(a => a.status === "CONFIRMED" || a.status === "IN_PROGRESS").length, icon: FaCalendarAlt },
            { label: "Đã hoàn thành", value: appointments.filter(a => a.status === "COMPLETED").length, icon: FaCheck },
          ].map(({ label, value, icon: Icon }, index) => (
            <div key={label} className={`group rounded-[1.6rem] p-6 shadow-[inset_0_1px_0_rgba(255,255,255,0.6),0_1px_3px_rgba(0,0,0,0.04)] border transition duration-300 hover:-translate-y-1 hover:shadow-md ${
              index === 0 && Number(value) > 0 
                ? "bg-gradient-to-br from-[#fff6f0] to-[#fff1e8] border-orange-900/5 shadow-[inset_0_1px_0_rgba(255,255,255,1),0_1px_3px_rgba(234,88,12,0.08)]" 
                : "bg-gradient-to-br from-white to-[#fbfaf7] border-black/[0.03]"
            }`}>
              <div className="flex items-center justify-between"><p className="text-sm font-medium text-[var(--muted)]">{label}</p><Icon className={index === 0 && Number(value) > 0 ? "text-[var(--coral)]" : "text-[var(--forest)]/70"} /></div>
              <p className="mt-4 text-4xl font-semibold tracking-tight text-[var(--ink)]">{value}</p>
            </div>
          ))}
        </section>

        {/* Pending queue */}
        <section id="queue" className="mb-8">
          <p className="text-xs font-bold uppercase tracking-[.15em] text-[var(--coral)]">Hàng đợi</p>
          <h2 className="mt-1 mb-4 text-xl font-semibold">Yêu cầu cần phản hồi</h2>
          {(overview?.pending_requests ?? []).length === 0 ? (
            <div className="rounded-[1.5rem] border border-black/5 bg-white p-12 text-center">
              <FaCheckCircle className="mx-auto text-4xl text-emerald-400 mb-4" />
              <p className="text-lg font-semibold">Không có yêu cầu đang chờ</p>
              <p className="text-sm text-[var(--muted)]">Khi có yêu cầu mới, chúng sẽ hiện ở đây.</p>
            </div>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2">
              {overview?.pending_requests.map((item) => {
                const isReschedule = item.customer_note?.includes("Dời lịch từ");
                return (
                  <article key={item.id} className="group rounded-[1.6rem] border border-black/[0.03] bg-gradient-to-br from-white to-[#fbfaf7] p-6 shadow-[inset_0_1px_0_rgba(255,255,255,0.6),0_1px_3px_rgba(0,0,0,0.04)] animate-card-rise transition-all duration-300 hover:-translate-y-1 hover:shadow-md">
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="font-bold text-[var(--ink)]">{item.customer?.full_name}</p>
                        <p className="text-xs font-medium text-[var(--muted)]">{item.customer?.phone}</p>
                      </div>
                      {item.expires_at && <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-700 flex items-center gap-1.5"><FaClock />{remaining(item.expires_at)}</span>}
                    </div>
                    {isReschedule && <p className="mt-4 text-xs font-semibold text-[var(--coral)] flex items-center gap-1.5">🔄 Yêu cầu dời lịch</p>}
                    <p className={`font-semibold text-[15px] leading-relaxed text-[var(--ink)] line-clamp-2 ${isReschedule ? 'mt-1' : 'mt-4'}`}>{item.property.title}</p>
                    <p className="mt-1 text-xs font-medium text-[var(--muted)] line-clamp-1">{item.property.address}</p>
                    <p className="mt-3 flex items-center gap-1.5 text-xs font-semibold text-[var(--muted)]"><FaCalendarAlt className="text-[var(--forest)]" />{new Date(item.preferred_start).toLocaleString("vi-VN")}</p>
                    {(item.property.is_stale || verified.has(item.property.id)) && (
                      <button
                        onClick={() => void handleVerifyProperty(item.property.id)}
                        disabled={verified.has(item.property.id)}
                        title={item.property.verification_label ?? undefined}
                        className="mt-3 w-full rounded-xl border border-amber-300 bg-amber-50 py-2 text-xs font-semibold text-amber-800 transition hover:bg-amber-100 disabled:border-emerald-200 disabled:bg-emerald-50 disabled:text-[var(--forest)]"
                      >
                        {verified.has(item.property.id)
                          ? "✓ Đã xác nhận còn trống"
                          : `⚠ ${item.property.verification_label ?? "Tin cũ"} — bấm để xác nhận`}
                      </button>
                    )}
                    <div className="mt-3 flex gap-2">
                      <button onClick={() => void handleAccept(item.id)} className="flex-1 rounded-xl bg-[var(--forest)] py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-[#1a4035]">✓ {isReschedule ? "Đồng ý dời" : "Nhận"}</button>
                      <button onClick={() => setReject({ id: item.id, reason: "" })} className="flex-1 rounded-xl border border-[var(--coral)]/50 py-2.5 text-sm font-semibold text-[var(--coral)] transition hover:bg-[var(--coral)]/5">✗ {isReschedule ? "Từ chối dời" : "Từ chối"}</button>
                    </div>
                  </article>
                );
              })}
            </div>
          )}
        </section>

        {/* Calendar / List toggle */}
        <section id="calendar">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <p className="text-xs font-bold uppercase tracking-[.15em] text-[var(--coral)]">Lịch trình</p>
              <h2 className="mt-1 text-xl font-semibold">Lịch tuần này</h2>
            </div>
            <div className="flex rounded-xl border border-black/10 bg-white overflow-hidden">
              <button onClick={() => setView("calendar")} className={`px-4 py-2 text-sm font-semibold flex items-center gap-1.5 ${view === "calendar" ? "bg-[var(--forest)] text-white" : ""}`}><FaTh /> Lịch</button>
              <button onClick={() => setView("list")} className={`px-4 py-2 text-sm font-semibold flex items-center gap-1.5 ${view === "list" ? "bg-[var(--forest)] text-white" : ""}`}><FaList /> Danh sách</button>
            </div>
          </div>

          {view === "calendar" ? (
            <WeekCalendar appointments={combinedAppointments} onAction={handleAppointmentAction} />
          ) : (
            <div className="space-y-3">
              {combinedAppointments.length === 0 && <p className="rounded-[1.5rem] bg-white p-10 text-center text-[var(--muted)]">Chưa có lịch trình nào.</p>}
              {combinedAppointments.map((a) => (
                <div key={a.id} className="group flex flex-col sm:flex-row sm:items-center gap-4 rounded-[1.6rem] border border-black/[0.03] bg-gradient-to-br from-white to-[#fbfaf7] p-5 shadow-[inset_0_1px_0_rgba(255,255,255,0.6),0_1px_3px_rgba(0,0,0,0.04)] transition duration-300 hover:-translate-y-1 hover:shadow-md">
                  <div className="flex-1 min-w-0">
                    <p className="font-bold text-[var(--ink)]">{a.property?.title ?? a.booking_code}</p>
                    <p className="text-xs font-medium text-[var(--muted)]">{a.property?.address}</p>
                    <p className="mt-1 text-xs font-semibold text-[var(--muted)] flex items-center gap-1.5"><FaClock className="text-[var(--forest)]" />{new Date(a.starts_at).toLocaleString("vi-VN")} – {new Date(a.ends_at).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" })}</p>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold border ${STATUS_COLORS[a.status]?.bg ?? "bg-stone-50 border-stone-200"} ${STATUS_COLORS[a.status]?.text ?? "text-stone-600"}`}>
                      <span className={`h-1.5 w-1.5 rounded-full ${STATUS_COLORS[a.status]?.dot ?? "bg-stone-400"} ${a.status === "IN_PROGRESS" || a.status === "WAITING_APPROVAL" ? "animate-pulse" : ""}`} />
                      {STATUS_LABELS[a.status] ?? a.status}
                    </span>
                    {a.status === "CONFIRMED" && (
                      <>
                        <button onClick={() => void handleAppointmentAction(a.id, "check-in")} className="rounded-lg bg-[var(--forest)] px-3 py-1.5 text-xs font-semibold text-white" title="Check-in"><FaUserCheck /></button>
                        <button onClick={() => void handleAppointmentAction(a.id, "no-show")} className="rounded-lg bg-red-500 px-3 py-1.5 text-xs font-semibold text-white" title="No-show"><FaExclamationCircle /></button>
                      </>
                    )}
                    {a.status === "IN_PROGRESS" && (
                      <button onClick={() => void handleAppointmentAction(a.id, "complete")} className="rounded-lg bg-[var(--ink)] px-3 py-1.5 text-xs font-semibold text-white" title="Hoàn thành"><FaCheckCircle /></button>
                    )}
                    {a.status === "WAITING_APPROVAL" && (
                      <>
                        <button onClick={() => void handleAppointmentAction(a.id, "accept")} className="rounded-lg bg-[var(--forest)] px-3 py-1.5 text-xs font-semibold text-white">Nhận</button>
                        <button onClick={() => void handleAppointmentAction(a.id, "reject")} className="rounded-lg border border-[var(--coral)] px-3 py-1.5 text-xs font-semibold text-[var(--coral)]">Từ chối</button>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Reject dialog */}
        {reject && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" onClick={() => setReject(null)}>
            <div className="w-full max-w-md rounded-[1.5rem] bg-white p-6 shadow-xl" onClick={(e) => e.stopPropagation()}>
              <h3 className="text-lg font-bold mb-4">Lý do từ chối</h3>
              <textarea value={reject.reason} onChange={(e) => setReject({ ...reject, reason: e.target.value })} placeholder="Nhập lý do (không bắt buộc)..." className="w-full rounded-xl border border-black/10 bg-[#fbfaf7] p-3 text-sm h-28 resize-none" />
              <div className="mt-4 flex gap-2">
                <button onClick={() => void handleReject()} className="flex-1 rounded-xl bg-[var(--coral)] py-2.5 text-sm font-semibold text-white">Xác nhận từ chối</button>
                <button onClick={() => setReject(null)} className="flex-1 rounded-xl border border-black/10 py-2.5 text-sm font-semibold">Hủy</button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default function SaleDashboard() {
  return (
    <ProtectedPage roles={["SALE"]}>
      <SaleDashboardContent />
    </ProtectedPage>
  );
}
