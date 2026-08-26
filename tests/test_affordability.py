from src.services.affordability import (
    DEFAULT_MAX_DTI,
    estimate_affordability,
    explain,
    format_vnd,
    purchase_guidance_lines,
)


def test_income_becomes_a_payment_capped_at_the_dti() -> None:
    estimate = estimate_affordability(17_500_000)

    assert estimate is not None
    assert estimate.max_monthly_payment_vnd == int(17_500_000 * DEFAULT_MAX_DTI)


def test_twenty_year_loan_at_ten_percent_lands_in_the_expected_range() -> None:
    """A 7tr/month payment services roughly 725tr over 20 years at 10%/year."""
    estimate = estimate_affordability(17_500_000)

    assert estimate is not None
    assert 700_000_000 < estimate.max_loan_vnd < 760_000_000
    # With the standard 30% down assumption that is a home just over 1 tỷ.
    assert 1_000_000_000 < estimate.assumed_price_vnd < 1_100_000_000


def test_unknown_savings_is_flagged_rather_than_hidden() -> None:
    estimate = estimate_affordability(17_500_000)

    assert estimate is not None
    assert estimate.own_capital_is_assumed
    assert estimate.needs_capital_question
    assert "vốn" in explain(estimate)


def test_known_savings_replaces_the_assumption() -> None:
    estimate = estimate_affordability(17_500_000, own_capital_vnd=1_000_000_000)

    assert estimate is not None
    assert not estimate.needs_capital_question
    assert estimate.assumed_price_vnd == estimate.max_loan_vnd + 1_000_000_000


def test_more_income_buys_proportionally_more_loan() -> None:
    single = estimate_affordability(17_500_000)
    double = estimate_affordability(35_000_000)

    assert single is not None and double is not None
    assert abs(double.max_loan_vnd - single.max_loan_vnd * 2) < 1_000_000


def test_income_too_small_returns_nothing_instead_of_a_bad_number() -> None:
    assert estimate_affordability(1_000_000) is None
    assert estimate_affordability(0) is None
    assert estimate_affordability(-5_000_000) is None


def test_zero_interest_does_not_divide_by_zero() -> None:
    estimate = estimate_affordability(17_500_000, annual_rate=0.0)

    assert estimate is not None
    assert estimate.max_loan_vnd == 7_000_000 * 240


def test_explanation_names_every_assumption_it_relies_on() -> None:
    text = explain(estimate_affordability(17_500_000))  # type: ignore[arg-type]

    assert "40%" in text  # the debt-service ratio
    assert "10%/năm" in text  # the interest rate
    assert "20 năm" in text  # the term
    assert "tham khảo" in text  # it does not present itself as a bank decision


def test_purchase_guidance_scales_with_income() -> None:
    """The consultation reply used to carry a fixed range for every income.

    Someone earning 50tr a month must not be told the same price ceiling as
    someone earning 15tr, so the two texts have to differ.
    """
    modest = purchase_guidance_lines(estimate_affordability(15_000_000))  # type: ignore[arg-type]
    comfortable = purchase_guidance_lines(estimate_affordability(50_000_000))  # type: ignore[arg-type]

    assert modest != comfortable
    assert "1.5 – 2 tỷ" not in modest  # the old hard-coded range
    assert "5 – 8 triệu" not in modest


def test_purchase_guidance_is_markdown_bullets_with_a_caveat() -> None:
    lines = purchase_guidance_lines(estimate_affordability(17_500_000)).strip().split("\n")  # type: ignore[arg-type]

    assert len(lines) == 4
    assert all(line.startswith("- ") for line in lines)
    assert "tham khảo" in lines[-1]


def test_purchase_guidance_mentions_savings_when_they_are_known() -> None:
    known = purchase_guidance_lines(
        estimate_affordability(17_500_000, own_capital_vnd=800_000_000)  # type: ignore[arg-type]
    )
    assumed = purchase_guidance_lines(estimate_affordability(17_500_000))  # type: ignore[arg-type]

    assert "800 triệu vốn tự có" in known
    assert "Nếu bạn có sẵn 30%" in assumed


def test_vnd_formatting_matches_how_listings_are_written() -> None:
    assert format_vnd(1_630_000_000) == "1.63 tỷ"
    assert format_vnd(2_000_000_000) == "2 tỷ"
    assert format_vnd(7_000_000) == "7 triệu"
    assert format_vnd(725_400_000) == "725.4 triệu"


def test_loan_schedule_calculation_and_dti_assessment() -> None:
    from src.services.affordability import calculate_loan_schedule, explain_loan_calculation

    # 2 billion in 3 years at 5% with 50tr/month income (user's exact scenario)
    res = calculate_loan_schedule(
        2_000_000_000,
        term_years=3,
        annual_rate=0.05,
        monthly_income_vnd=50_000_000,
    )
    assert res is not None
    assert res.term_months == 36
    assert res.monthly_principal_vnd == 55_555_556
    assert res.monthly_first_interest_vnd == 8_333_333
    assert res.monthly_first_payment_vnd == 63_888_889
    assert res.dti_first_month is not None
    assert res.dti_first_month > 1.0  # ~127% DTI

    explanation = explain_loan_calculation(res)
    assert "2 tỷ" in explanation
    assert "3 năm" in explanation
    assert "Cảnh báo rủi ro cao" in explanation
    assert "50 triệu" in explanation
