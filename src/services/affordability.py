"""Deterministic affordability maths for income-based property questions.

The LLM extracts the income figure a customer mentions; every number derived from
it is computed here. Keeping the arithmetic out of the model matters because a
wrong budget sends someone to view homes they cannot buy.

Assumptions are explicit fields on the result so the chat layer can state them
instead of presenting a bare number as fact.
"""

from __future__ import annotations

from dataclasses import dataclass

# Conservative defaults for the Vietnamese market. Banks will often lend against
# a higher debt-service ratio; 40% is the prudent line for a first-time buyer who
# still needs to live on the remainder.
DEFAULT_MAX_DTI = 0.40
DEFAULT_ANNUAL_RATE = 0.10
DEFAULT_TERM_YEARS = 20
DEFAULT_DOWN_PAYMENT_RATIO = 0.30

# Below this the numbers stop being meaningful; treat as "not enough information".
MIN_SUPPORTED_MONTHLY_INCOME = 3_000_000


@dataclass(frozen=True, slots=True)
class AffordabilityEstimate:
    """What a monthly income can support, and what had to be assumed to say so."""

    monthly_income_vnd: int
    max_monthly_payment_vnd: int
    max_loan_vnd: int
    assumed_price_vnd: int
    own_capital_vnd: int | None
    own_capital_is_assumed: bool
    annual_rate: float
    term_years: int
    max_dti: float
    down_payment_ratio: float

    @property
    def needs_capital_question(self) -> bool:
        """True when the price ceiling rests on a guess about the buyer's savings."""
        return self.own_capital_is_assumed


def _max_loan_for_payment(monthly_payment: float, annual_rate: float, term_years: int) -> float:
    """Invert the annuity formula: how much principal a fixed payment can service.

    P = M * (1 - (1 + r)^-n) / r, with r the monthly rate and n the month count.
    """
    if monthly_payment <= 0 or term_years <= 0:
        return 0.0
    months = term_years * 12
    monthly_rate = annual_rate / 12
    if monthly_rate <= 0:
        return monthly_payment * months
    discount = 1 - (1 + monthly_rate) ** (-months)
    return monthly_payment * discount / monthly_rate


def estimate_affordability(
    monthly_income_vnd: int,
    *,
    own_capital_vnd: int | None = None,
    annual_rate: float = DEFAULT_ANNUAL_RATE,
    term_years: int = DEFAULT_TERM_YEARS,
    max_dti: float = DEFAULT_MAX_DTI,
    down_payment_ratio: float = DEFAULT_DOWN_PAYMENT_RATIO,
) -> AffordabilityEstimate | None:
    """Derive a price ceiling from monthly income.

    Returns None when the income is too small or absent to say anything useful,
    so callers can stay silent rather than publish a misleading figure.

    When `own_capital_vnd` is unknown the ceiling assumes the buyer has the
    standard down payment; the result flags that assumption so the caller can ask
    instead of asserting.
    """
    if not monthly_income_vnd or monthly_income_vnd < MIN_SUPPORTED_MONTHLY_INCOME:
        return None

    max_monthly_payment = monthly_income_vnd * max_dti
    max_loan = _max_loan_for_payment(max_monthly_payment, annual_rate, term_years)

    capital_is_assumed = own_capital_vnd is None
    if capital_is_assumed:
        # Loan covers (1 - down_payment_ratio) of the price, so scale up from it.
        price = max_loan / (1 - down_payment_ratio) if down_payment_ratio < 1 else max_loan
    else:
        price = max_loan + max(own_capital_vnd or 0, 0)

    return AffordabilityEstimate(
        monthly_income_vnd=int(monthly_income_vnd),
        max_monthly_payment_vnd=int(round(max_monthly_payment)),
        max_loan_vnd=int(round(max_loan)),
        assumed_price_vnd=int(round(price)),
        own_capital_vnd=own_capital_vnd,
        own_capital_is_assumed=capital_is_assumed,
        annual_rate=annual_rate,
        term_years=term_years,
        max_dti=max_dti,
        down_payment_ratio=down_payment_ratio,
    )


