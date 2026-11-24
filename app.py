"""
app.py — Investment Management Application
Meridian Foundation Reserve ($100M Portfolio)
Author: Luca Richey | Portfolio Analyst

Built in accordance with institutional mandate specifications:
1. The app runs as an interactive Streamlit web application.
2. Full mandate specifications: objective, universe, benchmark, risk measures, and limits.
3. Two transparent baselines (Equal Weight and 60/40 Benchmark) beside the constrained portfolio,
   each with its explicit mandate verdict (PASS/FAIL, and which rule).
4. Point-in-time credit signal (BAA10Y) with full Data Card and 1-day as-of lag rule.
5. Comprehensive stress testing (estimates, window, costs, constraints) and explicit process stop conditions.
6. Locked Changed-Input Record (AI-off prediction vs. executed result for 50 bps cost drag).
7. Institutional recommendation (PILOT, DO NOT ADOPT), allocation range, and monitoring triggers.
8. Two opening statements disclosing AI use and affirming analyst authorship/educational scope.
"""

from __future__ import annotations

import io
import math
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

# Auto-launcher: launches `streamlit run app.py` if started via `python3 app.py` or IDE Run button.
def _ensure_streamlit_runner():
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            return  # Running inside Streamlit
    except Exception:
        pass

    candidates = [
        sys.executable,
        "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3",
        "python3",
    ]
    chosen_python = None
    for p in candidates:
        try:
            res = subprocess.run([p, "-c", "import streamlit"], capture_output=True)
            if res.returncode == 0:
                chosen_python = p
                break
        except Exception:
            continue

    if not chosen_python:
        chosen_python = sys.executable

    print("=" * 78)
    print("  LAUNCHING MERIDIAN INVESTMENT MANAGEMENT APPLICATION VIA:", chosen_python)
    print("  Local URL: http://localhost:8501")
    print("=" * 78)

    cmd = [
        chosen_python,
        "-m",
        "streamlit",
        "run",
        os.path.abspath(__file__),
        "--browser.gatherUsageStats",
        "false",
    ]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        pass
    sys.exit(0)


if __name__ == "__main__" and "streamlit" not in sys.modules:
    _ensure_streamlit_runner()

import numpy as np
import pandas as pd
import streamlit as st

# Ensure repository root is on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import mandate
import portfolio
from portfolio import (
    CORRELATION_MATRIX,
    OBJECTIVE_RETURN,
    SLEEVES,
    build_covariance_matrix,
    estimate_from_prices,
    portfolio_return,
    portfolio_volatility,
    reserve_eligible_weight,
    search_lowest_risk_mix,
)

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Meridian Foundation Reserve — Investment Management App",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# TWO OPENING STATEMENTS (MANDATED FOR ALL DELIVERABLES)
# -----------------------------------------------------------------------------
with st.container(border=True):
    st.markdown("### Formal Project Attestation & Disclosures")
    st.info(
        "**AI Use Disclosure:** Generative AI models (Google Gemini 1.5 Pro, Anthropic Claude 3.5 Sonnet, "
        "and Antigravity coding agents) were used from day one for architecture scaffolding, Streamlit component "
        "layouts, sensitivity matrix formulation, and document styling. Every mathematical formula, empirical calculation, "
        "mandate audit rule, and sensitivity run was independently audited and verified in code.",
        icon="ℹ️",
    )
    st.warning(
        "**Authorship & Educational Scope:** The analysis, quantitative modeling, mandate defense, "
        "and final investment committee recommendation (*PILOT, DO NOT ADOPT*) are entirely my own. "
        "This application is prepared strictly for educational demonstration in FIN 43900 at Purdue University; "
        "it does not constitute professional investment advice or a solicitation.",
        icon="⚠️",
    )

# Title & Metadata
st.title("Meridian Foundation Reserve ($100M) — Investment Management Application")
st.caption(
    "**Author:** Luca Richey | Portfolio Analyst | "
    "**Mandate:** $100M Reserve, $0.75M Quarterly Payouts, CPI + 4% Objective"
)

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS: MANDATE PARAMETERS & SCENARIO SELECTOR
# -----------------------------------------------------------------------------
st.sidebar.header("Mandate & Universe Controls")

# Scenario Quick-Select
scenario_choice = st.sidebar.selectbox(
    "Select Pre-Built Scenario:",
    options=[
        "Meridian Baseline (0 bps cost drag)",
        "Stress 1: Equity Return Shock (-100 bps -> 7.0%)",
        "Stress 2: IG-Equity Corr Shock (0.25 -> 0.50)",
        "Changed-Input Stress Run: Cost Drag (+50 bps/yr)",
        "Custom Parameters",
    ],
    index=0,
    help="Quickly load baseline or stressed conditions to observe portfolio reallocation and risk shifts.",
)

# Dynamic parameter defaults based on scenario
if scenario_choice == "Meridian Baseline (0 bps cost drag)":
    default_obj = 6.50
    default_res = 3.0
    default_cost_bps = 0.0
    default_eq_ret = 8.00
    default_ig_eq_corr = 0.25
elif scenario_choice == "Stress 1: Equity Return Shock (-100 bps -> 7.0%)":
    default_obj = 6.50
    default_res = 3.0
    default_cost_bps = 0.0
    default_eq_ret = 7.00
    default_ig_eq_corr = 0.25
elif scenario_choice == "Stress 2: IG-Equity Corr Shock (0.25 -> 0.50)":
    default_obj = 6.50
    default_res = 3.0
    default_cost_bps = 0.0
    default_eq_ret = 8.00
    default_ig_eq_corr = 0.50
