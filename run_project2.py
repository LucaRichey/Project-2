#!/usr/bin/env python3
"""
run_project2.py — Single-Command Decision & Risk Allocation Engine
Meridian Foundation Reserve ($100M Portfolio)

Author: Luca Richey | Portfolio Analyst
FIN 43900 — AI Finance Applications (Purdue University)

Reuses mandate.py, portfolio.py, and prices.csv directly (no duplicated math).
Produces the complete committee decision package in one deterministic command:
  1. Mandate Compliance Audit (Candidates A–E from mandate.py)
  2. Canonical Baselines (Benchmark 60/40, Equal Weight, Inverse Volatility)
  3. Mandate-Constrained Lowest-Risk Search (Baseline vs. Active Parameters)
  4. Locked Stress & Changed-Input Validation (Equity -100 bps, Corr 0.50, Cost +50 bps)
  5. Empirical ETF Proxy Universe Verification (prices.csv: BIL, IEF, LQD, VT; All vs. Last 36m)
  6. Committee Decision Line & Reversal Conditions

Usage:
  python3 run_project2.py
  python3 run_project2.py --cost-bps 50
  python3 run_project2.py --equity-return 7.0
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

# Ensure sibling modules (mandate.py, portfolio.py) and prices.csv resolve even
# when invoked from a different working directory (fixes cold-run path errors).
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = (
    SCRIPT_DIR
    if os.path.exists(os.path.join(SCRIPT_DIR, "mandate.py"))
    else os.path.dirname(SCRIPT_DIR)
)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import mandate
import portfolio


def _estimate_from_prices_stdlib(csv_path: str, last_36: bool = False) -> Dict[str, Any]:
    """Pure-stdlib fallback matching portfolio.estimate_from_prices exactly."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        tickers = header[1:]
        rows: List[List[float]] = []
        dates: List[str] = []
        for row in reader:
            if not row or all(cell.strip() == "" for cell in row):
                continue
            dates.append(row[0].strip())
            rows.append([float(x) for x in row[1:]])

    n_assets = len(tickers)
    monthly_returns: List[List[float]] = []
    for t in range(1, len(rows)):
        prev_p, curr_p = rows[t - 1], rows[t]
        monthly_returns.append(
            [(curr_p[j] - prev_p[j]) / prev_p[j] for j in range(n_assets)]
        )

    if last_36:
        monthly_returns = monthly_returns[-36:]

    n_obs = len(monthly_returns)
    means_m = [
        sum(r[j] for r in monthly_returns) / n_obs for j in range(n_assets)
    ]
    stds_m = [
        math.sqrt(
            sum((r[j] - means_m[j]) ** 2 for r in monthly_returns) / (n_obs - 1)
        )
        for j in range(n_assets)
    ]

    expected_returns = [m * 12.0 * 100.0 for m in means_m]
    volatilities = [s * math.sqrt(12.0) * 100.0 for s in stds_m]

    corr_matrix: List[List[float]] = []
    for i in range(n_assets):
        row_c: List[float] = []
        for j in range(n_assets):
            if i == j:
                row_c.append(1.0)
            else:
                cov_ij = sum(
                    (r[i] - means_m[i]) * (r[j] - means_m[j])
                    for r in monthly_returns
                ) / (n_obs - 1)
                row_c.append(cov_ij / (stds_m[i] * stds_m[j]))
        corr_matrix.append(row_c)

    portfolio.validate_correlation_matrix(corr_matrix)
    cov_matrix = portfolio.build_covariance_matrix(corr_matrix, volatilities)
    return {
        "tickers": tickers,
        "expected_returns": expected_returns,
        "volatilities": volatilities,
        "corr_matrix": corr_matrix,
        "cov_matrix": cov_matrix,
        "n_months": n_obs,
        "start_date": dates[0] if dates else "",
        "end_date": dates[-1] if dates else "",
    }


