"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import {
  FaArrowLeft, FaBrain, FaCalendarAlt, FaCheckCircle,
  FaExclamationCircle, FaMapMarkerAlt, FaSpinner, FaTimes
} from "react-icons/fa";
import Header from "@/components/Header";
import ProtectedPage from "@/components/ProtectedPage";
import PropertyImage from "@/components/PropertyImage";
import { useAuth } from "@/components/AuthProvider";
import { apiFetch } from "@/lib/api";
import { formatPropertyPrice } from "@/components/PropertyTile";
import type { Property } from "@/lib/types";

interface MemoryResponse { items: Record<string, unknown>; summary: string }

// ── AI comparison rows ────────────────────────────────────
const COMPARE_ROWS = [
  { key: "list_price", label: "Giá", format: (p: Property) => formatPropertyPrice(p.list_price) },
  { key: "bedrooms", label: "Phòng ngủ", format: (p: Property) => p.bedrooms != null ? `${p.bedrooms} PN` : "—" },
  { key: "area_sqm", label: "Diện tích", format: (p: Property) => p.area_sqm ? `${p.area_sqm} m²` : "—" },
  { key: "district", label: "Khu vực", format: (p: Property) => [p.district, p.province].filter(Boolean).join(", ") || "—" },
];

function bestIndex<T extends Property>(properties: T[], key: keyof T, higher: boolean): number {
  let best = -1;
  let bestVal = higher ? -Infinity : Infinity;
  properties.forEach((p, i) => {
    const v = Number(p[key]);
    if (!isNaN(v)) {
      if (higher ? v > bestVal : v < bestVal) { bestVal = v; best = i; }
    }
  });
  return best;
}

function buildAIComment(properties: Property[], memory: Record<string, unknown>): string {
  if (properties.length < 2) return "";
  const parts: string[] = [];
  const maxBudget = memory.max_price as number | undefined;

  // Price
  const cheapest = properties.reduce((a, b) => (a.list_price ?? Infinity) < (b.list_price ?? Infinity) ? a : b);
  parts.push(`${cheapest.title} có giá thấp nhất.`);

  if (maxBudget) {
    const over = properties.filter(p => p.list_price && p.list_price > maxBudget);
    if (over.length > 0) parts.push(`${over.map(p => p.title).join(", ")} vượt ngân sách của bạn.`);
  }

  // Area
  const largest = properties.reduce((a, b) => (a.area_sqm ?? 0) > (b.area_sqm ?? 0) ? a : b);
  if (largest.area_sqm) parts.push(`${largest.title} rộng rãi nhất (${largest.area_sqm} m²).`);

  // Memory hint
  const preferred = memory.district as string | undefined;
  if (preferred) {
    const match = properties.find(p => p.district?.toLowerCase().includes(preferred.toLowerCase()));
    if (match) parts.push(`${match.title} nằm đúng khu vực ${preferred} bạn ưu tiên.`);
  }

  return parts.join(" ");
}