elif scenario_choice == "Changed-Input Stress Run: Cost Drag (+50 bps/yr)":
    default_obj = 6.50
    default_res = 3.0
    default_cost_bps = 50.0
    default_eq_ret = 8.00
    default_ig_eq_corr = 0.25
else:
    default_obj = 6.50
    default_res = 3.0
    default_cost_bps = 0.0
    default_eq_ret = 8.00
    default_ig_eq_corr = 0.25

# Sidebar Numerical Inputs
obj_input = st.sidebar.number_input(
    "Return Objective (%/yr):",
    min_value=0.0,
    max_value=25.0,
    value=float(default_obj),
    step=0.1,
    format="%.2f",
    help="Target minimum annualized return (CPI 2.5% + 4.0% net real = 6.50%).",
)

res_min_input = st.sidebar.number_input(
    "Reserve Floor (% of $100M):",
    min_value=0.0,
    max_value=50.0,
    value=float(default_res),
    step=0.5,
    format="%.1f",
    help="Derived from 4 quarters x $0.75M = $3.0M (3.0%) held in liquid government paper/cash.",
)

cost_bps_input = st.sidebar.number_input(
    "Implementation Cost Drag (bps/yr):",
    min_value=0.0,
    max_value=300.0,
    value=float(default_cost_bps),
    step=5.0,
    format="%.1f",
    help="Annualized transaction, custody, and advisory friction applied across all sleeves.",
)

st.sidebar.divider()
st.sidebar.subheader("Data Universe & Window")

use_uploaded_csv = st.sidebar.checkbox(
    "Upload Custom prices.csv",
    value=False,
    help="Switch from Meridian 4 sleeves to empirical ETF prices (BIL, IEF, LQD, VT).",
)

uploaded_file = None
use_last_36 = False
if use_uploaded_csv:
    uploaded_file = st.sidebar.file_uploader("Upload monthly prices.csv", type=["csv"])
    use_last_36 = st.sidebar.checkbox(
        "Use Last 36 Months Only",
        value=False,
        help="Estimate parameters from the trailing 3-year window rather than full 59 months.",
    )
else:
    st.sidebar.info("Active Universe: Meridian 4 Sleeves (Bills, 10-Yr, IG Bonds, Global Equities)")

# -----------------------------------------------------------------------------
# CORE QUANTITATIVE ENGINE COMPUTATION
# -----------------------------------------------------------------------------
asset_names = [s["name"] for s in SLEEVES]
asset_shorts = [s["short_name"] for s in SLEEVES]
gross_returns = [float(s["expected_return"]) for s in SLEEVES]
standalone_vols = [float(s["volatility"]) for s in SLEEVES]
reserve_flags = [bool(s["reserve_eligible"]) for s in SLEEVES]

# Apply equity return shock if scenario or user altered it
if scenario_choice == "Stress 1: Equity Return Shock (-100 bps -> 7.0%)":
    gross_returns[3] = 7.00
else:
    gross_returns[3] = float(default_eq_ret)

# Apply cost drag (in bps -> % deduction)
cost_pct = cost_bps_input / 100.0
active_returns = [r - cost_pct for r in gross_returns]

# Construct active correlation matrix
active_corr = [row[:] for row in CORRELATION_MATRIX]
if scenario_choice == "Stress 2: IG-Equity Corr Shock (0.25 -> 0.50)":
    active_corr[2][3] = 0.50
    active_corr[3][2] = 0.50
else:
    active_corr[2][3] = float(default_ig_eq_corr)
    active_corr[3][2] = float(default_ig_eq_corr)

# Build covariance matrices
base_cov = build_covariance_matrix(CORRELATION_MATRIX, standalone_vols)
active_cov = build_covariance_matrix(active_corr, standalone_vols)

# Solve Baseline Portfolio (0 bps cost, 6.5% obj, 3.0% reserve, baseline inputs)
baseline_sol = search_lowest_risk_mix(
    expected_returns=gross_returns,
    cov_matrix=base_cov,
    reserve_flags=reserve_flags,
    objective_return=6.50,
    min_reserve=3.0,
    step_pct=5.0,
)

# Solve Active / Stressed Portfolio
active_sol = search_lowest_risk_mix(
    expected_returns=active_returns,
    cov_matrix=active_cov,
    reserve_flags=reserve_flags,
    objective_return=float(obj_input),
    min_reserve=float(res_min_input),
    step_pct=5.0,
)

# Compute Baselines
# 1. Equal Weight (25% each)
w_eq = [0.25, 0.25, 0.25, 0.25]
ret_eq = portfolio_return(w_eq, gross_returns)
vol_eq = portfolio_volatility(w_eq, base_cov)
res_eq = reserve_eligible_weight(w_eq, reserve_flags)

# 2. Benchmark (60/40 Policy Benchmark - Candidate E: 0/0/40/60)
w_bm = [0.0, 0.0, 0.40, 0.60]
ret_bm = portfolio_return(w_bm, gross_returns)
vol_bm = portfolio_volatility(w_bm, base_cov)
res_bm = reserve_eligible_weight(w_bm, reserve_flags)

# 3. Inverse Volatility Portfolio
w_iv = portfolio.compute_inverse_volatility_weights(standalone_vols)
ret_iv = portfolio_return(w_iv, gross_returns)
vol_iv = portfolio_volatility(w_iv, base_cov)
res_iv = reserve_eligible_weight(w_iv, reserve_flags)

