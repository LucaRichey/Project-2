"""
mandate.py — Portfolio Mandate Checker
Meridian Foundation Reserve ($100 Million Portfolio)

Author: Luca Richey
Course: FIN 43900 (AI Finance Applications, Purdue University)
Meridian Foundation Reserve: Portfolio Mandate Defense & Baselines

Standard library only. Computes all mandate checks from editable inputs.
Includes Candidate E: The Strategic Policy Benchmark (40% IG Bonds, 60% Global Equities).
"""

import sys

# ==============================================================================
# EDITABLE INPUTS
# ==============================================================================

# Holdings master table:
# holding, issuer, business days to redeem, reserve-eligible
HOLDINGS = [
    {"holding": "Cash", "issuer": "none", "days": 0, "reserve_eligible": True},
    {"holding": "Treasury bills", "issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True},
    {"holding": "Treasury 10-year note", "issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True},
    {"holding": "Global equity index fund", "issuer": "diversified fund", "days": 2, "reserve_eligible": False},
    {"holding": "Investment-grade bond fund", "issuer": "diversified fund", "days": 3, "reserve_eligible": False},
    {"holding": "Private real estate fund", "issuer": "diversified fund", "days": 90, "reserve_eligible": False},
    {"holding": "Acme Corp bonds", "issuer": "Acme Corp", "days": 4, "reserve_eligible": False},
    {"holding": "Acme Corp stock", "issuer": "Acme Corp", "days": 1, "reserve_eligible": False},
]

# Candidate portfolio allocations (weights as percent of total portfolio)
CANDIDATES = {
    "A": {
        "Cash": 2.0,
        "Treasury bills": 2.0,
        "Treasury 10-year note": 10.0,
        "Global equity index fund": 60.0,
        "Investment-grade bond fund": 26.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
    "B": {
        "Cash": 1.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 55.0,
        "Investment-grade bond fund": 20.0,
        "Private real estate fund": 15.0,
        "Acme Corp bonds": 5.0,
        "Acme Corp stock": 4.0,
    },
    "C": {
        "Cash": 1.0,
        "Treasury bills": 1.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 70.0,
        "Investment-grade bond fund": 20.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 8.0,
    },
    # Candidate D: The Mandate Stress Portfolio
    # Passes all checkable mandate rules, but offends S4 (Benchmark 60/40) & exposes S9/S10
    "D": {
        "Cash": 3.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 97.0,
        "Investment-grade bond fund": 0.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
    # Candidate E: The Strategic Policy Benchmark (60/40 Equity/IG Bond Policy)
    # 40% Investment-Grade Bond Fund, 60% Global Equity Index Fund
    # Fails S3 reserve rule at 0.0% — the client's own benchmark breaks the client's mandate!
    "E": {
        "Cash": 0.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 60.0,
        "Investment-grade bond fund": 40.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
}

# Mandate Parameters
RESERVE_SIZE = 100.0           # Reserve size in USD millions
QUARTERLY_DISTRIBUTION = 0.75  # Quarterly distribution in USD millions
QUARTERS_TO_COVER = 4          # Twelve months of payouts = 4 quarters
LIQUIDITY_WINDOW = 5           # Business days to redeem
MINIMUM_LIQUID_SHARE = 90.0    # Minimum liquid share percent
ISSUER_LIMIT = 8.0             # Single company issuer limit percent

# Exempt issuers from single company limit
EXEMPT_ISSUERS = {"none", "u.s. treasury", "diversified fund"}


# ==============================================================================
# COMPUTATION ENGINE
# ==============================================================================

def compute_reserve_minimum(quarters: int, distribution: float, reserve_size: float) -> float:
    """
    Compute required reserve minimum percent:
    quarters * distribution / reserve_size * 100
    """
    return (quarters * distribution / reserve_size) * 100.0


def evaluate_candidate(candidate_name: str, weights: dict, reserve_min: float) -> dict:
    """
    Evaluate all mandate rules for a single candidate portfolio.
    Returns dictionary with measured values, statuses, and overall verdict.
    """
    # 1. Weights sum to 100
    sum_w = sum(weights.values())
    sum_pass = abs(sum_w - 100.0) < 1e-5

    # 2. Long-only (lowest weight not negative)
    min_w = min(weights.values())
    long_only_pass = min_w >= -1e-5

    # 3. Reserve-eligible weight at least reserve minimum
    res_w = sum(weights.get(h["holding"], 0.0) for h in HOLDINGS if h["reserve_eligible"])
    reserve_pass = res_w >= (reserve_min - 1e-5)

    # 4. Weight redeemable within liquidity window at least minimum liquid share
    liq_w = sum(weights.get(h["holding"], 0.0) for h in HOLDINGS if h["days"] <= LIQUIDITY_WINDOW)
    liq_pass = liq_w >= (MINIMUM_LIQUID_SHARE - 1e-5)

    # 5. Largest single company issuer at most issuer limit
    company_totals = {}
    for h in HOLDINGS:
        iss = h["issuer"].strip()
        if iss.lower() not in EXEMPT_ISSUERS:
            company_totals[iss] = company_totals.get(iss, 0.0) + weights.get(h["holding"], 0.0)

    largest_co_w = max(company_totals.values()) if company_totals else 0.0
    issuer_pass = largest_co_w <= (ISSUER_LIMIT + 1e-5)

    # Calendar-year loss: Never tested statically
    loss_rule_text = "requires CIO clarification"

    # Compile check results
    checks = [
        ("Weights sum to 100", sum_w, sum_pass),
        ("Long-only (lowest weight)", min_w, long_only_pass),
        (f"Reserve >= {reserve_min:.1f}%", res_w, reserve_pass),
        (f"Redeemable in {LIQUIDITY_WINDOW} days >= {MINIMUM_LIQUID_SHARE:.0f}%", liq_w, liq_pass),
        (f"Largest single company <= {ISSUER_LIMIT:.0f}%", largest_co_w, issuer_pass),
    ]

    failed_rules = [c[0] for c in checks if not c[2]]
    fail_count = len(failed_rules)

    if fail_count == 0:
        verdict = "passes every checkable rule"
    else:
        verdict = f"fails {fail_count} rule(s)"

    return {
        "candidate": candidate_name,
        "sum_w": sum_w,
        "sum_pass": sum_pass,
        "min_w": min_w,
        "long_only_pass": long_only_pass,
        "res_w": res_w,
        "reserve_pass": reserve_pass,
        "liq_w": liq_w,
        "liq_pass": liq_pass,
        "largest_co_w": largest_co_w,
        "issuer_pass": issuer_pass,
        "loss_rule_text": loss_rule_text,
        "fail_count": fail_count,
        "verdict": verdict,
        "checks": checks,
    }


def run_all_checks():
    """Run checks on all candidates and print formatted results."""
    reserve_min = compute_reserve_minimum(QUARTERS_TO_COVER, QUARTERLY_DISTRIBUTION, RESERVE_SIZE)
    print(f"Reserve minimum: {reserve_min:.1f}% of the portfolio.\n")

    results = {}
    for name, weights in CANDIDATES.items():
        res = evaluate_candidate(name, weights, reserve_min)
        results[name] = res

        print(f"--- Candidate {name} ---")
        for label, val, passed in res["checks"]:
            status = "pass" if passed else "FAIL"
            print(f"{label}: {val:.1f} {status}")
        print(f"Calendar-year loss: {res['loss_rule_text']}")
        print(f"Verdict: {res['verdict']}\n")

    # Side-by-side comparative table
    col_w = 28
    lbl_w = 32
    cand_names = [k for k in CANDIDATES.keys()]
    total_w = lbl_w + 3 + (col_w + 3) * len(cand_names)

    print("=" * total_w)
    print("MANDATE COMPLIANCE SUMMARY TABLE".center(total_w))
    print("=" * total_w)
    header_cols = [f"{'Rule':<{lbl_w}}"] + [f"{c:^{col_w}}" for c in cand_names]
    print(" | ".join(header_cols))
    print("-" * total_w)

    rows = [
        ("Weights sum to 100", lambda r: f"{r['sum_w']:.1f} {'pass' if r['sum_pass'] else 'FAIL'}"),
        ("Long-only (lowest weight)", lambda r: f"{r['min_w']:.1f} {'pass' if r['long_only_pass'] else 'FAIL'}"),
        (f"Reserve >= {reserve_min:.1f}%", lambda r: f"{r['res_w']:.1f} {'pass' if r['reserve_pass'] else 'FAIL'}"),
        (f"Redeemable in {LIQUIDITY_WINDOW} days >= {MINIMUM_LIQUID_SHARE:.0f}%", lambda r: f"{r['liq_w']:.1f} {'pass' if r['liq_pass'] else 'FAIL'}"),
        (f"Largest single company <= {ISSUER_LIMIT:.0f}%", lambda r: f"{r['largest_co_w']:.1f} {'pass' if r['issuer_pass'] else 'FAIL'}"),
        ("Calendar-year loss", lambda r: r["loss_rule_text"]),
        ("Verdict", lambda r: r["verdict"]),
    ]

    for label, fn in rows:
        col_vals = [f"{fn(results[c]):^{col_w}}" for c in cand_names]
        print(f"{label:<{lbl_w}} | " + " | ".join(col_vals))
    print("=" * total_w)


if __name__ == "__main__":
    run_all_checks()

