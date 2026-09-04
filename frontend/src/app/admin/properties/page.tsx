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
  bedrooms?: number | null;
  bathrooms?: number | null;
}

interface PropertyForm {
  title: string;
  property_kind: string;
  area_sqm: number | string;
  list_price: number | string;
  address_line: string;
  province: string;
  district: string;
  ward: string;
  bedrooms: number | string;
  bathrooms: number | string;
  status: string;
  description: string;
}

const defaultForm: PropertyForm = {
  title: "",
  property_kind: "APARTMENT",
  area_sqm: "",
  list_price: "",
  address_line: "",
  province: "Hà Nội",
  district: "",
  ward: "",
  bedrooms: 2,
  bathrooms: 1,
  status: "AVAILABLE",
  description: "",
};

export default function AdminPropertiesPage() {
  const [items, setItems] = useState<PropertyItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");

  // Modal create/edit states
  const [modalOpen, setModalOpen] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [form, setForm] = useState<PropertyForm>(defaultForm);
  const [submitting, setSubmitting] = useState(false);
  
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

  const handleOpenCreate = () => {
    setEditingId(null);
    setForm(defaultForm);
    setModalOpen(true);
  };

  const handleOpenEdit = async (item: PropertyItem) => {
    setEditingId(item.id);
    setModalOpen(true);
    setForm({
      title: item.title,
      property_kind: item.property_kind,
      area_sqm: item.area_sqm,
      list_price: item.list_price ? (item.list_price / 1e9).toFixed(2) : "",
      address_line: item.address,
      province: "Hà Nội",
      district: "",
      ward: "",
      bedrooms: item.bedrooms ?? 2,
      bathrooms: item.bathrooms ?? 1,
      status: item.status,
      description: "",
    });

    try {
      const full = await apiFetch<Record<string, unknown>>(`/properties/${item.id}`);
      if (full) {
        setForm({
          title: (full.title as string) || item.title,
          property_kind: (full.property_kind as string) || item.property_kind,
          area_sqm: (full.area_sqm as number) || item.area_sqm,
          list_price: full.list_price ? ((full.list_price as number) / 1e9).toFixed(2) : (item.list_price ? (item.list_price / 1e9).toFixed(2) : ""),
          address_line: (full.address_line as string) || item.address,
          province: (full.province as string) || "Hà Nội",
          district: (full.district as string) || "",
          ward: (full.ward as string) || "",
          bedrooms: (full.bedrooms as number) ?? 2,
          bathrooms: (full.bathrooms as number) ?? 1,
          status: (full.status as string) || item.status,
          description: (full.description as string) || "",
        });
      }
    } catch {
      // Fallback already set
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.title.trim()) {
      alert("Vui lòng nhập tên bất động sản");
      return;
    }
    if (!form.area_sqm || Number(form.area_sqm) <= 0) {
      alert("Vui lòng nhập diện tích hợp lệ");
      return;
    }
    setSubmitting(true);
    try {
      const rawPrice = form.list_price ? Math.round(Number(form.list_price) * 1e9) : null;
      const payload = {
        title: form.title.trim(),
        property_kind: form.property_kind,
        area_sqm: Number(form.area_sqm),
        list_price: rawPrice,
        address_line: form.address_line.trim() || form.title.trim(),
        province: form.province.trim() || "Hà Nội",
        district: form.district.trim() || null,
        ward: form.ward.trim() || null,
        bedrooms: form.bedrooms ? Number(form.bedrooms) : null,
        bathrooms: form.bathrooms ? Number(form.bathrooms) : null,
        status: form.status,
        description: form.description.trim() || null,
      };

      if (editingId) {
        await apiFetch(`/admin/properties/${editingId}`, {
          method: "PATCH",
          body: JSON.stringify(payload),
        });
      } else {
        await apiFetch(`/admin/properties`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }
      setModalOpen(false);
      await load();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Lỗi khi lưu bất động sản");
    } finally {
      setSubmitting(false);
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
              <button 
                onClick={handleOpenCreate}
                className="bg-[var(--forest)] text-white px-5 py-2.5 rounded-xl font-semibold flex items-center gap-2 hover:opacity-90 transition-opacity cursor-pointer shadow-sm"
              >
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
                        <button 
                          onClick={() => handleOpenEdit(item)}
                          className="p-2 text-[var(--muted)] hover:text-blue-600 bg-[#fbfaf7] rounded-lg border border-black/5 hover:border-blue-300 cursor-pointer" 
                          title="Chỉnh sửa BĐS"
                        >
                          <FaEdit />
                        </button>
                        <button onClick={() => toggleStatus(item)} className="p-2 text-[var(--muted)] hover:text-red-600 bg-[#fbfaf7] rounded-lg border border-black/5 cursor-pointer" title={item.status === 'HIDDEN' ? "Hiện" : "Ẩn"}>
                          {item.status === 'HIDDEN' ? <FaEye /> : <FaEyeSlash />}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Create / Edit Property Modal */}
          {modalOpen && (
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs overflow-y-auto">
              <div className="bg-white rounded-2xl max-w-2xl w-full p-6 shadow-2xl border border-black/10 my-8 animate-in fade-in zoom-in-95 duration-150">
                <div className="flex justify-between items-start mb-5 pb-3 border-b border-black/5">
                  <div>
                    <h3 className="text-xl font-bold">{editingId ? "Chỉnh Sửa Bất Động Sản" : "Thêm Bất Động Sản Mới"}</h3>
                    <p className="text-xs text-[var(--muted)] mt-0.5">
                      {editingId ? "Cập nhật thông số kỹ thuật và trạng thái căn hộ" : "Thêm căn hộ mới vào kho hàng 3.796 BĐS"}
                    </p>
                  </div>
                  <button 
                    onClick={() => setModalOpen(false)}
                    className="text-gray-400 hover:text-gray-600 p-1 rounded-lg text-lg cursor-pointer"
                  >
                    ✕
                  </button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1">
                      Tên / Tiêu đề BĐS <span className="text-red-500">*</span>
                    </label>
                    <input 
                      type="text"
                      required
                      value={form.title}
                      onChange={(e) => setForm({...form, title: e.target.value})}
                      placeholder="VD: Căn hộ cao cấp Masteri Thảo Điền 2PN view sông"
                      className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1">
                        Loại hình
                      </label>
                      <select 
                        value={form.property_kind}
                        onChange={(e) => setForm({...form, property_kind: e.target.value})}
                        className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm bg-white"
                      >
                        <option value="APARTMENT">Căn hộ (APARTMENT)</option>
                        <option value="HOUSE">Nhà riêng (HOUSE)</option>
                        <option value="VILLA">Biệt thự (VILLA)</option>
                        <option value="TOWNHOUSE">Nhà phố (TOWNHOUSE)</option>
                        <option value="LAND">Đất nền (LAND)</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1">
                        Giá bán (Tỷ VNĐ)
                      </label>
                      <input 
                        type="number"
                        step="0.01"
                        min="0"
                        value={form.list_price}
                        onChange={(e) => setForm({...form, list_price: e.target.value})}
                        placeholder="VD: 3.85 (tương đương 3.85 tỷ)"
                        className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1">
                        Diện tích (m²) <span className="text-red-500">*</span>
                      </label>
                      <input 
                        type="number"
                        step="0.1"
                        min="1"
                        required
                        value={form.area_sqm}
                        onChange={(e) => setForm({...form, area_sqm: e.target.value})}
                        placeholder="VD: 75.5"
                        className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1">
                        Số phòng ngủ
                      </label>
                      <input 
                        type="number"
                        min="0"
                        max="20"
                        value={form.bedrooms}
                        onChange={(e) => setForm({...form, bedrooms: e.target.value})}
                        className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1">
                        Số phòng tắm / WC
                      </label>
                      <input 
                        type="number"
                        min="0"
                        max="20"
                        value={form.bathrooms}
                        onChange={(e) => setForm({...form, bathrooms: e.target.value})}
                        className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1">
                        Trạng thái
                      </label>
                      <select 
                        value={form.status}
                        onChange={(e) => setForm({...form, status: e.target.value})}
                        className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm bg-white"
                      >
                        <option value="AVAILABLE">AVAILABLE (Đang mở bán)</option>
                        <option value="PENDING">PENDING (Đang giữ chỗ)</option>
                        <option value="SOLD">SOLD (Đã bán)</option>
                        <option value="HIDDEN">HIDDEN (Tạm ẩn)</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1">
                        Tỉnh / Thành phố
                      </label>
                      <input 
                        type="text"
                        value={form.province}
                        onChange={(e) => setForm({...form, province: e.target.value})}
                        placeholder="Hà Nội, TP Hồ Chí Minh..."
                        className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1">
                        Quận / Huyện
                      </label>
                      <input 
                        type="text"
                        value={form.district}
                        onChange={(e) => setForm({...form, district: e.target.value})}
                        placeholder="VD: Cầu Giấy, Quận 7..."
                        className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1">
                        Phường / Xã
                      </label>
                      <input 
                        type="text"
                        value={form.ward}
                        onChange={(e) => setForm({...form, ward: e.target.value})}
                        placeholder="VD: Dịch Vọng Hậu..."
                        className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1">
                      Địa chỉ chi tiết (Đường, số nhà, tòa chung cư)
                    </label>
                    <input 
                      type="text"
                      value={form.address_line}
                      onChange={(e) => setForm({...form, address_line: e.target.value})}
                      placeholder="VD: Số 123 đường Cầu Giấy, Tòa tháp Discovery Complex"
                      className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-[var(--muted)] uppercase tracking-wider mb-1">
                      Mô tả BĐS
                    </label>
                    <textarea 
                      rows={3}
                      value={form.description}
                      onChange={(e) => setForm({...form, description: e.target.value})}
                      placeholder="Mô tả nội thất, pháp lý, tiện ích xung quanh căn hộ..."
                      className="w-full px-3.5 py-2.5 rounded-xl border border-black/10 focus:outline-none focus:border-[var(--forest)] focus:ring-1 focus:ring-[var(--forest)] text-sm"
                    />
                  </div>

                  <div className="flex justify-end gap-3 pt-4 border-t border-black/5">
                    <button
                      type="button"
                      onClick={() => setModalOpen(false)}
                      className="px-4 py-2 text-sm rounded-xl border border-black/10 font-semibold hover:bg-black/5 transition-colors cursor-pointer"
                    >
                      Hủy
                    </button>
                    <button
                      type="submit"
                      disabled={submitting}
                      className="px-5 py-2 text-sm bg-[var(--forest)] text-white rounded-xl font-semibold hover:opacity-90 transition-opacity flex items-center gap-2 cursor-pointer shadow-sm"
                    >
                      {submitting ? <FaSpinner className="animate-spin" /> : editingId ? "Lưu thay đổi" : "Tạo bất động sản"}
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