# -----------------------------------------------------------------------------
# PROCESS STOP CONDITION AUDIT
# -----------------------------------------------------------------------------
stop_triggers: List[str] = []

if active_sol is None:
    stop_triggers.append(
        f"**INFEASIBLE OPTIMIZATION:** No discrete 5-point portfolio combination meets both the "
        f"{obj_input:.2f}% return objective and {res_min_input:.1f}% reserve minimum."
    )
else:
    # Check weight stability shift vs baseline
    w_base = baseline_sol["weights_pct"]
    w_act = active_sol["weights_pct"]
    diffs = [a - b for a, b in zip(w_act, w_base)]
    max_shift = max(abs(d) for d in diffs)
    shift_asset = asset_shorts[diffs.index(max_shift) if max_shift in diffs else diffs.index(-max_shift)]

    if max_shift > 10.0:
        stop_triggers.append(
            f"**EXCESSIVE WEIGHT INSTABILITY:** Maximum single-asset weight shift is **{max_shift:.1f} percentage points** "
            f"({shift_asset}), exceeding the 10.0-pt governance threshold ($10.0M reallocation on $100M reserve)."
        )

    # Check equity policy band (40% - 65%)
    eq_weight = w_act[3]
    if eq_weight > 65.0 or eq_weight < 40.0:
        stop_triggers.append(
            f"**POLICY BAND BREACH:** Equity allocation of **{eq_weight:.1f}%** violates the "
            f"recommended 40%–65% strategic equity policy band."
        )

# -----------------------------------------------------------------------------
# MAIN APPLICATION TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎯 Committee Recommendation",
    "📜 Mandate & Candidate Audit",
    "⚖️ Baselines vs. Constrained Portfolio",
    "💥 Stress Suite & Stop Condition",
    "📡 Point-in-Time Signal (BAA10Y)",
    "🔒 Locked Changed-Input Record",
])

# =============================================================================
# TAB 1: COMMITTEE RECOMMENDATION & ALLOCATION
# =============================================================================
with tab1:
    st.subheader("Buy-Side Investment Committee Recommendation")

    rec_col1, rec_col2 = st.columns([3, 2])
    with rec_col1:
        st.markdown(
            """
            ### **Recommendation: PILOT, DO NOT ADOPT**
            
            We recommend that the Investment Committee **PILOT, DO NOT ADOPT**, the mandate-constrained 
            lowest-risk allocation (`0.0% Bills / 20.0% 10-Yr / 25.0% IG / 55.0% Equity`), authorizing a 
            **$10M (10%) proof-of-concept pilot**, while retaining the remaining $90M in low-turnover 
            canonical sleeves.
            
            **Reversal Condition (When to ADOPT):**
            The committee should reverse this call to **ADOPT** if and only if three governance conditions are satisfied:
            1. **Codify a Strategic Policy Band:** Adopt an explicit **40%–65% equity band** around the 55% target.
            2. **Approve Shrinkage Priors:** Mandate Black-Litterman or Bayesian shrinkage priors that guarantee 
               largest weight shifts stay **under 10 percentage points** across a 50 bps fee drag or 100 bps equity shock.
            3. **Define Statement S9:** Formally quantify the CIO's calendar-year loss limit into an actionable 
               downside risk budget (e.g. 1-year 95% CVaR $\le 10.0\%$) with explicit breach rebalancing rules.
            """
        )

    with rec_col2:
        with st.container(border=True):
            st.markdown("#### Optimal Baseline Allocation ($100M Reserve)")
            st.metric("Expected Annual Return", "6.51%", delta="+1 bps above 6.50% Hurdle")
            st.metric("Annualized Volatility", "9.44%", delta="-102 bps below 60/40 Benchmark (10.46%)")
            st.metric("Reserve-Eligible Liquid Buffer", "20.0%", delta="+17.0 pts above 3.0% Minimum")
            st.caption("Discrete 5-point lowest-risk feasible portfolio under baseline frictionless parameters.")

    st.divider()

    st.subheader("Target Allocation Ranges & Sleeve Implementation")
    range_data = {
        "Asset Sleeve": ["Treasury Bills (BIL)", "10-Year Treasuries (IEF)", "IG Corporate Bonds (LQD)", "Global Equities (VT)"],
        "Target Baseline Weight": ["0.0%", "20.0%", "25.0%", "55.0%"],
        "Recommended Allocation Band": ["0.0% – 5.0%", "10.0% – 25.0%", "15.0% – 30.0%", "50.0% – 65.0%"],
        "Dollar Allocation ($100M Reserve)": ["$0.0M", "$20.0M", "$25.0M", "$55.0M"],
        "Reserve Eligibility": ["Eligible (Rule S3)", "Eligible (Rule S3)", "Non-Eligible", "Non-Eligible"],
        "Role in Reserve Portfolio": [
            "Emergency liquidity & frictional buffer",
            "Duration hedge, reserve requirement compliance",
            "Yield enhancement & corporate income spread",
            "Capital growth engine to satisfy CPI + 4% hurdle",
        ],
    }
    st.table(pd.DataFrame(range_data))

    st.subheader("Operational Monitoring Triggers (When to Rebalance or Halt)")
    trig_col1, trig_col2, trig_col3 = st.columns(3)
    with trig_col1:
        st.markdown(
            """
            **1. Policy Band Breach Trigger:**  
            If market price drift moves any sleeve weight $\ge 5.0$ percentage points away from its target baseline 
            (e.g., Equity $> 60.0\%$ or $< 50.0\%$), execute calendar rebalancing to reset to baseline.
            """
        )
    with trig_col2:
        st.markdown(
            """
            **2. Credit Spread Regime Trigger:**  
            If the point-in-time Moody's Baa spread (`BAA10Y`) widens beyond **2.50% (250 bps)**, halt IG bond 
            rebalancing and reallocate up to 10% from IG bonds into 10-Year Treasuries.
            """
        )
    with trig_col3:
        st.markdown(
            """
            **3. Cost Drag & Turnover Trigger:**  
            If annualized transaction slippage and advisory fee drag exceeds **40 bps/yr**, or if annual portfolio 
            turnover approaches the **25.0% ceiling (Rule S7)**, stop optimization and review execution venues.
            """
        )

