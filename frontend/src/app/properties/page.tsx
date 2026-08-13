"use client";

import { FormEvent, Suspense, useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FaFilter, FaMagic, FaSearch, FaSlidersH, FaTimes } from "react-icons/fa";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import PropertyTile from "@/components/PropertyTile";
import { apiFetch } from "@/lib/api";
import { useAuth } from "@/components/AuthProvider";
import type { Property } from "@/lib/types";

interface PropertyResponse { items: Property[]; total: number }
interface Filters { keyword: string; district: string; propertyKind: string; minPrice: string; maxPrice: string; bedrooms: string; minArea: string; sort: string }

const emptyFilters: Filters = { keyword: "", district: "", propertyKind: "", minPrice: "", maxPrice: "", bedrooms: "", minArea: "", sort: "newest" };

function PropertiesContent() {
  const { user } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [filters, setFilters] = useState<Filters>(() => ({ ...emptyFilters, keyword: searchParams.get("keyword") ?? "", district: searchParams.get("district") ?? "" }));
  const [applied, setApplied] = useState(filters);
  const [properties, setProperties] = useState<Property[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [savedIds, setSavedIds] = useState<Set<string>>(new Set());
  const [showFilters, setShowFilters] = useState(false);
  const pageSize = 9;

  const query = useMemo(() => {
    const params = new URLSearchParams({ limit: String(pageSize), skip: String((page - 1) * pageSize), sort: applied.sort });
    if (applied.keyword) params.set("keyword", applied.keyword);
    if (applied.district) params.set("district", applied.district);
    if (applied.propertyKind) params.set("property_kind", applied.propertyKind);
    if (applied.minPrice) params.set("min_price", String(Number(applied.minPrice) * 1_000_000_000));
    if (applied.maxPrice) params.set("max_price", String(Number(applied.maxPrice) * 1_000_000_000));
    if (applied.bedrooms) params.set("min_bedrooms", applied.bedrooms);
    if (applied.minArea) params.set("min_area", applied.minArea);
    return params.toString();
  }, [applied, page]);

  const loadProperties = useCallback(async () => {
    setLoading(true); setError("");
    try { const data = await apiFetch<PropertyResponse>(`/properties?${query}`); setProperties(data.items ?? []); setTotal(data.total ?? 0); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Không thể tải kho nhà"); }
    finally { setLoading(false); }
  }, [query]);

  useEffect(() => { const timer = window.setTimeout(() => void loadProperties(), 0); return () => window.clearTimeout(timer); }, [loadProperties]);
  useEffect(() => { const timer = window.setTimeout(() => { if (user?.role === "CUSTOMER") void apiFetch<{ ids: string[] }>("/favorites/ids").then((data) => setSavedIds(new Set(data.ids))).catch(() => setSavedIds(new Set())); else setSavedIds(new Set()); }, 0); return () => window.clearTimeout(timer); }, [user]);

  function applyFilters(event?: FormEvent) { event?.preventDefault(); setPage(1); setApplied(filters); setShowFilters(false); }
  function clearFilters() { setFilters(emptyFilters); setApplied(emptyFilters); setPage(1); router.replace("/properties"); }
  async function toggleSaved(property: Property) {
    if (!user) { router.push(`/login?next=${encodeURIComponent("/properties")}`); return; }
    if (user.role !== "CUSTOMER") { setError("Chỉ tài khoản khách hàng có thể lưu nhà."); return; }
    const saved = savedIds.has(property.id);
    try { await apiFetch(`/favorites/${property.id}`, { method: saved ? "DELETE" : "PUT" }); setSavedIds((current) => { const next = new Set(current); if (saved) next.delete(property.id); else next.add(property.id); return next; }); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Không thể cập nhật nhà đã lưu"); }
  }

  const activeCount = Object.entries(applied).filter(([key, value]) => value && key !== "sort").length;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));

  const filterPanel = <form onSubmit={applyFilters} className="space-y-5">
    <div className="flex items-center justify-between"><h2 className="flex items-center gap-2 font-semibold"><FaSlidersH /> Bộ lọc</h2><button type="button" onClick={() => setShowFilters(false)} className="lg:hidden" aria-label="Đóng bộ lọc"><FaTimes /></button></div>
    <label className="block text-sm font-medium">Khu vực<input value={filters.district} onChange={(event) => setFilters({ ...filters, district: event.target.value })} placeholder="Cầu Giấy, Thanh Xuân…" className="mt-2 w-full rounded-xl border border-black/10 bg-[#fbfaf7] px-4 py-3 text-sm outline-none focus:border-[var(--sage)]" /></label>
    <label className="block text-sm font-medium">Loại nhà<select value={filters.propertyKind} onChange={(event) => setFilters({ ...filters, propertyKind: event.target.value })} className="mt-2 w-full rounded-xl border border-black/10 bg-[#fbfaf7] px-4 py-3 text-sm"><option value="">Tất cả loại hình</option><option value="APARTMENT">Căn hộ</option><option value="HOUSE">Nhà riêng</option><option value="TOWNHOUSE">Nhà phố</option><option value="VILLA">Biệt thự</option><option value="LAND">Đất</option></select></label>
    <div><p className="text-sm font-medium">Khoảng giá (tỷ)</p><div className="mt-2 grid grid-cols-2 gap-2"><input inputMode="decimal" value={filters.minPrice} onChange={(event) => setFilters({ ...filters, minPrice: event.target.value })} placeholder="Từ" className="min-w-0 rounded-xl border border-black/10 bg-[#fbfaf7] px-3 py-3 text-sm" /><input inputMode="decimal" value={filters.maxPrice} onChange={(event) => setFilters({ ...filters, maxPrice: event.target.value })} placeholder="Đến" className="min-w-0 rounded-xl border border-black/10 bg-[#fbfaf7] px-3 py-3 text-sm" /></div></div>
    <label className="block text-sm font-medium">Phòng ngủ tối thiểu<select value={filters.bedrooms} onChange={(event) => setFilters({ ...filters, bedrooms: event.target.value })} className="mt-2 w-full rounded-xl border border-black/10 bg-[#fbfaf7] px-4 py-3 text-sm"><option value="">Không giới hạn</option><option value="1">1 phòng</option><option value="2">2 phòng</option><option value="3">3 phòng trở lên</option></select></label>
    <label className="block text-sm font-medium">Diện tích tối thiểu (m²)<input type="number" min="0" value={filters.minArea} onChange={(event) => setFilters({ ...filters, minArea: event.target.value })} placeholder="Ví dụ: 60" className="mt-2 w-full rounded-xl border border-black/10 bg-[#fbfaf7] px-4 py-3 text-sm" /></label>
    <button className="w-full rounded-full bg-[var(--forest)] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[var(--ink)]">Áp dụng bộ lọc</button><button type="button" onClick={clearFilters} className="w-full text-sm font-semibold text-[var(--muted)] hover:text-[var(--ink)]">Xóa tất cả</button>
  </form>;

  return <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)]"><Header /><main>
    <section className="border-b border-black/5 bg-[#e6eee7] px-4 py-12 sm:px-6 lg:px-8"><div className="mx-auto max-w-7xl"><p className="text-xs font-bold uppercase tracking-[.2em] text-[var(--coral)]">Kho nhà có thể xem</p><div className="mt-3 flex flex-col justify-between gap-5 md:flex-row md:items-end"><div><h1 className="text-4xl font-semibold tracking-[-.045em] sm:text-5xl">Tìm bằng bộ lọc.<br /><span className="text-[var(--forest)]">Hiểu sâu bằng Nera.</span></h1><p className="mt-4 max-w-xl text-[var(--muted)]">Duyệt dữ liệu nhà thật hoặc mô tả nhu cầu tự nhiên để AI giúp thu hẹp lựa chọn.</p></div><Link href="/chat" className="inline-flex w-fit items-center gap-2 rounded-full bg-[var(--ink)] px-6 py-3 text-sm font-semibold text-white"><FaMagic /> Mô tả cho Nera</Link></div></div></section>
    <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8"><form onSubmit={applyFilters} className="flex gap-3"><div className="relative flex-1"><FaSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-[var(--muted)]" /><input value={filters.keyword} onChange={(event) => setFilters({ ...filters, keyword: event.target.value })} placeholder="Tên dự án, đường, phường hoặc quận…" className="w-full rounded-2xl border border-black/10 bg-white py-4 pl-12 pr-4 shadow-sm outline-none focus:border-[var(--sage)] focus:ring-4 focus:ring-[var(--sage)]/10" /></div><button className="rounded-2xl bg-[var(--forest)] px-6 font-semibold text-white">Tìm</button><button type="button" onClick={() => setShowFilters(true)} className="relative rounded-2xl border border-black/10 bg-white px-5 lg:hidden"><FaFilter />{activeCount > 0 && <span className="absolute -right-1 -top-1 grid h-5 w-5 place-items-center rounded-full bg-[var(--coral)] text-[10px] text-white">{activeCount}</span>}</button></form>
      <div className="mt-8 grid gap-8 lg:grid-cols-[260px_1fr]"><aside className="hidden h-fit rounded-[1.5rem] border border-black/5 bg-white p-5 shadow-sm lg:block lg:sticky lg:top-24">{filterPanel}</aside><div>
        <div className="mb-5 flex flex-wrap items-center justify-between gap-3"><p className="text-sm text-[var(--muted)]"><strong className="text-[var(--ink)]">{total}</strong> căn phù hợp</p><select value={filters.sort} onChange={(event) => { const next = { ...filters, sort: event.target.value }; setFilters(next); setApplied({ ...applied, sort: event.target.value }); setPage(1); }} className="rounded-xl border border-black/10 bg-white px-4 py-2.5 text-sm"><option value="newest">Mới nhất</option><option value="price_asc">Giá thấp đến cao</option><option value="price_desc">Giá cao đến thấp</option><option value="area_desc">Diện tích lớn nhất</option></select></div>
        {error && <div role="alert" className="mb-5 rounded-2xl border border-red-100 bg-red-50 p-4 text-sm text-red-700">{error} <button onClick={() => void loadProperties()} className="ml-2 font-semibold underline">Thử lại</button></div>}
        {loading ? <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">{Array.from({ length: 6 }).map((_, index) => <div key={index} className="h-[390px] animate-pulse rounded-[1.7rem] bg-white" />)}</div> : properties.length === 0 ? <div className="rounded-[1.7rem] border border-black/5 bg-white p-12 text-center"><div className="text-5xl">🏡</div><h2 className="mt-5 text-xl font-semibold">Chưa có căn khớp hoàn toàn</h2><p className="mt-2 text-sm text-[var(--muted)]">Nới bộ lọc hoặc mô tả ưu tiên để Nera tìm phương án gần nhất.</p><button onClick={clearFilters} className="mt-5 rounded-full bg-[var(--ink)] px-5 py-2.5 text-sm font-semibold text-white">Xóa bộ lọc</button></div> : <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">{properties.map((property) => <PropertyTile key={property.id} property={property} saved={savedIds.has(property.id)} onSave={(item) => void toggleSaved(item)} compact />)}</div>}
        {totalPages > 1 && <nav aria-label="Phân trang" className="mt-10 flex items-center justify-center gap-2"><button onClick={() => setPage((value) => Math.max(1, value - 1))} disabled={page === 1} className="rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-semibold disabled:opacity-30">Trước</button><span className="px-3 text-sm text-[var(--muted)]">{page} / {totalPages}</span><button onClick={() => setPage((value) => Math.min(totalPages, value + 1))} disabled={page === totalPages} className="rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-semibold disabled:opacity-30">Sau</button></nav>}
      </div></div>
    </section>
    {showFilters && <div className="fixed inset-0 z-50 bg-black/40 p-4 lg:hidden" onClick={() => setShowFilters(false)}><aside className="ml-auto h-full w-full max-w-sm overflow-y-auto bg-white p-6" onClick={(event) => event.stopPropagation()}>{filterPanel}</aside></div>}
  </main><Footer /></div>;
}

export default function PropertiesPage() { return <Suspense fallback={<div className="grid min-h-screen place-items-center bg-[var(--paper)]">Đang mở kho nhà…</div>}><PropertiesContent /></Suspense>; }