def load_prices_estimation(csv_path: str, last_36: bool = False) -> Dict[str, Any]:
    """Use portfolio.estimate_from_prices when pandas is installed; else stdlib fallback."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.reader(f) if r]
    start_date = rows[1][0].strip() if len(rows) > 1 else ""
    end_date = rows[-1][0].strip() if len(rows) > 1 else ""

    try:
        est = portfolio.estimate_from_prices(csv_path, last_36=last_36)
        est["start_date"] = start_date
        est["end_date"] = end_date
        return est
    except ImportError:
        return _estimate_from_prices_stdlib(csv_path, last_36=last_36)


def largest_weight_shift(
    base_weights: List[float],
    new_weights: List[float],
    labels: List[str],
) -> Tuple[float, str, float, float]:
    """Return (max_abs_shift_pts, asset_label, base_w, new_w)."""
    diffs = [abs(n - b) for b, n in zip(base_weights, new_weights)]
    max_shift = max(diffs)
    idx = diffs.index(max_shift)
    return max_shift, labels[idx], base_weights[idx], new_weights[idx]


def evaluate_meridian_decision(
    objective_return: float = 6.5,
    min_reserve: float = 3.0,
    equity_return_override: Optional[float] = None,
    ig_eq_corr: float = 0.25,
    cost_bps: float = 0.0,
) -> Dict[str, Any]:
    """
    Core Project 2 decision engine block.
    Applies editable parameters (return objective, reserve minimum, equity return,
    IG-equity correlation, and annual cost drag in bps), validates the correlation
    matrix, runs the 5-point discrete long-only grid search, and returns the
    mandate verdict and stability shift relative to the Meridian baseline.
    """
    sleeves = portfolio.SLEEVES
    labels = [s["short_name"] for s in sleeves]
    vols = [float(s["volatility"]) for s in sleeves]
    reserve_flags = [bool(s["reserve_eligible"]) for s in sleeves]

    # Build baseline Meridian covariance and solution
    portfolio.validate_correlation_matrix(portfolio.CORRELATION_MATRIX)
    base_cov = portfolio.build_covariance_matrix(portfolio.CORRELATION_MATRIX, vols)
    base_rets = [float(s["expected_return"]) for s in sleeves]
    baseline_sol = portfolio.search_lowest_risk_mix(
        expected_returns=base_rets,
        cov_matrix=base_cov,
        reserve_flags=reserve_flags,
        objective_return=6.5,
        min_reserve=3.0,
        step_pct=5.0,
    )

    # Build active (possibly stressed / changed-input) parameters
    active_corr = [row[:] for row in portfolio.CORRELATION_MATRIX]
    active_corr[2][3] = ig_eq_corr
    active_corr[3][2] = ig_eq_corr
    portfolio.validate_correlation_matrix(active_corr)
    active_cov = portfolio.build_covariance_matrix(active_corr, vols)

    active_rets = base_rets[:]
    if equity_return_override is not None:
        active_rets[3] = float(equity_return_override)
    cost_pct = cost_bps / 100.0
    net_rets = [r - cost_pct for r in active_rets]

    active_sol = portfolio.search_lowest_risk_mix(
        expected_returns=net_rets,
        cov_matrix=active_cov,
        reserve_flags=reserve_flags,
        objective_return=objective_return,
        min_reserve=min_reserve,
        step_pct=5.0,
    )

    # Evaluate mandate verdict & stability classification
    if active_sol is None:
        mandate_verdict = "FAIL (INFEASIBLE — no mix meets objective and reserve rules)"
        shift_info = None
    else:
        shift_info = largest_weight_shift(
            baseline_sol["weights_pct"], active_sol["weights_pct"], labels
        )
        max_shift = shift_info[0]
        if max_shift >= 10.0:
            mandate_verdict = (
                f"PASS MANDATE / UNSTABLE ({max_shift:.1f}-pt capital shift; "
                f"vol {active_sol['volatility']:.2f}%)"
            )
        else:
            mandate_verdict = (
                f"PASS MANDATE / STABLE ({max_shift:.1f}-pt shift; "
                f"vol {active_sol['volatility']:.2f}%)"
            )

    return {
        "labels": labels,
        "base_rets": base_rets,
        "net_rets": net_rets,
        "baseline_sol": baseline_sol,
        "active_sol": active_sol,
        "shift_info": shift_info,
        "mandate_verdict": mandate_verdict,
        "cost_bps": cost_bps,
        "objective_return": objective_return,
        "min_reserve": min_reserve,
        "ig_eq_corr": ig_eq_corr,
    }


def format_weights(weights: List[float]) -> str:
    return " / ".join(f"{w:.1f}%" for w in weights)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the complete FIN 43900 Project 2 decision pipeline."
    )
    parser.add_argument(
        "--cost-bps",
        type=float,
        default=0.0,
        help="Annualized implementation/advisory cost drag in basis points (default: 0.0).",
    )
    parser.add_argument(
        "--equity-return",
        type=float,
        default=None,
        help="Override Meridian Global Equity expected return in percent (default: 8.0).",
    )
    parser.add_argument(
        "--objective",
        type=float,
        default=6.5,
        help="Target annualized nominal return objective in percent (default: 6.5).",
    )
    parser.add_argument(
        "--reserve-min",
        type=float,
        default=3.0,
        help="Minimum reserve-eligible weight in percent (default: 3.0).",
    )
    parser.add_argument(
        "--ig-eq-corr",
        type=float,
        default=0.25,
        help="Pairwise correlation between IG bonds and Global Equity (default: 0.25).",
    )
    parser.add_argument(
        "--prices",
        type=str,
        default=os.path.join(REPO_ROOT, "prices.csv"),
        help="Path to monthly ETF prices CSV (default: prices.csv in repo root).",
    )
    args = parser.parse_args()

    width = 92
    print("=" * width)
    print("MERIDIAN FOUNDATION RESERVE ($100M) — DECISION & RISK ALLOCATION RUNNER".center(width))
    print("Author: Luca Richey | Portfolio Analyst".center(width))
    print("=" * width)
    print(f"Active Parameters : Objective >= {args.objective:.2f}% | Reserve >= {args.reserve_min:.1f}% | "
          f"Cost Drag = {args.cost_bps:.1f} bps | IG-Equity Corr = {args.ig_eq_corr:.2f} | "
          f"Equity Return = {args.equity_return if args.equity_return is not None else 8.0:.2f}%")
    print(f"Prices Data File  : {os.path.relpath(args.prices, REPO_ROOT)}")
    print()

    # ------------------------------------------------------------------
    # 1. MANDATE COMPLIANCE AUDIT (reusing mandate.py)
    # ------------------------------------------------------------------
    reserve_min_calc = mandate.compute_reserve_minimum(
        mandate.QUARTERS_TO_COVER, mandate.QUARTERLY_DISTRIBUTION, mandate.RESERVE_SIZE
    )
    print("[1] MANDATE COMPLIANCE AUDIT (mandate.py)")
    print(f"    Derived Reserve Minimum: {reserve_min_calc:.1f}% "
          f"({mandate.QUARTERS_TO_COVER} quarters x ${mandate.QUARTERLY_DISTRIBUTION:.2f}M / ${mandate.RESERVE_SIZE:.0f}M)")
    print(f"    {'Candidate':<12} {'Reserve %':>10} {'Liquid 5d %':>12} {'Max Issuer %':>13}   {'Verdict'}")
    print("    " + "-" * 80)
    for cname, cweights in mandate.CANDIDATES.items():
        res = mandate.evaluate_candidate(cname, cweights, reserve_min_calc)
        print(
            f"    Candidate {cname:<2} {res['res_w']:>9.1f}% {res['liq_w']:>11.1f}% "
            f"{res['largest_co_w']:>12.1f}%   {res['verdict']}"
        )
    print("    Note: Calendar-year loss limit (CIO Statement S9) remains unquantified -> requires CIO clarification.")
    print()

    # ------------------------------------------------------------------
    # 2. CANONICAL PORTFOLIO BASELINES (reusing portfolio.py)
    # ------------------------------------------------------------------
    vols = [float(s["volatility"]) for s in portfolio.SLEEVES]
    base_cov = portfolio.build_covariance_matrix(portfolio.CORRELATION_MATRIX, vols)
    baselines = [
        ("Benchmark (60/40)", [0.0, 0.0, 40.0, 60.0]),
        ("Equal Weight", portfolio.compute_equal_weights(len(portfolio.SLEEVES))),
        ("Inverse Volatility", portfolio.compute_inverse_volatility_weights(vols)),
    ]
    print("[2] CANONICAL PORTFOLIO BASELINES (portfolio.py)")
    print(f"    {'Portfolio':<20} {'Bills / 10-Yr / IG / Equity':<30} {'Return':>8} {'Vol':>8} {'Reserve':>9} {'Meets 6.5%?':>12}")
    print("    " + "-" * 88)
    for bname, bw in baselines:
        ev = portfolio.evaluate_portfolio(bname, bw, portfolio.SLEEVES, base_cov, 6.5)
        w_str = " / ".join(f"{w:.1f}" for w in ev["weights_pct"])
        meets = "yes" if ev["meets_objective"] else "no"
        print(
            f"    {bname:<20} {w_str:<30} {ev['expected_return']:>7.2f}% "
            f"{ev['volatility']:>7.2f}% {ev['reserve_eligible_pct']:>8.1f}% {meets:>12}"
        )
    print()

    # ------------------------------------------------------------------
    # 3. MERIDIAN DECISION SEARCH (BASELINE vs. ACTIVE PARAMETERS)
    # ------------------------------------------------------------------
    dec = evaluate_meridian_decision(
        objective_return=args.objective,
        min_reserve=args.reserve_min,
        equity_return_override=args.equity_return,
        ig_eq_corr=args.ig_eq_corr,
        cost_bps=args.cost_bps,
    )
    b_sol = dec["baseline_sol"]
    a_sol = dec["active_sol"]

    print("[3] MERIDIAN MANDATE-CONSTRAINED LOWEST-RISK SEARCH (5-point grid)")
    print(f"    Baseline (0 bps cost, 8.0% eq, 0.25 corr): {format_weights(b_sol['weights_pct'])}")
    print(f"      -> Return: {b_sol['expected_return']:.2f}% | Volatility: {b_sol['volatility']:.2f}% | "
          f"Reserve-Eligible: {b_sol['reserve_eligible_pct']:.1f}% | Verdict: PASS (102 bps below 60/40 vol)")
    if a_sol is not None:
        print(f"    Active Run (net sleeve returns {[round(x, 2) for x in dec['net_rets']]}%): "
              f"{format_weights(a_sol['weights_pct'])}")
        print(f"      -> Return: {a_sol['expected_return']:.2f}% | Volatility: {a_sol['volatility']:.2f}% | "
              f"Reserve-Eligible: {a_sol['reserve_eligible_pct']:.1f}%")
        max_shift, s_asset, s_old, s_new = dec["shift_info"]
        print(f"      -> Largest Weight Change vs. Baseline: {max_shift:.1f} pts "
              f"({s_asset}: {s_old:.1f}% -> {s_new:.1f}%, ${max_shift:.1f}M on $100M reserve)")
        print(f"      -> Volatility Delta vs. Baseline: {a_sol['volatility'] - b_sol['volatility']:+.2f}% "
              f"({(a_sol['volatility'] - b_sol['volatility']) * 100:+.0f} bps)")
    print(f"    MANDATE VERDICT: {dec['mandate_verdict']}")
    print()

    # ------------------------------------------------------------------
    # 4. VALIDATION & STRESS SUITE (MERIDIAN UNIVERSE)
    # ------------------------------------------------------------------
    stress_runs = [
        ("Baseline (As Loaded)", dict(cost_bps=0.0, equity_return_override=None, ig_eq_corr=0.25)),
        ("Stress 1: Equity Return 8.0% -> 7.0%", dict(cost_bps=0.0, equity_return_override=7.0, ig_eq_corr=0.25)),
        ("Stress 2: IG-Equity Corr 0.25 -> 0.50", dict(cost_bps=0.0, equity_return_override=None, ig_eq_corr=0.50)),
        ("Changed Input: Cost Drag 0 -> 50 bps", dict(cost_bps=50.0, equity_return_override=None, ig_eq_corr=0.25)),
    ]
    print("[4] VALIDATION & STRESS SUITE (Meridian Universe, Objective >= 6.50%, Reserve >= 3.0%)")
    print(f"    {'Scenario':<38} {'Mix (B/10Y/IG/Eq)':<20} {'Ret':>6} {'Vol':>6} {'Res':>6} {'Max Shift':>10}")
    print("    " + "-" * 88)
    for sname, skw in stress_runs:
        sdec = evaluate_meridian_decision(**skw)
        ssol = sdec["active_sol"]
        if ssol is None:
            print(f"    {sname:<38} {'INFEASIBLE':<20} {'--':>6} {'--':>6} {'--':>6} {'--':>10}")
        else:
            mix_str = "/".join(f"{w:.0f}" for w in ssol["weights_pct"])
            mshift = sdec["shift_info"][0]
            print(
                f"    {sname:<38} {mix_str:<20} {ssol['expected_return']:>5.2f}% "
                f"{ssol['volatility']:>5.2f}% {ssol['reserve_eligible_pct']:>5.1f}% {mshift:>8.1f} pt"
            )
    print()

    # ------------------------------------------------------------------
    # 5. EMPIRICAL ETF UNIVERSE (prices.csv: BIL, IEF, LQD, VT)
    # ------------------------------------------------------------------
    est_all = load_prices_estimation(args.prices, last_36=False)
    est_36 = load_prices_estimation(args.prices, last_36=True)
    etf_flags = [True, True, False, False]  # BIL, IEF reserve-eligible; LQD, VT not
    cost_pct = args.cost_bps / 100.0

    etf_all_sol = portfolio.search_lowest_risk_mix(
        [r - cost_pct for r in est_all["expected_returns"]],
        est_all["cov_matrix"],
        etf_flags,
        args.objective,
        args.reserve_min,
        5.0,
    )
    etf_36_sol = portfolio.search_lowest_risk_mix(
        [r - cost_pct for r in est_36["expected_returns"]],
        est_36["cov_matrix"],
        etf_flags,
        args.objective,
        args.reserve_min,
        5.0,
    )

    print(f"[5] EMPIRICAL ETF PROXY UNIVERSE ({', '.join(est_all['tickers'])} | "
          f"{est_all['start_date']} to {est_all['end_date']} | Cost Drag = {args.cost_bps:.1f} bps)")
    print(f"    Empirical Annualized Means (All {est_all['n_months']}m) : " +
          ", ".join(f"{t}={r:.2f}%" for t, r in zip(est_all["tickers"], est_all["expected_returns"])))
    print(f"    Empirical Annualized Means (Last {est_36['n_months']}m): " +
          ", ".join(f"{t}={r:.2f}%" for t, r in zip(est_36["tickers"], est_36["expected_returns"])))
    if etf_all_sol:
        print(f"    All Months Mix ({'/'.join(est_all['tickers'])}): "
              f"{format_weights(etf_all_sol['weights_pct'])} | "
              f"Ret={etf_all_sol['expected_return']:.2f}% | Vol={etf_all_sol['volatility']:.2f}% | "
              f"Res={etf_all_sol['reserve_eligible_pct']:.1f}%")
    if etf_36_sol:
        print(f"    Last 36m Mix   ({'/'.join(est_36['tickers'])}): "
              f"{format_weights(etf_36_sol['weights_pct'])} | "
              f"Ret={etf_36_sol['expected_return']:.2f}% | Vol={etf_36_sol['volatility']:.2f}% | "
              f"Res={etf_36_sol['reserve_eligible_pct']:.1f}%")
    if etf_all_sol and etf_36_sol:
        etf_shift, etf_t, etf_o, etf_n = largest_weight_shift(
            etf_all_sol["weights_pct"], etf_36_sol["weights_pct"], est_all["tickers"]
        )
        print(f"    Window Sensitivity (All vs. 36m): {etf_shift:.1f} pts ({etf_t}: {etf_o:.1f}% -> {etf_n:.1f}%)")
    print()

    # ------------------------------------------------------------------
    # 6. COMMITTEE DECISION LINE
    # ------------------------------------------------------------------
    print("[6] COMMITTEE DECISION LINE")
    print("    PILOT, DO NOT ADOPT, the Meridian lowest-risk allocation (0% Bills / 20% 10-Yr /")
    print("    25% IG / 55% Equity; 6.51% return, 9.44% volatility, 20.0% reserve-eligible) — and")
    print("    reverse to ADOPT only if the Investment Committee codifies a 40%–65% equity policy")
    print("    band, approves shrinkage/Black-Litterman return priors that keep largest weight")
    print("    shifts under 10 percentage points across a 50 bps cost drag or 100 bps equity-return")
    print("    shock, and quantifies the CIO's calendar-year drawdown limit (Statement S9).")
    print("=" * width)


if __name__ == "__main__":
    main()
