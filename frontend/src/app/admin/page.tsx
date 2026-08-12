"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { FaBuilding, FaCalendarAlt, FaRobot, FaSearch, FaSignOutAlt, FaUsers } from "react-icons/fa";
import ProtectedPage from "@/components/ProtectedPage";
import { useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";
import type { Booking, User, UserRole } from "@/lib/types";

interface AdminOverview { stats: { users: number; properties: number; bookings: number; pending: number }; recent_bookings: Booking[] }

const statusLabel: Record<string, string> = { WAITING_APPROVAL: "Chờ Sale", BOOKED: "Đã xác nhận", CANCELLED: "Đã hủy", REJECTED: "Bị từ chối", EXPIRED: "Hết hạn" };

function AdminDashboardContent() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [overview, setOverview] = useState<AdminOverview | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [query, setQuery] = useState("");
  const [role, setRole] = useState<UserRole | "">("");
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    try {
      const overviewData = await apiFetch<AdminOverview>("/admin/overview");
      setOverview(overviewData);
      if (user?.role === "ADMIN") setUsers(await apiFetch<User[]>(`/admin/users${role ? `?role=${role}` : ""}`));
      setError("");
    } catch (err) { setError(err instanceof Error ? err.message : "Không tải được dữ liệu"); }
  }, [role, user]);

  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  const visibleUsers = useMemo(() => users.filter((item) => `${item.full_name} ${item.email} ${item.phone ?? ""}`.toLowerCase().includes(query.toLowerCase())), [users, query]);

  async function changeStatus(target: User) {
    const next = target.status === "ACTIVE" ? "LOCKED" : "ACTIVE";
    if (!window.confirm(`${next === "LOCKED" ? "Khóa" : "Mở khóa"} tài khoản ${target.full_name}?`)) return;
    try { await apiFetch(`/admin/users/${target.id}/status`, { method: "PATCH", body: JSON.stringify({ status: next }) }); await load(); }
    catch (err) { setError(err instanceof Error ? err.message : "Không cập nhật được tài khoản"); }
  }

  async function handleLogout() { await logout(); router.replace("/login"); }

  return <div className="min-h-screen bg-slate-50 text-slate-900 lg:flex">
    <aside className="bg-[#0b132b] p-5 text-white lg:min-h-screen lg:w-64"><div className="flex items-center gap-3 border-b border-white/10 pb-5"><FaRobot className="text-2xl text-teal-400"/><div><p className="font-bold">Booking Bot</p><p className="text-xs text-teal-300">Quản trị hệ thống</p></div></div><nav className="mt-6 space-y-2" aria-label="Điều hướng quản trị"><a href="#tong-quan" className="flex items-center gap-3 rounded-xl bg-white/10 px-4 py-3 text-sm"><FaCalendarAlt/> Tổng quan</a><a href="#bookings" className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm hover:bg-white/10"><FaBuilding/> Booking</a>{user?.role === "ADMIN" && <a href="#users" className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm hover:bg-white/10"><FaUsers/> Người dùng</a>}</nav><button onClick={() => void handleLogout()} className="mt-8 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm text-red-300 hover:bg-white/10"><FaSignOutAlt/> Đăng xuất</button></aside>
    <main className="min-w-0 flex-1 p-4 sm:p-8"><header id="tong-quan" className="mb-8"><h1 className="text-2xl font-bold">Dashboard quản trị</h1><p className="mt-1 text-sm text-slate-500">Xin chào {user?.full_name}. Dữ liệu được cập nhật trực tiếp từ hệ thống.</p></header>{error && <div role="alert" className="mb-5 rounded-xl bg-red-50 p-4 text-sm text-red-700">{error}</div>}
      <section className="mb-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{[{label:"Người dùng",value:overview?.stats.users,icon:<FaUsers/>},{label:"Bất động sản",value:overview?.stats.properties,icon:<FaBuilding/>},{label:"Tổng booking",value:overview?.stats.bookings,icon:<FaCalendarAlt/>},{label:"Đang chờ",value:overview?.stats.pending,icon:<FaCalendarAlt/>}].map((stat)=><div key={stat.label} className="rounded-2xl bg-white p-6 shadow-sm"><div className="flex items-center justify-between text-sm text-slate-500"><span>{stat.label}</span><span className="text-teal-600">{stat.icon}</span></div><p className="mt-2 text-3xl font-bold">{stat.value ?? "–"}</p></div>)}</section>
      <section id="bookings" className="mb-10"><h2 className="mb-4 text-lg font-bold">Booking gần đây</h2><div className="overflow-x-auto rounded-2xl bg-white shadow-sm"><table className="w-full min-w-[760px] text-left text-sm"><thead className="bg-slate-50 text-slate-500"><tr><th className="p-4">Mã yêu cầu</th><th className="p-4">Khách hàng</th><th className="p-4">Bất động sản</th><th className="p-4">Sale</th><th className="p-4">Trạng thái</th></tr></thead><tbody className="divide-y divide-slate-100">{overview?.recent_bookings.map((booking)=><tr key={booking.id}><td className="p-4 font-mono">{booking.request_code}</td><td className="p-4">{booking.customer?.full_name}<br/><span className="text-xs text-slate-400">{booking.customer?.phone ?? booking.customer?.email}</span></td><td className="p-4">{booking.property.title}</td><td className="p-4">{booking.sale?.full_name ?? "Chưa gán"}</td><td className="p-4"><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold">{statusLabel[booking.status] ?? booking.status}</span></td></tr>)}{overview?.recent_bookings.length === 0 && <tr><td colSpan={5} className="p-8 text-center text-slate-500">Chưa có booking.</td></tr>}</tbody></table></div></section>
      {user?.role === "ADMIN" && <section id="users"><div className="mb-4 flex flex-col justify-between gap-3 sm:flex-row sm:items-center"><h2 className="text-lg font-bold">Quản lý người dùng</h2><div className="flex gap-2"><label className="relative"><span className="sr-only">Tìm người dùng</span><FaSearch className="absolute left-3 top-3 text-slate-400"/><input value={query} onChange={(e)=>setQuery(e.target.value)} className="rounded-xl border border-slate-200 py-2 pl-9 pr-3 text-sm" placeholder="Tên, email, SĐT"/></label><select aria-label="Lọc vai trò" value={role} onChange={(e)=>setRole(e.target.value as UserRole | "")} className="rounded-xl border border-slate-200 px-3 text-sm"><option value="">Tất cả vai trò</option><option value="CUSTOMER">Khách hàng</option><option value="SALE">Sale</option><option value="COORDINATOR">Điều phối</option><option value="ADMIN">Admin</option></select></div></div><div className="overflow-x-auto rounded-2xl bg-white shadow-sm"><table className="w-full min-w-[760px] text-left text-sm"><thead className="bg-slate-50 text-slate-500"><tr><th className="p-4">Người dùng</th><th className="p-4">Vai trò</th><th className="p-4">Điện thoại</th><th className="p-4">Trạng thái</th><th className="p-4">Thao tác</th></tr></thead><tbody className="divide-y divide-slate-100">{visibleUsers.map((item)=><tr key={item.id}><td className="p-4 font-medium">{item.full_name}<br/><span className="font-normal text-slate-400">{item.email}</span></td><td className="p-4">{item.role}</td><td className="p-4">{item.phone || "–"}</td><td className="p-4">{item.status}</td><td className="p-4"><button disabled={item.id===user.id || item.status==="DISABLED"} onClick={()=>void changeStatus(item)} className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-semibold hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40">{item.status==="ACTIVE" ? "Khóa" : "Mở khóa"}</button></td></tr>)}</tbody></table></div></section>}
    </main>
  </div>;
}

export default function AdminDashboard() { return <ProtectedPage roles={["ADMIN", "COORDINATOR"]}><AdminDashboardContent/></ProtectedPage>; }
