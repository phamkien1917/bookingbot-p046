/* eslint-disable @next/next/no-img-element */
"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { FaBookmark, FaCalendarAlt, FaMapMarkerAlt, FaSpinner, FaTrash } from "react-icons/fa";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ProtectedPage from "@/components/ProtectedPage";
import { apiFetch } from "@/lib/api";
import type { Property } from "@/lib/types";

function SavedContent() {
  const [properties, setProperties] = useState<Property[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    try { setProperties((await apiFetch<{ items: Property[] }>("/favorites")).items); setError(""); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Không tải được danh sách đã lưu"); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { const timer = window.setTimeout(() => void load(), 0); return () => window.clearTimeout(timer); }, [load]);

  async function remove(property: Property) {
    try { await apiFetch<void>(`/favorites/${property.id}`, { method: "DELETE" }); setProperties((items) => items.filter((item) => item.id !== property.id)); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Không thể bỏ lưu bất động sản"); }
  }

  return <ProtectedPage roles={["CUSTOMER"]}><div className="min-h-screen bg-slate-50 text-slate-900"><Header /><main className="mx-auto max-w-6xl px-4 py-10"><div className="mb-8 flex items-center gap-3"><FaBookmark className="text-2xl text-teal-600" /><div><h1 className="text-3xl font-bold">Căn đã lưu</h1><p className="mt-1 text-sm text-slate-500">Danh sách được lưu theo tài khoản của bạn.</p></div></div>{error && <div role="alert" className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}{loading ? <div className="grid place-items-center py-24"><FaSpinner className="animate-spin text-3xl text-teal-500" /></div> : properties.length === 0 ? <div className="rounded-3xl bg-white py-20 text-center shadow-sm"><FaBookmark className="mx-auto mb-4 text-4xl text-slate-300" /><p className="text-slate-500">Bạn chưa lưu bất động sản nào.</p><Link href="/chat" className="mt-5 inline-block rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white">Tìm nhà với AI</Link></div> : <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">{properties.map((property) => <article key={property.id} className="overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm"><div className="h-48 bg-slate-100">{property.media[0]?.url ? <img src={property.media[0].url} alt={property.title} className="h-full w-full object-cover" /> : <div className="grid h-full place-items-center text-4xl">🏠</div>}</div><div className="p-5"><h2 className="font-bold line-clamp-2">{property.title}</h2><p className="mt-2 text-sm font-bold text-indigo-700">{property.list_price ? `${(property.list_price / 1e9).toFixed(1)} tỷ` : "Liên hệ"}</p><p className="mt-2 line-clamp-2 text-xs text-slate-500"><FaMapMarkerAlt className="mr-1 inline text-teal-500" />{[property.address_line, property.district, property.province].filter(Boolean).join(", ")}</p><div className="mt-5 flex gap-2"><Link href={`/properties/${property.id}`} className="flex-1 rounded-xl border border-slate-200 py-2.5 text-center text-sm font-semibold">Xem chi tiết</Link><Link href={`/booking/schedule?property_id=${property.id}`} className="rounded-xl bg-indigo-700 px-3 py-2.5 text-white" aria-label="Đặt lịch"><FaCalendarAlt /></Link><button onClick={() => void remove(property)} className="rounded-xl border border-red-200 px-3 py-2.5 text-red-500" aria-label="Bỏ lưu"><FaTrash /></button></div></div></article>)}</div>}</main><Footer /></div></ProtectedPage>;
}

export default function SavedPage() { return <SavedContent />; }
