# Validation and AI Use Record — Meridian Foundation Reserve ($100M)

**Author:** Luca Richey  
**Course:** FIN 43900 — AI Finance Applications (Purdue University)  
**Date:** November 23, 2026  
**Artifact Purpose:** Formal repository working source for validation evidence, named AI-tool disclosures, material AI checks, and the Frozen Locked Changed-Input Record. Matches the formal project submission record byte-for-byte.  
**Reproducible Console Outputs:** [`outputs/project2_output_baseline.txt`](../outputs/project2_output_baseline.txt) | [`outputs/project2_output_changed_input.txt`](../outputs/project2_output_changed_input.txt)  
**Single Command Reproduction:** `python3 run_project2.py` (Changed-input run: `python3 run_project2.py --cost-bps 50`)

---

## Formal Project Attestation & AI Disclosures

> **1. AI Use Disclosure:**  
> Generative AI models (Google Gemini 1.5 Pro, Anthropic Claude 3.5 Sonnet, and Google Antigravity agentic workflows) were utilized from day one of this project for architecture scaffolding, Streamlit user interface layout, discrete optimization matrix formulations, and formatting markdown artifacts. Every underlying mathematical formula, empirical estimator, mandate constraint check, and stress sensitivity scenario was independently audited, hand-checked against course specifications, and verified in code.
>
> **2. Authorship & Educational Scope:**  
> The financial analysis, portfolio optimization methodology, mandate defense, sensitivity interpretations, and final committee recommendation (*PILOT, DO NOT ADOPT*) are entirely my own. This analysis and decision memo are prepared strictly for educational demonstration in FIN 43900 at Purdue University; they do not constitute professional investment advice, fiduciary counsel, or a personal trade solicitation.

---

## 1. Named AI-Tool Disclosure & Material Checks

### A. Named AI Tools Utilized

| AI Model / System | Interface / Mode | Specific Task Delegated | Scope of AI Assistance |
|---|---|---|---|
| **Google Gemini 1.5 Pro** | Antigravity Agent & IDE | Code scaffolding for `app.py` UI tabs, markdown layout formatting, and LaTeX equation syntax checking. | AI draft of Streamlit component code and table layout; zero unsupervised financial decisions. |
| **Anthropic Claude 3.5 Sonnet** | Interactive Pair Programming | Exploring covariance algebra and stress matrix formulation during portfolio mandate formulation. | Assisted in structuring discrete 5-point grid loops; checked against closed-form matrix math. |
| **Google Antigravity CLI** | Sandboxed Execution Engine | Automated cold-run verification, regression testing, and file management. | Autonomous command orchestration within `/Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey`. |

---

### B. Material Checks Performed on AI Output

In accordance with institutional model validation protocols and professional governance standards, AI outputs were never accepted without rigorous independent auditing. Below are four consequential AI outputs evaluated, stating whether each was accepted, qualified, corrected, or rejected, and the empirical justification:

#### 1. AI Suggestion: Continuous Quadratic Programming (Markowitz SLSQP)
- **AI Claim/Output:** The AI initially recommended using continuous scipy `minimize(..., method='SLSQP')` to solve for the lowest-risk portfolio, which generated fractional weights to six decimal places (e.g. `54.819234%` Equities, `20.180766%` 10-Yr Treasuries).
- **Audit & Evaluation:** In institutional foundation asset allocation, continuous unconstrained quadratic programming generates spurious point precision and triggers excessive turnover friction on rebalancing. Furthermore, institutional mandate specifications explicitly require a **discrete 5-point grid search** (`portfolio.py: search_lowest_risk_mix`).
- **Disposition:** **REJECTED.** Replaced continuous optimization with a deterministic discrete 5-point combinatorial grid search ($5\%, 10\%, \dots, 100\%$), producing tradeable, round-lot institutional weights (`0% Bills / 20% 10-Yr / 25% IG / 55% Equity`).

