"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import { FaBars, FaCalendarAlt, FaRobot, FaTimes, FaUserCircle } from "react-icons/fa";
import { roleHome, useAuth } from "./AuthProvider";

const NAV_LINKS = [
  { href: "/", label: "Trang chủ" },
  { href: "/properties", label: "Bất động sản" },
  { href: "/#how-it-works", label: "Cách hoạt động" },
];

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, loading, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const customerActions = !user || user.role === "CUSTOMER";
  const navLinks = customerActions
    ? [...NAV_LINKS, { href: "/my-bookings", label: "Lịch xem của tôi" }, { href: "/booking/manual", label: "Đặt lịch thủ công" }]
    : NAV_LINKS;

  const handleLogout = async () => {
    try {
      await logout();
      setMobileOpen(false);
      router.push("/");
      router.refresh();
    } catch (reason) {
      window.alert(reason instanceof Error ? reason.message : "Không thể kết nối máy chủ để đăng xuất");
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16 gap-3">
          <Link href="/" className="flex items-center min-w-0">
            <FaRobot className="h-8 w-8 text-slate-800 shrink-0" />
            <span className="ml-2 text-lg sm:text-xl font-bold text-slate-800 truncate">Booking Bot AI</span>
          </Link>

          <nav className="hidden lg:flex space-x-7">
            {navLinks.map((link) => (
              <Link key={link.href} href={link.href} className={`py-2 text-sm font-medium transition-colors ${pathname === link.href ? "text-teal-600" : "text-slate-500 hover:text-slate-800"}`}>
                {link.label}
              </Link>
            ))}
          </nav>

          <div className="hidden sm:flex items-center gap-3">
            {!loading && (user ? (
              <>
                <Link href={roleHome(user.role)} className="flex items-center gap-2 text-slate-600 hover:text-teal-600">
                  <FaUserCircle className="text-xl" /><span className="hidden xl:inline text-sm font-medium">{user.full_name}</span>
                </Link>
                <button onClick={handleLogout} className="text-red-500 text-sm font-medium hover:text-red-600">Đăng xuất</button>
              </>
            ) : <Link href="/login" className="text-slate-600 font-medium hover:text-slate-900 px-3 py-2">Đăng nhập</Link>)}
            <Link href={customerActions ? "/chat" : user ? roleHome(user.role) : "/chat"} className="bg-[#0b132b] text-white px-4 py-2 rounded-full text-sm font-medium flex items-center hover:bg-slate-800">
              <FaCalendarAlt className="mr-2" /> {customerActions ? "Đặt lịch với AI" : "Vào dashboard"}
            </Link>
          </div>

          <button aria-label="Mở menu" onClick={() => setMobileOpen((value) => !value)} className="sm:hidden p-2 text-slate-700">
            {mobileOpen ? <FaTimes /> : <FaBars />}
          </button>
        </div>

        {mobileOpen && (
          <div className="sm:hidden border-t border-slate-100 py-4 space-y-2">
            {navLinks.map((link) => <Link key={link.href} href={link.href} onClick={() => setMobileOpen(false)} className="block px-3 py-2 rounded-lg text-slate-600 hover:bg-slate-50">{link.label}</Link>)}
            <Link href={customerActions ? "/chat" : user ? roleHome(user.role) : "/chat"} onClick={() => setMobileOpen(false)} className="block px-3 py-2 rounded-lg bg-slate-900 text-white">{customerActions ? "Đặt lịch với AI" : "Vào dashboard"}</Link>
            {user ? (
              <><Link href={roleHome(user.role)} onClick={() => setMobileOpen(false)} className="block px-3 py-2 text-teal-700">{user.full_name}</Link><button onClick={handleLogout} className="w-full text-left px-3 py-2 text-red-500">Đăng xuất</button></>
            ) : <Link href="/login" onClick={() => setMobileOpen(false)} className="block px-3 py-2 text-teal-700">Đăng nhập</Link>}
          </div>
        )}
      </div>
    </header>
  );
}
