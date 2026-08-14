"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FaLock, FaCheck, FaArrowLeft, FaEye, FaEyeSlash } from "react-icons/fa";
import { useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";

export default function ChangePasswordPage() {
  const router = useRouter();
  const { user, loading } = useAuth();
  
  const [form, setForm] = useState({ current_password: "", new_password: "", confirm_password: "" });
  const [showPassword, setShowPassword] = useState({ current: false, new: false, confirm: false });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (!loading && !user) {
      router.replace("/login?next=/change-password");
    }
  }, [user, loading, router]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (form.new_password !== form.confirm_password) {
      setError("Mật khẩu xác nhận không khớp.");
      return;
    }
    
    setIsSubmitting(true);
    setError("");
    setSuccess(false);

    try {
      await apiFetch("/auth/password", {
        method: "PUT",
        body: JSON.stringify({
          current_password: form.current_password,
          new_password: form.new_password
        })
      });
      setSuccess(true);
      setForm({ current_password: "", new_password: "", confirm_password: "" });
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Không thể đổi mật khẩu");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (loading || !user) {
    return <main className="min-h-screen bg-[var(--paper)] grid place-items-center"><div className="h-8 w-8 animate-spin rounded-full border-4 border-black/10 border-t-[var(--forest)]" /></main>;
  }

  return (
    <main className="min-h-screen bg-[var(--paper)] flex flex-col items-center py-12 px-4 sm:px-8">
      <div className="w-full max-w-md">
        <Link href="/" className="inline-flex items-center gap-2 text-sm text-[var(--muted)] hover:text-[var(--ink)] mb-8">
          <FaArrowLeft /> Trở về
        </Link>
        
        <div className="mb-8 text-center">
          <span className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-[var(--forest)]/10 text-[var(--forest)] mb-4">
            <FaLock className="text-2xl" />
          </span>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--ink)]">Đổi mật khẩu</h1>
          <p className="mt-2 text-sm text-[var(--muted)]">Đảm bảo mật khẩu của bạn dài ít nhất 6 ký tự.</p>
        </div>

        <form onSubmit={(e) => void submit(e)} className="space-y-4 bg-white p-6 sm:p-8 rounded-3xl shadow-sm border border-black/5">
          {error && <div className="rounded-xl bg-red-50 p-4 text-sm text-red-600">{error}</div>}
          {success && <div className="rounded-xl bg-green-50 p-4 text-sm text-green-700 flex items-center gap-2"><FaCheck /> Đổi mật khẩu thành công.</div>}

          <div>
            <label className="mb-2 block text-sm font-medium text-[var(--ink)]">Mật khẩu hiện tại</label>
            <div className="relative">
              <input 
                type={showPassword.current ? "text" : "password"} 
                required 
                value={form.current_password} 
                onChange={(e) => setForm({ ...form, current_password: e.target.value })} 
                className="w-full rounded-xl border border-black/10 bg-white px-4 py-3 text-[15px] outline-none transition focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)]" 
              />
              <button type="button" onClick={() => setShowPassword({ ...showPassword, current: !showPassword.current })} className="absolute right-4 top-1/2 -translate-y-1/2 text-stone-400 hover:text-[var(--forest)]">
                {showPassword.current ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-[var(--ink)]">Mật khẩu mới</label>
            <div className="relative">
              <input 
                type={showPassword.new ? "text" : "password"} 
                required 
                minLength={6}
                value={form.new_password} 
                onChange={(e) => setForm({ ...form, new_password: e.target.value })} 
                className="w-full rounded-xl border border-black/10 bg-white px-4 py-3 text-[15px] outline-none transition focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)]" 
              />
              <button type="button" onClick={() => setShowPassword({ ...showPassword, new: !showPassword.new })} className="absolute right-4 top-1/2 -translate-y-1/2 text-stone-400 hover:text-[var(--forest)]">
                {showPassword.new ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-[var(--ink)]">Xác nhận mật khẩu mới</label>
            <div className="relative">
              <input 
                type={showPassword.confirm ? "text" : "password"} 
                required 
                minLength={6}
                value={form.confirm_password} 
                onChange={(e) => setForm({ ...form, confirm_password: e.target.value })} 
                className="w-full rounded-xl border border-black/10 bg-white px-4 py-3 text-[15px] outline-none transition focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)]" 
              />
              <button type="button" onClick={() => setShowPassword({ ...showPassword, confirm: !showPassword.confirm })} className="absolute right-4 top-1/2 -translate-y-1/2 text-stone-400 hover:text-[var(--forest)]">
                {showPassword.confirm ? <FaEyeSlash /> : <FaEye />}
              </button>
            </div>
          </div>

          <button 
            type="submit" 
            disabled={isSubmitting} 
            className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--ink)] px-4 py-3.5 text-[15px] font-semibold text-white transition hover:bg-[var(--forest)] disabled:opacity-50"
          >
            {isSubmitting ? "Đang xử lý..." : "Cập nhật mật khẩu"}
          </button>
        </form>
      </div>
    </main>
  );
}
