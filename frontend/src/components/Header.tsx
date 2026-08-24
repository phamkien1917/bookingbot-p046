"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import { FaBars, FaBookmark, FaCalendarAlt, FaMagic, FaSignOutAlt, FaTimes, FaUserCircle } from "react-icons/fa";
import { roleHome, useAuth } from "./AuthProvider";
import NotificationBell from "./NotificationBell";

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, loading, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);
  const isCustomer = !user || user.role === "CUSTOMER";
  const customerLinks = [
    { href: "/saved", label: "Đã lưu", icon: <FaBookmark /> },
    { href: "/my-bookings", label: "Lịch xem", icon: <FaCalendarAlt /> },
  ];



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
          {!loading && user && <NotificationBell />}
          {!loading && (user ? <div className="relative"><button onClick={() => setProfileMenuOpen((open) => !open)} className="flex items-center gap-2 rounded-full px-3 py-2 text-sm font-medium text-[var(--muted)] hover:bg-white hover:text-[var(--forest)]"><FaUserCircle className="text-lg" /><span className="max-w-28 truncate">{user.full_name}</span></button>{profileMenuOpen && <><div className="fixed inset-0 z-40" onClick={() => setProfileMenuOpen(false)} /><div className="absolute right-0 top-12 z-50 w-56 rounded-2xl border border-black/5 bg-white p-2 shadow-[0_20px_60px_rgba(20,40,35,.16)]"><Link href="/profile" onClick={() => setProfileMenuOpen(false)} className="block w-full rounded-xl px-4 py-2.5 text-left text-sm font-medium hover:bg-stone-50 text-[var(--ink)]">Cập nhật thông tin</Link><Link href="/change-password" onClick={() => setProfileMenuOpen(false)} className="block w-full rounded-xl px-4 py-2.5 text-left text-sm font-medium hover:bg-stone-50 text-[var(--ink)]">Đổi mật khẩu</Link><button onClick={() => { setProfileMenuOpen(false); void handleLogout(); }} className="flex w-full items-center gap-2 rounded-xl px-4 py-2.5 text-left text-sm font-medium text-red-600 hover:bg-red-50"><FaSignOutAlt /> Đăng xuất</button></div></>}</div> : <Link href="/login" className="rounded-full px-4 py-2 text-sm font-semibold text-[var(--forest)] hover:bg-white">Đăng nhập</Link>)}
          <Link href={isCustomer ? "/chat?new=1" : user ? roleHome(user.role) : "/chat?new=1"} className="flex items-center gap-2 rounded-full bg-[var(--ink)] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[var(--forest)]"><FaMagic />{isCustomer ? "Nói với Nera" : "Không gian làm việc"}</Link>
        </div>

        <button onClick={() => setMobileOpen((open) => !open)} className="grid h-10 w-10 place-items-center rounded-full bg-white sm:hidden" aria-label="Mở menu">{mobileOpen ? <FaTimes /> : <FaBars />}</button>
      </div>
      {mobileOpen && <div className="border-t border-black/5 bg-[var(--paper)] p-4 sm:hidden"><nav className="space-y-1">{isCustomer && customerLinks.map((link) => <Link key={link.href} href={link.href} onClick={() => setMobileOpen(false)} className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium text-[var(--muted)] hover:bg-white">{link.icon}{link.label}</Link>)}{user && !isCustomer && <Link href={roleHome(user.role)} onClick={() => setMobileOpen(false)} className="block rounded-xl bg-[var(--ink)] px-4 py-3 text-sm font-semibold text-white">Mở không gian làm việc</Link>}{user ? <button onClick={() => void handleLogout()} className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium text-red-600"><FaSignOutAlt />Đăng xuất</button> : <Link href="/login" onClick={() => setMobileOpen(false)} className="block rounded-xl px-4 py-3 text-sm font-semibold text-[var(--forest)]">Đăng nhập để Nera nhớ bạn</Link>}</nav></div>}
    </header>
  );
}
