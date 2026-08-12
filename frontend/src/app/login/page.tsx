"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FaEye, FaEyeSlash, FaRobot } from "react-icons/fa";
import { postLoginDestination, useAuth } from "@/components/AuthProvider";
import type { User } from "@/lib/types";

export default function LoginPage() {
  const router = useRouter();
  const { user, login, register } = useAuth();
  const [isRegister, setIsRegister] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [authenticatedUser, setAuthenticatedUser] = useState<User | null>(null);
  const [form, setForm] = useState({ full_name: "", email: "", phone: "", password: "" });

  useEffect(() => {
    if (!authenticatedUser || user?.id !== authenticatedUser.id) return;
    const next = new URLSearchParams(window.location.search).get("next");
    router.replace(postLoginDestination(authenticatedUser.role, next));
    router.refresh();
  }, [authenticatedUser, router, user]);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const signedInUser = isRegister ? await register(form) : await login(form.email, form.password);
      setAuthenticatedUser(signedInUser);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Không thể đăng nhập");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-cyan-50 via-white to-indigo-50 grid place-items-center px-4 py-10">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-xl border border-slate-100 p-7 sm:p-9">
        <Link href="/" className="flex items-center justify-center gap-2 mb-7 text-slate-800"><FaRobot className="text-3xl text-teal-500" /><span className="text-xl font-bold">Booking Bot AI</span></Link>
        <h1 className="text-2xl font-bold text-slate-800">{isRegister ? "Tạo tài khoản khách hàng" : "Đăng nhập hệ thống"}</h1>
        <p className="text-sm text-slate-500 mt-1 mb-6">Hệ thống tự chuyển đến đúng khu vực Customer, Sale hoặc Admin.</p>
        {error && <div role="alert" className="bg-red-50 border border-red-200 text-red-600 text-sm px-4 py-3 rounded-xl mb-4">{error}</div>}
        <form onSubmit={submit} className="space-y-4">
          {isRegister && <label className="block text-sm font-medium text-slate-700">Họ và tên<input value={form.full_name} onChange={(event) => setForm({ ...form, full_name: event.target.value })} required minLength={2} className="mt-1 w-full px-4 py-3 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-teal-400" /></label>}
          <label className="block text-sm font-medium text-slate-700">Email<input type="email" autoComplete="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} required className="mt-1 w-full px-4 py-3 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-teal-400" /></label>
          {isRegister && <label className="block text-sm font-medium text-slate-700">Số điện thoại<input type="tel" autoComplete="tel" value={form.phone} onChange={(event) => setForm({ ...form, phone: event.target.value })} required pattern="^\+?[0-9]{8,15}$" className="mt-1 w-full px-4 py-3 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-teal-400" /></label>}
          <label className="block text-sm font-medium text-slate-700">Mật khẩu<div className="relative mt-1"><input type={showPassword ? "text" : "password"} autoComplete={isRegister ? "new-password" : "current-password"} value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} required minLength={6} className="w-full px-4 py-3 pr-12 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-teal-400" /><button type="button" aria-label={showPassword ? "Ẩn mật khẩu" : "Hiện mật khẩu"} onClick={() => setShowPassword((value) => !value)} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">{showPassword ? <FaEyeSlash /> : <FaEye />}</button></div></label>
          <button disabled={loading} className="w-full bg-[#00b4d8] text-white py-3.5 rounded-xl font-bold hover:bg-cyan-600 disabled:opacity-50">{loading ? "Đang xử lý..." : isRegister ? "Đăng ký" : "Đăng nhập"}</button>
        </form>
        <button onClick={() => { setIsRegister((value) => !value); setError(""); }} className="w-full mt-5 text-sm text-teal-700 font-semibold">{isRegister ? "Đã có tài khoản? Đăng nhập" : "Chưa có tài khoản? Đăng ký khách hàng"}</button>
        {!isRegister && <div className="mt-6 bg-slate-50 rounded-xl p-3 text-xs text-slate-500"><p className="font-semibold text-slate-700 mb-1">Tài khoản demo – mật khẩu Demo@123</p><p>Customer: customer.demo@example.com</p><p>Sale: kien.sale@example.com</p><p>Admin: admin.demo@example.com</p></div>}
      </div>
    </main>
  );
}
