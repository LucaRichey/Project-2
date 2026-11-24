# Project 2 — 12-Row Submission Manifest & Evidence Index

**Course:** FIN 43900 — AI Finance Applications (Purdue University)  
**Student:** Luca Richey  
**Project:** Project 2 — Investment Management Application  
**Mandate:** Meridian Foundation Reserve ($100M Portfolio)  
**Date:** November 23, 2026  
**Status:** Complete & Decision-Ready  

---

## Formal Project Attestation & Disclosures

> **1. AI Use Disclosure:** Generative AI models (Google Gemini 1.5 Pro, Anthropic Claude 3.5 Sonnet, and Google Antigravity agentic workflows) were utilized from day one for architecture scaffolding, Streamlit user interface layout, discrete optimization matrix formulations, and formatting markdown artifacts. Every underlying mathematical formula, empirical estimator, mandate constraint check, and stress sensitivity scenario was independently audited, hand-checked against course specifications, and verified in code.
>
> **2. Authorship & Educational Scope:** The financial analysis, portfolio optimization methodology, mandate defense, sensitivity interpretations, and final committee recommendation (*PILOT, DO NOT ADOPT*) are entirely my own. This analysis and decision memo are prepared strictly for educational demonstration in FIN 43900 at Purdue University; they do not constitute professional investment advice, fiduciary counsel, or a personal trade solicitation.

---

## Uniform 12-Row Submission Manifest

