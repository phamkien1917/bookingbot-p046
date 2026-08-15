"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { FaBars, FaBell, FaCalendarAlt, FaChartLine, FaExclamationTriangle, FaRobot, FaSearch, FaShieldAlt, FaSignOutAlt, FaSyncAlt, FaTimes, FaUsers } from "react-icons/fa";
import ProtectedPage from "@/components/ProtectedPage";
import { useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";
import type { Booking, User, UserRole } from "@/lib/types";

interface AdminOverview { stats: { users: number; properties: number; bookings: number; pending: number; conversion_rate: number; no_shows: number }; recent_bookings: Booking[] }
interface DailyBooking { date: string; total: number; confirmed: number; cancelled: number; no_show: number }
interface WeeklyConversion { week_label: string; total: number; confirmed: number; rate: number }
interface Analytics { daily_bookings: DailyBooking[]; status_distribution: Record<string, number>; weekly_conversion: WeeklyConversion[] }

const statusLabel: Record<string, string> = { WAITING_APPROVAL: "Chờ Sale", BOOKED: "Đã xác nhận", CANCELLED: "Đã hủy", REJECTED: "Bị từ chối", EXPIRED: "Hết hạn", APPROVED: "Đã duyệt" };
const statusStyle: Record<string, string> = { WAITING_APPROVAL: "bg-amber-50 text-amber-700", BOOKED: "bg-emerald-50 text-emerald-700", CANCELLED: "bg-stone-100 text-stone-600", REJECTED: "bg-red-50 text-red-700", EXPIRED: "bg-red-50 text-red-700" };

/* ===================== SVG CHARTS ===================== */

function MiniLineChart({ data }: { data: DailyBooking[] }) {
  if (!data.length) return <div className="h-48 grid place-items-center text-sm text-[var(--muted)]">Chưa có dữ liệu</div>;
  const maxVal = Math.max(...data.map(d => d.total), 1);
  const w = 320, h = 140, px = 32, py = 20;
  const points = data.map((d, i) => ({ x: px + (i / Math.max(data.length - 1, 1)) * (w - px * 2), y: py + (1 - d.total / maxVal) * (h - py * 2) }));
  const confirmedPts = data.map((d, i) => ({ x: px + (i / Math.max(data.length - 1, 1)) * (w - px * 2), y: py + (1 - d.confirmed / maxVal) * (h - py * 2) }));
  const line = (pts: typeof points) => pts.map((p, i) => `${i === 0 ? "M" : "L"}${p.x},${p.y}`).join(" ");
  const area = (pts: typeof points) => line(pts) + ` L${pts[pts.length - 1].x},${h - py} L${pts[0].x},${h - py} Z`;

  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="w-full h-auto">
      <defs>
        <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="var(--forest)" stopOpacity=".15" /><stop offset="100%" stopColor="var(--forest)" stopOpacity="0" /></linearGradient>
      </defs>
      {/* Grid lines */}
      {[0, 0.25, 0.5, 0.75, 1].map(f => <line key={f} x1={px} x2={w - px} y1={py + f * (h - py * 2)} y2={py + f * (h - py * 2)} stroke="black" strokeOpacity=".06" />)}
      {/* Area + lines */}
      <path d={area(points)} fill="url(#areaGrad)" />
      <path d={line(points)} fill="none" stroke="var(--forest)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
      <path d={line(confirmedPts)} fill="none" stroke="var(--coral)" strokeWidth="2" strokeDasharray="5,4" strokeLinecap="round" />
      {/* Dots */}
      {points.map((p, i) => <circle key={i} cx={p.x} cy={p.y} r="3.5" fill="var(--forest)" stroke="white" strokeWidth="2" />)}
      {/* X labels */}
      {data.map((d, i) => <text key={i} x={points[i].x} y={h - 2} textAnchor="middle" fontSize="9" fill="var(--muted)">{d.date.slice(5)}</text>)}
      {/* Y labels */}
      {[0, Math.round(maxVal / 2), maxVal].map((v, i) => <text key={i} x={px - 6} y={py + (1 - v / maxVal) * (h - py * 2) + 3} textAnchor="end" fontSize="9" fill="var(--muted)">{v}</text>)}
    </svg>
  );
}

