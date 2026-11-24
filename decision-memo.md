# Investment Committee Decision Memo — Meridian Foundation Reserve ($100M)

**Author:** Luca Richey | Portfolio Analyst  
**Course:** FIN 43900 — AI Finance Applications (Purdue University)  
**Date:** November 23, 2026  
**Data As-Of Date:** October 26, 2026 (Prices dataset: 60 monthly observations from 2021-11-01 to 2026-10-01; FRED/ALFRED credit spread `BAA10Y`: 2026-10-26)  
**Reproducible Console Outputs:** [`outputs/project2_output_baseline.txt`](../outputs/project2_output_baseline.txt) | [`outputs/project2_output_changed_input.txt`](../outputs/project2_output_changed_input.txt)  
**One-Command Cold-Run Reproduction:** `python3 run_project2.py` (Changed-input run: `python3 run_project2.py --cost-bps 50`)  
**Interactive Web Application:** `streamlit run app.py`

---

## Formal Project Attestation & AI Disclosures

> **1. AI Use Disclosure:**  
> Generative AI models (Google Gemini 1.5 Pro, Anthropic Claude 3.5 Sonnet, and Google Antigravity agentic workflows) were utilized from day one of this project for architecture scaffolding, Streamlit user interface layout, discrete optimization matrix formulations, and formatting markdown artifacts. Every underlying mathematical formula, empirical estimator, mandate constraint check, and stress sensitivity scenario was independently audited, hand-checked against course specifications, and verified in code.
>
> **2. Authorship & Educational Scope:**  
> The financial analysis, portfolio optimization methodology, mandate defense, sensitivity interpretations, and final committee recommendation (*PILOT, DO NOT ADOPT*) are entirely my own. This analysis and decision memo are prepared strictly for educational demonstration in FIN 43900 at Purdue University; they do not constitute professional investment advice, fiduciary counsel, or a personal trade solicitation.

---

## 1. Executive Decision Line & Recommendation

> ### **RECOMMENDATION: PILOT, DO NOT ADOPT**
>
> We recommend that the Investment Committee **PILOT, DO NOT ADOPT**, the Meridian mandate-constrained lowest-risk allocation (`0.0% Bills / 20.0% 10-Yr Treasuries / 25.0% IG Corporate Bonds / 55.0% Global Equities`), authorizing an initial **$10.0M (10.0%) proof-of-concept pilot**, while retaining the remaining $90.0M in low-turnover canonical benchmark sleeves.
>
> **The Baseline Candidate Portfolio delivers:**
> - **Expected Nominal Return:** **6.51%** per annum (exceeding the 6.50% hurdle by +1 basis point),
> - **Annualized Volatility:** **9.44%** (providing a **102 bps volatility reduction** relative to the 10.46% risk of the 60/40 policy benchmark),
> - **Reserve-Eligible Buffer:** **20.0%** (comfortably exceeding the non-negotiable 3.0% reserve floor by +17.0 percentage points).

### Committee Reversal Conditions (When to ADOPT)
The Investment Committee should reverse this recommendation to **ADOPT** if and only if three governance conditions are formally enacted:
1. **Codify an Explicit Strategic Equity Policy Band:** Adopt an enforceable **40%–65% policy range** around the 55% central equity target, legally prohibiting the optimizer from concentrating up to 70%–80% in equities during yield compression or cost drag.
2. **Approve Bayesian / Black-Litterman Shrinkage Priors:** Mandate return shrinkage priors that guarantee the largest single-asset weight shift stays **under 10.0 percentage points ($10.0M)** across a 50 bps annual cost drag or a 100 bps equity expected return shock.
3. **Quantify Statement S9 Drawdown Limits:** Formally define the Chief Investment Officer's calendar-year loss aspiration into an actionable ex-ante risk budget (e.g. 1-year 95% Conditional Value-at-Risk $\le 10.0\%$) with codified stop-loss and rebalancing breach protocols.

---

## 2. Decision Allocation Range vs. False Point Precision

Rather than presenting false point precision, we recommend implementing the portfolio within structured institutional allocation bands:

