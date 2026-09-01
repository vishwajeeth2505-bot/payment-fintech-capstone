# Credit Risk & Lending ML — Part 2

## Task 1–2: EDA & Preprocessing
•⁠  ⁠Measured default rate: 20.25%
•⁠  ⁠Missing credit_bureau_score: 20.00% (80 of 400 rows)
•⁠  ⁠Thin-file flag: 320 not thin-file, 80 thin-file
•⁠  ⁠Train/test split: 300 / 100, stratified on default, random_state=42
•⁠  ⁠Training median bureau score used for imputation: 612.00

## Task 3–4: Classification Models

| Metric | Logistic Regression | Decision Tree |
|---|---|---|
| Confusion Matrix | [[69, 11], [13, 7]] | [[61, 19], [14, 6]] |
| Accuracy | 0.7600 | 0.6700 |
| Precision | 0.3889 | 0.2400 |
| Recall | 0.3500 | 0.3000 |
| F1 | 0.3684 | 0.2667 |
| ROC-AUC | 0.7188 | 0.5312 |

## Task 5: Risk-Based Pricing Table

| Risk Tier | N | Actual Default Rate | Illustrative Rate |
|---|---|---|---|
| Low | 25 | 8% | 8–10% |
| Medium-Low | 25 | 12% | 11–14% |
| Medium-High | 25 | 20% | 15–19% |
| High | 25 | 40% | 20–25% |

## Task 6: Isolation Forest Anomaly Detection
•⁠  ⁠Contamination rate: 0.0566 (15/265)
•⁠  ⁠Total flagged: 15
•⁠  ⁠Seeded anomalies caught: 11 / 15
•⁠  ⁠Recall: 0.7333

## Task 8: Bias-Awareness Note
•  Even though this dataset has no explicit gender or location field,employment_type could still acts as a hidden proxy for a protected attribute in a real deployment. The dataset splits applicants into salaried,self-employed,and gig workers.In india,gig work and self-employment are not evenly distributed across all groups access to salaried corporate jobs is often shaped by factors like gender,region,educational background,meaning gig or self-employed workers may disproportionately come from specific communities. If the model learns that gig workers default more often and prices them worse as a result, it isn’t directly discriminating on gender or background — but because employment type correlates with those attributes, the model ends up indirectly penalizing certain groups without ever “seeing” who they are. This is the core risk of a proxy variable: a field that looks neutral on its face but quietly encodes something the model was never supposed to use.Before this model goes live, I would recommend two governance steps. First, a maker-checker human review for any declined application from a thin-file applicant (someone with no credit_bureau_score) — since these applicants have the least data behind their score, they’re the most likely to be unfairly rejected based on indirect signals like employment type or income, rather than genuine creditworthiness. Second, a regular audit of approval rates broken down by employment_type, comparing default-adjusted approval rates across salaried, self-employed, and gig applicants. If gig or self-employed applicants are being declined at meaningfully higher rates even after accounting for their actual default risk, that’s a signal the model has learned a biased pattern and needs to be retrained or have that feature reweighted.

## Task 9: Final Comparison & Recommendation
•⁠ Based on the results, I would deploy the Logistic Regression model for Paytm Postpaid. It outperformed the Decision Tree on every metric: accuracy of 0.7600 vs 0.6700, precision of 0.3889 vs 0.2400, recall of 0.3500 vs 0.3000, and — most importantly — an ROC-AUC of 0.7188 vs 0.5312. ROC-AUC matters most here because it measures how well the model ranks risky applicants above safe ones across all thresholds, which is exactly what’s needed to build the risk-based pricing tiers; the Decision Tree’s 0.5312 is barely better than random guessing, likely because it overfit on this relatively small 300-row training set. The Isolation Forest anomaly detector caught 11 of the 15 seeded anomalies (73.3% recall), which is a solid but not perfect result — it’s a useful first-pass fraud signal, but flagged transactions should still route to manual review rather than automatic blocking, since roughly 1 in 4 real anomalies would slip through.