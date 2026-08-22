"use client";

import { FormEvent, Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FaBrain, FaEye, FaEyeSlash, FaMagic, FaSpinner } from "react-icons/fa";
import { postLoginDestination, useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";
import type { User } from "@/lib/types";

const demos = [
  { label: "Khách hàng", email: "customer.demo@example.com" },
  { label: "Sale", email: "kien.sale@example.com" },
  { label: "Admin", email: "admin.demo@example.com" },
];

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { user, login, register, refresh } = useAuth();
  const [isRegister, setIsRegister] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const [error, setError] = useState("");
  const [authenticatedUser, setAuthenticatedUser] = useState<User | null>(null);
  const [form, setForm] = useState({ full_name: "", email: "", phone: "", password: "" });

  // Handle Google OAuth redirect callback token if present in URL
  useEffect(() => {
    const googleToken = searchParams.get("google_token");
    if (googleToken) {
      localStorage.setItem("nera_auth_token", googleToken);
      void refresh().then(() => {
        const next = searchParams.get("next");
        router.replace(next || "/");
      });
    }
  }, [searchParams, refresh, router]);

  useEffect(() => {
    if (!authenticatedUser || user?.id !== authenticatedUser.id) return;
    const next = searchParams.get("next");
    router.replace(postLoginDestination(authenticatedUser.role, next));
    router.refresh();
  }, [authenticatedUser, router, searchParams, user]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const signedInUser = isRegister ? await register(form) : await login(form.email, form.password);
      setAuthenticatedUser(signedInUser);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Email hoặc mật khẩu không chính xác.");
    } finally {
      setLoading(false);
    }
  }

  async function handleGoogleSignIn() {
    setGoogleLoading(true);
    setError("");
    try {
      const res = await apiFetch<{ url: string }>("/auth/google/signin-url");
      if (res.url) {
        window.location.href = res.url;
      }
    } catch (reason) {
      setError(
        reason instanceof Error
          ? reason.message
          : "Google OAuth chưa được cấu hình Client ID. Bạn có thể đăng nhập bằng email & mật khẩu."
      );
      setGoogleLoading(false);
    }
  }

  return (
    <div className="w-full max-w-md">
      <Link href="/" className="mb-9 flex items-center gap-3 lg:hidden">
        <span className="grid h-10 w-10 place-items-center rounded-2xl bg-[var(--ink)] text-white">
          <FaMagic />
        </span>
        <strong>Nera</strong>
      </Link>
      <div className="mb-8">
        <span className="mb-5 grid h-12 w-12 place-items-center rounded-2xl bg-[#e5eee6] text-[var(--forest)]">
          <FaBrain />
        </span>
        <h2 className="text-3xl font-semibold tracking-[-.045em]">
          {isRegister ? "Để Nera làm quen với bạn" : "Chào mừng bạn quay lại"}
        </h2>
        <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
          {isRegister
            ? "Tạo tài khoản người mua. Tài khoản Sale và Admin do hệ thống cấp."
            : "Một cửa đăng nhập, tự động chuyển đúng không gian của từng vai trò."}
        </p>
      </div>

      {error && (
        <div role="alert" className="mb-5 rounded-2xl border border-red-100 bg-red-50 p-4 text-sm text-red-700">
          <p>{error}</p>
          {!isRegister && (
            <p className="mt-2 text-xs">
              Quên mật khẩu?{" "}
              <Link href="/forgot-password" className="font-bold underline hover:text-red-900">
                Đặt lại mật khẩu tại đây
              </Link>
            </p>
          )}
        </div>
      )}

      {/* Google Sign-in Button */}
      <div className="mb-5">
        <button
          type="button"
          onClick={handleGoogleSignIn}
          disabled={googleLoading}
          className="flex w-full items-center justify-center gap-3 rounded-2xl border border-black/10 bg-white py-3.5 text-sm font-semibold text-stone-700 shadow-sm transition hover:border-black/20 hover:bg-stone-50 disabled:opacity-50"
        >
          <svg className="h-5 w-5" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
            />
          </svg>
          {googleLoading ? "Đang kết nối Google…" : "Đăng nhập bằng Google"}
        </button>

        <div className="relative my-6 flex items-center justify-center">
          <div className="w-full border-t border-black/10" />
          <span className="absolute bg-[var(--paper)] px-3 text-xs font-semibold uppercase tracking-wider text-stone-400">
            Hoặc bằng email
          </span>
        </div>
      </div>

      <form onSubmit={submit} className="space-y-4">
        {isRegister && (
          <label className="block text-sm font-semibold">
            Họ và tên
            <input
              value={form.full_name}
              onChange={(event) => setForm({ ...form, full_name: event.target.value })}
              required
              minLength={2}
              className="mt-2 w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10"
            />
          </label>
        )}

        <label className="block text-sm font-semibold">
          Email
          <input
            type="email"
            autoComplete="email"
            value={form.email}
            onChange={(event) => setForm({ ...form, email: event.target.value })}
            required
            className="mt-2 w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10"
          />
        </label>

        {isRegister && (
          <label className="block text-sm font-semibold">
            Số điện thoại
            <input
              type="tel"
              autoComplete="tel"
              value={form.phone}
              onChange={(event) => setForm({ ...form, phone: event.target.value })}
              required
              pattern="^\+?[0-9]{8,15}$"
              className="mt-2 w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10"
            />
          </label>
        )}

        <div>
          <div className="flex items-center justify-between">
            <label className="text-sm font-semibold">Mật khẩu</label>
            {!isRegister && (
              <Link href="/forgot-password" className="text-xs font-semibold text-[var(--forest)] hover:underline">
                Quên mật khẩu?
              </Link>
            )}
          </div>
          <div className="relative mt-2">
            <input
              type={showPassword ? "text" : "password"}
              autoComplete={isRegister ? "new-password" : "current-password"}
              value={form.password}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
              required
              minLength={6}
              className="w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 pr-12 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10"
            />
            <button
              type="button"
              aria-label={showPassword ? "Ẩn mật khẩu" : "Hiện mật khẩu"}
              onClick={() => setShowPassword((value) => !value)}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-stone-400"
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </button>
          </div>
        </div>

        <button
          disabled={loading}
          className="w-full rounded-2xl bg-[var(--ink)] py-3.5 font-semibold text-white transition hover:bg-[var(--forest)] disabled:opacity-50"
        >
          {loading ? "Đang xử lý…" : isRegister ? "Tạo tài khoản" : "Tiếp tục"}
        </button>
      </form>

      <button
        onClick={() => {
          setIsRegister((value) => !value);
          setError("");
        }}
        className="mt-5 w-full text-sm font-semibold text-[var(--forest)]"
      >
        {isRegister ? "Đã có tài khoản? Đăng nhập" : "Lần đầu đến đây? Tạo tài khoản người mua"}
      </button>

      {process.env.NEXT_PUBLIC_ENABLE_DEMO_LOGIN === "true" && !isRegister && (
        <div className="mt-8 border-t border-black/5 pt-6">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[.14em] text-stone-400">
            Vào nhanh bản demo · mật khẩu Demo@123
          </p>
          <div className="flex flex-wrap gap-2">
            {demos.map((demo) => (
              <button
                key={demo.email}
                onClick={() =>
                  setForm((current) => ({
                    ...current,
                    email: demo.email,
                    password: "Demo@123",
                  }))
                }
                className="rounded-full border border-black/10 bg-white px-3 py-2 text-xs font-semibold text-[var(--muted)] hover:border-[var(--sage)] hover:text-[var(--forest)]"
              >
                {demo.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function LoginPage() {
  return (
    <main className="grid min-h-screen bg-[var(--paper)] lg:grid-cols-[.92fr_1.08fr]">
      <section className="relative hidden overflow-hidden bg-[var(--ink)] p-12 text-white lg:flex lg:flex-col lg:justify-between">
        <div className="absolute -right-32 top-28 h-96 w-96 rounded-full bg-[#477462]/35 blur-3xl" />
        <Link href="/" className="relative flex items-center gap-3">
          <span className="grid h-11 w-11 place-items-center rounded-2xl bg-white/10">
            <FaMagic className="text-[#b9d5bf]" />
          </span>
          <span className="text-xl font-semibold tracking-[-.03em]">Nera</span>
        </Link>
        <div className="relative max-w-lg">
          <p className="text-xs font-bold uppercase tracking-[.2em] text-[#b9d5bf]">Trải nghiệm tiếp nối</p>
          <h1 className="mt-5 text-5xl font-semibold leading-[1.05] tracking-[-.05em]">
            Quay lại đúng nơi câu chuyện đang dở.
          </h1>
          <p className="mt-6 max-w-md text-lg leading-8 text-white/60">
            Đăng nhập để Nera nhớ nhu cầu, căn đã lưu và lịch xem của bạn — không phải bắt đầu lại từ một form trống.
          </p>
        </div>
        <p className="relative text-xs text-white/35">© 2026 Nera Home · Đồng hành cùng bạn tìm kiếm không gian sống lý tưởng.</p>
      </section>

      <section className="grid place-items-center px-4 py-10 sm:px-8">
        <Suspense fallback={<div className="flex items-center gap-2 text-stone-500"><FaSpinner className="animate-spin" /> Đang tải trang đăng nhập…</div>}>
          <LoginForm />
        </Suspense>
      </section>
    </main>
  );
}