| Asset Sleeve | Target Baseline Weight | Recommended Policy Band | Target Capital ($100M Reserve) | Capital Band ($100M Reserve) | Role in Meridian Mandate |
|---|:---:|:---:|:---:|:---:|---|
| **Treasury Bills (`BIL`)** | **0.0%** | **0.0% – 5.0%** | $0.0M | $0.0M – $5.0M | Frictional cash cushion & tactical emergency buffer |
| **10-Year Treasuries (`IEF`)** | **20.0%** | **10.0% – 25.0%** | $20.0M | $10.0M – $25.0M | Duration hedge, term premium, Rule S3 reserve compliance |
| **IG Corporate Bonds (`LQD`)** | **25.0%** | **15.0% – 30.0%** | $25.0M | $15.0M – $30.0M | Credit spread yield enhancement; non-reserve asset |
| **Global Equities (`VT`)** | **55.0%** | **50.0% – 65.0%** | $55.0M | $50.0M – $65.0M | Primary growth engine to satisfy CPI + 4.0% real return |
| **Total Portfolio** | **100.0%** | **100.0%** | **$100.0M** | **$100.0M** | **Full Mandate Compliance** |

---

## 3. Mandate Rules & Candidate Portfolio Audit (`mandate.py`)

For the **$100M Meridian Foundation Reserve** with quarterly distributions of **$0.75M** covering **4 quarters** (12 months of grantmaking payouts):

### Mathematical Formulation of Mandate Rules:
1. **Rule S2 (Return Objective):** $E[R_p] = \sum_{i} w_i \mu_i \ge 6.50\%$ (CPI estimated at 2.50% + 4.00% net real return).
2. **Rule S3 (Derived Reserve Minimum):** $\text{Reserve Floor} = \frac{4 \times \$0.75\text{M}}{\$100.0\text{M}} = \mathbf{3.0\%}$ in reserve-eligible liquid assets (`Cash`, `Treasury bills`, `Treasury 10-year notes`).
3. **Rule S5 (Long-Only Constraint):** $w_i \ge 0 \quad \forall i, \quad \sum_{i} w_i = 1.0$; zero leverage, borrowing, or derivative contracts.
4. **Rule S6 (Single-Issuer Concentration Cap):** $\sum_{k \in \text{Issuer } j} w_k \le 8.0\%$ for any non-exempt corporate entity (e.g. Acme Corp equity + debt). Cash, Treasuries, and registered diversified funds are legally exempt.
5. **Rule S7 (Turnover Ceiling):** Annual portfolio turnover $\le 25.0\%$ without prior Investment Committee authorization.
6. **Rule S8 (Secondary Liquidity Threshold):** At least **90.0%** of the portfolio must be redeemable at NAV within **5 business days**.
7. **Rule S9 (Calendar-Year Loss Limit):** Ex-post market outcome ("cannot have a calendar-year loss greater than 10%"); **requires CIO clarification** before it can be modeled ex-ante.

### Audit of Candidate Portfolios:
Every candidate portfolio evaluated under our mandate compliance engine (`mandate.py`) produces the following deterministic compliance verdict:

| Candidate Portfolio | Reserve % ($\ge 3.0\%$) | 5-Day Liquidity ($\ge 90.0\%$) | Max Issuer % ($\le 8.0\%$) | Compliance Verdict | Failure Diagnostics / Notes |
|---|:---:|:---:|:---:|:---:|---|
| **Candidate A** | **14.0%** (PASS) | **100.0%** (PASS) | **0.0%** (PASS) | **PASS** | Passes 100% of checkable mandate rules. |
| **Candidate B** | 1.0% (FAIL) | 85.0% (FAIL) | 9.0% (FAIL) | **FAIL (3 Rules)** | Fails S3 (1% < 3%); fails S8 (15% Private Real Estate has 90d lockup); fails S6 (Acme Corp 5% bond + 4% stock = 9%). |
| **Candidate C** | 2.0% (FAIL) | 100.0% (PASS) | 8.0% (PASS) | **FAIL (1 Rule)** | Fails S3 reserve floor (1% Cash + 1% Bills = 2.0% < 3.0%). |
| **Candidate D (Attack Portfolio)** | 3.0% (PASS) | 100.0% (PASS) | 0.0% (PASS) | **PASS (Static)** | Statically passes, but substantively unacceptable (97% equities, 0% bonds; extreme benchmark tracking error). |
| **Candidate E (60/40 Benchmark)** | **0.0%** (FAIL) | 100.0% (PASS) | 0.0% (PASS) | **FAIL (1 Rule)** | **The client's own policy benchmark violates Rule S3** (0.0% reserve-eligible paper < 3.0% required minimum). |

