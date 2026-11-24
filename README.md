# Meridian Foundation Reserve ($100M) — Investment Management Application

**Author:** Luca Richey  
**Course:** FIN 43900 — AI Finance Applications (Purdue University)  
**Project:** Project 2 — Investment Management Application  
**Target Portfolio:** Meridian Foundation Reserve ($100M Fund, $0.75M Quarterly Payouts, CPI + 4.0% Objective)  
**Date:** November 23, 2026  
**One-Command Cold Run:** `python3 run_project2.py`  
**Changed-Input Run (50 bps Cost Drag):** `python3 run_project2.py --cost-bps 50`  
**Interactive Streamlit Web App:** `streamlit run app.py` (or `python3 app.py`)

---

## Formal Project Attestation & Disclosures

> **1. AI Use Disclosure:**  
> Generative AI models (Google Gemini 1.5 Pro, Anthropic Claude 3.5 Sonnet, and Google Antigravity agentic workflows) were utilized from day one of this project for architecture scaffolding, Streamlit user interface layout, discrete optimization matrix formulations, and formatting markdown artifacts. Every underlying mathematical formula, empirical estimator, mandate constraint check, and stress sensitivity scenario was independently audited, hand-checked against course specifications, and verified in code.
>
> **2. Authorship & Educational Scope:**  
> The financial analysis, portfolio optimization methodology, mandate defense, sensitivity interpretations, and final committee recommendation (*PILOT, DO NOT ADOPT*) are entirely my own. This analysis and application are prepared strictly for educational demonstration in FIN 43900 at Purdue University; they do not constitute professional investment advice, fiduciary counsel, or a personal trade solicitation.

---

## Executive Decision Line & Recommendation

> ### **RECOMMENDATION: PILOT, DO NOT ADOPT**
>
> We recommend that the Investment Committee **PILOT, DO NOT ADOPT**, the Meridian mandate-constrained lowest-risk allocation (`0.0% Bills / 20.0% 10-Yr Treasuries / 25.0% IG Corporate Bonds / 55.0% Global Equities`), authorizing an initial **$10.0M (10.0%) proof-of-concept pilot**, while retaining the remaining $90.0M in low-turnover canonical benchmark sleeves.
>
> **The Baseline Candidate Portfolio delivers:**
> - **Expected Nominal Return:** **6.51%** per annum (exceeding the 6.50% hurdle by +1 basis point),
> - **Annualized Volatility:** **9.44%** (providing a **102 bps volatility reduction** relative to the 10.46% risk of the 60/40 policy benchmark),
> - **Reserve-Eligible Buffer:** **20.0%** (comfortably exceeding the non-negotiable 3.0% reserve floor by +17.0 percentage points).

### Committee Reversal Conditions (When to ADOPT)
The Investment Committee should reverse this recommendation to **ADOPT** if and only if three governance conditions are formally codified:
1. **Codify an Explicit Strategic Equity Policy Band:** Adopt an enforceable **40%–65% policy range** around the 55% central equity target, legally prohibiting the optimizer from concentrating up to 70%–80% in equities during yield compression or cost drag.
2. **Approve Bayesian / Black-Litterman Shrinkage Priors:** Mandate return shrinkage priors that guarantee the largest single-asset weight shift stays **under 10.0 percentage points ($10.0M)** across a 50 bps annual cost drag or a 100 bps equity expected return shock.
3. **Quantify Statement S9 Drawdown Limits:** Formally define the Chief Investment Officer's calendar-year loss aspiration into an actionable ex-ante risk budget (e.g. 1-year 95% Conditional Value-at-Risk $\le 10.0\%$) with codified stop-loss and rebalancing breach protocols.

---

## One Command to Reproduce the Entire Decision

Execute this single command from the repository root (or from any working directory — paths resolve relative to the script):

```bash
python3 run_project2.py
```

- **Execution Runtime:** `< 0.3 seconds` (verified cold run: `0.275s` on Python 3.11; zero external dependencies required for core CLI runner via built-in stdlib fallback).
- **Locked Changed-Input Run (50 bps annual cost drag):**
  ```bash
  python3 run_project2.py --cost-bps 50
  ```
- **Launch Interactive Streamlit Web Application:**
  ```bash
  pip install -r requirements.txt
  streamlit run app.py
  ```
  *(Alternatively, run `python3 app.py` or click "Run" in your IDE; the built-in auto-launcher detects Streamlit and opens your browser at `http://localhost:8501`).*

---

## Visible Executed Outputs (Readable Without Running Code)