def format_vnd(amount: int) -> str:
    """Render a VND amount the way Vietnamese listings do: tỷ and triệu."""
    if amount >= 1_000_000_000:
        billions = amount / 1_000_000_000
        text = f"{billions:.2f}".rstrip("0").rstrip(".")
        return f"{text} tỷ"
    if amount >= 1_000_000:
        millions = amount / 1_000_000
        text = f"{millions:.1f}".rstrip("0").rstrip(".")
        return f"{text} triệu"
    return f"{amount:,}".replace(",", ".") + " đồng"


def explain(estimate: AffordabilityEstimate) -> str:
    """One paragraph a customer can check, with the assumptions named."""
    parts = [
        f"Với thu nhập {format_vnd(estimate.monthly_income_vnd)}/tháng, "
        f"khoản trả góp an toàn khoảng {format_vnd(estimate.max_monthly_payment_vnd)}/tháng "
        f"(giữ ở mức {int(estimate.max_dti * 100)}% thu nhập để còn chi phí sinh hoạt).",
        f"Mức đó vay được khoảng {format_vnd(estimate.max_loan_vnd)} "
        f"nếu lãi suất {estimate.annual_rate * 100:.0f}%/năm và vay trong {estimate.term_years} năm.",
    ]
    if estimate.own_capital_is_assumed:
        parts.append(
            f"Nếu bạn có sẵn {int(estimate.down_payment_ratio * 100)}% giá trị căn nhà, "
            f"tầm giá phù hợp vào khoảng {format_vnd(estimate.assumed_price_vnd)}. "
            "Con số này đổi nhiều theo số vốn bạn đang có."
        )
    else:
        parts.append(
            f"Cộng với {format_vnd(estimate.own_capital_vnd or 0)} vốn tự có, "
            f"tầm giá phù hợp vào khoảng {format_vnd(estimate.assumed_price_vnd)}."
        )
    parts.append("Đây là ước tính tham khảo; lãi suất và điều kiện vay thực tế do ngân hàng quyết định.")
    return " ".join(parts)


def _demo() -> None:
    """Self-check: the numbers must stay in a range a human would accept."""
    # 17.5tr/month, no capital known: the classic case from production.
    est = estimate_affordability(17_500_000)
    assert est is not None
    assert est.max_monthly_payment_vnd == 7_000_000, est.max_monthly_payment_vnd
    # 20-year annuity at 10% services roughly 103x the monthly payment.
    assert 700_000_000 < est.max_loan_vnd < 760_000_000, est.max_loan_vnd
    assert 1_000_000_000 < est.assumed_price_vnd < 1_100_000_000, est.assumed_price_vnd
    assert est.needs_capital_question

    # Known capital replaces the assumption and raises the ceiling.
    with_capital = estimate_affordability(17_500_000, own_capital_vnd=1_000_000_000)
    assert with_capital is not None
    assert not with_capital.needs_capital_question
    assert with_capital.assumed_price_vnd > est.assumed_price_vnd
    assert with_capital.assumed_price_vnd == with_capital.max_loan_vnd + 1_000_000_000

    # More income buys proportionally more loan.
    doubled = estimate_affordability(35_000_000)
    assert doubled is not None
    assert abs(doubled.max_loan_vnd - est.max_loan_vnd * 2) < 1_000_000

    # Too little income, or none, must return nothing rather than a bad number.
    assert estimate_affordability(1_000_000) is None
    assert estimate_affordability(0) is None

    # A zero rate degrades to simple division, not a divide-by-zero.
    zero_rate = estimate_affordability(17_500_000, annual_rate=0.0)
    assert zero_rate is not None
    assert zero_rate.max_loan_vnd == 7_000_000 * 240

    assert format_vnd(1_630_000_000) == "1.63 tỷ"
    assert format_vnd(7_000_000) == "7 triệu"

    print(explain(est))
    print("affordability self-check OK")


if __name__ == "__main__":
    _demo()
