"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { FaCalendarAlt, FaCheck, FaClock, FaHome, FaRobot, FaSignOutAlt, FaTimes } from "react-icons/fa";
import ProtectedPage from "@/components/ProtectedPage";
import { useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";
import type { Booking } from "@/lib/types";

interface SaleOverview {
  stats: { pending: number; confirmed: number };
  pending_requests: Booking[];
  schedule: Booking[];
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("vi-VN", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
}

function SaleDashboardContent() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [data, setData] = useState<SaleOverview | null>(null);
  const [error, setError] = useState("");
  const [workingId, setWorkingId] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      setData(await apiFetch<SaleOverview>("/sale/overview"));
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Không tải được dữ liệu");
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  async function decide(booking: Booking, accept: boolean) {
    let reason = "";
    if (!accept) {
      reason = window.prompt("Lý do từ chối lịch này:", "Không thể phục vụ khung giờ đã chọn") ?? "";
      if (!reason.trim()) return;
    }
    setWorkingId(booking.id);
    try {
      await apiFetch(`/sale/requests/${booking.id}/${accept ? "accept" : "reject"}`, {
        method: "POST",
        body: accept ? undefined : JSON.stringify({ reason }),
      });
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Không xử lý được yêu cầu");
    } finally {
      setWorkingId(null);
    }
  }

  async function handleLogout() {
    await logout();
    router.replace("/login");
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 lg:flex">
      <aside className="bg-[#0b132b] p-5 text-white lg:min-h-screen lg:w-64">
        <div className="flex items-center gap-3 border-b border-white/10 pb-5">
          <FaRobot className="text-2xl text-teal-400" />
          <div><p className="font-bold">Booking Bot</p><p className="text-xs text-teal-300">Cổng nhân viên Sale</p></div>
        </div>
        <nav className="mt-6 space-y-2" aria-label="Điều hướng Sale">
          <a href="#tong-quan" className="flex items-center gap-3 rounded-xl bg-white/10 px-4 py-3 text-sm"><FaHome /> Tổng quan</a>
          <a href="#yeu-cau" className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm hover:bg-white/10"><FaClock /> Yêu cầu chờ xử lý</a>
          <a href="#lich" className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm hover:bg-white/10"><FaCalendarAlt /> Lịch đã xác nhận</a>
        </nav>
        <button onClick={() => void handleLogout()} className="mt-8 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm text-red-300 hover:bg-white/10"><FaSignOutAlt /> Đăng xuất</button>
      </aside>

      <main className="flex-1 p-4 sm:p-8">
        <header id="tong-quan" className="mb-8">
          <h1 className="text-2xl font-bold">Xin chào, {user?.full_name}</h1>
          <p className="mt-1 text-sm text-slate-500">Các yêu cầu dưới đây là dữ liệu thực từ hệ thống.</p>
        </header>
        {error && <div role="alert" className="mb-5 rounded-xl bg-red-50 p-4 text-sm text-red-700">{error}</div>}
        <section className="mb-8 grid gap-4 sm:grid-cols-2" aria-label="Số liệu Sale">
          <div className="rounded-2xl bg-white p-6 shadow-sm"><p className="text-sm text-slate-500">Đang chờ xử lý</p><p className="mt-2 text-4xl font-bold text-orange-500">{data?.stats.pending ?? "–"}</p></div>
          <div className="rounded-2xl bg-white p-6 shadow-sm"><p className="text-sm text-slate-500">Đã xác nhận</p><p className="mt-2 text-4xl font-bold text-teal-600">{data?.stats.confirmed ?? "–"}</p></div>
        </section>

        <section id="yeu-cau" className="mb-10">
          <h2 className="mb-4 text-lg font-bold">Yêu cầu cần phản hồi</h2>
          {!data ? <p className="text-sm text-slate-500">Đang tải…</p> : data.pending_requests.length === 0 ? (
            <div className="rounded-2xl bg-white p-8 text-center text-slate-500">Không có yêu cầu nào đang chờ.</div>
          ) : <div className="grid gap-4 xl:grid-cols-2">{data.pending_requests.map((booking) => (
            <article key={booking.id} className="rounded-2xl border border-slate-100 bg-white p-5 shadow-sm">
              <div className="flex flex-wrap justify-between gap-3"><div><p className="font-bold">{booking.customer?.full_name}</p><a className="text-sm text-teal-700 hover:underline" href={`tel:${booking.customer?.phone ?? ""}`}>{booking.customer?.phone || booking.customer?.email}</a></div><span className="rounded-full bg-orange-50 px-3 py-1 text-xs font-semibold text-orange-700">{booking.request_code}</span></div>
              <div className="my-4 rounded-xl bg-slate-50 p-4"><p className="font-semibold">{booking.property.title}</p><p className="mt-1 text-sm text-slate-500">{booking.property.address}</p><p className="mt-2 text-sm"><FaClock className="mr-2 inline text-teal-600" />{formatDate(booking.preferred_start)}</p></div>
              {booking.customer_note && <p className="mb-4 text-sm text-slate-600">Ghi chú: {booking.customer_note}</p>}
              <div className="flex gap-3"><button disabled={workingId === booking.id} onClick={() => void decide(booking, false)} className="flex-1 rounded-xl border border-red-200 py-2.5 text-sm font-semibold text-red-600 hover:bg-red-50 disabled:opacity-50"><FaTimes className="mr-2 inline" />Từ chối</button><button disabled={workingId === booking.id} onClick={() => void decide(booking, true)} className="flex-1 rounded-xl bg-teal-600 py-2.5 text-sm font-semibold text-white hover:bg-teal-700 disabled:opacity-50"><FaCheck className="mr-2 inline" />Nhận lịch</button></div>
            </article>
          ))}</div>}
        </section>

        <section id="lich">
          <h2 className="mb-4 text-lg font-bold">Lịch đã xác nhận</h2>
          <div className="overflow-x-auto rounded-2xl border border-slate-100 bg-white shadow-sm">
            <table className="w-full min-w-[700px] text-left text-sm"><thead className="bg-slate-50 text-slate-500"><tr><th className="p-4">Thời gian</th><th className="p-4">Khách hàng</th><th className="p-4">Bất động sản</th><th className="p-4">Mã lịch</th></tr></thead><tbody className="divide-y divide-slate-100">{data?.schedule.map((booking) => <tr key={booking.id}><td className="p-4 font-medium">{formatDate(booking.appointment?.starts_at ?? booking.preferred_start)}</td><td className="p-4">{booking.customer?.full_name}<br/><a className="text-xs text-teal-700" href={`tel:${booking.customer?.phone ?? ""}`}>{booking.customer?.phone}</a></td><td className="p-4">{booking.property.title}</td><td className="p-4 font-mono">{booking.appointment?.booking_code}</td></tr>)}{data?.schedule.length === 0 && <tr><td colSpan={4} className="p-8 text-center text-slate-500">Chưa có lịch được xác nhận.</td></tr>}</tbody></table>
          </div>
        </section>
      </main>
    </div>
  );
}

export default function SaleDashboard() {
  return <ProtectedPage roles={["SALE"]}><SaleDashboardContent /></ProtectedPage>;
}
