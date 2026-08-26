"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FormEvent, Suspense, useEffect, useState } from "react";
import { FaArrowLeft, FaCheckCircle, FaEye, FaEyeSlash, FaKey, FaLock, FaMagic } from "react-icons/fa";
import { apiFetch } from "@/lib/api";

function ForgotPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const tokenFromUrl = searchParams.get("token") || "";

  const [step, setStep] = useState<1 | 2>(1);
  const [email, setEmail] = useState("");
  const [token, setToken] = useState(tokenFromUrl);
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  const [debugToken, setDebugToken] = useState<string | null>(null);

  useEffect(() => {
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
      setStep(2);
    }
  }, [tokenFromUrl]);

  async function handleVerifyEmail(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccessMsg("");
    setDebugToken(null);

    try {
      const res = await apiFetch<{ message: string; debug_reset_token?: string }>("/auth/forgot-password", {
        method: "POST",
        body: JSON.stringify({ email }),
      });

      setSuccessMsg(res.message || "Yêu cầu đã được ghi nhận. Vui lòng kiểm tra email của bạn.");
      if (res.debug_reset_token) {
        setDebugToken(res.debug_reset_token);
      }
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Đã có lỗi xảy ra. Vui lòng thử lại.");
    } finally {
      setLoading(false);
    }
  }

  async function handleResetPassword(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setSuccessMsg("");

    if (newPassword !== confirmPassword) {
      setError("Mật khẩu xác nhận không khớp.");
      return;
    }

    if (newPassword.length < 8) {
      setError("Mật khẩu phải có ít nhất 8 ký tự.");
      return;
    }

    setLoading(true);

    try {
      const res = await apiFetch<{ message: string }>("/auth/reset-password", {
        method: "POST",
        body: JSON.stringify({ token, new_password: newPassword }),
      });

      setSuccessMsg(res.message || "Đặt lại mật khẩu thành công!");
      setTimeout(() => {
        router.push("/login");
      }, 2000);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Không thể đặt lại mật khẩu. Vui lòng thử lại.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="grid min-h-screen bg-[var(--paper)] lg:grid-cols-[.92fr_1.08fr]">
      <section className="relative hidden overflow-hidden bg-[var(--ink)] p-12 text-white lg:flex lg:flex-col lg:justify-between">
        <div className="absolute -right-32 top-28 h-96 w-96 rounded-full bg-[#477462]/35 blur-3xl" />
        <Link href="/" className="relative flex items-center gap-3">
          <img src="/brand/logo/nera-logo-reverse.svg" alt="Nera" className="h-8 w-auto" />
        </Link>
        <div className="relative max-w-lg">
          <p className="text-xs font-bold uppercase tracking-[.2em] text-[#b9d5bf]">Bảo mật & Khôi phục</p>
          <h1 className="mt-5 text-5xl font-semibold leading-[1.05] tracking-[-.05em]">Lấy lại quyền truy cập dễ dàng.</h1>
          <p className="mt-6 max-w-md text-lg leading-8 text-white/60">
            Thiết lập mật khẩu mới trong 30 giây để tiếp tục quản lý danh sách nhà và lịch hẹn của bạn.
          </p>
        </div>
        <p className="relative text-xs text-white/35">© 2026 Nera Home · Bảo mật & Quyền riêng tư.</p>
      </section>

      <section className="grid place-items-center px-4 py-10 sm:px-8">
        <div className="w-full max-w-md">
          <Link href="/login" className="mb-8 inline-flex items-center gap-2 text-sm font-semibold text-[var(--muted)] transition hover:text-[var(--forest)]">
            <FaArrowLeft /> Quay lại đăng nhập
          </Link>

          <div className="mb-8">
            <span className="mb-5 grid h-12 w-12 place-items-center rounded-2xl bg-[#e5eee6] text-[var(--forest)]">
              {step === 1 ? <FaKey /> : <FaLock />}
            </span>
            <h2 className="text-3xl font-semibold tracking-[-.045em]">
              {step === 1 ? "Quên mật khẩu?" : "Tạo mật khẩu mới"}
            </h2>
            <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
              {step === 1
                ? "Nhập email đăng ký. Nếu tài khoản tồn tại, chúng tôi sẽ gửi một liên kết bảo mật."
                : "Thiết lập mật khẩu mới bằng liên kết bảo mật đã được gửi cho bạn."}
            </p>
          </div>

          {error && (
            <div role="alert" className="mb-5 rounded-2xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-700">
              {error}
            </div>
          )}

          {successMsg && (
            <div role="status" className="mb-5 flex items-center gap-3 rounded-2xl border border-emerald-100 bg-emerald-50 px-4 py-3.5 text-sm font-medium text-emerald-800">
              <FaCheckCircle className="shrink-0 text-lg text-emerald-600" />
              <span>{successMsg}{step === 2 ? " Đang chuyển hướng về trang Đăng nhập…" : ""}</span>
            </div>
          )}

          {step === 1 ? (
            <form onSubmit={handleVerifyEmail} className="space-y-4">
              <label className="block text-sm font-semibold">
                Email tài khoản
                <input
                  type="email"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  required
                  className="mt-2 w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10"
                />
              </label>

              <button
                disabled={loading || !email.trim()}
                className="w-full rounded-2xl bg-[var(--ink)] py-3.5 font-semibold text-white transition hover:bg-[var(--forest)] disabled:opacity-50 cursor-pointer"
              >
                {loading ? "Đang gửi yêu cầu…" : "Gửi liên kết đặt lại mật khẩu"}
              </button>

              {debugToken && (
                <div className="mt-6 rounded-2xl border border-dashed border-amber-300 bg-amber-50/80 p-4">
                  <p className="text-xs font-bold uppercase tracking-wider text-amber-800">Chế độ Demo / Thử nghiệm</p>
                  <p className="mt-1 text-xs text-amber-700">
                    Vì chưa cấu hình SMTP email thật, mã token khôi phục được hiển thị trực tiếp bên dưới:
                  </p>
                  <button
                    type="button"
                    onClick={() => {
                      setToken(debugToken);
                      setStep(2);
                    }}
                    className="mt-3 inline-flex items-center gap-2 rounded-xl bg-amber-600 px-4 py-2 text-xs font-semibold text-white shadow-xs hover:bg-amber-700"
                  >
                    Bấm để đặt lại mật khẩu ngay →
                  </button>
                </div>
              )}
            </form>
          ) : (
            <form onSubmit={handleResetPassword} className="space-y-4">
              <div>
                <label className="text-sm font-semibold">Mật khẩu mới</label>
                <div className="relative mt-2">
                  <input
                    type={showPassword ? "text" : "password"}
                    autoComplete="new-password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                    minLength={8}
                    placeholder="Tối thiểu 8 ký tự"
                    className="w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 pr-12 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10"
                  />
                  <button
                    type="button"
                    aria-label={showPassword ? "Ẩn mật khẩu" : "Hiện mật khẩu"}
                    onClick={() => setShowPassword((v) => !v)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-stone-400"
                  >
                    {showPassword ? <FaEyeSlash /> : <FaEye />}
                  </button>
                </div>
              </div>

              <div>
                <label className="text-sm font-semibold">Xác nhận mật khẩu mới</label>
                <div className="relative mt-2">
                  <input
                    type={showPassword ? "text" : "password"}
                    autoComplete="new-password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    minLength={8}
                    placeholder="Nhập lại mật khẩu mới"
                    className="w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 pr-12 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10"
                  />
                </div>
              </div>

              <button
                disabled={loading || !newPassword || !confirmPassword}
                className="w-full rounded-2xl bg-[var(--ink)] py-3.5 font-semibold text-white transition hover:bg-[var(--forest)] disabled:opacity-50 cursor-pointer"
              >
                {loading ? "Đang xử lý…" : "Cập nhật mật khẩu"}
              </button>

              <button
                type="button"
                onClick={() => {
                  setStep(1);
                  setToken("");
                  setNewPassword("");
                  setConfirmPassword("");
                  setError("");
                }}
                className="mt-3 w-full text-center text-xs font-semibold text-[var(--muted)] hover:text-[var(--forest)]"
              >
                Nhập lại email khác
              </button>
            </form>
          )}

          <div className="mt-8 border-t border-black/5 pt-6 text-center text-xs text-[var(--muted)]">
            Cần trợ giúp thêm?{" "}
            <Link href="/chat" className="font-semibold text-[var(--forest)] hover:underline">
              Trò chuyện cùng Nera
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}

export default function ForgotPasswordPage() {
  return (
    <Suspense fallback={<div className="grid min-h-screen place-items-center bg-[var(--paper)]">Đang tải…</div>}>
      <ForgotPasswordForm />
    </Suspense>
  );
}
