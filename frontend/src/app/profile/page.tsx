"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FaUserEdit, FaCheck, FaArrowLeft } from "react-icons/fa";
import { useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";

export default function ProfilePage() {
  const router = useRouter();
  const { user, loading, refresh } = useAuth();
  
  const [form, setForm] = useState({ full_name: "", phone: "" });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (user) {
      setForm({
        full_name: user.full_name || "",
        phone: user.phone || ""
      });
    } else if (!loading) {
      router.replace("/login?next=/profile");
    }
  }, [user, loading, router]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setError("");
    setSuccess(false);

    try {
      await apiFetch("/auth/me", {
        method: "PUT",
        body: JSON.stringify(form)
      });
      await refresh();
      setSuccess(true);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Không thể cập nhật thông tin");
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
            <FaUserEdit className="text-2xl" />
          </span>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--ink)]">Thông tin cá nhân</h1>
          <p className="mt-2 text-sm text-[var(--muted)]">Cập nhật họ tên và số điện thoại liên hệ.</p>
        </div>

        <form onSubmit={(e) => void submit(e)} className="space-y-4 bg-white p-6 sm:p-8 rounded-3xl shadow-sm border border-black/5">
          {error && <div className="rounded-xl bg-red-50 p-4 text-sm text-red-600">{error}</div>}
          {success && <div className="rounded-xl bg-green-50 p-4 text-sm text-green-700 flex items-center gap-2"><FaCheck /> Đã cập nhật thông tin thành công.</div>}

          <div>
            <label className="mb-2 block text-sm font-medium text-[var(--ink)]">Email (Không thể thay đổi)</label>
            <input 
              type="email" 
              value={user.email} 
              disabled 
              className="w-full rounded-xl border border-black/10 bg-stone-50 px-4 py-3 text-[15px] outline-none text-[var(--muted)] cursor-not-allowed" 
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-[var(--ink)]">Họ và tên</label>
            <input 
              type="text" 
              required 
              minLength={2}
              value={form.full_name} 
              onChange={(e) => setForm({ ...form, full_name: e.target.value })} 
              className="w-full rounded-xl border border-black/10 bg-white px-4 py-3 text-[15px] outline-none transition focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)]" 
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-[var(--ink)]">Số điện thoại</label>
            <input 
              type="tel" 
              pattern="^\+?[0-9]{8,15}$"
              title="Số điện thoại chỉ bao gồm số, có thể bắt đầu bằng dấu +, từ 8-15 ký tự"
              value={form.phone} 
              onChange={(e) => setForm({ ...form, phone: e.target.value })} 
              className="w-full rounded-xl border border-black/10 bg-white px-4 py-3 text-[15px] outline-none transition focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)]" 
            />
          </div>

          <button 
            type="submit" 
            disabled={isSubmitting} 
            className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--ink)] px-4 py-3.5 text-[15px] font-semibold text-white transition hover:bg-[var(--forest)] disabled:opacity-50"
          >
            {isSubmitting ? "Đang lưu..." : "Lưu thay đổi"}
          </button>
        </form>
      </div>
    </main>
  );
}
