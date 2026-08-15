/* eslint-disable @next/next/no-img-element */
"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import {
  FaArrowRight, FaBrain, FaCheck, FaCheckCircle, FaComments,
  FaExclamationCircle, FaSpinner, FaTimes, FaTrash
} from "react-icons/fa";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ProtectedPage from "@/components/ProtectedPage";
import { apiFetch } from "@/lib/api";

interface MemoryResponse { items: Record<string, unknown>; summary: string }

const FIELD_LABELS: Record<string, string> = {
  district: "Khu vực",
  province: "Tỉnh/TP",
  property_kind: "Loại nhà",
  bedrooms: "Phòng ngủ",
  min_price: "Giá từ",
  max_price: "Giá tới",
  budget: "Ngân sách",
  keyword: "Từ khoá",
  features: "Tiện ích",
  move_in: "Thời gian chuyển vào",
  family_size: "Thành viên gia đình",
  commute_max_min: "Di chuyển tối đa (phút)",
};

const FIELD_ICONS: Record<string, string> = {
  district: "📍", province: "🗺️", property_kind: "🏠", bedrooms: "🛏️",
  min_price: "💰", max_price: "💰", budget: "💰", keyword: "🔍",
  features: "✨", move_in: "📅", family_size: "👨‍👩‍👧", commute_max_min: "🚇",
};