function DonutChart({ dist }: { dist: Record<string, number> }) {
  const items = [
    { key: "booked", label: "Đã xác nhận", color: "var(--forest)" },
    { key: "waiting_approval", label: "Đang chờ", color: "#e6a23c" },
    { key: "cancelled", label: "Đã hủy", color: "var(--muted)" },
    { key: "rejected", label: "Từ chối", color: "var(--coral)" },
    { key: "no_show", label: "No-show", color: "#ef4444" },
    { key: "expired", label: "Hết hạn", color: "#94a3b8" },
  ].filter(i => (dist[i.key] ?? 0) > 0);
  const total = items.reduce((s, i) => s + (dist[i.key] ?? 0), 0) || 1;
  const r = 55, cx = 70, cy = 70, stroke = 22;
  let cumAngle = -90;

  return (
    <div className="flex items-center gap-6">
      <svg viewBox="0 0 140 140" className="w-36 h-36 shrink-0">
        {items.map(item => {
          const val = dist[item.key] ?? 0;
          const angle = (val / total) * 360;
          const start = cumAngle;
          cumAngle += angle;
          const startRad = (start * Math.PI) / 180;
          const endRad = ((start + angle) * Math.PI) / 180;
          const largeArc = angle > 180 ? 1 : 0;
          const x1 = cx + r * Math.cos(startRad), y1 = cy + r * Math.sin(startRad);
          const x2 = cx + r * Math.cos(endRad), y2 = cy + r * Math.sin(endRad);
          return <path key={item.key} d={`M ${x1} ${y1} A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2}`} fill="none" stroke={item.color} strokeWidth={stroke} />;
        })}
        <text x={cx} y={cy - 4} textAnchor="middle" fontSize="22" fontWeight="700" fill="var(--ink)">{total}</text>
        <text x={cx} y={cy + 12} textAnchor="middle" fontSize="10" fill="var(--muted)">tổng</text>
      </svg>
      <div className="space-y-2">
        {items.map(item => (
          <div key={item.key} className="flex items-center gap-2 text-xs">
            <span className="h-2.5 w-2.5 rounded-full shrink-0" style={{ background: item.color }} />
            <span className="text-[var(--muted)]">{item.label}</span>
            <span className="font-semibold ml-auto">{dist[item.key] ?? 0}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function BarChart({ data }: { data: WeeklyConversion[] }) {
  if (!data.length) return <div className="h-40 grid place-items-center text-sm text-[var(--muted)]">Chưa có dữ liệu</div>;
  const maxRate = Math.max(...data.map(d => d.rate), 10);
  return (
    <div className="flex items-end gap-3 h-36">
      {data.map((d, i) => (
        <div key={i} className="flex-1 flex flex-col items-center gap-2">
          <span className="text-xs font-semibold">{d.rate}%</span>
          <div className="w-full rounded-t-lg transition-all duration-500" style={{ height: `${(d.rate / maxRate) * 100}%`, minHeight: 8, background: i === data.length - 1 ? "var(--forest)" : "var(--sage)" }} />
          <span className="text-[10px] text-[var(--muted)] text-center leading-tight">{d.week_label}</span>
        </div>
      ))}
    </div>
  );
}

/* ===================== MAIN COMPONENT ===================== */

function AdminDashboardContent() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [overview, setOverview] = useState<AdminOverview | null>(null);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [query, setQuery] = useState("");
  const [role, setRole] = useState<UserRole | "">("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const load = useCallback(async (quiet = false) => {
    if (!quiet) setLoading(true);
    try {
      const [ov, an] = await Promise.all([
        apiFetch<AdminOverview>("/admin/overview"),
        apiFetch<Analytics>("/admin/analytics"),
      ]);
      setOverview(ov);
      setAnalytics(an);
      if (user?.role === "ADMIN") setUsers(await apiFetch<User[]>(`/admin/users${role ? `?role=${role}` : ""}`));
      setError("");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Không tải được dữ liệu vận hành");
    } finally {
      if (!quiet) setLoading(false);
    }
  }, [role, user]);

  useEffect(() => { const initial = window.setTimeout(() => void load(), 0); const interval = window.setInterval(() => void load(true), 20_000); return () => { window.clearTimeout(initial); window.clearInterval(interval); }; }, [load]);
  const visibleUsers = useMemo(() => users.filter((item) => `${item.full_name} ${item.email} ${item.phone ?? ""}`.toLowerCase().includes(query.toLowerCase())), [users, query]);
  const pipeline = useMemo(() => { const items = overview?.recent_bookings ?? []; return { waiting: items.filter((item) => item.status === "WAITING_APPROVAL").length, booked: items.filter((item) => item.status === "BOOKED").length, failed: items.filter((item) => ["REJECTED", "EXPIRED", "CANCELLED"].includes(item.status)).length }; }, [overview]);

  async function changeStatus(target: User) {
    const next = target.status === "ACTIVE" ? "LOCKED" : "ACTIVE";
    if (!window.confirm(`${next === "LOCKED" ? "Khóa" : "Mở khóa"} tài khoản ${target.full_name}?`)) return;
    try { await apiFetch(`/admin/users/${target.id}/status`, { method: "PATCH", body: JSON.stringify({ status: next }) }); await load(true); } catch { setError("Không cập nhật được tài khoản."); }
  }
  async function handleLogout() { await logout(); router.replace("/login"); }

  const sidebar = (
    <aside className={`bg-[var(--ink)] p-5 text-white lg:sticky lg:top-0 lg:min-h-screen lg:w-72 ${sidebarOpen ? "fixed inset-0 z-50" : "hidden lg:block"}`}>
      <div className="flex items-center justify-between border-b border-white/10 pb-5">
        <div className="flex items-center gap-3">
          <span className="grid h-11 w-11 place-items-center rounded-2xl bg-white/10"><FaRobot className="text-[#a9c9b0]" /></span>
          <div><p className="font-semibold">Nera Operations</p><p className="text-xs text-white/40">Control room</p></div>
        </div>
        <button onClick={() => setSidebarOpen(false)} className="lg:hidden text-white/60 hover:text-white" aria-label="Đóng menu"><FaTimes /></button>
      </div>
      <nav className="mt-6 space-y-2">
        <a href="#overview" onClick={() => setSidebarOpen(false)} className="flex items-center gap-3 rounded-xl bg-white/10 px-4 py-3 text-sm"><FaChartLine /> Sức khỏe hệ thống</a>
        <a href="#analytics" onClick={() => setSidebarOpen(false)} className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm hover:bg-white/10"><FaCalendarAlt /> Phân tích & biểu đồ</a>
        <a href="#bookings" onClick={() => setSidebarOpen(false)} className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm hover:bg-white/10"><FaBell /> Booking pipeline</a>
        <Link href="/admin/properties" onClick={() => setSidebarOpen(false)} className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm hover:bg-white/10"><FaChartLine /> Kho Bất động sản</Link>
        {user?.role === "ADMIN" && (
          <>
            <a href="#users" onClick={() => setSidebarOpen(false)} className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm hover:bg-white/10"><FaUsers /> Người dùng</a>
            <Link href="/admin/sales" onClick={() => setSidebarOpen(false)} className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm hover:bg-white/10"><FaRobot /> Quản lý Sale</Link>
          </>
        )}
      </nav>
      <div className="mt-8 rounded-2xl border border-white/10 bg-white/5 p-4">
        <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[.12em] text-[#a9c9b0]"><FaShieldAlt /> Hệ thống</p>
        <p className="mt-3 flex items-center gap-2 text-sm"><i className="h-2 w-2 rounded-full bg-emerald-400" /> API đang hoạt động</p>
        <p className="mt-2 text-xs text-white/40">Tự làm mới mỗi 20 giây</p>
      </div>
      <button onClick={() => void handleLogout()} className="mt-6 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm text-[#e8a58d] hover:bg-white/10"><FaSignOutAlt /> Đăng xuất</button>
    </aside>
  );

  return (
    <div className="min-h-screen bg-[#f4f5f1] text-[var(--ink)] lg:flex">
      {sidebar}
      {sidebarOpen && <div className="fixed inset-0 z-40 bg-black/50 lg:hidden" onClick={() => setSidebarOpen(false)} />}

      <main className="min-w-0 flex-1 p-4 sm:p-8 xl:p-10">
        {/* Mobile header */}
        <button onClick={() => setSidebarOpen(true)} className="mb-4 rounded-xl border border-black/10 bg-white p-3 lg:hidden" aria-label="Mở menu"><FaBars /></button>

        <header id="overview" className="mb-8 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-xs font-bold uppercase tracking-[.18em] text-[var(--coral)]">Trung tâm vận hành</p>
            <h1 className="mt-2 text-3xl font-semibold tracking-[-.04em]">Quan sát vấn đề trước khi khách gặp phải.</h1>
            <p className="mt-2 text-sm text-[var(--muted)]">Xin chào {user?.full_name}. Số liệu lấy trực tiếp từ luồng booking và tài khoản.</p>
          </div>
          <button onClick={() => void load()} disabled={loading} className="inline-flex items-center gap-2 rounded-full border border-black/10 bg-white px-4 py-2.5 text-sm font-semibold"><FaSyncAlt className={loading ? "animate-spin" : ""} /> Làm mới</button>
        </header>

        {error && <div role="alert" className="mb-5 rounded-2xl border border-red-100 bg-red-50 p-4 text-sm text-red-700">{error}</div>}

        {/* Stat cards */}
        <section className="mb-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {[
            { label: "Tổng booking", value: overview?.stats.bookings, note: "Toàn bộ yêu cầu", icon: FaCalendarAlt },
            { label: "Đang chờ Sale", value: overview?.stats.pending, note: "Cần theo dõi SLA", icon: FaBell },
            { label: "Tỷ lệ xác nhận", value: overview ? `${overview.stats.conversion_rate}%` : undefined, note: "Booking chuyển thành lịch", icon: FaChartLine },
            { label: "No-show", value: overview?.stats.no_shows, note: "Cần gọi lại khách", icon: FaExclamationTriangle },
          ].map(({ label, value, note, icon: Icon }, index) => (
            <div key={label} className={`rounded-[1.5rem] p-5 shadow-sm ${index === 1 && Number(value) > 0 ? "bg-[#fff1e8]" : "bg-white"}`}>
              <div className="flex items-center justify-between"><p className="text-sm text-[var(--muted)]">{label}</p><Icon className={index === 1 ? "text-[var(--coral)]" : "text-[var(--forest)]"} /></div>
              <p className="mt-3 text-4xl font-semibold">{value ?? "–"}</p>
              <p className="mt-2 text-xs text-[var(--muted)]">{note}</p>
            </div>
          ))}
        </section>

        {/* Charts Section */}
        <section id="analytics" className="mb-8 grid gap-6 xl:grid-cols-3">
          <div className="rounded-[1.6rem] border border-black/5 bg-white p-6 shadow-sm xl:col-span-1">
            <p className="text-xs font-bold uppercase tracking-[.15em] text-[var(--coral)]">Xu hướng 7 ngày</p>
            <h2 className="mt-2 text-lg font-semibold">Booking theo ngày</h2>
            <p className="mb-4 text-xs text-[var(--muted)]"><span className="inline-block h-2 w-4 rounded-full bg-[var(--forest)] mr-1 align-middle" /> Tổng · <span className="inline-block h-0.5 w-4 border-t-2 border-dashed border-[var(--coral)] mr-1 align-middle" /> Xác nhận</p>
            <MiniLineChart data={analytics?.daily_bookings ?? []} />
          </div>
          <div className="rounded-[1.6rem] border border-black/5 bg-white p-6 shadow-sm xl:col-span-1">
            <p className="text-xs font-bold uppercase tracking-[.15em] text-[var(--coral)]">Phân bổ trạng thái</p>
            <h2 className="mt-2 mb-5 text-lg font-semibold">Tổng quan booking</h2>
            <DonutChart dist={analytics?.status_distribution ?? {}} />
          </div>
          <div className="rounded-[1.6rem] border border-black/5 bg-white p-6 shadow-sm xl:col-span-1">
            <p className="text-xs font-bold uppercase tracking-[.15em] text-[var(--coral)]">Hiệu suất</p>
            <h2 className="mt-2 mb-5 text-lg font-semibold">Conversion rate 4 tuần</h2>
            <BarChart data={analytics?.weekly_conversion ?? []} />
          </div>
        </section>

        {/* Operations alert + pipeline */}
        <div className="mb-8 grid gap-6 xl:grid-cols-[.9fr_1.1fr]">
          <section className="rounded-[1.6rem] bg-[var(--forest)] p-6 text-white">
            <p className="text-xs font-bold uppercase tracking-[.15em] text-[#bcd2c1]">Cảnh báo vận hành</p>
            <h2 className="mt-2 text-xl font-semibold">{overview?.stats.pending ? `${overview.stats.pending} yêu cầu đang chờ phản hồi` : "Không có cảnh báo khẩn"}</h2>
            <p className="mt-3 text-sm leading-6 text-white/60">{overview?.stats.pending ? "Theo dõi yêu cầu sắp hết hạn; hệ thống sẽ tự phân Sale khác nếu cần." : "Luồng phân Sale và xác nhận lịch đang trong ngưỡng bình thường."}</p>
            <div className="mt-5 flex gap-3">
              <a href="#bookings" className="rounded-full bg-white px-4 py-2 text-xs font-semibold text-[var(--forest)]">Mở pipeline</a>
              <span className="rounded-full border border-white/15 px-4 py-2 text-xs text-white/70">{overview?.stats.no_shows ?? 0} no-show</span>
            </div>
          </section>
          <section className="rounded-[1.6rem] border border-black/5 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div><p className="text-xs font-bold uppercase tracking-[.15em] text-[var(--coral)]">Pipeline gần đây</p><h2 className="mt-2 text-xl font-semibold">Từ yêu cầu đến lịch xem</h2></div>
              <FaChartLine className="text-[var(--forest)]" />
            </div>
            <div className="mt-6 grid grid-cols-3 gap-3">
              {[["Chờ Sale", pipeline.waiting, "bg-amber-400"], ["Đã đặt", pipeline.booked, "bg-emerald-500"], ["Không thành công", pipeline.failed, "bg-red-400"]].map(([label, value, color]) => (
                <div key={String(label)}><div className={`h-2 rounded-full ${color}`} /><p className="mt-3 text-2xl font-semibold">{value}</p><p className="text-xs text-[var(--muted)]">{label}</p></div>
              ))}
            </div>
          </section>
        </div>

        {/* Booking table */}
        <section id="bookings" className="mb-10">
          <div className="mb-4"><p className="text-xs font-bold uppercase tracking-[.15em] text-[var(--coral)]">Live operations</p><h2 className="mt-1 text-xl font-semibold">Booking gần đây</h2></div>
          <div className="overflow-x-auto rounded-[1.5rem] border border-black/5 bg-white shadow-sm">
            <table className="w-full min-w-[800px] text-left text-sm">
              <thead className="bg-[#f7f7f3] text-[var(--muted)]"><tr><th className="p-4">Yêu cầu</th><th className="p-4">Khách hàng</th><th className="p-4">Nhà quan tâm</th><th className="p-4">Sale phụ trách</th><th className="p-4">Trạng thái</th></tr></thead>
              <tbody className="divide-y divide-black/5">
                {overview?.recent_bookings.map((booking) => (
                  <tr key={booking.id} className="transition hover:bg-[#fbfaf7]">
                    <td className="p-4 font-mono text-xs">{booking.request_code}</td>
                    <td className="p-4 font-medium">{booking.customer?.full_name}<br /><span className="text-xs font-normal text-[var(--muted)]">{booking.customer?.phone ?? booking.customer?.email}</span></td>
                    <td className="max-w-xs p-4"><span className="line-clamp-2">{booking.property.title}</span></td>
                    <td className="p-4">{booking.sale?.full_name ?? <span className="text-[var(--coral)]">Chưa gán</span>}</td>
                    <td className="p-4"><span className={`rounded-full px-3 py-1.5 text-xs font-semibold ${statusStyle[booking.status] ?? "bg-stone-100"}`}>{statusLabel[booking.status] ?? booking.status}</span></td>
                  </tr>
                ))}
                {overview?.recent_bookings.length === 0 && <tr><td colSpan={5} className="p-10 text-center text-[var(--muted)]">Chưa có booking.</td></tr>}
              </tbody>
            </table>
          </div>
        </section>

        {/* Users table */}
        {user?.role === "ADMIN" && (
          <section id="users">
            <div className="mb-4 flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
              <div>
                <p className="text-xs font-bold uppercase tracking-[.15em] text-[var(--coral)]">Access control</p>
                <h2 className="mt-1 text-xl font-semibold">Người dùng hệ thống</h2>
                <p className="mt-1 text-xs text-[var(--muted)]">{overview?.stats.users ?? users.length} tài khoản · {overview?.stats.properties ?? 0} căn trong kho</p>
              </div>
              <div className="flex gap-2">
                <label className="relative"><span className="sr-only">Tìm người dùng</span><FaSearch className="absolute left-3 top-3 text-[var(--muted)]" /><input value={query} onChange={(event) => setQuery(event.target.value)} className="rounded-xl border border-black/10 bg-white py-2 pl-9 pr-3 text-sm" placeholder="Tên, email, SĐT" /></label>
                <select aria-label="Lọc vai trò" value={role} onChange={(event) => setRole(event.target.value as UserRole | "")} className="rounded-xl border border-black/10 bg-white px-3 text-sm"><option value="">Tất cả vai trò</option><option value="CUSTOMER">Khách hàng</option><option value="SALE">Sale</option><option value="COORDINATOR">Điều phối</option><option value="ADMIN">Admin</option></select>
              </div>
            </div>
            <div className="overflow-x-auto rounded-[1.5rem] border border-black/5 bg-white shadow-sm">
              <table className="w-full min-w-[760px] text-left text-sm">
                <thead className="bg-[#f7f7f3] text-[var(--muted)]"><tr><th className="p-4">Người dùng</th><th className="p-4">Vai trò</th><th className="p-4">Điện thoại</th><th className="p-4">Trạng thái</th><th className="p-4">Thao tác</th></tr></thead>
                <tbody className="divide-y divide-black/5">
                  {visibleUsers.map((item) => (
                    <tr key={item.id} className="hover:bg-[#fbfaf7]">
                      <td className="p-4 font-medium">{item.full_name}<br /><span className="font-normal text-[var(--muted)]">{item.email}</span></td>
                      <td className="p-4">{item.role}</td>
                      <td className="p-4">{item.phone || "–"}</td>
                      <td className="p-4"><span className={`rounded-full px-3 py-1 text-xs font-semibold ${item.status === "ACTIVE" ? "bg-emerald-50 text-emerald-700" : "bg-red-50 text-red-700"}`}>{item.status}</span></td>
                      <td className="p-4"><button disabled={item.id === user.id || item.status === "DISABLED"} onClick={() => void changeStatus(item)} className="rounded-full border border-black/10 px-3 py-1.5 text-xs font-semibold disabled:opacity-40">{item.status === "ACTIVE" ? "Khóa" : "Mở khóa"}</button></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default function AdminDashboard() { return <ProtectedPage roles={["ADMIN", "COORDINATOR"]}><AdminDashboardContent /></ProtectedPage>; }
