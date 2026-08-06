"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect } from "react";
import { FaRobot, FaCalendarAlt, FaUserCircle } from "react-icons/fa";
import LoginModal from "./LoginModal";

const NAV_LINKS = [
  { href: "/", label: "Trang chủ" },
  { href: "/properties", label: "Căn hộ" },
  { href: "/#how-it-works", label: "Cách hoạt động" },
  { href: "/my-bookings", label: "Lịch xem của tôi" },
];

export default function Header() {
  const pathname = usePathname();
  const [showLogin, setShowLogin] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Check login state
    const token = localStorage.getItem("access_token");
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("token_type");
    setIsLoggedIn(false);
    window.location.reload();
  };

  return (
    <>
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex-shrink-0 flex items-center cursor-pointer">
              <FaRobot className="h-8 w-8 text-slate-800" />
              <span className="ml-2 text-xl font-bold text-slate-800">Booking Bot AI</span>
            </Link>

            <nav className="hidden md:flex space-x-8">
              {NAV_LINKS.map((link) => (
                <Link key={link.href} href={link.href}
                  className={`py-2 font-medium transition-colors ${
                    pathname === link.href
                      ? "text-teal-600 font-semibold border-b-2 border-teal-600"
                      : "text-slate-500 hover:text-slate-800"
                  }`}>
                  {link.label}
                </Link>
              ))}
            </nav>

            <div className="flex items-center space-x-4">
              {isLoggedIn ? (
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2 text-slate-600">
                    <FaUserCircle className="text-xl" />
                    <span className="text-sm font-medium">Tài khoản</span>
                  </div>
                  <button onClick={handleLogout} className="text-red-500 text-sm font-medium hover:text-red-600">
                    Đăng xuất
                  </button>
                </div>
              ) : (
                <button onClick={() => setShowLogin(true)} className="text-slate-600 font-medium hover:text-slate-900 px-3 py-2">
                  Đăng nhập
                </button>
              )}
              
              <Link href="/chat" className="bg-[#0b132b] text-white px-5 py-2 rounded-full font-medium flex items-center hover:bg-slate-800 transition-colors">
                <FaCalendarAlt className="mr-2 h-4 w-4" />
                Đặt lịch với AI
              </Link>
            </div>
          </div>
        </div>
      </header>
      {showLogin && <LoginModal onClose={() => setShowLogin(false)} />}
    </>
  );
}
