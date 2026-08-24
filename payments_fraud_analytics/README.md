# Payments & Fraud Analytics — Part 1

## Overview
This part builds a payments-and-fraud analytics workbench for a synthetic Paytm-style
dataset (547 transactions, seed 42), covering spreadsheet analysis, SQL fraud detection,
Python reconciliation, and a 4-layer visual dashboard.

## Setup
Run ⁠ python3 generate_data.py ⁠ first — creates merchants.csv, users.csv, ledger.csv,
and gateway_export.csv. Run ⁠ python3 build_db.py ⁠ to build paytm_payments.db.
Run ⁠ python3 queries.py ⁠ for SQL fraud detection. Run ⁠ python3 reconcile.py ⁠ for
Part C reconciliation. Run ⁠ python3 dashboard.py ⁠ for the Part D dashboard images.

## Design decisions
•⁠  ⁠Nested IF/AND rule: "High-Value Merchant Day" = merchant's daily total > ₹5,000
  AND region is not East (using the default rule stated in the brief).
•⁠  ⁠Employment/payment-method fee tiers (HLOOKUP table) are illustrative percentages,
  not real MDR rates.

## Dashboard interpretations

### Headline scorecards
Total GMV across the 30-day window was ₹382,603, with an 85.56% success rate.
The reconciliation match rate of 90.49% shows most transactions agree exactly between
the internal ledger and gateway export, while the remaining ~10% reflects the
deliberately injected missing/mismatched/extra rows. The 5.12% chargeback ratio is
elevated above a typical baseline because of the 15 seeded burner-account frauds.

### Trends layer
Daily GMV fluctuates without a strong trend across the window, consistent with
randomly generated baseline transactions. Chargeback counts spike on specific days,
which line up with when burner-account fraud transactions were injected — a red flag
a real ops team would investigate.

### Breakdown layer
UPI dominates GMV by payment method, reflecting its 55% weighting in the underlying
transaction generator and mirroring real Indian payment habits. Across merchant
categories, GMV is fairly evenly spread, with no single category responsible for a
disproportionate share of volume.

### Details layer
Among the top 10 merchants by transaction count, a small number are flagged
"HIGH RISK" for exceeding a 1% chargeback ratio — these merchants warrant manual
review. Most top merchants sit comfortably under this threshold, suggesting the
flagged cases are genuine outliers rather than a systemic issue.
