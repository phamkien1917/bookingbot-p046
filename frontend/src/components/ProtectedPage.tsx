"use client";

import { useEffect, useRef } from "react";
import { usePathname, useRouter } from "next/navigation";
import { FaSpinner } from "react-icons/fa";
import { useAuth } from "./AuthProvider";
import type { UserRole } from "@/lib/types";

export default function ProtectedPage({ roles, children }: { roles: UserRole[]; children: React.ReactNode }) {
  const { user, loading, authUnavailable, refresh } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const verifiedMismatch = useRef("");

  useEffect(() => {
    if (loading || authUnavailable) return;
    if (!user) router.replace(`/login?next=${encodeURIComponent(pathname)}`);
    else if (!roles.includes(user.role)) {
      const mismatchKey = `${user.id}:${user.role}:${pathname}`;
      if (verifiedMismatch.current !== mismatchKey) {
        verifiedMismatch.current = mismatchKey;
        const timer = window.setTimeout(() => void refresh(), 0);
        return () => window.clearTimeout(timer);
      }
      router.replace("/unauthorized");
    } else {
      verifiedMismatch.current = "";
    }
  }, [authUnavailable, loading, pathname, refresh, roles, router, user]);

  if (authUnavailable) {
    return <div className="min-h-screen grid place-items-center bg-slate-50 px-4"><div className="max-w-md text-center"><h1 className="text-xl font-bold text-slate-800">Tạm thời mất kết nối máy chủ</h1><p className="mt-2 text-sm text-slate-500">Phiên đăng nhập của bạn vẫn được giữ. Hãy thử kết nối lại thay vì đăng nhập lại.</p><button onClick={() => void refresh()} className="mt-5 rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white">Thử kết nối lại</button></div></div>;
  }

  if (loading || !user || !roles.includes(user.role)) {
    return <div className="min-h-screen grid place-items-center bg-slate-50"><FaSpinner className="animate-spin text-3xl text-teal-500" /></div>;
  }
  return children;
}
