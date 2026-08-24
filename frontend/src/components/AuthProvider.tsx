"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";
import { API_BASE, ApiError, apiFetch } from "@/lib/api";
import type { User } from "@/lib/types";

interface RegisterInput {
  full_name: string;
  email: string;
  phone: string;
  password: string;
}

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  authUnavailable: boolean;
  login: (email: string, password: string) => Promise<User>;
  register: (input: RegisterInput) => Promise<User>;
  logout: () => Promise<void>;
  refresh: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function roleHome(role: User["role"]): string {
  if (role === "ADMIN" || role === "COORDINATOR") return "/admin";
  if (role === "SALE") return "/sale";
  return "/";
}

export function postLoginDestination(role: User["role"], next: string | null): string {
  if (!next || !next.startsWith("/") || next.startsWith("//")) return roleHome(role);

  const pathname = next.split(/[?#]/, 1)[0];
  if (pathname === "/login" || pathname === "/unauthorized") return roleHome(role);
  if (pathname.startsWith("/admin")) {
    return role === "ADMIN" || role === "COORDINATOR" ? next : roleHome(role);
  }
  if (pathname.startsWith("/sale")) {
    return role === "SALE" ? next : roleHome(role);
  }
  if (pathname.startsWith("/booking") || pathname.startsWith("/my-bookings") || pathname.startsWith("/saved")) {
    return role === "CUSTOMER" ? next : roleHome(role);
  }
  return next;
}

export default function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [authUnavailable, setAuthUnavailable] = useState(false);
  const operationVersion = useRef(0);

  const refresh = useCallback(async () => {
    const operation = operationVersion.current;
    setLoading(true);
    try {
      for (let attempt = 0; attempt < 5; attempt += 1) {
        try {
          const currentUser = await apiFetch<User>("/auth/me");
          if (operation === operationVersion.current) {
            setUser(currentUser);
            setAuthUnavailable(false);
          }
          return;
        } catch (reason) {
          if (reason instanceof ApiError && (reason.status === 401 || reason.status === 403)) {
            if (operation === operationVersion.current) {
              setUser(null);
              setAuthUnavailable(false);
            }
            return;
          }
          if (attempt < 4) await new Promise((resolve) => window.setTimeout(resolve, 250 * (attempt + 1)));
        }
      }
      if (operation === operationVersion.current) setAuthUnavailable(true);
    } finally {
      if (operation === operationVersion.current) setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => void refresh(), 0);
    return () => window.clearTimeout(timer);
  }, [refresh]);

  const login = useCallback(async (email: string, password: string) => {
    const operation = ++operationVersion.current;
    setLoading(true);
    setUser(null);
    setAuthUnavailable(false);
    try {
      const body = new URLSearchParams({ username: email, password });
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body,
      });
      const payload = (await response.json()) as { detail?: string; user?: User; access_token?: string };
      if (!response.ok || !payload.user) throw new Error(payload.detail ?? "Đăng nhập thất bại");
      if (payload.access_token && typeof window !== "undefined") {
        localStorage.setItem("nera_auth_token", payload.access_token);
      }

      // Read the new cookie back from the server before protected pages render.
      const confirmedUser = await apiFetch<User>("/auth/me");
      if (operation === operationVersion.current) setUser(confirmedUser);
      return confirmedUser;
    } catch (reason) {
      if (!(reason instanceof ApiError) || reason.status >= 500) setAuthUnavailable(true);
      throw reason;
    } finally {
      if (operation === operationVersion.current) setLoading(false);
    }
  }, []);

  const register = useCallback(async (input: RegisterInput) => {
    await apiFetch<User>("/auth/register", { method: "POST", body: JSON.stringify(input) });
    return login(input.email, input.password);
  }, [login]);

  const logout = useCallback(async () => {
    const operation = ++operationVersion.current;
    setLoading(true);
    try {
      if (typeof window !== "undefined") {
        localStorage.removeItem("nera_auth_token");
        // Prevent the next account from reusing a conversation owned by the
        // account signing out. Guest-to-customer login remains uninterrupted.
        sessionStorage.removeItem("nera_chat_session_id");
      }
      await apiFetch<void>("/auth/logout", { method: "POST" });
      if (operation === operationVersion.current) {
        setUser(null);
        setAuthUnavailable(false);
      }
    } catch (reason) {
      if (operation === operationVersion.current) setAuthUnavailable(true);
      throw reason;
    } finally {
      if (operation === operationVersion.current) setLoading(false);
    }
  }, []);

  const value = useMemo(() => ({ user, loading, authUnavailable, login, register, logout, refresh }), [user, loading, authUnavailable, login, register, logout, refresh]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
}
