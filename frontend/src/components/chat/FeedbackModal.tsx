"use client";

import { useState } from "react";
import { FaTimes } from "react-icons/fa";

import type { Property } from "@/lib/types";

const REASONS = [
  "Giá hơi cao",
  "Đi làm quá xa",
  "Diện tích hơi nhỏ",
  "Không thích khu vực",
  "Thiếu tiện ích",
];

export interface FeedbackModalProps {
  property: Property;
  onClose: () => void;
  onSubmit: (text: string) => void;
}

export default function FeedbackModal({ property, onClose, onSubmit }: FeedbackModalProps) {
  const [selected, setSelected] = useState<string[]>([]);
  const [extra, setExtra] = useState("");

  function toggle(reason: string) {
    setSelected((current) => current.includes(reason)
      ? current.filter((item) => item !== reason)
      : [...current, reason]);
  }

  function submit() {
    const reasons = [...selected, ...(extra.trim() ? [extra.trim()] : [])];
    if (!reasons.length) return;
    onSubmit(`Về căn “${property.title}”, tôi không thích vì: ${reasons.join(", ")}`);
    onClose();
  }

  return (
    <div role="dialog" aria-modal="true" className="fixed inset-0 z-50 grid place-items-center bg-black/55 p-4">
      <div className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-xs font-bold uppercase text-[var(--coral)]">Phản hồi của bạn</p>
            <h2 className="mt-1 line-clamp-2 font-semibold">{property.title}</h2>
          </div>
          <button onClick={onClose} aria-label="Đóng" className="rounded-full bg-stone-100 p-2"><FaTimes /></button>
        </div>
        <p className="mt-5 text-sm font-semibold">Điều gì khiến căn này chưa phù hợp?</p>
        <div className="mt-3 flex flex-wrap gap-2">
          {REASONS.map((reason) => (
            <button key={reason} onClick={() => toggle(reason)} className={`rounded-full border px-3 py-1.5 text-xs ${selected.includes(reason) ? "bg-[var(--forest)] text-white" : "border-black/10"}`}>
              {reason}
            </button>
          ))}
        </div>
        <textarea value={extra} onChange={(event) => setExtra(event.target.value)} rows={3} placeholder="Lý do khác…" className="mt-4 w-full rounded-xl border border-black/10 p-3 text-sm" />
        <div className="mt-4 flex gap-3">
          <button onClick={onClose} className="flex-1 rounded-full border border-black/10 py-2.5 text-sm font-semibold">Bỏ qua</button>
          <button onClick={submit} disabled={!selected.length && !extra.trim()} className="flex-1 rounded-full bg-[var(--forest)] py-2.5 text-sm font-semibold text-white disabled:opacity-40">Gửi phản hồi</button>
        </div>
      </div>
    </div>
  );
}