Every material input, date, and finance result is preserved in clean console captures directly viewable on GitHub:

- **Baseline Decision Console Output (`0 bps` cost drag):** [`outputs/project2_output_baseline.txt`](outputs/project2_output_baseline.txt)
- **Changed-Input Console Output (`50 bps` cost drag):** [`outputs/project2_output_changed_input.txt`](outputs/project2_output_changed_input.txt)
- **Point-in-Time FRED/ALFRED Verification Log:** [`audit_verification.txt`](audit_verification.txt)
- **Investment Committee Decision Memo:** [`docs/decision-memo.md`](docs/decision-memo.md)
- **Validation and AI Use Record:** [`docs/validation-and-ai-use.md`](docs/validation-and-ai-use.md)

---

## Key Verified Numbers at a Glance

| Scenario (Meridian Universe, Objective $\ge 6.50\%$, Reserve $\ge 3.0\%$) | Mix (Bills / 10-Yr / IG / Equity) | Expected Return | Annual Volatility | Reserve Buffer | Largest Shift ($\Delta w_{\max}$) | Mandate Verdict & Decision Effect |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **Equal Weight (Baseline 1)** | `25 / 25 / 25 / 25` | 5.20% | 5.21% | 50.0% | — | **FAIL MANDATE** (Violates Rule S2: Return < 6.50%) |
| **60/40 Policy Benchmark (Cand. E)** | `0 / 0 / 40 / 60` | 6.80% | 10.46% | 0.0% | — | **FAIL MANDATE** (Violates Rule S3: Reserve 0.0% < 3.0%) |
| **Inverse Volatility (Alt. Baseline)** | `84.3 / 6.0 / 7.0 / 2.6` | 3.77% | 1.05% | 90.3% | — | **FAIL MANDATE** (Violates Rule S2: Return < 6.50%) |
| **Meridian Baseline (`0 bps` cost)** | `0 / 20 / 25 / 55` | **6.51%** | **9.44%** | **20.0%** | 0.0 pts | **PASS MANDATE** (Baseline Candidate: 102 bps below 60/40 vol) |
| **Stress 1: Equity Return `8.0% -> 7.0%`** | `0 / 10 / 10 / 80` | 6.53% | 12.94% | 10.0% | 25.0 pts | **Reinforces PILOT** (Vol spikes +350 bps; $25M moved to equity) |
| **Stress 2: IG–Equity Corr `0.25 -> 0.50`** | `0 / 40 / 0 / 60` | 6.52% | 9.73% | 40.0% | 25.0 pts | **Reinforces PILOT** (IG dumped from 25% to 0%; $25M moved to 10-Yr) |
| **Changed-Input Test: Cost Drag `50 bps`** | `0 / 10 / 20 / 70` | 6.53% | **11.57%** | 10.0% | **15.0 pts** | **Survives & Reinforces PILOT** (Vol spikes +213 bps, now > 60/40 vol) |
| **Empirical ETF All 59m (`prices.csv`)** | `60 / 0 / 0 / 40` | 6.85% | 6.01% | 60.0% | — | Empirical historical fit |
| **Empirical ETF Last 36m (`prices.csv`)** | `85 / 0 / 0 / 15` | 6.83% | 1.77% | 85.0% | 25.0 pts | Window distortion: VT realized 21.21% bull run |

---

## Summary of the Eight Base Requirements

Every requirement for Project 2 is fully implemented and audited:

1. **The App Runs:** Fully interactive multi-tab Streamlit web application in [`app.py`](app.py), launched locally with one command (`streamlit run app.py`) or via IDE auto-launcher (`python3 app.py`).
2. **Mandate Architecture:** Encoded in [`mandate.py`](mandate.py) with formal classification of Statements S1–S10 into Objectives, Hard Constraints, Preferences, and Unverifiable Promises. Enforces the derived Rule S3 reserve floor of $4 \times \$0.75\text{M} / \$100\text{M} = \mathbf{3.0\%}$ in liquid government paper/cash.
3. **Two Baselines Beside Constrained Portfolio:** Explicitly presents **Equal Weight** (25/25/25/25; fails S2 return hurdle) and **60/40 Policy Benchmark** (0/0/40/60; fails S3 reserve floor) alongside our constrained mix (0/20/25/55; passes all checkable rules), displaying the exact mandate verdict (PASS/FAIL, and which rule) for each in `app.py`, `run_project2.py`, and `docs/decision-memo.md`.
4. **Point-in-Time Signal & Formal Data Card:** Features the Moody's Baa Corporate Spread over 10-Yr Treasury (`BAA10Y`), audited in St. Louis Fed FRED/ALFRED vintage databases. Admitted under a strict **1-business-day as-of lag rule** with **0 historical revisions** (in contrast to macroeconomic survey `PAYEMS` which exhibited 381 historical revisions and was rejected).
5. **Stress Suite & Process Stop Condition:** Evaluates multi-dimensional shocks (return shock, correlation shock, fee drag, window sensitivity). Implements an automated **Kill Switch / Process Stop Condition** that halts automated rebalancing if $\Delta w_{\max} > 10.0$ pts, if equity weight leaves 40%–65%, if optimization is infeasible, or if `BAA10Y` crosses 250 bps.
6. **Locked Changed-Input Record:** Human-authored prediction locked and committed to GitHub before execution; load-bearing input: 50 bps annual cost drag. Preserves exact before/after outputs (`0/20/25/55` vs `0/10/20/70`, +15.0 pt equity shift, +213 bps volatility jump) and failure diagnosis in [`docs/validation-and-ai-use.md`](docs/validation-and-ai-use.md).
7. **Institutional Recommendation & Ranges:** Recommends **PILOT, DO NOT ADOPT** with an allocation range (Bills: 0%–5%, 10-Yr: 10%–25%, IG Bonds: 15%–30%, Equities: 50%–65%) and standing operational monitoring triggers.
8. **Mandatory Opening Statements:** Prominently opens `README.md`, `docs/decision-memo.md`, `docs/validation-and-ai-use.md`, and all three video transcripts.

---

## Uniform 12-Row Submission Manifest