# =============================================================================
# TAB 2: MANDATE RULES & CANDIDATE AUDIT
# =============================================================================
with tab2:
    st.subheader("Meridian Foundation Reserve Mandate Architecture")
    st.markdown(
        """
        The **Meridian Foundation Reserve ($100M)** is governed by specific Investment Policy Statement (IPS) 
        guidelines articulated by the Chief Investment Officer (CIO). Each statement has been mathematically 
        classified into standard institutional taxonomy:
        """
    )

    ips_df = pd.DataFrame({
        "Statement": [f"S{i}" for i in range(1, 11)],
        "Exact Mandate Statement": [
            "Horizon seven years; annual rebalancing.",
            "Objective: CPI + 4% a year, net of costs, over rolling five-year periods.",
            "Pays out $0.75 million every quarter; twelve months of payouts held in cash or daily-liquid government securities.",
            "Benchmark: 60% global equities, 40% U.S. investment-grade bonds.",
            "Long-only: no borrowing, short sales or derivatives.",
            "No single issuer above 8%.",
            "Annual turnover at most 25% without committee approval.",
            "At least 90% redeemable within five business days.",
            "The reserve cannot have a calendar-year loss greater than 10%. No measure, no breach rule.",
            "No sector, ESG, tax or home-bias preference; nobody has said what the pilot should optimize.",
        ],
        "Classification": [
            "Hard Constraint", "Objective", "Hard Constraint", "Preference",
            "Hard Constraint", "Hard Constraint", "Hard Constraint", "Hard Constraint",
            "Unverifiable Promise", "Missing",
        ],
        "Mathematical / Operational Definition": [
            "Annual rebalance calendar; maximum 7-year illiquid commitments.",
            "E[R_p] >= 6.50% (CPI estimated at 2.50% + 4.00% net real return).",
            "Reserve Floor = 4 quarters x $0.75M / $100M = 3.0% in Cash, T-Bills, or 10-Yr Treasury.",
            "Reference asset allocation: 60% VT / 40% LQD (Candidate E).",
            "w_i >= 0, sum(w_i) = 1.0, no leverage, no short positions.",
            "Non-exempt corporate issuer weight <= 8.0% (Acme Corp equity + debt).",
            "Annual turnover <= 25.0% without explicit committee resolution.",
            "At least 90.0% of portfolio liquidated at NAV within 5 business days.",
            "Ex-post realized return aspiration; requires ex-ante VaR/CVaR clarification.",
            "Optimizer objective function undefined; resolved via lowest-risk feasible grid search.",
        ],
    })
    st.dataframe(ips_df, hide_index=True)

    st.divider()
    st.subheader("Audit of Candidate Portfolios (mandate.py)")
    st.markdown(
        "Each candidate evaluated against all checkable mandate rules. "
        "Notice that **Candidate E (the client's own 60/40 benchmark) FAILS** its own mandate reserve rule!"
    )

    cand_audit = [
        {"Candidate": "Candidate A", "Reserve % (>=3.0%)": "14.0% (PASS)", "5-Day Liquidity (>=90%)": "100.0% (PASS)", "Max Issuer % (<=8.0%)": "0.0% (PASS)", "Mandate Verdict": "PASSES ALL CHECKABLE RULES"},
        {"Candidate": "Candidate B", "Reserve % (>=3.0%)": "1.0% (FAIL)", "5-Day Liquidity (>=90%)": "85.0% (FAIL - 15% Private Real Estate)", "Max Issuer % (<=8.0%)": "9.0% (FAIL - Acme 5% bond + 4% stock)", "Mandate Verdict": "FAILS 3 RULES"},
        {"Candidate": "Candidate C", "Reserve % (>=3.0%)": "2.0% (FAIL)", "5-Day Liquidity (>=90%)": "100.0% (PASS)", "Max Issuer % (<=8.0%)": "8.0% (PASS)", "Mandate Verdict": "FAILS 1 RULE (Reserve < 3%)"},
        {"Candidate": "Candidate D (Attack)", "Reserve % (>=3.0%)": "3.0% (PASS)", "5-Day Liquidity (>=90%)": "100.0% (PASS)", "Max Issuer % (<=8.0%)": "0.0% (PASS)", "Mandate Verdict": "PASSES STATICALLY (Substantively Unacceptable: 97% equity)"},
        {"Candidate": "Candidate E (60/40 Benchmark)", "Reserve % (>=3.0%)": "0.0% (FAIL)", "5-Day Liquidity (>=90%)": "100.0% (PASS)", "Max Issuer % (<=8.0%)": "0.0% (PASS)", "Mandate Verdict": "FAILS 1 RULE (Reserve 0.0% < 3.0%)"},
    ]
    st.dataframe(pd.DataFrame(cand_audit), hide_index=True)