---

## 4. Two Transparent Baselines vs. Constrained Portfolio

To evaluate the mathematical value added by mandate-constrained optimization, we compare two canonical transparent baselines directly against our portfolio:

| Portfolio Specification | Mix (Bills / 10-Yr / IG / Equity) | Expected Return | Annualized Volatility | Reserve Weight | Meets 6.50% Hurdle? | Meets 3.0% Reserve? | Mandate Verdict & Ruling Rule |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Baseline 1: Equal Weight** | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No (5.20%) | Yes (50.0%) | **FAIL MANDATE** (Violates Rule S2: return is 130 bps below 6.50% hurdle) |
| **Baseline 2: 60/40 Policy Benchmark (Cand. E)** | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes (6.80%) | No (0.0%) | **FAIL MANDATE** (Violates Rule S3: reserve 0.0% is below 3.0% floor) |
| **Alternative Baseline: Inverse Volatility** | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No (3.77%) | Yes (90.3%) | **FAIL MANDATE** (Violates Rule S2: return is 273 bps below 6.50% hurdle) |
| **Meridian Lowest-Risk Feasible Portfolio** | **0.0 / 20.0 / 25.0 / 55.0** | **6.51%** | **9.44%** | **20.0%** | **Yes (6.51%)** | **Yes (20.0%)** | **PASSES EVERY CHECKABLE RULE** (102 bps lower risk than 60/40) |

### Key Analytical Takeaways:
1. **Equal Weight is Unusable:** While naive 1/N allocation provides attractive diversification and high reserve liquidity (50.0%), its 5.20% expected return severely impairs the foundation's real purchasing power, failing the CPI + 4% mandate by 130 bps.
2. **The Benchmark is Legally Inadmissible:** The CIO's 60/40 reference benchmark (Candidate E) holds 40% in diversified investment-grade corporate bonds and 60% in global equities. Because corporate bonds are subject to credit spreads and secondary liquidity friction, they are not reserve-eligible under Rule S3. Thus, **the client cannot adopt its own policy benchmark without violating its trust agreement**.
3. **The Constrained Portfolio Dominates:** By allocating 20% to 10-Year Treasuries and 25% to IG corporate bonds, the constrained portfolio satisfies the 3.0% reserve rule with a massive 17.0-point safety margin, achieves the 6.50% return target, and reduces portfolio volatility from 10.46% to 9.44% (-102 bps).

---

## 5. Point-in-Time Signal & Formal Data Card (`BAA10Y`)

To prevent look-ahead bias and backtest contamination, our application incorporates an empirical point-in-time signal derived from St. Louis Fed FRED and ALFRED vintage database audits:

### Formal Point-in-Time Data Card
```yaml
Data Card: Moody's Seasoned Baa Corporate Bond Yield Spread over 10-Year Treasury
Series ID: BAA10Y
Provider: Federal Reserve Bank of St. Louis (FRED) & Moody's Investors Service
Economic Concept: Investment-grade credit risk premium and corporate default spread
Role in Strategy: Regime filter governing active allocation between corporate credit (LQD) and Treasuries (IEF)
Units: Percent (e.g. 1.45% represents 145 basis points)
Frequency: Daily (business days; market holidays excluded)
Publication Schedule: Daily at 4:15 PM Eastern Time following secondary market close
Observed Publication Lag: 1 business day (execution lag between observation date and morning availability)
Historical Revisions: 0 historical revisions (audited across 10+ years in ALFRED vintage database)
Point-in-Time Admission Rule: ADMIT WITH STRICT 1-DAY AS-OF LAG (Signal_T = f(BAA10Y_{t <= T-1}))
Hand-Checked Calibration Points:
  - 2026-10-26: 1.45%
  - 2026-09-30: 1.47%
  - 2024-01-02: 1.62%
Revocation Trigger: Quarantine immediately if provider alters calculation to include modeled/survey estimates
```