function formatValue(key: string, value: unknown): string {
  if (Array.isArray(value)) return value.join(", ");
  if ((key === "min_price" || key === "max_price" || key === "budget") && typeof value === "number") {
    if (value >= 1_000_000_000) return `${(value / 1_000_000_000).toFixed(1)} tỷ`;
    if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(0)} triệu`;
  }
  return String(value);
}

function MemoryContent() {
  const [data, setData] = useState<MemoryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [deletingKey, setDeletingKey] = useState<string | null>(null);
  const [clearing, setClearing] = useState(false);
  const [confirmClear, setConfirmClear] = useState(false);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setData(await apiFetch<MemoryResponse>("/memory"));
    } catch {
      setError("Không tải được memory. Vui lòng thử lại.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void load(); }, [load]);

  async function deleteKey(key: string) {
    setDeletingKey(key);
    try {
      await apiFetch(`/memory/${key}`, { method: "DELETE" });
      setData(prev => prev ? { ...prev, items: Object.fromEntries(Object.entries(prev.items).filter(([k]) => k !== key)) } : null);
    } catch { setError("Không thể xóa tiêu chí này."); }
    finally { setDeletingKey(null); }
  }

  async function clearAll() {
    setClearing(true);
    try {
      await apiFetch("/memory", { method: "DELETE" });
      setData({ items: {}, summary: "" });
      setConfirmClear(false);
    } catch { setError("Không thể xóa memory."); }
    finally { setClearing(false); }
  }

  const entries = Object.entries(data?.items ?? {}).filter(([, v]) => v !== null && v !== "" && (!Array.isArray(v) || (v as unknown[]).length > 0));

  return (
    <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)]">
      <Header />
      <main className="mx-auto max-w-3xl px-4 py-10">
        {/* Header */}
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 rounded-full bg-[#edf3ed] px-4 py-2 text-xs font-bold text-[var(--forest)] mb-4">
            <FaBrain /> Memory của bạn
          </div>
          <h1 className="text-3xl font-bold tracking-tight">Những điều Nera đang ghi nhớ</h1>
          <p className="mt-2 text-[var(--muted)] leading-6">
            Đây là thông tin Nera dùng để cá nhân hóa gợi ý. Bạn có thể xem, xóa hoặc cập nhật bất kỳ lúc nào.
          </p>
        </div>

        {error && <div role="alert" className="mb-6 rounded-2xl bg-red-50 border border-red-100 p-4 text-sm text-red-700">{error}</div>}

        {loading ? (
          <div className="grid place-items-center py-24"><FaSpinner className="animate-spin text-3xl text-[var(--forest)]" /></div>
        ) : entries.length === 0 ? (
          <div className="rounded-[2rem] border border-black/5 bg-white p-12 text-center shadow-sm">
            <FaBrain className="mx-auto mb-4 text-5xl text-stone-200" />
            <p className="text-lg font-semibold">Nera chưa lưu gì về bạn</p>
            <p className="mt-2 text-sm text-[var(--muted)]">Trò chuyện tự nhiên và Nera sẽ ghi nhớ sở thích dần dần.</p>
            <Link href="/chat" className="mt-6 inline-flex items-center gap-2 rounded-full bg-[var(--forest)] px-6 py-3 font-semibold text-white">
              Bắt đầu trò chuyện <FaArrowRight />
            </Link>
          </div>
        ) : (
          <>
            {/* Summary banner */}
            {data?.summary && (
              <div className="mb-6 flex gap-4 rounded-2xl bg-[#edf3ed] p-5">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-2xl bg-[var(--forest)] text-white"><FaBrain /></span>
                <div>
                  <p className="text-xs font-bold uppercase tracking-wide text-[var(--forest)] mb-1">Tóm tắt sở thích</p>
                  <p className="text-sm leading-6">{data.summary}</p>
                </div>
              </div>
            )}

            {/* Memory items grid */}
            <div className="grid gap-3 sm:grid-cols-2">
              {entries.map(([key, value]) => (
                <div key={key}
                  className="group relative flex items-start gap-3 rounded-2xl border border-black/5 bg-white p-4 shadow-sm transition hover:shadow-md">
                  <span className="text-xl">{FIELD_ICONS[key] ?? "🔖"}</span>
                  <div className="min-w-0 flex-1">
                    <p className="text-[10px] font-bold uppercase tracking-wide text-[var(--muted)]">{FIELD_LABELS[key] ?? key}</p>
                    <p className="mt-0.5 font-semibold text-sm">{formatValue(key, value)}</p>
                    <p className="mt-1 text-[10px] text-[var(--muted)]">Đã xác nhận ✓</p>
                  </div>
                  <button
                    onClick={() => void deleteKey(key)}
                    disabled={deletingKey === key}
                    className="absolute right-3 top-3 grid h-7 w-7 place-items-center rounded-full text-[var(--muted)] opacity-0 group-hover:opacity-100 hover:bg-red-50 hover:text-red-500 transition"
                    aria-label={`Xóa ${FIELD_LABELS[key] ?? key}`}>
                    {deletingKey === key ? <FaSpinner className="animate-spin text-xs" /> : <FaTimes className="text-xs" />}
                  </button>
                </div>
              ))}
            </div>

            {/* What memory is used for */}
            <div className="mt-8 rounded-2xl border border-black/5 bg-white p-6 shadow-sm">
              <h2 className="font-semibold mb-4">Nera dùng memory này để làm gì?</h2>
              <div className="grid sm:grid-cols-3 gap-4">
                {[
                  { icon: <FaCheckCircle className="text-emerald-500" />, title: "Gợi ý phù hợp hơn", text: "Tự động lọc theo tiêu chí bạn đã chia sẻ." },
                  { icon: <FaComments className="text-[var(--forest)]" />, title: "Không hỏi lại từ đầu", text: "Lần sau trở lại, Nera tiếp tục từ nơi bạn dừng." },
                  { icon: <FaExclamationCircle className="text-amber-500" />, title: "So sánh sát hơn", text: "Nêu rõ điểm nào phù hợp và điểm nào cần cân nhắc." },
                ].map(item => (
                  <div key={item.title} className="rounded-xl bg-[#fbfaf7] p-4">
                    <div className="text-xl mb-2">{item.icon}</div>
                    <p className="text-xs font-bold">{item.title}</p>
                    <p className="mt-1 text-xs text-[var(--muted)] leading-5">{item.text}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* CTAs */}
            <div className="mt-6 flex flex-wrap gap-4 items-center justify-between">
              <div className="flex gap-3">
                <Link href="/chat" className="flex items-center gap-2 rounded-full bg-[var(--forest)] px-5 py-3 text-sm font-semibold text-white">
                  Tiếp tục tìm nhà <FaArrowRight />
                </Link>
                {entries.length >= 2 && (
                  <Link href="/compare" className="flex items-center gap-2 rounded-full border border-[var(--sage)]/50 px-5 py-3 text-sm font-semibold text-[var(--forest)]">
                    So sánh căn đã lưu
                  </Link>
                )}
              </div>
              <button onClick={() => setConfirmClear(true)}
                className="flex items-center gap-2 rounded-full border border-red-200 px-5 py-3 text-sm font-semibold text-red-500 hover:bg-red-50">
                <FaTrash /> Xóa toàn bộ memory
              </button>
            </div>
          </>
        )}
      </main>
      <Footer />

      {/* Clear confirm modal */}
      {confirmClear && (
        <div role="dialog" aria-modal="true" className="fixed inset-0 z-50 grid place-items-center bg-black/55 p-4">
          <div className="w-full max-w-md rounded-[1.7rem] bg-white p-6 shadow-2xl animate-message-in">
            <span className="grid h-12 w-12 place-items-center rounded-2xl bg-red-50 text-red-600 text-xl"><FaTrash /></span>
            <h2 className="mt-5 text-xl font-semibold">Xóa toàn bộ memory?</h2>
            <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
              Nera sẽ không còn nhớ gì về bạn. Lần tiếp theo trò chuyện sẽ bắt đầu từ đầu.
            </p>
            <div className="mt-6 flex gap-3">
              <button onClick={() => setConfirmClear(false)} className="flex-1 rounded-full border border-black/10 py-2.5 font-semibold">Giữ lại</button>
              <button onClick={() => void clearAll()} disabled={clearing}
                className="flex-1 rounded-full bg-red-600 py-2.5 font-semibold text-white disabled:opacity-40">
                {clearing ? "Đang xóa…" : "Xóa memory"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function MemoryPage() {
  return (
    <ProtectedPage roles={["CUSTOMER"]}>
      <MemoryContent />
    </ProtectedPage>
  );
}
