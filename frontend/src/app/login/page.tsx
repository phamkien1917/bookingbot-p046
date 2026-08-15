"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FaBrain, FaCheck, FaEye, FaEyeSlash, FaMagic } from "react-icons/fa";
import { postLoginDestination, useAuth } from "@/components/AuthProvider";
import type { User } from "@/lib/types";

const demos = [
  { label: "Khách hàng", email: "customer.demo@example.com" },
  { label: "Sale", email: "kien.sale@example.com" },
  { label: "Admin", email: "admin.demo@example.com" },
];

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

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const signedInUser = isRegister ? await register(form) : await login(form.email, form.password);
      setAuthenticatedUser(signedInUser);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Không thể đăng nhập");
    } finally { setLoading(false); }
  }

  return (
    <main className="grid min-h-screen bg-[var(--paper)] lg:grid-cols-[.92fr_1.08fr]">
      <section className="relative hidden overflow-hidden bg-[var(--ink)] p-12 text-white lg:flex lg:flex-col lg:justify-between">
        <div className="absolute -right-32 top-28 h-96 w-96 rounded-full bg-[#477462]/35 blur-3xl" />
        <Link href="/" className="relative flex items-center gap-3"><span className="grid h-11 w-11 place-items-center rounded-2xl bg-white/10"><FaMagic className="text-[#b9d5bf]" /></span><span className="text-xl font-semibold tracking-[-.03em]">Nera</span></Link>
        <div className="relative max-w-lg">
          <p className="text-xs font-bold uppercase tracking-[.2em] text-[#b9d5bf]">Trải nghiệm tiếp nối</p>
          <h1 className="mt-5 text-5xl font-semibold leading-[1.05] tracking-[-.05em]">Quay lại đúng nơi câu chuyện đang dở.</h1>
          <p className="mt-6 max-w-md text-lg leading-8 text-white/60">Đăng nhập để Nera nhớ nhu cầu, căn đã lưu và lịch xem của bạn — không phải bắt đầu lại từ một form trống.</p>
          <div className="mt-9 space-y-4 text-sm text-white/75"><p className="flex items-center gap-3"><FaCheck className="text-[#b9d5bf]" /> Sở thích được lưu ở PostgreSQL</p><p className="flex items-center gap-3"><FaCheck className="text-[#b9d5bf]" /> Bạn có thể xem và xóa memory</p><p className="flex items-center gap-3"><FaCheck className="text-[#b9d5bf]" /> Phiên đăng nhập dùng cookie HttpOnly</p></div>
        </div>
        <p className="relative text-xs text-white/35">Nera chỉ dùng memory để cá nhân hóa trải nghiệm tìm nhà.</p>
      </section>

      <section className="grid place-items-center px-4 py-10 sm:px-8">
        <div className="w-full max-w-md">
          <Link href="/" className="mb-9 flex items-center gap-3 lg:hidden"><span className="grid h-10 w-10 place-items-center rounded-2xl bg-[var(--ink)] text-white"><FaMagic /></span><strong>Nera</strong></Link>
          <div className="mb-8"><span className="mb-5 grid h-12 w-12 place-items-center rounded-2xl bg-[#e5eee6] text-[var(--forest)]"><FaBrain /></span><h2 className="text-3xl font-semibold tracking-[-.045em]">{isRegister ? "Để Nera làm quen với bạn" : "Chào mừng bạn quay lại"}</h2><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{isRegister ? "Tạo tài khoản người mua. Tài khoản Sale và Admin do hệ thống cấp." : "Một cửa đăng nhập, tự động chuyển đúng không gian của từng vai trò."}</p></div>

          {error && <div role="alert" className="mb-5 rounded-2xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}
          <form onSubmit={submit} className="space-y-4">
            {isRegister && <label className="block text-sm font-semibold">Họ và tên<input value={form.full_name} onChange={(event) => setForm({ ...form, full_name: event.target.value })} required minLength={2} className="mt-2 w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10" /></label>}
            <label className="block text-sm font-semibold">Email<input type="email" autoComplete="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} required className="mt-2 w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10" /></label>
            {isRegister && <label className="block text-sm font-semibold">Số điện thoại<input type="tel" autoComplete="tel" value={form.phone} onChange={(event) => setForm({ ...form, phone: event.target.value })} required pattern="^\+?[0-9]{8,15}$" className="mt-2 w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10" /></label>}
            <label className="block text-sm font-semibold">Mật khẩu<div className="relative mt-2"><input type={showPassword ? "text" : "password"} autoComplete={isRegister ? "new-password" : "current-password"} value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} required minLength={6} className="w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 pr-12 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10" /><button type="button" aria-label={showPassword ? "Ẩn mật khẩu" : "Hiện mật khẩu"} onClick={() => setShowPassword((value) => !value)} className="absolute right-4 top-1/2 -translate-y-1/2 text-stone-400">{showPassword ? <FaEyeSlash /> : <FaEye />}</button></div></label>
            <button disabled={loading} className="w-full rounded-2xl bg-[var(--ink)] py-3.5 font-semibold text-white transition hover:bg-[var(--forest)] disabled:opacity-50">{loading ? "Đang xử lý…" : isRegister ? "Tạo tài khoản" : "Tiếp tục"}</button>
          </form>
          <button onClick={() => { setIsRegister((value) => !value); setError(""); }} className="mt-5 w-full text-sm font-semibold text-[var(--forest)]">{isRegister ? "Đã có tài khoản? Đăng nhập" : "Lần đầu đến đây? Tạo tài khoản người mua"}</button>

          {!isRegister && <div className="mt-8 border-t border-black/5 pt-6"><p className="mb-3 text-xs font-semibold uppercase tracking-[.14em] text-stone-400">Vào nhanh bản demo · mật khẩu Demo@123</p><div className="flex flex-wrap gap-2">{demos.map((demo) => <button key={demo.email} onClick={() => setForm((current) => ({ ...current, email: demo.email, password: "Demo@123" }))} className="rounded-full border border-black/10 bg-white px-3 py-2 text-xs font-semibold text-[var(--muted)] hover:border-[var(--sage)] hover:text-[var(--forest)]">{demo.label}</button>)}</div></div>}
        </div>
      </section>
    </main>
  );
}
