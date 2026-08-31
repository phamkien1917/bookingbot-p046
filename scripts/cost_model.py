"""Mô hình chi phí vận hành Nera. Đổi giả định ở CONFIG, chạy: python scripts/cost_model.py

Tài liệu: docs/research/COST_MODEL.md
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252

CONFIG = {
    # LLM: openai/gpt-4o-mini (render.yaml). Giá USD / 1 triệu token.
    "price_in_per_m": 0.15,
    "price_in_cached_per_m": 0.075,
    "price_out_per_m": 0.60,
    "usd_to_vnd": 26_000,
    # Hình dạng một lượt gọi LLM
    "tokens_in_fresh": 1_300,
    "tokens_in_cached": 1_200,
    "tokens_out": 350,
    # Hình dạng một cuộc hội thoại
    "turns_per_conversation": 7,
    "llm_calls_per_turn": 2.0,
    "goong_vnd_per_conversation": 60,
    # Chuyển đổi
    "conversations_per_booking": 5,
    "commission_vnd_per_deal": 100_000_000,
    # Kinh tế đơn vị
    "price_vnd_per_seat_month": 300_000,
    "conversations_per_seat_month": 75,       # trung bình sale ít/bận
    "fixed_infra_vnd_per_month": 2_000_000,   # ~77 USD
}


def llm_cost_per_call_vnd(c: dict) -> float:
    usd = (
        c["tokens_in_fresh"] * c["price_in_per_m"] / 1e6
        + c["tokens_in_cached"] * c["price_in_cached_per_m"] / 1e6
        + c["tokens_out"] * c["price_out_per_m"] / 1e6
    )
    return usd * c["usd_to_vnd"]


def cost_per_conversation_vnd(c: dict) -> float:
    calls = c["turns_per_conversation"] * c["llm_calls_per_turn"]
    return calls * llm_cost_per_call_vnd(c) + c["goong_vnd_per_conversation"]


def cost_per_booking_vnd(c: dict) -> float:
    return c["conversations_per_booking"] * cost_per_conversation_vnd(c)


def margin_at_seats(c: dict, seats: int) -> float:
    """Biên lợi nhuận trên doanh thu 1 tài khoản, ở quy mô `seats` tài khoản."""
    variable = c["conversations_per_seat_month"] * cost_per_conversation_vnd(c)
    fixed_share = c["fixed_infra_vnd_per_month"] / seats
    cost = variable + fixed_share
    return 1 - cost / c["price_vnd_per_seat_month"]


def breakeven_seats(c: dict) -> int:
    """Số tài khoản trả phí tối thiểu để bù toàn bộ chi phí."""
    variable = c["conversations_per_seat_month"] * cost_per_conversation_vnd(c)
    contribution = c["price_vnd_per_seat_month"] - variable
    if contribution <= 0:
        return -1
    return -(-c["fixed_infra_vnd_per_month"] // contribution)  # ceil


def report(c: dict = CONFIG) -> None:
    print(f"LLM / lượt gọi          : {llm_cost_per_call_vnd(c):8.1f} VND")
    print(f"Chi phí / cuộc hội thoại : {cost_per_conversation_vnd(c):8.0f} VND")
    print(f"Chi phí / lịch hẹn chốt  : {cost_per_booking_vnd(c):8.0f} VND")
    pct = cost_per_booking_vnd(c) / c["commission_vnd_per_deal"] * 100
    print(f"  = {pct:.4f}% hoa hồng mỗi giao dịch")
    for s in (20, 50, 200):
        print(f"Biên lợi nhuận @ {s:3d} tài khoản : {margin_at_seats(c, s)*100:5.1f}%")
    print(f"Hòa vốn tại              : {breakeven_seats(c)} tài khoản trả phí")


def demo() -> None:
    """Self-check: các bất biến của mô hình."""
    c = CONFIG
    assert 5 < llm_cost_per_call_vnd(c) < 30, "1 lượt gọi gpt-4o-mini nên ~13 VND"
    assert 150 < cost_per_conversation_vnd(c) < 1_000, "cuộc hội thoại nên vài trăm VND"
    assert cost_per_booking_vnd(c) < 10_000, "lịch hẹn nên dưới 10k VND"
    assert margin_at_seats(c, 20) < margin_at_seats(c, 200), "quy mô lớn hơn thì biên cao hơn"
    assert margin_at_seats(c, 200) > 0.7, "ở 200 tài khoản biên nên trên 70%"
    assert 1 <= breakeven_seats(c) <= 15, "hòa vốn nên trong khoảng 5-10 tài khoản"
    # tỷ giá tăng 10% -> chi phí lượt gọi tăng ~10%
    base = llm_cost_per_call_vnd(c)
    bumped = llm_cost_per_call_vnd({**c, "usd_to_vnd": c["usd_to_vnd"] * 1.1})
    assert abs(bumped / base - 1.1) < 1e-9
    print("demo OK")


if __name__ == "__main__":
    demo()
    print("-" * 40)
    report()