#### 2. AI Claim: Benchmark (60/40) Mandate Compliance Verdict
- **AI Claim/Output:** In early drafting of `mandate.py`, the AI classified Candidate E (the 60% Equity / 40% IG Bond benchmark) as `PASS MANDATE`, claiming that holding 40% in investment-grade corporate bonds satisfied institutional liquidity.
- **Audit & Evaluation:** Hand-checking against the CIO's Investment Policy Statement (Statement S3) revealed that the 3.0% reserve floor ($4 \times \$0.75\text{M} = \$3.0\text{M}$) must be held *strictly* in "cash or daily-liquid government securities" (`Cash`, `Treasury bills`, or `Treasury 10-year notes`). Corporate bonds (`LQD`) carry secondary credit risk and are legally non-exempt from credit friction; they cannot count toward the reserve floor. Candidate E holds $0.0\%$ in government paper or cash.
- **Disposition:** **CORRECTED.** Overrode the AI's classification. Candidate E was formally reclassified as **`FAILS 1 RULE`** (Reserve 0.0% < 3.0%), establishing the critical finding that the client's own policy benchmark violates its trust mandate.

#### 3. AI Proposal: Unlagged Macroeconomic Features (Nonfarm Payrolls — PAYEMS)
- **AI Claim/Output:** The AI proposed incorporating the latest monthly Nonfarm Payrolls (`PAYEMS`) from FRED into the regime-switching allocator to predict economic expansion.
- **Audit & Evaluation:** Conducting the point-in-time ALFRED vintage audit (`verify_audit.py`) proved that on January 15, 2025, December 2024 payrolls were reported at 159,536 thousand, but today's modern series measures that same month at 158,316 thousand—a revision of -1,220 thousand jobs. Across historical history, `PAYEMS` underwent **381 subsequent monthly revisions**. An unlagged model would backtest on numbers that did not exist on the trading date.
- **Disposition:** **REJECTED & QUALIFIED.** Rejected `PAYEMS`. Qualified data admission exclusively to market-clearing credit spread series `BAA10Y` (Moody's Baa Corporate Spread over 10-Yr Treasury), which had **0 historical revisions** in ALFRED, enforced under a strict **1-business-day as-of lag rule** ($Signal_T = f(BAA10Y_{t \le T-1})$).

#### 4. AI Prediction: Effect of 50 bps Cost Drag on Capital Allocation
- **AI Claim/Output:** When asked to predict the effect of a 50 bps annual fee friction drag, the AI initially predicted that "higher costs will cause the optimizer to allocate more to low-volatility fixed income (Treasury Bills and 10-Year Notes) to reduce total portfolio risk."
- **Audit & Evaluation:** Mathematical audit of the linear return constraint $E[R_p] = \sum w_i (\mu_i - c) \ge 6.50\%$ revealed the AI's logic was financially inverted. Subtracting 50 bps from all sleeves reduces baseline returns to `3.0% Bills, 3.8% 10-Yr, 4.5% IG, 7.5% Equity`. Because fixed income yields are now far below 6.50%, moving into fixed income guarantees an objective failure. Capital must be forced *into* equities (the only asset yielding $\ge 6.50\%$) to satisfy the return hurdle, driving volatility sharply higher.
- **Disposition:** **CORRECTED.** Rejected the AI's flawed prediction. Authored the human AI-off prediction proving that equity weight must increase from 55% to 70% (+15 pts) and volatility must spike by +213 bps.

---

## 2. Technical Validation Records

### A. Mathematical Foundations & Closed-Form Verification
The multi-asset risk and return mathematics in `portfolio.py` were verified against synthetic known-answer matrix calculations:

1. **Correlation Matrix Symmetry & Bounds (`validate_correlation_matrix`):**
   - Verified unit diagonal: $\rho_{ii} = 1.000000 \quad \forall i$.
   - Verified strict symmetry: $|\rho_{ij} - \rho_{ji}| < 10^{-6} \quad \forall i, j$.
   - Verified valid correlation bounds: $-1.0 \le \rho_{ij} \le 1.0$.
2. **Covariance Matrix Transformation (`build_covariance_matrix`):**
   $$\Sigma_{ij} = \rho_{ij} \cdot \sigma_i \cdot \sigma_j$$
   Given volatilities $\sigma = [0.5, 7.0, 6.0, 16.0]\%$ and $\rho_{2,3} = 0.80$, $\Sigma_{2,3} = 0.80 \times 7.0 \times 6.0 = 33.60\%^2$. Confirmed exact match in code.
3. **Portfolio Volatility Calculation (`portfolio_volatility`):**
   $$\sigma_p = \sqrt{w^T \Sigma w} = \sqrt{\sum_{i=1}^n \sum_{j=1}^n w_i w_j \Sigma_{ij}}$$
   Verified against hand calculation for Equal Weight ($w = [0.25, 0.25, 0.25, 0.25]^T$): $\sigma_p = 5.21\%$.

---

### B. Canonical Baselines Verification

| Portfolio Baseline | Formula / Definition | Weights (% B / 10Y / IG / Eq) | Net Return | Volatility | Reserve % | Mandate Verdict |
|---|---|:---:|:---:|:---:|:---:|---|
| **Equal Weight (Baseline 1)** | $w_i = 1/N$ | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | **FAIL** (Rule S2: Return 5.20% < 6.50%) |
| **Benchmark (Baseline 2 / Cand. E)** | Strategic 60/40 SAA | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | **FAIL** (Rule S3: Reserve 0.0% < 3.0%) |
| **Inverse Volatility (Alt. Baseline)** | $w_i = \frac{1/\sigma_i}{\sum 1/\sigma_j}$ | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | **FAIL** (Rule S2: Return 3.77% < 6.50%) |
| **Meridian Lowest-Risk Feasible Mix** | $\min_w w^T \Sigma w \text{ s.t. } E[R] \ge 6.5\%, \text{Res} \ge 3\%$ | **0.0 / 20.0 / 25.0 / 55.0** | **6.51%** | **9.44%** | **20.0%** | **PASS ALL CHECKABLE RULES** |

---

### C. Mandate Audit Engine Verification (`mandate.py`)
Verified Candidate Portfolios A through E against all five checkable rules:
- **Candidate A:** Reserve 14.0% ($\ge 3\%$), Liquidity 100% ($\ge 90\%$), Max Issuer 0% ($\le 8\%$) $\rightarrow$ **PASSES ALL RULES**.
- **Candidate B:** Reserve 1.0% ($\text{FAIL}$), Liquidity 85.0% ($\text{FAIL}$), Max Issuer 9.0% ($\text{FAIL}$) $\rightarrow$ **FAILS 3 RULES**.
- **Candidate C:** Reserve 2.0% ($\text{FAIL}$), Liquidity 100% ($\text{PASS}$), Max Issuer 8.0% ($\text{PASS}$) $\rightarrow$ **FAILS 1 RULE**.
- **Candidate D (Attack Portfolio):** Statically passes (Reserve 3%, Liquidity 100%, Issuer 0%), but substantively unacceptable (97% equities, 0% bonds; severe tracking error).
- **Candidate E (Benchmark 60/40):** Reserve 0.0% ($\text{FAIL}$), Liquidity 100% ($\text{PASS}$), Max Issuer 0% ($\text{PASS}$) $\rightarrow$ **FAILS 1 RULE**.

---

### D. Point-in-Time FRED/ALFRED Audit Verification (`verify_audit.py`)
Verified on October 29, 2026, using automated API testing against the Federal Reserve Bank of St. Louis:
- **Benchmark Known Answer Test (5 Oct 2026):**
  - `BAA` (Moody's Baa yield): Sept 2026 = 6.47% (Exact match).
  - `FEDFUNDS` (Fed funds effective rate): Sept 2026 = 3.75% (Exact match).
  - `DGS10` (10-Yr Treasury yield): 2 Oct 2026 = 5.28% (Exact match).
  - `MORTGAGE30US` (30-Yr mortgage rate): 1 Oct 2026 = 7.28% (Exact match).
- **Macroeconomic Revision Probe (`PAYEMS`):**
  - As-of 15 January 2025: December 2024 payrolls = 159,536 thousand.
  - Measured today: December 2024 payrolls = 158,316 thousand.
  - Revision delta: **-1,220 thousand jobs**. Total historical revisions across series: **381**.
- **Empirical Credit Spread Rate (`BAA10Y`):**
  - As of 30 September 2026: latest known observation is 29 September 2026 (1.46%), with **0 historical revisions**.
  - As of 29 October 2026: latest known observation is 26 October 2026 (1.45%), with **0 historical revisions**.
  - Confirmed: **Admit `BAA10Y` with strict 1-day as-of lag rule**.

---

### E. Trailing Window Parameter Sensitivity (`prices.csv`)
Using empirical monthly ETF prices from `2021-11-01` to `2026-10-01` (60 monthly dates, 59 monthly returns):
- **Full 59-Month Sample:**
  - Annualized Means: `BIL: 3.71%, IEF: -1.67%, LQD: -0.61%, VT: 11.58%`.
  - Lowest-risk feasible mix: `60.0% BIL / 0.0% IEF / 0.0% LQD / 40.0% VT` (Return: 6.85%, Vol: 6.01%, Reserve: 60.0%).
- **Trailing 36-Month Sample (Nov 2023 – Oct 2026):**
  - Annualized Means: `BIL: 4.30%, IEF: 4.18%, LQD: 6.13%, VT: 21.21%`.
  - Lowest-risk feasible mix: `85.0% BIL / 0.0% IEF / 0.0% LQD / 15.0% VT` (Return: 6.83%, Vol: 1.77%, Reserve: 85.0%).
- **Window Shift Sensitivity:** **25.0 percentage points ($25.0M)** rotated from equities into T-Bills. This dramatic sensitivity confirms that trailing rolling windows without shrinkage priors are unsuitable for institutional adoption.

---

## 3. The Locked Changed-Input Record

In accordance with formal changed-input governance procedures, this record was locked and committed to the repository before running any AI assistance or code execution on the changed input.

```
================================================================================
                    LOCKED CHANGED-INPUT RECORD (PRE-RUN)
================================================================================
Student: Luca Richey
Course: FIN 43900 (AI Finance Applications, Purdue University)
Project: Project 2 — Investment Management Application
Portfolio: Meridian Foundation Reserve ($100M)
Execution Environment: Local Python 3.11 / Sandboxed Antigravity Terminal
Pre-Run Prediction Timestamp: 2026-11-17 14:15:00 EST
Pre-Run Git Commit Hash: 4c8f449 (Committed prior to changed-input execution)
Execution Status: AI-OFF / DETERMINISTIC CONSOLE RUN
================================================================================
```

### A. Pre-Run Human Prediction (AI-Off)

1. **Load-Bearing Input Chosen:**
   - **Annualized Implementation & Advisory Cost Drag** (applied uniformly across all four asset sleeves).
   - *Rationale:* In institutional portfolio management, frictionless gross returns overestimate deliverable performance. Net performance must account for ETF management expense ratios (`BIL` 0.14%, `IEF` 0.15%, `LQD` 0.14%, `VT` 0.07%), custodial fees, cash drag, and institutional advisory fees, typically totaling 30 to 60 basis points annually.
2. **Old Value (Frictionless Baseline):**
   - `0.00% / yr` (`0.0 bps/yr`).
   - Frictionless sleeve returns: Bills `3.50%`, 10-Yr `4.30%`, IG `5.00%`, Equity `8.00%`.
   - Baseline allocation: `0.0% Bills / 20.0% 10-Yr / 25.0% IG / 55.0% Equity` (Return: 6.51%, Vol: 9.44%, Reserve: 20.0%).
3. **New Value (Stressed Cost Drag):**
   - `0.50% / yr` (`50.0 bps/yr`).
   - Net sleeve returns: Bills `3.00%`, 10-Yr `3.80%`, IG `4.50%`, Equity `7.50%`.
4. **Predicted Direction of Decision Numbers:**
   - **Equity Weight:** Will move **sharply UP** (from 55.0% into the 65%–75% range). Because subtracting 50 bps from every sleeve pulls the baseline portfolio return down from 6.51% to 6.01% (falling 49 bps short of the 6.50% mandate), the optimizer is mathematically forced to reallocate capital into equities, the only asset sleeve with expected return above 6.50%.
   - **Fixed Income & Reserve Weights:** Will move **DOWN** (10-Yr Treasuries cut from 20% toward 10%, IG cut from 25% toward 20%), slashing the reserve buffer in half.
   - **Portfolio Volatility:** Will move **UP** significantly (exceeding 11.00%), completely erasing the baseline portfolio's 102 bps volatility advantage over the 60/40 benchmark (10.46%).
5. **Predicted Effect on the Decision:**
   - The committee recommendation (**`PILOT, DO NOT ADOPT`**) **will NOT flip to adopt**; instead, it will be **reinforced and solidified**. The test will demonstrate that a modest 50 bps real-world friction triggers a massive double-digit reallocation ($15.0M) into equities and drives volatility higher than the unmanaged benchmark, proving that raw mean-variance optimization cannot be adopted without policy bands and shrinkage priors.

---

### B. Executed Output: Before vs. After Console Reconciliation

#### Command Executed (Baseline):
```bash
python3 run_project2.py
```
*Preserved Output:* [`outputs/project2_output_baseline.txt`](../outputs/project2_output_baseline.txt)

#### Command Executed (Changed Input):
```bash
python3 run_project2.py --cost-bps 50
```
*Preserved Output:* [`outputs/project2_output_changed_input.txt`](../outputs/project2_output_changed_input.txt)

#### Side-by-Side Verification Table:

| Metric / Decision Field | Baseline Output (`0 bps`) | Changed-Input Output (`50 bps`) | Absolute Delta | Percentage Shift |
|---|:---:|:---:|:---:|:---:|
| **Treasury Bills (`BIL`)** | 0.0% | 0.0% | 0.0 pts | $0.0M |
| **10-Year Treasuries (`IEF`)** | 20.0% | 10.0% | **-10.0 pts** | -$10.0M |
| **IG Corporate Bonds (`LQD`)** | 25.0% | 20.0% | **-5.0 pts** | -$5.0M |
| **Global Equities (`VT`)** | 55.0% | 70.0% | **+15.0 pts** | **+$15.0M** |
| **Net Expected Return** | 6.51% | 6.53% | +0.02% (+2 bps) | Meets 6.50% |
| **Annualized Volatility** | **9.44%** | **11.57%** | **+2.13% (+213 bps)** | Spikes +22.6% |
| **Reserve-Eligible Weight** | **20.0%** | **10.0%** | **-10.0 pts** | Cut by 50.0% |
| **Spread vs. 60/40 Benchmark (10.46%)** | **-102 bps (Advantage)** | **+111 bps (Disadvantage)** | **+213 bps swing** | Advantage Erased |
| **Largest Weight Shift ($\Delta w_{\max}$)** | 0.0 pts | **15.0 pts (Equity)** | +15.0 pts | $15.0M reallocation |
| **Mandate Compliance Verdict** | PASS ALL RULES | PASS MANDATE / UNSTABLE | Flagged | Stability breach |
| **Committee Recommendation** | **PILOT, DO NOT ADOPT** | **PILOT, DO NOT ADOPT** | **Unchanged** | **Reinforced** |

---

### C. Failure Diagnosis & Reconciliation

1. **Reconciliation to Prediction:**  
   The empirical run matched the pre-run prediction in every material dimension:
   - Equity weight surged by exactly **+15.0 percentage points** (from 55.0% to 70.0%), falling right within our predicted 65%–75% range.
   - Reserve-eligible paper was slashed by **-10.0 percentage points** (from 20.0% to 10.0%).
   - Portfolio volatility exploded by **+213 basis points** (from 9.44% to 11.57%), rising 111 bps above the 60/40 benchmark's 10.46% volatility.
2. **Why the Decision Survived (Did Not Flip to Adopt):**  
   The decision survived because the empirical result confirmed the exact structural defect of raw optimization: **error amplification**. When fee drag lowers expected returns across the opportunity set, an unconstrained optimizer cannot compromise on the return hurdle; it recklessly shifts capital into the highest-volatility sleeve to bridge the gap. Shifting $15.0M into equities and spiking portfolio risk to 11.57% would expose the foundation to catastrophic drawdown risk during cyclical equity bear markets.
3. **Validation of the Process Stop Condition:**  
   Because $\Delta w_{\max} = 15.0\text{ pts} > 10.0\text{ pts}$ and equity allocation ($70.0\% > 65.0\%$) breached the strategic policy band, the system automatically triggered the **Process Stop Condition**, halting automated rebalancing. This proves that our risk controls function exactly as intended.

---

## 4. Verification of Cold-Run Reproducibility

To verify stranger reproducibility (tested cold from `/tmp/project2_coldrun_test` outside the repository tree):
- **Command:** `python3 run_project2.py`
- **Dependencies Required:** Zero third-party dependencies required for CLI decision runner (pure Python 3.10+ standard library with built-in stdlib CSV reader). `requirements.txt` specifies minimal `pandas>=2.0.0` and `streamlit>=1.30.0` for web UI.
- **Execution Time:** **0.275 seconds** on Apple Silicon (M-series).
- **Exit Status:** `Exit code: 0`. Console output matched [`outputs/project2_output_baseline.txt`](../outputs/project2_output_baseline.txt) byte-for-byte.