| Row # | Manifest Item Name | Location / Evidence Pointer | Description / Verification Status | Audit Domain & Governance Scope |
|:---:|---|---|---|---|
| **1** | **Repository URL** | [GitHub Repository](https://github.com/lucarichey/FIN43900-Project2) | Clean, locally runnable codebase containing `run_project2.py`, `app.py`, `mandate.py`, `portfolio.py`, `prices.csv`, `asof.py`, and `requirements.txt`. | Technical Execution & System Reproducibility |
| **2** | **Research Evolution (Editions A & B)** | *Internal research tracking per project architecture* | Editions A and B are retained for internal research tracking per project architecture; Video 1 documents research evolution, thinking shifts, and checked AI outputs. Reference: [`docs/validation-and-ai-use.md`](https://github.com/lucarichey/FIN43900-Project2/blob/main/docs/validation-and-ai-use.md). | Research Methodology & Prior Evolution |
| **3** | **Decision Memo** | [`docs/decision-memo.md`](https://github.com/lucarichey/FIN43900-Project2/blob/main/docs/decision-memo.md) | Formal investment committee memo containing decision first (*PILOT, DO NOT ADOPT*), allocation range, mandate audit, two baselines vs constrained mix, BAA10Y data card, stress runs, stop condition, and monitoring triggers. | Financial Soundness & Committee Recommendation |
| **4** | **Validation and AI Use Record** | [`docs/validation-and-ai-use.md`](https://github.com/lucarichey/FIN43900-Project2/blob/main/docs/validation-and-ai-use.md) | Authoritative frozen validation record containing named AI tool disclosures, material AI checks, covariance math verification, mandate audit proofs, and the complete **Locked Changed-Input Record** (50 bps cost drag). | Quantitative Validation & AI Governance Audit |
| **5** | **Video 1 URL (YouTube)** | [Video 1: Research Evolution & AI Check](https://youtu.be/Ji0lqSjpR0g) | Unlisted YouTube link with captions enabled; covers how the system and student thinking changed, and the audit/correction of continuous SLSQP vs discrete grid search and unlagged PAYEMS vs BAA10Y. | Research Authorship & Empirical Evidence |
| **6** | **Video 1 Transcript** | [`docs/transcript-video-1.txt`](https://github.com/lucarichey/FIN43900-Project2/blob/main/docs/transcript-video-1.txt) | Corrected, word-for-word plain-text transcript of Video 1 including opening statements, section timestamps, and exact dialogue. | Verbatim Spoken Record & Transcript Audit |
| **7** | **Video 2 URL (YouTube)** | [Video 2: Codebase Walkthrough](https://youtu.be/bI1Jfo0gMn4) | Unlisted YouTube link with captions enabled; demonstrates repository architecture, mathematical functions, cold-run reproduction, live Locked Changed-Input test, and S9 drawdown limitation. | Codebase Architecture & Technical Ownership |
| **8** | **Video 2 Transcript** | [`docs/transcript-video-2.txt`](https://github.com/lucarichey/FIN43900-Project2/blob/main/docs/transcript-video-2.txt) | Corrected, word-for-word plain-text transcript of Video 2 including code pointers, terminal execution commands, and diagnostics. | Verbatim Spoken Record & Code Walkthrough |
| **9** | **Video 3 URL (YouTube)** | [Video 3: Committee Defense](https://youtu.be/jEmcOVmqI6c) | Unlisted YouTube link with captions enabled; opens with `app.py` running live on screen, leads with recommendation (*PILOT, DO NOT ADOPT*), defends allocation range, baselines, stress sensitivities, reversal conditions, and the ask. | Investment Defense & Live System Demonstration |
| **10** | **Video 3 Transcript** | [`docs/transcript-video-3.txt`](https://github.com/lucarichey/FIN43900-Project2/blob/main/docs/transcript-video-3.txt) | Corrected, word-for-word plain-text transcript of Video 3 including committee pitch, live app commentary, and reversal conditions. | Verbatim Spoken Record & Committee Pitch |
| **11** | **Evidence Index & Repository Access Confirmation** | [`Section 2: Evidence Index`](#2-timestamped-evidence-index--access-confirmation) | Comprehensive timestamped evidence index referencing exact moments in each video, file links, and instructional team private access confirmation. | Traceability & Repository Access Verification |
| **12** | **Optional Deployed-Output URL** | [Localhost Live Runner: `streamlit run app.py`](http://localhost:8501) | Fully interactive multi-tab Streamlit web application running locally via single terminal command or IDE runner; visible console captures in `outputs/`. | Interactive Execution & User Interface |

---

## 2. Timestamped Evidence Index & Access Confirmation

### A. Video Timestamp Index

#### Video 1: Research Evolution & AI-Output Audit (2:20)
- **`0:00 - 0:25`** — Formal Opening Attestations: AI tool disclosure (Gemini 1.5 Pro, Claude 3.5 Sonnet) & authorship/educational scope statement.
- **`0:25 - 1:05`** — System Evolution & Thinking Shift: Transition from naive Markowitz optimization to discovering Candidate E benchmark fails Rule S3 reserve floor, and identifying 50 bps cost drag instability.
- **`1:05 - 1:55`** — Consequential AI Output Audited & Checked: Detailed audit of AI continuous SLSQP optimization proposal producing fractional 6-decimal weights; rejected and corrected to discrete 5-point grid search (`portfolio.py`); audit of unlagged `PAYEMS` vs. 1-day lagged `BAA10Y`.
- **`1:55 - 2:20`** — Synthesis & Reversal Justification: Evidence justifying the final recommendation to **PILOT, DO NOT ADOPT**.

#### Video 2: Codebase Architecture & Technical Ownership (3:40)
- **`0:00 - 0:25`** — Formal Opening Attestations & Architecture Purpose.
- **`0:25 - 1:15`** — Repository Architecture & Data Flow: Review of `mandate.py`, `portfolio.py`, `run_project2.py`, `app.py`, and `prices.csv` with zero code duplication.
- **`1:15 - 2:00`** — Key Files & Financial Functions: Line-by-line explanation of `validate_correlation_matrix`, `build_covariance_matrix`, and `search_lowest_risk_mix`.
- **`2:00 - 3:00`** — Live Cold-Run & Locked Changed-Input Demonstration: Terminal execution of `python3 run_project2.py` (< 0.3s) and `python3 run_project2.py --cost-bps 50`, showing the +15.0 pt equity shift and +213 bps volatility spike.
- **`3:00 - 3:45`** — Failure Mode & Limitation Defense: Critical analysis of Statement S9 calendar-year drawdown limit, ex-post stochastic nature, and the active **Process Stop Condition**.

#### Video 3: Investment Committee Defense & Strategy Presentation (3:45)
- **`0:00 - 0:30`** — Live Application Opening & Formal Opening Statements: Live demonstration of `app.py` running in browser with mandatory project disclosures.
- **`0:30 - 1:15`** — Executive Decision Line: Recommendation to **PILOT, DO NOT ADOPT** with a $10M (10%) proof-of-concept pilot; baseline point: `0/20/25/55` (6.51% return, 9.44% vol, 20.0% reserve).
- **`1:15 - 2:00`** — The Two Baselines & Benchmark Failure: Why Equal Weight fails Rule S2 (5.20% return) and why the client's 60/40 benchmark fails Rule S3 (0.0% reserve).
- **`2:00 - 2:50`** — Stress Testing & Changed Input Defense: Demonstration of fee drag (+50 bps) and window sensitivity (36m trailing bull-market distortion), proving why raw optimization cannot be adopted.
- **`2:50 - 3:35`** — Reversal Conditions & Process Stop Condition: The three committee governance requirements (40%–65% equity band, shrinkage priors, quantified S9 rule) and active operational triggers.
- **`3:35 - 3:55`** — The Committee Ask: Specific formal approval requests for pilot allocation and governance codification.

---

### B. Instructional Team Repository Access Confirmation
- **Repository Access:** Confirmed configured for instructional team access (Purdue FIN 43900 instructional staff).
- **Branch:** `main`
- **Dependencies:** All dependencies documented in `requirements.txt` (`pandas>=2.0.0`, `numpy>=1.24.0`, `streamlit>=1.30.0`); core runner requires zero third-party packages (Python standard library only).
- **Security Check:** Zero credentials, passwords, private tokens, or proprietary API keys are committed anywhere in the repository.
