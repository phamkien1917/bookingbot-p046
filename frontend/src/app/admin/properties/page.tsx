"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { FaArrowLeft, FaEdit, FaEye, FaEyeSlash, FaPlus, FaSearch, FaSpinner } from "react-icons/fa";
import ProtectedPage from "@/components/ProtectedPage";
import Header from "@/components/Header";
import { apiFetch } from "@/lib/api";

interface PropertyItem {
  id: string;
  code: string;
  title: string;
  property_kind: string;
  status: string;
  area_sqm: number;
  list_price: number | null;
  address: string;
}

export default function AdminPropertiesPage() {
  const [items, setItems] = useState<PropertyItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  
  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await apiFetch<{items: PropertyItem[], total: number}>(`/admin/properties?limit=50&q=${query}`);
      setItems(res.items);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Không tải được danh sách BĐS");
    } finally {
      setLoading(false);
    }
  }, [query]);

  useEffect(() => {
    const timer = setTimeout(() => void load(), 300);
    return () => clearTimeout(timer);
  }, [load]);

  const toggleStatus = async (item: PropertyItem) => {
    const newStatus = item.status === "HIDDEN" ? "AVAILABLE" : "HIDDEN";
    if (!window.confirm(`Đổi trạng thái BĐS ${item.code} thành ${newStatus}?`)) return;
    try {
      await apiFetch(`/admin/properties/${item.id}`, {
        method: "PATCH",
        body: JSON.stringify({ status: newStatus })
      });
      await load();
    } catch {
      alert("Lỗi khi cập nhật trạng thái");
    }
  };

  return (
    <ProtectedPage roles={["ADMIN", "COORDINATOR"]}>
      <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)] font-sans">
        <Header />
        <main className="max-w-6xl mx-auto px-4 py-8">
          <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <Link href="/admin" className="text-sm text-[var(--muted)] flex items-center mb-2 hover:text-[var(--ink)]"><FaArrowLeft className="mr-2"/> Về trang quản trị</Link>
              <h1 className="text-3xl font-bold">Kho Bất Động Sản</h1>
            </div>
            <div className="flex items-center gap-3">
              <div className="relative">
                <FaSearch className="absolute left-3 top-3.5 text-[var(--muted)]" />
                <input 
                  type="text" 
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Tìm kiếm BĐS..." 
                  className="pl-9 pr-4 py-2.5 rounded-xl border border-black/10 w-full md:w-64 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)]"
                />
              </div>
              <button className="bg-[var(--forest)] text-white px-5 py-2.5 rounded-xl font-semibold flex items-center gap-2 hover:opacity-90 transition-opacity">
                <FaPlus /> Thêm mới
              </button>
            </div>
          </div>
          
          {error && <div className="bg-red-50 text-red-600 p-4 rounded-xl mb-6">{error}</div>}
          
          <div className="bg-white rounded-[1.5rem] border border-black/5 shadow-sm overflow-x-auto">
            <table className="w-full text-left text-sm whitespace-nowrap">
              <thead className="bg-[#fbfaf7] text-[var(--muted)] border-b border-black/5">
                <tr>
                  <th className="p-4 font-semibold">Mã BĐS</th>
                  <th className="p-4 font-semibold">Tên BĐS</th>
                  <th className="p-4 font-semibold">Loại</th>
                  <th className="p-4 font-semibold">Giá / Diện tích</th>
                  <th className="p-4 font-semibold">Trạng thái</th>
                  <th className="p-4 font-semibold text-right">Thao tác</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-black/5">
                {loading ? (
                  <tr><td colSpan={6} className="p-12 text-center"><FaSpinner className="animate-spin text-2xl text-[var(--forest)] mx-auto" /></td></tr>
                ) : items.length === 0 ? (
                  <tr><td colSpan={6} className="p-12 text-center text-[var(--muted)]">Không tìm thấy bất động sản nào.</td></tr>
                ) : items.map((item) => (
                  <tr key={item.id} className="hover:bg-[#fbfaf7] transition-colors">
                    <td className="p-4 font-mono font-medium">{item.code}</td>
                    <td className="p-4">
                      <p className="font-bold text-[15px] truncate max-w-[300px]">{item.title}</p>
                      <p className="text-xs text-[var(--muted)] truncate max-w-[300px]">{item.address}</p>
                    </td>
                    <td className="p-4"><span className="bg-slate-100 text-slate-700 px-2.5 py-1 rounded-md text-xs font-semibold">{item.property_kind}</span></td>
                    <td className="p-4">
                      <p className="font-bold text-[var(--coral)]">{item.list_price ? (item.list_price / 1e9).toFixed(2) + " Tỷ" : "Thỏa thuận"}</p>
                      <p className="text-xs text-[var(--muted)]">{item.area_sqm} m²</p>
                    </td>
                    <td className="p-4">
                      <span className={`px-3 py-1.5 inline-flex text-xs font-bold rounded-full ${item.status === 'AVAILABLE' ? 'bg-emerald-50 text-emerald-700' : item.status === 'HIDDEN' ? 'bg-stone-100 text-stone-600' : 'bg-blue-50 text-blue-700'}`}>
                        {item.status}
                      </span>
                    </td>
                    <td className="p-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Link href={`/properties/${item.id}`} target="_blank" className="p-2 text-[var(--muted)] hover:text-[var(--forest)] bg-[#fbfaf7] rounded-lg border border-black/5" title="Xem trên web">
                          <FaEye />
                        </Link>
                        <button className="p-2 text-[var(--muted)] hover:text-blue-600 bg-[#fbfaf7] rounded-lg border border-black/5" title="Chỉnh sửa">
                          <FaEdit />
                        </button>
                        <button onClick={() => toggleStatus(item)} className="p-2 text-[var(--muted)] hover:text-red-600 bg-[#fbfaf7] rounded-lg border border-black/5" title={item.status === 'HIDDEN' ? "Hiện" : "Ẩn"}>
                          {item.status === 'HIDDEN' ? <FaEye /> : <FaEyeSlash />}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </main>
      </div>
    </ProtectedPage>
  );
}