| Row # | Manifest Item Name | Location / Evidence Pointer | Description / Verification Status | Audit Domain & Governance Scope |
|:---:|---|---|---|---|
| **1** | **Repository URL** | [GitHub Repository](https://github.com/lucarichey/FIN43900-Project2) | Clean, locally runnable codebase containing `run_project2.py`, `app.py`, `mandate.py`, `portfolio.py`, `prices.csv`, `asof.py`, and `requirements.txt`. | Technical Execution & System Reproducibility |
| **2** | **Research Evolution (Editions A & B)** | *Internal research tracking per project architecture* | Editions A and B are retained for internal research tracking per project architecture; Video 1 covers how system and thinking changed plus the AI-output check. Reference: [`docs/validation-and-ai-use.md`](docs/validation-and-ai-use.md). | Research Methodology & Prior Evolution |
| **3** | **Decision Memo** | [`docs/decision-memo.md`](docs/decision-memo.md) | Formal investment committee memo containing decision first (*PILOT, DO NOT ADOPT*), allocation range, mandate audit, two baselines vs constrained mix, BAA10Y data card, stress runs, stop condition, and monitoring triggers. | Financial Soundness & Committee Recommendation |
| **4** | **Validation and AI Use Record** | [`docs/validation-and-ai-use.md`](docs/validation-and-ai-use.md) | Authoritative frozen validation record containing named AI tool disclosures, material AI checks, covariance math verification, mandate audit proofs, and the complete **Locked Changed-Input Record** (50 bps cost drag). | Quantitative Validation & AI Governance Audit |
| **5** | **Video 1 URL (YouTube)** | [Video 1: Research Evolution & AI Check](https://youtu.be/Ji0lqSjpR0g) | Unlisted YouTube link with captions enabled; covers how the system and student thinking changed, and the audit/correction of continuous SLSQP vs discrete grid search and unlagged PAYEMS vs BAA10Y. | Research Authorship & Empirical Evidence |
| **6** | **Video 1 Transcript** | [`docs/transcript-video-1.txt`](docs/transcript-video-1.txt) | Corrected, word-for-word plain-text transcript of Video 1 including opening statements, section timestamps, and exact dialogue. | Verbatim Spoken Record & Transcript Audit |
| **7** | **Video 2 URL (YouTube)** | [Video 2: Codebase Walkthrough](https://youtu.be/bI1Jfo0gMn4) | Unlisted YouTube link with captions enabled; demonstrates repository architecture, mathematical functions, cold-run reproduction, live Locked Changed-Input test, and S9 drawdown limitation. | Codebase Architecture & Technical Ownership |
| **8** | **Video 2 Transcript** | [`docs/transcript-video-2.txt`](docs/transcript-video-2.txt) | Corrected, word-for-word plain-text transcript of Video 2 including code pointers, terminal execution commands, and diagnostics. | Verbatim Spoken Record & Code Walkthrough |
| **9** | **Video 3 URL (YouTube)** | [Video 3: Committee Defense](https://youtu.be/jEmcOVmqI6c) | Unlisted YouTube link with captions enabled; opens with `app.py` running live on screen, leads with recommendation (*PILOT, DO NOT ADOPT*), defends allocation range, baselines, stress sensitivities, reversal conditions, and the ask. | Investment Defense & Live System Demonstration |
| **10** | **Video 3 Transcript** | [`docs/transcript-video-3.txt`](docs/transcript-video-3.txt) | Corrected, word-for-word plain-text transcript of Video 3 including committee pitch, live app commentary, and reversal conditions. | Verbatim Spoken Record & Committee Pitch |
| **11** | **Evidence Index & Repository Access Confirmation** | [`docs/manifest.md`](docs/manifest.md) (Section 2) | Comprehensive timestamped evidence index referencing exact moments in each video, file links, and instructional team private access confirmation. | Traceability & Repository Access Verification |
| **12** | **Optional Deployed-Output URL** | [Localhost Live Runner: `streamlit run app.py`](http://localhost:8501) | Fully interactive multi-tab Streamlit web application running locally via single terminal command or IDE runner; visible console captures in `outputs/`. | Interactive Execution & User Interface |

---

## Repository Map

```
FIN43900-Project2/
├── README.md                      # Primary project orientation, cold-run commands, manifest, and disclosures
├── requirements.txt               # Minimal dependencies (pandas>=2.0.0, streamlit>=1.30.0, numpy>=1.24.0)
├── run_project2.py                # Single-command CLI decision runner (pure stdlib capable, < 0.3s runtime)
├── app.py                         # Interactive Streamlit web application with 6 dedicated tabs & auto-launcher
├── mandate.py                     # Meridian mandate compliance engine (S1–S10 classification, Candidates A–E)
├── portfolio.py                   # Multi-asset covariance, correlation validation, baselines, and grid optimizer
├── prices.csv                     # 60 monthly observations (2021-11-01 to 2026-10-01) for BIL, IEF, LQD, VT
├── asof.py                        # 4-rule provenance gate & point-in-time filter
├── verify_audit.py                # St. Louis Fed FRED/ALFRED benchmark known answer test & revision probe
├── audit_verification.txt         # Captured execution log proving 0 revisions for BAA10Y vs 381 for PAYEMS
├── docs/
│   ├── decision-memo.md           # Formal Investment Committee Decision Memo
│   ├── validation-and-ai-use.md   # Authoritative validation record & Frozen Locked Changed-Input Record
│   ├── manifest.md                # 12-row submission manifest & timestamped video evidence index
│   ├── transcript-video-1.txt     # Corrected plain-text transcript for Video 1 (Research Evolution & AI Check)
│   ├── transcript-video-2.txt     # Corrected plain-text transcript for Video 2 (Codebase Walkthrough)
│   └── transcript-video-3.txt     # Corrected plain-text transcript for Video 3 (Committee Defense)
└── outputs/
    ├── project2_output_baseline.txt      # Exact console output for 0 bps baseline run
    └── project2_output_changed_input.txt # Exact console output for 50 bps changed-input run
```

---

## Known Limitations & Governance Risks

1. **Unquantified Statement S9 (Drawdown Limit):**  
   The CIO's mandate states: *"The reserve cannot have a calendar-year loss greater than 10%."* As established in `mandate.py`, realized calendar-year loss is an ex-post market outcome governed by stochastic returns. A portfolio with 55% equities can experience a calendar-year loss greater than 10% in severe downturns. Without an ex-ante probabilistic risk model (e.g. 1-year 95% CVaR $\le 10\%$) and an enforceable rebalancing rule, treating S9 as a static pass/fail check would provide false security. Hence, the engine flags S9 as *requires CIO clarification*.
2. **Estimation Window Distortion:**  
   Trailing rolling windows without shrinkage priors are vulnerable to cyclical regimes. For example, testing `prices.csv` over the trailing 36-month window (Nov 2023 – Oct 2026) captures `VT`'s extraordinary 21.21% annualized bull-market run, causing the optimizer to slash equity to 15% and park 85% in Treasury Bills. Backward-looking trailing windows must never be deployed without Bayesian shrinkage priors.
3. **Turnover Friction (Rule S7):**  
   Unconstrained quarterly rebalancing under volatile market conditions can trigger annual turnover exceeding the 25.0% mandate ceiling. Our recommendation to **PILOT, DO NOT ADOPT** protects the foundation against turnover friction until the committee establishes formal rebalancing bands.
