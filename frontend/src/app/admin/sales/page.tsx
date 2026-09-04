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
    } catch {
      alert("Lỗi khi cập nhật trạng thái nhận khách");
    }
  };
  
  const [editingSale, setEditingSale] = useState<SaleProfileItem | null>(null);
  const [editForm, setEditForm] = useState({
    job_title: "",
    branch_name: "",
    max_daily_tours: 5,
    is_accepting_tours: true,
  });
  const [submitting, setSubmitting] = useState(false);

  const handleOpenEdit = (item: SaleProfileItem) => {
    setEditingSale(item);
    setEditForm({
      job_title: item.job_title || "",
      branch_name: item.branch_name || "",
      max_daily_tours: item.max_daily_tours || 5,
      is_accepting_tours: item.is_accepting_tours ?? true,
    });
  };

  const handleSaveEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingSale) return;
    setSubmitting(true);
    try {
      await apiFetch(`/admin/sales/${editingSale.id}`, {
        method: "PATCH",
        body: JSON.stringify({
          job_title: editForm.job_title || null,
          branch_name: editForm.branch_name || null,
          max_daily_tours: Number(editForm.max_daily_tours),
          is_accepting_tours: editForm.is_accepting_tours,
        }),
      });
      setEditingSale(null);
      await load();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Lỗi khi lưu thông tin Sale");
    } finally {
      setSubmitting(false);
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
                    <p className="flex justify-between"><span className="text-[var(--muted)]">Lịch tối đa/ngày:</span> <span className="font-semibold">{item.max_daily_tours} lịch</span></p>
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
                      <button onClick={() => handleOpenEdit(item)} className="p-2 text-[var(--muted)] hover:text-blue-600 bg-[#fbfaf7] rounded-lg border border-black/5 hover:border-blue-300" title="Chỉnh sửa thông tin">
                        <FaEdit />
                      </button>
                    </div>
                  </div>
                </article>
              ))
            )}
          </div>

          {/* Edit Sale Profile Modal */}
          {editingSale && (
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
              <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-black/10 animate-in fade-in zoom-in-95 duration-150">
                <div className="flex justify-between items-start mb-5 pb-3 border-b border-black/5">
                  <div>
                    <h3 className="text-xl font-bold">Chỉnh Sửa Hồ Sơ Sale</h3>
                    <p className="text-xs text-[var(--muted)] mt-0.5">{editingSale.full_name} ({editingSale.email})</p>
                  </div>
                  <button 
                    onClick={() => setEditingSale(null)}
                    className="text-gray-400 hover:text-gray-600 p-1 rounded-lg text-lg"
                  >
                    ✕
                  </button>
                </div>

                <form onSubmit={handleSaveEdit} className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1.5">
                      Chức vụ
                    </label>
                    <input 
                      type="text"
                      value={editForm.job_title}
                      onChange={(e) => setEditForm({...editForm, job_title: e.target.value})}
                      placeholder="VD: Chuyên viên tư vấn cao cấp"
                      className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1.5">
                      Chi nhánh / Văn phòng
                    </label>
                    <input 
                      type="text"
                      value={editForm.branch_name}
                      onChange={(e) => setEditForm({...editForm, branch_name: e.target.value})}
                      placeholder="VD: Trung tâm tư vấn Hà Nội"
                      className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1.5">
                      Số lịch dẫn tối đa / ngày
                    </label>
                    <input 
                      type="number"
                      min={1}
                      max={20}
                      value={editForm.max_daily_tours}
                      onChange={(e) => setEditForm({...editForm, max_daily_tours: parseInt(e.target.value) || 1})}
                      className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                    />
                  </div>

                  <div className="pt-2">
                    <label className="flex items-center gap-3 cursor-pointer select-none">
                      <input 
                        type="checkbox"
                        checked={editForm.is_accepting_tours}
                        onChange={(e) => setEditForm({...editForm, is_accepting_tours: e.target.checked})}
                        className="w-4 h-4 rounded text-[var(--forest)] focus:ring-[var(--forest)] border-gray-300"
                      />
                      <span className="text-sm font-medium">Bật tiếp nhận lịch dẫn khách từ AI</span>
                    </label>
                  </div>

                  <div className="flex justify-end gap-3 pt-4 border-t border-black/5">
                    <button
                      type="button"
                      onClick={() => setEditingSale(null)}
                      className="px-4 py-2 text-sm rounded-xl border border-black/10 font-semibold hover:bg-black/5 transition-colors"
                    >
                      Hủy
                    </button>
                    <button
                      type="submit"
                      disabled={submitting}
                      className="px-5 py-2 text-sm bg-[var(--forest)] text-white rounded-xl font-semibold hover:opacity-90 transition-opacity flex items-center gap-2"
                    >
                      {submitting ? <FaSpinner className="animate-spin" /> : "Lưu thay đổi"}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}
        </main>
      </div>
    </ProtectedPage>
  );
}
