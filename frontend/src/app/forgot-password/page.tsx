"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FaArrowLeft, FaCheckCircle, FaEye, FaEyeSlash, FaKey, FaLock, FaMagic } from "react-icons/fa";
import { apiFetch } from "@/lib/api";

export default function ForgotPasswordPage() {
  const router = useRouter();
  const [step, setStep] = useState<1 | 2>(1);
  const [email, setEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  async function handleVerifyEmail(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await apiFetch<{ message: string; exists: boolean; email?: string }>("/auth/forgot-password", {
        method: "POST",
        body: JSON.stringify({ email }),
      });

      if (!res.exists) {
        setError("Không tìm thấy tài khoản tương ứng với email này. Vui lòng kiểm tra lại.");
        return;
      }

      setStep(2);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Đã xảy ra lỗi khi kiểm tra email.");
    } finally {
      setLoading(false);
    }
  }

  async function handleResetPassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    if (newPassword.length < 6) {
      setError("Mật khẩu mới phải có ít nhất 6 ký tự.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("Xác nhận mật khẩu không khớp.");
      return;
    }

    setLoading(true);
    try {
      const res = await apiFetch<{ message: string }>("/auth/reset-password", {
        method: "POST",
        body: JSON.stringify({
          email,
          new_password: newPassword,
        }),
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
          <span className="grid h-11 w-11 place-items-center rounded-2xl bg-white/10">
            <FaMagic className="text-[#b9d5bf]" />
          </span>
          <span className="text-xl font-semibold tracking-[-.03em]">Nera</span>
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
                ? "Nhập email đăng ký của bạn để xác thực và đặt lại mật khẩu mới."
                : `Thiết lập mật khẩu mới cho tài khoản ${email}.`}
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
              <span>{successMsg} Đang chuyển hướng về trang Đăng nhập…</span>
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
                type="submit"
                disabled={loading || !email.trim()}
                className="w-full rounded-2xl bg-[var(--ink)] py-3.5 font-semibold text-white transition hover:bg-[var(--forest)] disabled:opacity-50"
              >
                {loading ? "Đang kiểm tra…" : "Tiếp tục"}
              </button>
            </form>
          ) : (
            <form onSubmit={handleResetPassword} className="space-y-4">
              <label className="block text-sm font-semibold">
                Mật khẩu mới
                <div className="relative mt-2">
                  <input
                    type={showPassword ? "text" : "password"}
                    autoComplete="new-password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                    minLength={6}
                    placeholder="Ít nhất 6 ký tự"
                    className="w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 pr-12 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10"
                  />
                  <button
                    type="button"
                    aria-label={showPassword ? "Ẩn mật khẩu" : "Hiện mật khẩu"}
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-stone-400"
                  >
                    {showPassword ? <FaEyeSlash /> : <FaEye />}
                  </button>
                </div>
              </label>

              <label className="block text-sm font-semibold">
                Xác nhận mật khẩu mới
                <div className="relative mt-2">
                  <input
                    type={showPassword ? "text" : "password"}
                    autoComplete="new-password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    minLength={6}
                    placeholder="Nhập lại mật khẩu mới"
                    className="w-full rounded-2xl border border-black/10 bg-white px-4 py-3.5 pr-12 font-normal outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10"
                  />
                </div>
              </label>

              <button
                type="submit"
                disabled={loading || !newPassword || !confirmPassword}
                className="w-full rounded-2xl bg-[var(--ink)] py-3.5 font-semibold text-white transition hover:bg-[var(--forest)] disabled:opacity-50"
              >
                {loading ? "Đang cập nhật…" : "Cập nhật mật khẩu"}
              </button>

              <button
                type="button"
                onClick={() => setStep(1)}
                className="w-full text-center text-xs font-semibold text-[var(--muted)] hover:text-[var(--forest)]"
              >
                Đổi email khác
              </button>
            </form>
          )}

          <div className="mt-8 border-t border-black/5 pt-6 text-center text-xs text-[var(--muted)]">
            Cần thêm hỗ trợ?{" "}
            <Link href="/chat" className="font-semibold text-[var(--forest)] hover:underline">
              Trò chuyện cùng Nera
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
