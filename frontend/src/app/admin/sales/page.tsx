"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { FaArrowLeft, FaEdit, FaRobot, FaSearch, FaSpinner, FaUserCheck, FaUserSlash } from "react-icons/fa";
import ProtectedPage from "@/components/ProtectedPage";
import Header from "@/components/Header";
import { apiFetch } from "@/lib/api";

interface SaleProfileItem {
  id: string;
  full_name: string;
  email: string;
  phone: string | null;
  status: string;
  employee_code: string | null;
  job_title: string | null;
  branch_name: string | null;
  max_daily_tours: number;
  is_accepting_tours: boolean;
}

export default function AdminSalesPage() {
  const [items, setItems] = useState<SaleProfileItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  
  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await apiFetch<SaleProfileItem[]>(`/admin/sales`);
      setItems(res);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Không tải được danh sách Sale");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const toggleAccepting = async (item: SaleProfileItem) => {
    try {
      await apiFetch(`/admin/sales/${item.id}`, {
        method: "PATCH",
        body: JSON.stringify({ is_accepting_tours: !item.is_accepting_tours })
      });
      await load();
    } catch (err) {
      alert("Lỗi khi cập nhật trạng thái nhận khách");
    }
  };
  
  const filteredItems = items.filter(i => `${i.full_name} ${i.email} ${i.employee_code}`.toLowerCase().includes(query.toLowerCase()));

  return (
    <ProtectedPage roles={["ADMIN", "COORDINATOR"]}>
      <div className="min-h-screen bg-[var(--paper)] text-[var(--ink)] font-sans">
        <Header />
        <main className="max-w-6xl mx-auto px-4 py-8">
          <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <Link href="/admin" className="text-sm text-[var(--muted)] flex items-center mb-2 hover:text-[var(--ink)]"><FaArrowLeft className="mr-2"/> Về trang quản trị</Link>
              <h1 className="text-3xl font-bold">Quản Lý Nhân Viên Sale</h1>
            </div>
            <div className="relative w-full md:w-64">
              <FaSearch className="absolute left-3 top-3.5 text-[var(--muted)]" />
              <input 
                type="text" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Tìm kiếm Sale..." 
                className="pl-9 pr-4 py-2.5 rounded-xl border border-black/10 w-full focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)]"
              />
            </div>
          </div>
          
          {error && <div className="bg-red-50 text-red-600 p-4 rounded-xl mb-6">{error}</div>}
          
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {loading ? (
              <div className="col-span-full py-20 text-center"><FaSpinner className="animate-spin text-3xl text-[var(--forest)] mx-auto" /></div>
            ) : filteredItems.length === 0 ? (
              <div className="col-span-full py-20 text-center text-[var(--muted)]">Không tìm thấy nhân viên Sale nào.</div>
            ) : (
              filteredItems.map(item => (
                <article key={item.id} className="bg-white rounded-[1.5rem] border border-black/5 p-6 shadow-sm hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 bg-[#e6eee7] text-[var(--forest)] rounded-full flex items-center justify-center font-bold text-xl">
                        {item.full_name.charAt(0)}
                      </div>
                      <div>
                        <h3 className="font-bold text-lg leading-tight">{item.full_name}</h3>
                        <p className="text-xs text-[var(--muted)]">{item.employee_code || "Chưa có mã NV"}</p>
                      </div>
                    </div>
                    <span className={`px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md ${item.status === 'ACTIVE' ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700'}`}>
                      {item.status}
                    </span>
                  </div>
                  
                  <div className="space-y-2.5 text-sm mb-6 pb-6 border-b border-black/5">
                    <p className="flex justify-between"><span className="text-[var(--muted)]">Chức vụ:</span> <span className="font-medium">{item.job_title || "Chuyên viên tư vấn"}</span></p>
                    <p className="flex justify-between"><span className="text-[var(--muted)]">Chi nhánh:</span> <span className="font-medium">{item.branch_name || "Trụ sở chính"}</span></p>
                    <p className="flex justify-between"><span className="text-[var(--muted)]">Email:</span> <span>{item.email}</span></p>
                    <p className="flex justify-between"><span className="text-[var(--muted)]">SĐT:</span> <span>{item.phone || "---"}</span></p>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs text-[var(--muted)] mb-1">Trạng thái nhận khách</p>
                      <p className="text-sm font-bold flex items-center gap-1.5">
                        {item.is_accepting_tours ? <><FaRobot className="text-[var(--forest)]"/> Đang kích hoạt AI</> : <><FaUserSlash className="text-red-500"/> Tạm ngưng</>}
                      </p>
                    </div>
                    <div className="flex gap-2">
                      <button onClick={() => toggleAccepting(item)} className={`p-2 rounded-lg border ${item.is_accepting_tours ? 'text-amber-600 border-amber-200 bg-amber-50 hover:bg-amber-100' : 'text-[var(--forest)] border-[var(--sage)] bg-[#e6eee7] hover:bg-[#d5e0d7]'}`} title={item.is_accepting_tours ? "Tạm ngưng nhận khách" : "Bật nhận khách"}>
                        {item.is_accepting_tours ? <FaUserSlash /> : <FaUserCheck />}
                      </button>
                      <button className="p-2 text-[var(--muted)] hover:text-blue-600 bg-[#fbfaf7] rounded-lg border border-black/5" title="Chỉnh sửa">
                        <FaEdit />
                      </button>
                    </div>
                  </div>
                </article>
              ))
            )}
          </div>
        </main>
      </div>
    </ProtectedPage>
  );
}