### Contrast with Macroeconomic Survey Data:
In our point-in-time provenance audit, macroeconomic surveyed series such as Nonfarm Payrolls (`PAYEMS`) revealed **381 historical monthly revisions**, with numbers being rewritten by over 1.2 million jobs years after initial publication. Trading on modern flattened downloads of `PAYEMS` introduces fatal look-ahead bias. In contrast, `BAA10Y` is derived from finalized secondary market-clearing trades and has **zero revisions**. With an explicit 1-business-day as-of lag, `BAA10Y` is point-in-time safe.

### Credit Regime Gating Protocol:
- **Normal Regime ($BAA10Y \le 2.00\%$):** Corporate credit markets functioning normally. IG sleeve maintained at baseline 25.0%.
- **Caution Regime ($2.00\% < BAA10Y \le 2.50\%$):** Credit spreads widening. Bar any discretionary allocation increases to corporate bonds.
- **Distress Regime ($BAA10Y > 2.50\%$):** Systemic credit dislocation. Halts automated rebalancing, triggers the **Process Stop Condition**, and reallocates up to 10% from corporate bonds into 10-Year Treasuries.

---

## 6. Stress Testing Suite & The Process Stop Condition

Unconstrained mean-variance optimization is famously sensitive to minor estimate errors ("error maximization"). We subjected the Meridian universe to four multi-dimensional stress runs:

| Scenario Description | Sleeve Expected Returns (B / 10Y / IG / Eq) | Optimal Mix (B / 10Y / IG / Eq) | Net Return | Annual Volatility | Reserve Buffer | Largest Shift ($\Delta w_{\max}$) | Impact on Investment Decision |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Baseline (As Loaded)** | `[3.5%, 4.3%, 5.0%, 8.0%]` | `0 / 20 / 25 / 55` | 6.51% | 9.44% | 20.0% | 0.0 pts | Frictionless baseline candidate |
| **Stress 1: Equity Return Shock (-100 bps)** | `[3.5%, 4.3%, 5.0%, 7.0%]` | `0 / 10 / 10 / 80` | 6.53% | 12.94% | 10.0% | **25.0 pts** (Equity) | **Reinforces PILOT:** Vol spikes +350 bps; $25M forced into equities to reach 6.50% |
| **Stress 2: IG–Equity Corr Shock (0.25 -> 0.50)** | `[3.5%, 4.3%, 5.0%, 8.0%]` | `0 / 40 / 0 / 60` | 6.52% | 9.73% | 40.0% | **25.0 pts** (IG dumped) | **Reinforces PILOT:** Corporate credit dumped from 25% to 0%; $25M rotated to 10-Yr |
| **Changed-Input Stress Run: Cost Drag (+50 bps)** | `[3.0%, 3.8%, 4.5%, 7.5%]` | `0 / 10 / 20 / 70` | 6.53% | **11.57%** | 10.0% | **15.0 pts** (Equity) | **Survives & Reinforces PILOT:** Vol spikes +213 bps, making portfolio riskier than 60/40 benchmark |

### Window Sensitivity: Full History vs. Trailing 36 Months (`prices.csv`)
Using our empirical ETF price history (`BIL`, `IEF`, `LQD`, `VT` from 2021-11-01 to 2026-10-01):
- **Full 59-Month Sample:** Optimal mix is `60.0% BIL / 0.0% IEF / 0.0% LQD / 40.0% VT` (Return: 6.85%, Vol: 6.01%, Reserve: 60.0%).
- **Trailing 36-Month Sample:** Optimal mix is `85.0% BIL / 0.0% IEF / 0.0% LQD / 15.0% VT` (Return: 6.83%, Vol: 1.77%, Reserve: 85.0%).
- **Window Sensitivity:** Triggers a **25.0 percentage point capital shift ($25.0M)** into T-bills. Because trailing 3-year `VT` realized an extraordinary 21.21% annualized return, the optimizer slashes equity to 15% and hides in cash. This is a trailing bull-market distortion, not an ex-ante forecast, proving why unanchored rolling windows must be rejected.