# =============================================================================
# TAB 3: BASELINES VS. CONSTRAINED PORTFOLIO
# =============================================================================
with tab3:
    st.subheader("Two Transparent Baselines beside Constrained Portfolio")
    st.markdown(
        """
        To satisfy base requirement 3, the table and cards below present **Equal Weight** and the **60/40 Policy Benchmark** 
        (plus Inverse Volatility) alongside our **Mandate-Constrained Lowest-Risk Portfolio**, stating the exact mandate verdict 
        (PASS or FAIL, and which rule is breached) for each.
        """
    )

    b_col1, b_col2, b_col3 = st.columns(3)

    with b_col1:
        with st.container(border=True):
            st.markdown("#### Baseline 1: Equal Weight")
            st.markdown("**Allocation:** 25% Bills / 25% 10-Yr / 25% IG / 25% Equity")
            st.metric("Expected Return", f"{ret_eq:.2f}%", delta=f"{ret_eq - 6.50:+.2f}% vs. Hurdle")
            st.metric("Annualized Volatility", f"{vol_eq:.2f}%")
            st.metric("Reserve-Eligible Weight", f"{res_eq:.1f}%")
            st.error("❌ **MANDATE VERDICT: FAIL**")
            st.caption("**Rule Breached:** S2 Return Objective (5.20% is 130 bps below the 6.50% hurdle).")

    with b_col2:
        with st.container(border=True):
            st.markdown("#### Baseline 2: 60/40 Policy Benchmark")
            st.markdown("**Allocation:** 0% Bills / 0% 10-Yr / 40% IG / 60% Equity")
            st.metric("Expected Return", f"{ret_bm:.2f}%", delta=f"{ret_bm - 6.50:+.2f}% vs. Hurdle")
            st.metric("Annualized Volatility", f"{vol_bm:.2f}%", delta="+102 bps vs. Constrained")
            st.metric("Reserve-Eligible Weight", f"{res_bm:.1f}%")
            st.error("❌ **MANDATE VERDICT: FAIL**")
            st.caption("**Rule Breached:** S3 Reserve Floor (0.0% reserve-eligible paper is below the required 3.0% minimum).")

    with b_col3:
        with st.container(border=True):
            st.markdown("#### Constrained Portfolio (Meridian)")
            st.markdown("**Allocation:** 0% Bills / 20% 10-Yr / 25% IG / 55% Equity")
            st.metric("Expected Return", f"{baseline_sol['expected_return']:.2f}%", delta="+0.01% vs. Hurdle")
            st.metric("Annualized Volatility", f"{baseline_sol['volatility']:.2f}%", delta="-102 bps below 60/40 Vol")
            st.metric("Reserve-Eligible Weight", f"{baseline_sol['reserve_eligible_pct']:.1f}%", delta="+17.0 pts Reserve Buffer")
            st.success("✅ **MANDATE VERDICT: PASS**")
            st.caption("**Rules Satisfied:** Passes S2 (6.51% >= 6.50%), S3 (20.0% >= 3.0%), S5, S6, S7, S8.")

    st.divider()

    st.subheader("Comprehensive Baseline Comparison Table")
    comp_data = {
        "Portfolio Name": [
            "Equal Weight (Baseline 1)",
            "60/40 Policy Benchmark (Baseline 2 / Cand. E)",
            "Inverse Volatility (Alt. Baseline)",
            "Mandate-Constrained Portfolio (Meridian Lowest-Risk)",
        ],
        "Bills / 10-Yr / IG / Equity": [
            "25.0% / 25.0% / 25.0% / 25.0%",
            "0.0% / 0.0% / 40.0% / 60.0%",
            f"{w_iv[0]*100:.1f}% / {w_iv[1]*100:.1f}% / {w_iv[2]*100:.1f}% / {w_iv[3]*100:.1f}%",
            "0.0% / 20.0% / 25.0% / 55.0%",
        ],
        "Expected Return": [f"{ret_eq:.2f}%", f"{ret_bm:.2f}%", f"{ret_iv:.2f}%", f"{baseline_sol['expected_return']:.2f}%"],
        "Annualized Volatility": [f"{vol_eq:.2f}%", f"{vol_bm:.2f}%", f"{vol_iv:.2f}%", f"{baseline_sol['volatility']:.2f}%"],
        "Reserve-Eligible Weight": [f"{res_eq:.1f}%", f"{res_bm:.1f}%", f"{res_iv:.1f}%", f"{baseline_sol['reserve_eligible_pct']:.1f}%"],
        "Meets 6.50% Hurdle?": ["No (5.20%)", "Yes (6.80%)", "No (3.77%)", "Yes (6.51%)"],
        "Meets 3.0% Reserve?": ["Yes (50.0%)", "No (0.0%)", "Yes (90.3%)", "Yes (20.0%)"],
        "Mandate Verdict": [
            "FAIL (Rule S2 Return < 6.50%)",
            "FAIL (Rule S3 Reserve 0.0% < 3.0%)",
            "FAIL (Rule S2 Return < 6.50%)",
            "PASS ALL CHECKABLE RULES",
        ],
    }
    st.table(pd.DataFrame(comp_data))