function CompareContent() {
  const { user } = useAuth();
  const [properties, setProperties] = useState<Property[]>([]);
  const [memory, setMemory] = useState<Record<string, unknown>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [removed, setRemoved] = useState<string[]>([]);
  const [decisionMade, setDecisionMade] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [favRes, memRes] = await Promise.all([
        apiFetch<{ items: Property[] }>("/favorites"),
        user?.role === "CUSTOMER" ? apiFetch<MemoryResponse>("/memory") : Promise.resolve({ items: {}, summary: "" }),
      ]);
      setProperties(favRes.items ?? []);
      setMemory((memRes as MemoryResponse).items ?? {});
    } catch (err) {
      setError(err instanceof Error ? err.message : "Không tải được dữ liệu");
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => { void load(); }, [load]);

  const visible = properties.filter(p => !removed.includes(p.id)).slice(0, 3);
  const aiComment = buildAIComment(visible, memory);

  if (!user) return (
    <div className="grid min-h-screen place-items-center bg-[var(--paper)]">
      <div className="text-center">
        <p className="text-lg font-semibold">Vui lòng đăng nhập để so sánh căn hộ</p>
        <Link href="/login?next=/compare" className="mt-4 inline-block rounded-full bg-[var(--forest)] px-6 py-3 text-white font-semibold">Đăng nhập</Link>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)]">
      <Header />
      <main className="mx-auto max-w-7xl px-4 py-8">
        <div className="mb-6 flex items-center gap-3">
          <Link href="/chat" className="flex items-center gap-2 text-sm text-[var(--muted)] hover:text-[var(--ink)]">
            <FaArrowLeft /> Về chat
          </Link>
          <span className="text-black/20">/</span>
          <h1 className="text-xl font-bold">So sánh căn hộ</h1>
        </div>

        {loading ? (
          <div className="grid place-items-center py-24"><FaSpinner className="animate-spin text-3xl text-[var(--forest)]" /></div>
        ) : error ? (
          <div className="rounded-2xl border border-red-100 bg-red-50 p-6 text-red-700">{error}</div>
        ) : visible.length < 2 ? (
          <div className="rounded-[1.7rem] border border-black/5 bg-white p-12 text-center shadow-sm">
            <FaBrain className="mx-auto mb-4 text-4xl text-[var(--forest)]" />
            <p className="text-lg font-semibold">Chưa đủ căn để so sánh</p>
            <p className="mt-2 text-sm text-[var(--muted)]">Lưu ít nhất 2 căn hộ từ Nera để so sánh bên nhau.</p>
            <Link href="/chat" className="mt-6 inline-flex items-center gap-2 rounded-full bg-[var(--forest)] px-6 py-3 font-semibold text-white">
              Tìm nhà với Nera
            </Link>
          </div>
        ) : (
          <>
            {/* Properties header */}
            <div className={`grid gap-4 mb-0 ${visible.length === 3 ? "grid-cols-3" : "grid-cols-2"}`}
              style={{ gridTemplateColumns: `120px repeat(${visible.length}, 1fr)` }}>
              <div /> {/* Row label spacer */}
              {visible.map((p, i) => {
                const isLowest = i === bestIndex(visible, "list_price", false);
                const isLargest = i === bestIndex(visible, "area_sqm", true);
                return (
                  <div key={p.id} className="relative overflow-hidden rounded-[1.5rem] border border-black/5 bg-white shadow-sm">
                    <button onClick={() => setRemoved(r => [...r, p.id])}
                      className="absolute right-3 top-3 z-10 grid h-7 w-7 place-items-center rounded-full bg-white/80 text-xs text-[var(--muted)] hover:bg-red-50 hover:text-red-500 shadow-sm"
                      aria-label="Bỏ khỏi so sánh">
                      <FaTimes />
                    </button>
                    <div className="h-36 bg-stone-100">
                      {(p.image || p.media?.[0]?.url)
                        ? <PropertyImage src={p.image || p.media[0].url} alt={p.title} className="h-full w-full object-cover" />
                        : <div className="grid h-full place-items-center text-4xl">🏠</div>}
                    </div>
                    <div className="p-4">
                      {isLowest && <span className="mb-2 inline-block rounded-full bg-[#e4f5ea] px-2 py-0.5 text-[10px] font-bold text-emerald-700">Giá thấp nhất</span>}
                      {isLargest && <span className="mb-2 ml-1 inline-block rounded-full bg-[#eef3ee] px-2 py-0.5 text-[10px] font-bold text-[var(--forest)]">Rộng nhất</span>}
                      <h2 className="font-semibold text-sm leading-snug line-clamp-2">{p.title}</h2>
                      <p className="mt-1 text-xs text-[var(--muted)] flex items-center gap-1">
                        <FaMapMarkerAlt className="text-[var(--forest)]" />
                        {[p.district, p.province].filter(Boolean).join(", ") || "—"}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Comparison rows */}
            <div className="mt-3 rounded-[1.5rem] border border-black/5 bg-white shadow-sm overflow-hidden">
              {COMPARE_ROWS.map((row, ri) => {
                const minIdx = row.key === "list_price" ? bestIndex(visible, "list_price" as keyof Property, false) : -1;
                const maxIdx = row.key === "area_sqm" ? bestIndex(visible, "area_sqm" as keyof Property, true) : -1;

                return (
                  <div key={row.key}
                    className={`grid items-center gap-4 px-4 py-3 ${ri % 2 === 0 ? "bg-[#fbfaf7]" : "bg-white"}`}
                    style={{ gridTemplateColumns: `120px repeat(${visible.length}, 1fr)` }}>
                    <span className="text-xs font-bold uppercase tracking-wide text-[var(--muted)]">{row.label}</span>
                    {visible.map((p, i) => {
                      const isHighlight = i === minIdx || i === maxIdx;
                      return (
                        <span key={p.id} className={`text-sm font-semibold text-center ${isHighlight ? "text-[var(--forest)]" : "text-[var(--ink)]"}`}>
                          {isHighlight && <FaCheckCircle className="inline mr-1 text-emerald-500 text-[10px]" />}
                          {row.format(p)}
                        </span>
                      );
                    })}
                  </div>
                );
              })}

              {/* Memory-based match */}
              <div className="grid items-start gap-4 bg-[#f0f5f1] px-4 py-4"
                style={{ gridTemplateColumns: `120px repeat(${visible.length}, 1fr)` }}>
                <span className="text-xs font-bold uppercase tracking-wide text-[var(--forest)] flex items-center gap-1"><FaBrain /> Phù hợp</span>
                {visible.map(p => {
                  const maxBudget = memory.max_price as number | undefined;
                  const beds = memory.bedrooms as number | undefined;
                  const matchOk: string[] = [];
                  const matchCaution: string[] = [];
                  if (maxBudget && p.list_price) {
                    if (p.list_price <= maxBudget) matchOk.push("Trong ngân sách");
                    else matchCaution.push("Hơi vượt ngân sách");
                  }
                  if (beds && p.bedrooms != null) {
                    if (p.bedrooms >= beds) matchOk.push(`Đủ ${p.bedrooms} PN`);
                    else matchCaution.push("Thiếu phòng ngủ");
                  }
                  const dist = memory.district as string | undefined;
                  if (dist && p.district?.toLowerCase().includes(dist.toLowerCase())) matchOk.push(`Đúng khu ${dist}`);
                  return (
                    <div key={p.id} className="text-xs space-y-1">
                      {matchOk.map(r => <p key={r} className="flex items-center gap-1 text-[var(--forest)]"><FaCheckCircle className="text-emerald-500 shrink-0" />{r}</p>)}
                      {matchCaution.map(r => <p key={r} className="flex items-center gap-1 text-amber-700"><FaExclamationCircle className="shrink-0" />{r}</p>)}
                      {matchOk.length === 0 && matchCaution.length === 0 && <p className="text-[var(--muted)]">—</p>}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* AI Overall Comment */}
            {aiComment && (
              <div className="mt-5 rounded-2xl border border-[var(--sage)]/30 bg-[#edf3ed] p-5 flex gap-4">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-2xl bg-[var(--forest)] text-white"><FaBrain /></span>
                <div>
                  <p className="text-xs font-bold uppercase tracking-wide text-[var(--forest)] mb-1">Nhận xét từ Nera</p>
                  <p className="text-sm leading-6">{aiComment}</p>
                </div>
              </div>
            )}

            {/* Decision CTA */}
            <div className="mt-6 rounded-2xl border border-black/5 bg-white p-6 shadow-sm">
              <p className="font-semibold text-center mb-1">Lúc này điều gì quan trọng hơn với bạn?</p>
              <p className="text-xs text-center text-[var(--muted)] mb-5">Chọn để Nera thu hẹp lựa chọn.</p>
              <div className="flex flex-wrap justify-center gap-3">
                {["Đi làm thuận tiện", "Không gian bếp rộng", "Diện tích lớn nhất", "Tiết kiệm chi phí"].map(opt => (
                  <button key={opt} onClick={() => setDecisionMade(opt)}
                    className={`rounded-full border px-4 py-2 text-sm font-medium transition ${decisionMade === opt ? "border-[var(--forest)] bg-[var(--forest)] text-white" : "border-black/10 hover:border-[var(--sage)]"}`}>
                    {opt}
                  </button>
                ))}
              </div>
              {decisionMade && (
                <div className="mt-5 rounded-xl bg-[#f0f5f1] p-4 text-center">
                  <p className="text-sm font-semibold text-[var(--forest)]">✓ Nera đã ghi nhận: ưu tiên “{decisionMade}”</p>
                  <p className="text-xs text-[var(--muted)] mt-1">Thông tin này sẽ được dùng cho gợi ý tiếp theo.</p>
                  <Link href={`/chat?prompt=${encodeURIComponent(`Với ưu tiên ${decisionMade}, căn nào trong danh sách cân nhắc của tôi phù hợp nhất?`)}`}
                    className="mt-4 inline-flex items-center gap-2 rounded-full bg-[var(--forest)] px-5 py-2.5 text-sm font-semibold text-white">
                    Hỏi Nera ngay →
                  </Link>
                </div>
              )}
            </div>

            {/* Book buttons */}
            <div className={`mt-4 grid gap-3 ${visible.length === 3 ? "grid-cols-3" : "grid-cols-2"}`}>
              {visible.map(p => (
                <Link key={p.id} href={`/booking/schedule?property_id=${p.id}`}
                  className="flex items-center justify-center gap-2 rounded-2xl bg-[var(--ink)] py-3.5 text-sm font-semibold text-white hover:bg-[var(--forest)] transition">
                  <FaCalendarAlt /> Đặt lịch xem {p.title.split(" ").slice(0, 2).join(" ")}
                </Link>
              ))}
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default function ComparePage() {
  return (
    <ProtectedPage roles={["CUSTOMER"]}>
      <CompareContent />
    </ProtectedPage>
  );
}
