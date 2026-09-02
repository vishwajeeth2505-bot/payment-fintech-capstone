# Paytm FinTech Analytics & AI Platform — Capstone

 This repository is the executive capstone submission for FinTech + AI: a single connected platform for Paytm spanning payments/fraud analytics, credit-risk ML, and AI-augmented advisory + blockchain risk. All monetary figures are in INR. Total: 100 marks across 3 parts.

 Repository Structure

 paytm-capstone/
 ├── payments_fraud_analytics/   (Part 1 — 35 marks)
 ├── credit_risk_lending_ml/     (Part 2 — 40 marks)
 ├── ai_advisory_blockchain/     (Part 3 — 25 marks)
 └── README.md                   (this file)

 Setup

 Each part folder is self-contained. Parts 1 & 2 need pandas, numpy, scikit-learn, matplotlib. Part 3 uses the Python standard library only — no external dependencies.
 pip install pandas numpy scikit-learn matplotlib

# Part 1 — Payments & Fraud Analytics (/payments_fraud_analytics, 35 marks)

 How to run (from the folder):

 python3 generate_data.py   # creates merchants.csv,   users.csv, ledger.csv, gateway_export.csv
 python3 build_db.py        # builds paytm_payments.db
 python3 queries.py         # SQL fraud detection
 python3 reconcile.py       # Part C reconciliation
 python3 dashboard.py       # Part D dashboard images

 Design decisions: Synthetic dataset of 547 transactions (seed 42). Fraud-flag logic uses a nested IF/AND rule — “High-Value Merchant Day” = merchant’s daily total > ₹5,000 AND region is not East. Full detail in payments_fraud_analytics/README.md.

# Part 2 — Credit Risk & Lending ML (/credit_risk_lending_ml, 40 marks)

 How to run (from the folder):
 python3 generate_data.py
 python3 eda.py
 python3 preprocessing.py
 python3 anomaly_detection.py

 Design decisions: 400 applicants (seed 42), 20.25% default rate, 20% missing credit_bureau_score (imputed with training median, 612.00). 300/100 stratified train/test split. Logistic Regression outperformed Decision Tree (ROC-AUC 0.7188 vs 0.5312) and was selected for the risk-pricing table. Isolation Forest caught 11 of 15 seeded transaction anomalies. Full detail, including the bias note, in credit_risk_lending_ml/README.md.

# Part 3 — AI-Augmented FinTech Advisory & Blockchain Risk (/ai_advisory_blockchain, 25 marks)

 No external packages required — Python 3 standard library only (os, math, re).

 LLM mode: All required outputs and recorded transcripts for this part were generated with MOCK_LLM left at its default (unset, i.e. MOCK_LLM=1) — the fully deterministic, rule-based mock path. No LLM API key, signup, or network call was used anywhere in this part. The optional MOCK_LLM=0 extension (Groq free tier) was not attempted.

 How to run (from the folder):
 python3 advisory_agent.py        # Part A — portfolio advisory agent, all 5 investor profiles
 python3 extract_disclosure.py    # Part B — disclosure signal extraction, all 6 snippets
 python3 debate.py                # Part C — bull/bear/synthesizer debate demo
 python3 dcf_calculator.py        # Part D — DCF valuation + 3x3 sensitivity table



	•	Part A: CAPM expected return computed strictly from beta (never analyst_expected_return); portfolio variance uses the prescribed ρ=0.3 pairwise correlation; escalation triggers on a hard >20% std-dev threshold. Aggressive-tier portfolios (INV03, INV05) correctly escalate at ~20.58% std dev.
	•	Part B: risk-flag and sentiment classification use keyword/regex rules only — no LLM call in the graded path.
	•	Part C: each agent’s argument is built from an f-string template referencing the chosen ticker’s actual beta/return/std-dev numbers.
	•	Part D: WACC (11.32–12.32%) and terminal growth (4.32–6.32%) are set ≥3pp apart so WACC exceeds terminal growth in all 9 sensitivity-grid cells. DCF (INR 1,401,488,810) cross-checked against an EV/EBITDA multiple estimate (INR 864,000,000), a +62.2% difference, noted in writing.
	•	Part E: blockchain_risk_note.md covers stablecoin type/DAO governance risk, a justified 2% max crypto-allocation recommendation, and a T.A.N.G. fraud-framework analysis (Authority + Greed) with named bank-side defenses.