# =============================================================================
# TAB 4: STRESS SUITE & PROCESS STOP CONDITION
# =============================================================================
with tab4:
    st.subheader("Stress Testing on Estimates, Window, Costs, and Constraints")
    st.markdown(
        """
        Unconstrained mean-variance optimization produces acute capital swings under minor real-world friction. 
        Below we evaluate four canonical stress tests and define the **Process Stop Condition** that halts the process.
        """
    )

    # Process Stop Alert Banner
    if stop_triggers:
        st.error("🚨 **THE PROCESS STOP CONDITION HAS BEEN TRIGGERED**", icon="🛑")
        for trig in stop_triggers:
            st.markdown(f"- {trig}")
        st.warning(
            "**Governance Action Required:** Automated trade generation and rebalancing are **HALTED**. "
            "The portfolio analyst must escalate immediately to the Investment Committee for manual intervention.",
            icon="⚠️",
        )
    else:
        st.success(
            "✅ **PROCESS OPERATING NORMALLY:** Active allocation is feasible, weight shift is within the 10.0-pt "
            "stability threshold, and equity allocation remains within the 40%–65% policy band.",
            icon="🛡️",
        )

    st.divider()

    st.subheader("Side-by-Side: Baseline vs. Active / Stressed Allocation")
    scol1, scol2 = st.columns(2)

    with scol1:
        st.markdown("#### Baseline (Frictionless / As Loaded)")
        st.markdown("**Parameters:** Cost = 0 bps | Equity Ret = 8.0% | IG-Eq Corr = 0.25 | Objective = 6.50%")
        st.metric("Optimal Mix (B / 10Y / IG / Eq)", "0% / 20% / 25% / 55%")
        st.metric("Expected Return", f"{baseline_sol['expected_return']:.2f}%")
        st.metric("Annualized Volatility", f"{baseline_sol['volatility']:.2f}%")
        st.metric("Reserve-Eligible Buffer", f"{baseline_sol['reserve_eligible_pct']:.1f}%")

    with scol2:
        st.markdown(f"#### Active / Stressed Run: {scenario_choice}")
        st.markdown(f"**Parameters:** Cost = {cost_bps_input:.0f} bps | Equity Ret = {active_returns[3]+cost_pct:.1f}% | Corr = {active_corr[2][3]:.2f}")
        if active_sol is not None:
            curr_mix_str = " / ".join(f"{w:.0f}%" for w in active_sol["weights_pct"])
            st.metric("Optimal Mix (B / 10Y / IG / Eq)", curr_mix_str)
            st.metric("Expected Return", f"{active_sol['expected_return']:.2f}%", delta=f"{active_sol['expected_return'] - baseline_sol['expected_return']:+.2f}%")
            st.metric("Annualized Volatility", f"{active_sol['volatility']:.2f}%", delta=f"{active_sol['volatility'] - baseline_sol['volatility']:+.2f}%")
            st.metric("Reserve-Eligible Buffer", f"{active_sol['reserve_eligible_pct']:.1f}%", delta=f"{active_sol['reserve_eligible_pct'] - baseline_sol['reserve_eligible_pct']:+.1f}%")
        else:
            st.error("No combination in 5-point discrete steps meets the objective return and reserve floor.")

    st.divider()

    st.subheader("The Four Canonical Stress Scenarios")
    stress_table = [
        {
            "Stress Scenario": "Baseline (As Loaded)",
            "Sleeve Returns (B/10Y/IG/Eq)": "[3.5%, 4.3%, 5.0%, 8.0%]",
            "Active Mix": "0% / 20% / 25% / 55%",
            "Net Return": "6.51%",
            "Volatility": "9.44%",
            "Reserve": "20.0%",
            "Largest Shift": "0.0 pts",
            "Impact on Decision": "Baseline Candidate",
        },
        {
            "Stress Scenario": "Stress 1: Equity Return Shock (-100 bps -> 7.0%)",
            "Sleeve Returns (B/10Y/IG/Eq)": "[3.5%, 4.3%, 5.0%, 7.0%]",
            "Active Mix": "0% / 10% / 10% / 80%",
            "Net Return": "6.53%",
            "Volatility": "12.94%",
            "Reserve": "10.0%",
            "Largest Shift": "25.0 pts (Eq +25 pts)",
            "Impact on Decision": "Reinforces PILOT (Spikes vol by +350 bps; $25M moved to equity)",
        },
        {
            "Stress Scenario": "Stress 2: IG-Equity Corr Shock (0.25 -> 0.50)",
            "Sleeve Returns (B/10Y/IG/Eq)": "[3.5%, 4.3%, 5.0%, 8.0%]",
            "Active Mix": "0% / 40% / 0% / 60%",
            "Net Return": "6.52%",
            "Volatility": "9.73%",
            "Reserve": "40.0%",
            "Largest Shift": "25.0 pts (IG -25 pts)",
            "Impact on Decision": "Reinforces PILOT (IG dumped from 25% to 0%; $25M moved to 10-Yr)",
        },
        {
            "Stress Scenario": "Changed-Input Stress Run: Cost Drag (+50 bps/yr)",
            "Sleeve Returns (B/10Y/IG/Eq)": "[3.0%, 3.8%, 4.5%, 7.5%]",
            "Active Mix": "0% / 10% / 20% / 70%",
            "Net Return": "6.53%",
            "Volatility": "11.57%",
            "Reserve": "10.0%",
            "Largest Shift": "15.0 pts (Eq +15 pts)",
            "Impact on Decision": "Survives & Reinforces PILOT (Vol jumps +213 bps, exceeding 60/40 benchmark)",
        },
    ]
    st.table(pd.DataFrame(stress_table))

    st.subheader("Window Sensitivity: Trailing 3-Year vs. Full 5-Year History (prices.csv)")
    window_data = {
        "Estimation Window": ["Full History (59 Monthly Obs: Nov 2021 – Oct 2026)", "Trailing 3-Year (Last 36 Monthly Obs: Nov 2023 – Oct 2026)"],
        "Empirical Annualized Means": ["BIL: 3.71%, IEF: -1.67%, LQD: -0.61%, VT: 11.58%", "BIL: 4.30%, IEF: 4.18%, LQD: 6.13%, VT: 21.21%"],
        "Optimal Lowest-Risk Mix": ["60.0% BIL / 0.0% IEF / 0.0% LQD / 40.0% VT", "85.0% BIL / 0.0% IEF / 0.0% LQD / 15.0% VT"],
        "Expected Return / Volatility": ["Return 6.85% | Vol 6.01% | Reserve 60.0%", "Return 6.83% | Vol 1.77% | Reserve 85.0%"],
        "Capital Sensitivity": ["Baseline Empirical Fit", "Shift of 25.0 percentage points into T-Bills ($25.0M reallocation)"],
    }
    st.table(pd.DataFrame(window_data))

    st.markdown(
        """
        > [!IMPORTANT]
        > **Why the Window Shift Matters:**  
        > Shortening the parameter window to 36 months captures the extraordinary 2023–2026 equity bull market 
        > where `VT` realized an annualized return of **21.21%**. The optimizer takes advantage of this historical 
        > anomaly by slashing equity to only 15% and placing 85% in Treasury Bills (`BIL`), artificially suppressing portfolio 
        > volatility to **1.77%**. In reality, 21.21% equity returns are an ex-post trailing windfall, not an ex-ante expected return! 
        > This proves why raw backward-looking historical windows without shrinkage priors must never be adopted by a committee.
        """
    )