### The Process Stop Condition (Kill Switch Protocol)
The automated optimization process immediately **STOPS** (refuses to execute rebalancing orders, logs a critical risk breach, and escalates to the Investment Committee) if any of the following triggers occur:
1. **Infeasibility:** No discrete 5-point asset allocation meets both the return objective ($E[R_p] \ge 6.50\%$) and the reserve floor ($\ge 3.0\%$).
2. **Excessive Estimation Instability:** Any 50 bps cost revision or 100 bps return revision causes a maximum single-asset weight shift $\Delta w_{\max} > 10.0$ percentage points ($10.0M reallocation).
3. **Policy Band Breach:** Optimal equity allocation breaches the recommended 40%–65% strategic equity policy band (e.g. forced to 70% or 80% under stress).
4. **Credit Spread Distress Trigger:** Point-in-time `BAA10Y` credit spread widens beyond 250 bps ($2.50\%$), indicating systemic credit market dislocation.
5. **Drawdown Breach Condition:** Expected 1-year 95% CVaR / VaR exceeds the CIO's unquantified Statement S9 calendar-year limit.

---

## 7. Summary of Locked Changed-Input Record

Per formal changed-input governance procedures, our human-authored prediction was locked and committed to GitHub prior to execution. Below is the verified before/after reconciliation:

- **Load-Bearing Input:** Annualized implementation and advisory cost drag (+50 bps/yr, from 0.00% to 0.50%).
- **Pre-Run Prediction:** Subtracting 50 bps from every sleeve will drop the baseline portfolio return from 6.51% to 6.01%, failing the 6.50% objective. To recover this shortfall, the optimizer will shift capital aggressively into equities (moving from 55% to 65%–75%), deplete reserve-eligible fixed income, and spike portfolio volatility above the 10.46% benchmark level. The recommendation (`PILOT, DO NOT ADOPT`) will survive and be strengthened.
- **Executed Output:**
  - Optimal Mix shifted from `0 / 20 / 25 / 55` to `0 / 10 / 20 / 70` (Equity surged **+15.0 pts**, 10-Yr cut **-10.0 pts**, IG cut **-5.0 pts**).
  - Portfolio Volatility jumped from **9.44% to 11.57% (+213 bps)**.
  - Net Expected Return: **6.53%**; Reserve Buffer cut from **20.0% to 10.0%**.
- **Reconciliation & Diagnosis:** The prediction matched empirical execution. The baseline's 102 bps volatility advantage over the 60/40 benchmark was completely wiped out, turning into a **111 bps risk disadvantage** (11.57% vs 10.46%). This failure mode proves why raw mean-variance optimization cannot be adopted without strategic policy bands and shrinkage priors.

*(For full pre-run prediction text, commit hashes, and detailed step-by-step audit logs, see [`docs/validation-and-ai-use.md`](validation-and-ai-use.md).)*

---

## 8. Operational Monitoring Triggers & Committee Action Requested

### Standing Operational Monitoring Triggers:
1. **Quarterly Policy Band Drift Check:** If normal market price drift moves any sleeve weight by $\ge \pm 5.0$ percentage points from its target baseline (e.g. Equities $> 60\%$ or $< 50\%$), execute calendar rebalancing to reset to baseline.
2. **Point-in-Time Credit Spread Trigger:** Monitor daily `BAA10Y` with a 1-day as-of lag. If spread crosses 200 bps, halt corporate credit additions; if spread crosses 250 bps, trigger the Process Stop Condition and shift up to 10% into 10-Year Treasuries.
3. **Inflation & Real Return Trigger:** If 5-year rolling breakeven inflation expectation rises above 3.50% (pushing the CPI + 4% hurdle above 7.50%), trigger formal asset-liability modeling review.
4. **Implementation Friction Drag:** Monitor realized turnover and execution slippage. If annualized cost drag exceeds 40 bps, re-evaluate trading venues.
5. **Secondary Liquidity Cushion:** Ensure that at all times, liquid government securities and cash exceed $3.0M (Rule S3) and 5-day redeemable assets exceed 90.0% (Rule S8).

### Action Requested from the Investment Committee:
1. **Approve a $10.0M (10.0%) Allocation to the Meridian Lowest-Risk Pilot Portfolio** for an initial 12-month evaluation period.
2. **Retain the remaining $90.0M Reserve Balance in Canonical Core Allocations** (Cash/Treasuries and broad benchmark sleeves).
3. **Adopt Formal Governance Amendments** codifying:
   - A strategic equity policy band of **40.0% to 65.0%**,
   - Bayesian / Black-Litterman return shrinkage priors for future automated rebalancing models, and
   - A quantifiable definition and breach rule for Statement S9 calendar-year drawdown limits.
