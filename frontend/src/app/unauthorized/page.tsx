"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";

export default function UnauthorizedPage() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  async function loginAgain() {
    setLoading(true);
    try {
      if (user) await logout();
      router.replace("/login");
      router.refresh();
    } finally {
      setLoading(false);
    }
  }

  return <main className="min-h-screen grid place-items-center bg-slate-50 px-4"><div className="text-center"><p className="text-6xl mb-4 text-slate-200">403</p><h1 className="text-2xl font-bold text-slate-800">Bạn không có quyền truy cập</h1><p className="text-slate-500 mt-2 mb-6">Hãy đăng nhập bằng tài khoản có vai trò phù hợp.</p><button onClick={() => void loginAgain()} disabled={loading} className="inline-block bg-slate-900 text-white px-6 py-3 rounded-xl disabled:opacity-50">{loading ? "Đang chuyển tài khoản…" : "Đăng xuất và đăng nhập lại"}</button></div></main>;
}