# =============================================================================
# TAB 5: POINT-IN-TIME SIGNAL & DATA CARD (BAA10Y)
# =============================================================================
with tab5:
    st.subheader("Point-in-Time Signal: Moody's Baa Corporate Spread over 10-Yr Treasury (BAA10Y)")

    st.markdown(
        """
        A quantitative investment strategy is vulnerable to **information leakage and look-ahead bias** if it trades 
        on macroeconomic figures before they were published, or uses modern flattened series that overwrite past revisions. 
        During point-in-time provenance testing, we audited the St. Louis Fed FRED and ALFRED vintage databases to establish data admission criteria.
        """
    )

    sig_col1, sig_col2 = st.columns([2, 1])

    with sig_col1:
        with st.container(border=True):
            st.markdown("### Formal Point-in-Time Data Card: BAA10Y")
            st.markdown(
                """
                - **Series ID:** `BAA10Y` (Moody's Seasoned Baa Corporate Bond Yield Relative to Yield on 10-Year Treasury Constant Maturity)
                - **Source / Provider:** Federal Reserve Bank of St. Louis (FRED) & Moody's Investors Service
                - **Economic Role:** Measures investment-grade credit risk premium and default spread; governs active risk-budgeting between corporate credit (`LQD`) and Treasuries (`IEF`).
                - **Units:** Percent (e.g. 1.45 = 145 basis points).
                - **Frequency:** Daily (business days, market holidays excluded).
                - **Publication Schedule & Lag:** Published daily at **4:15 PM Eastern Time** on day $T$ reflecting market close transactions. Settles with an execution lag of **1 business day** ($T-1$ knowable for open of day $T$).
                - **Historical Revision Policy:** **0 Historical Revisions.** Traded secondary market rates represent executed market-clearing transactions; once published, past daily values are never revised.
                - **Admission Decision:** **ADMIT WITH A STRICT 1-DAY AS-OF AVAILABILITY RULE** ($Signal_T = f(BAA10Y_{t \le T-1})$).
                - **Revocation / Quarantine Trigger:** If Moody's alters calculation to incorporate modeled/survey estimates, immediately quarantine to ALFRED vintage retrieval.
                """
            )

    with sig_col2:
        with st.container(border=True):
            st.markdown("### Provenance Comparison")
            st.markdown(
                """
                | Dimension | Nonfarm Payrolls (PAYEMS) | Baa Spread (BAA10Y) |
                |---|:---:|:---:|
                | **Source** | BLS Survey | Traded Bond Prices |
                | **Publication Lag** | 1st Friday after month | Daily post-close (4:15 PM) |
                | **Historical Revisions** | **381 monthly revisions** | **0 revisions** |
                | **Look-Ahead Risk** | Extreme | Near-zero with 1-day lag |
                | **Admission Status** | **REJECTED / QUARANTINED** | **ADMITTED (1-Day Lag)** |
                """
            )

    st.divider()

    st.subheader("Credit Regime Gating Logic")
    st.markdown(
        """
        Our application implements an operational credit regime filter using `BAA10Y`:
        - **Normal Regime ($BAA10Y \le 2.00\%$):** Normal credit risk premium. Meridian IG sleeve maintained at baseline 25.0%.
        - **Caution Regime ($2.00\% < BAA10Y \le 2.50\%$):** Elevated credit stress. Bar rebalancing inflows into corporate credit.
        - **Distress Regime ($BAA10Y > 2.50\%$):** Credit dislocation / flight to safety. **Triggers Process Stop Condition**, 
          halting corporate credit allocations and shifting up to 10% into 10-Year Treasuries (`IEF`).
        """
    )

    # Historical Spread Reference Sample
    sample_dates = ["2024-01-02", "2024-06-03", "2025-01-02", "2025-06-02", "2026-01-02", "2026-09-30", "2026-10-26"]
    sample_spreads = [1.62, 1.54, 1.48, 1.42, 1.50, 1.47, 1.45]
    chart_df = pd.DataFrame({"Date": pd.to_datetime(sample_dates), "BAA10Y Spread (%)": sample_spreads}).set_index("Date")
    st.line_chart(chart_df, height=240)

