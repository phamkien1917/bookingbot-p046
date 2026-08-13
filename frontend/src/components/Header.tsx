"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { FaBars, FaBell, FaBookmark, FaCalendarAlt, FaComments, FaMagic, FaSignOutAlt, FaTimes, FaUserCircle } from "react-icons/fa";
import { roleHome, useAuth } from "./AuthProvider";
import { apiFetch } from "@/lib/api";

type Notice = { id: string; template_key: string; payload: Record<string, unknown>; status: string };

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, loading, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [noticeOpen, setNoticeOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notice[]>([]);
  const isCustomer = !user || user.role === "CUSTOMER";
  const customerLinks = [
    { href: "/chat", label: "Trò chuyện", icon: <FaComments /> },
    { href: "/saved", label: "Đã lưu", icon: <FaBookmark /> },
    { href: "/my-bookings", label: "Lịch xem", icon: <FaCalendarAlt /> },
  ];

  useEffect(() => {
    let active = true;
    const load = async () => {
      if (!user) { setNotifications([]); return; }
      try {
        const data = await apiFetch<{ items: Notice[] }>("/notifications");
        if (active) setNotifications(data.items);
      } catch { if (active) setNotifications([]); }
    };
    void load();
    const timer = window.setInterval(() => void load(), 30000);
    return () => { active = false; window.clearInterval(timer); };
  }, [user]);

  async function markRead(id: string) {
    try {
      await apiFetch<void>(`/notifications/${id}/read`, { method: "POST" });
      setNotifications((items) => items.map((item) => item.id === id ? { ...item, status: "DELIVERED" } : item));
    } catch { /* Keep the notification available for a retry. */ }
  }

  async function handleLogout() {
    await logout();
    setMobileOpen(false);
    router.replace("/");
    router.refresh();
  }

  return (
    <header className="sticky top-0 z-40 border-b border-black/5 bg-[var(--paper)]/88 backdrop-blur-xl">
      <div className="mx-auto flex h-[72px] max-w-7xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-3" aria-label="Nera - trang chủ">
          <span className="grid h-10 w-10 place-items-center rounded-2xl bg-[var(--ink)] text-white shadow-sm"><FaMagic /></span>
          <span><strong className="block text-[17px] leading-4 tracking-[-.03em]">Nera</strong><small className="text-[10px] font-semibold uppercase tracking-[.15em] text-[var(--muted)]">AI home companion</small></span>
        </Link>

        {isCustomer && <nav className="hidden items-center gap-1 md:flex" aria-label="Điều hướng chính">{customerLinks.map((link) => <Link key={link.href} href={link.href} className={`flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition ${pathname === link.href ? "bg-white text-[var(--forest)] shadow-sm" : "text-[var(--muted)] hover:bg-white/70 hover:text-[var(--ink)]"}`}><span className="text-xs">{link.icon}</span>{link.label}</Link>)}</nav>}

        <div className="hidden items-center gap-2 sm:flex">
          {!loading && user && <div className="relative"><button onClick={() => setNoticeOpen((open) => !open)} className="relative grid h-10 w-10 place-items-center rounded-full text-[var(--muted)] hover:bg-white" aria-label="Thông báo" aria-expanded={noticeOpen}><FaBell />{notifications.some((item) => item.status === "PENDING") && <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-[var(--coral)] ring-2 ring-[var(--paper)]" />}</button>{noticeOpen && <div className="absolute right-0 top-12 z-50 w-80 rounded-2xl border border-black/5 bg-white p-3 shadow-[0_20px_60px_rgba(20,40,35,.16)]"><p className="px-2 pb-2 text-sm font-semibold">Thông báo</p>{notifications.length === 0 ? <p className="rounded-xl bg-stone-50 p-4 text-xs text-[var(--muted)]">Chưa có cập nhật mới.</p> : notifications.slice(0, 5).map((item) => <button key={item.id} onClick={() => void markRead(item.id)} className={`mb-1 w-full rounded-xl p-3 text-left text-xs hover:bg-stone-50 ${item.status === "PENDING" ? "bg-[#eef5ef]" : ""}`}><span className="font-semibold">{item.template_key === "sale_booking_request" ? "Yêu cầu xem nhà mới" : item.template_key === "booking_confirmed" ? "Lịch xem đã xác nhận" : "Cập nhật lịch xem"}</span><span className="mt-1 block text-[var(--muted)]">{String(item.payload.property_title ?? "Nera")}</span></button>)}</div>}</div>}
          {!loading && (user ? <><Link href={roleHome(user.role)} className="flex items-center gap-2 rounded-full px-3 py-2 text-sm font-medium text-[var(--muted)] hover:bg-white hover:text-[var(--forest)]"><FaUserCircle className="text-lg" /><span className="max-w-28 truncate">{user.full_name}</span></Link><button onClick={() => void handleLogout()} className="grid h-10 w-10 place-items-center rounded-full text-stone-400 hover:bg-red-50 hover:text-red-600" aria-label="Đăng xuất"><FaSignOutAlt /></button></> : <Link href="/login" className="rounded-full px-4 py-2 text-sm font-semibold text-[var(--forest)] hover:bg-white">Đăng nhập</Link>)}
          <Link href={isCustomer ? "/chat" : user ? roleHome(user.role) : "/chat"} className="flex items-center gap-2 rounded-full bg-[var(--ink)] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[var(--forest)]"><FaMagic />{isCustomer ? "Nói với Nera" : "Không gian làm việc"}</Link>
        </div>

        <button onClick={() => setMobileOpen((open) => !open)} className="grid h-10 w-10 place-items-center rounded-full bg-white sm:hidden" aria-label="Mở menu">{mobileOpen ? <FaTimes /> : <FaBars />}</button>
      </div>
      {mobileOpen && <div className="border-t border-black/5 bg-[var(--paper)] p-4 sm:hidden"><nav className="space-y-1">{isCustomer && customerLinks.map((link) => <Link key={link.href} href={link.href} onClick={() => setMobileOpen(false)} className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium text-[var(--muted)] hover:bg-white">{link.icon}{link.label}</Link>)}{user && !isCustomer && <Link href={roleHome(user.role)} onClick={() => setMobileOpen(false)} className="block rounded-xl bg-[var(--ink)] px-4 py-3 text-sm font-semibold text-white">Mở không gian làm việc</Link>}{user ? <button onClick={() => void handleLogout()} className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium text-red-600"><FaSignOutAlt />Đăng xuất</button> : <Link href="/login" onClick={() => setMobileOpen(false)} className="block rounded-xl px-4 py-3 text-sm font-semibold text-[var(--forest)]">Đăng nhập để Nera nhớ bạn</Link>}</nav></div>}
    </header>
  );
}