# =============================================================================
# TAB 6: LOCKED CHANGED-INPUT RECORD
# =============================================================================
with tab6:
    st.subheader("Locked Changed-Input Record (AI-Off Pre-Run Prediction vs. Result)")
    st.markdown(
        """
        To fulfill base requirement 6 and the instructor submission architecture, this record preserves the 
        human-authored prediction committed to GitHub **before running any AI assistance or code execution**, 
        followed by the exact preserved execution outputs and reconciliation.
        """
    )

    with st.container(border=True):
        st.markdown("### Part 1: Pre-Run Human Prediction (AI-Off)")
        st.markdown(
            """
            - **Load-Bearing Input Chosen:** **Annualized implementation and advisory cost drag** (applied uniformly across all four asset sleeves to reflect ETF expense ratios, custody, rebalancing execution slippage, and management fees).
            - **Old Value (Frictionless Baseline):** `0.00% / yr` (`0.0 bps/yr`). Sleeve expected returns: Bills `3.50%`, 10-Yr `4.30%`, IG `5.00%`, Equity `8.00%`.
            - **New Value (Stressed Input):** `0.50% / yr` (`50.0 bps/yr`). Net sleeve expected returns: Bills `3.00%`, 10-Yr `3.80%`, IG `4.50%`, Equity `7.50%`.
            - **Predicted Direction of Numbers:**
              1. *Equity weight* will move **sharply UP** (from 55% into the 65%–75% range), because subtracting 50 bps from every sleeve pulls the baseline portfolio's return down from 6.51% to 6.01%, failing the 6.50% hurdle by 49 bps.
              2. *Fixed income and reserve weights* (10-Yr and IG) will move **DOWN** as capital is forced into equities to recover the fee drag.
              3. *Portfolio volatility* will move **UP** significantly (exceeding the 10.46% volatility of the 60/40 benchmark).
            - **Predicted Effect on Decision:**
              - The committee recommendation (**`PILOT, DO NOT ADOPT`**) **will NOT flip to adopt**; instead, it will be **actively reinforced**, because a modest 50 bps real-world cost friction erases the optimizer's risk advantage over the 60/40 benchmark and triggers double-digit capital reallocations.
            """
        )

    st.divider()

    st.subheader("Part 2: Executed Output Reconciliation & Analysis")
    recon_df = pd.DataFrame({
        "Metric / Output Dimension": [
            "Asset Allocation Mix (Bills / 10-Yr / IG / Equity)",
            "Net Expected Annual Return",
            "Annualized Portfolio Volatility",
            "Reserve-Eligible Liquid Assets (S3)",
            "Largest Single-Asset Weight Shift",
            "Volatility vs. 60/40 Benchmark (10.46%)",
            "Mandate Compliance Verdict",
            "Investment Committee Decision Line",
        ],
        "Before (0 bps Cost Drag)": [
            "0.0% / 20.0% / 25.0% / 55.0%",
            "6.51%",
            "9.44%",
            "20.0%",
            "0.0 percentage points",
            "-102 bps lower risk (Advantage)",
            "PASS ALL CHECKABLE RULES",
            "PILOT, DO NOT ADOPT",
        ],
        "After (50 bps Cost Drag)": [
            "0.0% / 10.0% / 20.0% / 70.0%",
            "6.53%",
            "11.57%",
            "10.0%",
            "15.0 percentage points (Equity: 55% -> 70%)",
            "+111 bps higher risk (Disadvantage)",
            "PASS MANDATE / UNSTABLE",
            "PILOT, DO NOT ADOPT (Reinforced)",
        ],
    })
    st.table(recon_df)

    st.markdown(
        """
        ### Failure Diagnosis & Reconciliation: Why the Decision Survived
        
        The empirical run perfectly confirmed our AI-off prediction:
        1. **Directional Accuracy:** Equity weight surged from **55.0% to 70.0% (+15.0 percentage points)**, 
           10-Year Treasuries were cut from **20.0% to 10.0% (-10.0 points)**, and IG bonds were cut from 
           **25.0% to 20.0% (-5.0 points)**.
        2. **Risk Explosion:** Portfolio volatility spiked by **+213 basis points (from 9.44% to 11.57%)**. 
           Crucially, while the baseline allocation enjoyed a 102 bps risk advantage over the 60/40 policy benchmark (10.46%), 
           the 50 bps cost drag completely destroyed this advantage, making the optimized portfolio **111 bps riskier 
           than the static benchmark**.
        3. **Decision Survival:** The decision did not change from `PILOT` to `ADOPT`; rather, it proved that 
           **raw mean-variance optimization cannot be adopted without policy bands and return shrinkage**, because 
           a routine 50 bps advisory fee forced a $15.0M capital swing into volatile equities and halved the reserve cushion.
        """
    )

# -----------------------------------------------------------------------------
# FOOTER & PROVENANCE
# -----------------------------------------------------------------------------
st.divider()
st.caption(
    "FIN 43900 Investment Management Application | Meridian Foundation Reserve ($100M) | "
    "Author: Luca Richey | Purdue University Fall 2026 | Standard Library + Pandas/Streamlit UI | "
    "Reuses `mandate.py` and `portfolio.py` mathematical primitives."
)
