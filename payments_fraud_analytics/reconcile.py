import pandas as pd

def reconcile_payments(ledger_df, gateway_df):
    missing_in_gateway = ledger_df[~ledger_df["transaction_id"].isin(gateway_df["transaction_id"])]
    missing_in_ledger = gateway_df[~gateway_df["transaction_id"].isin(ledger_df["transaction_id"])]
    
    merged = pd.merge(
        ledger_df, gateway_df,
        on="transaction_id",
        suffixes=("_ledger", "_gateway")
    )
    
    amount_mismatches = merged[merged["amount_inr_ledger"] != merged["amount_inr_gateway"]].copy()
    amount_mismatches["amount_difference"] = amount_mismatches["amount_inr_ledger"] - amount_mismatches["amount_inr_gateway"]
    
    status_mismatches = merged[merged["status_ledger"] != merged["status_gateway"]]
    
    return missing_in_gateway, missing_in_ledger, amount_mismatches, status_mismatches

ledger_df = pd.read_csv("ledger.csv")
gateway_df = pd.read_csv("gateway_export.csv")

missing_in_gateway, missing_in_ledger, amount_mismatches, status_mismatches = reconcile_payments(ledger_df, gateway_df)

print(f"Missing in gateway (in ledger, not gateway): {len(missing_in_gateway)}")
print(f"Missing in ledger (extra in gateway): {len(missing_in_ledger)}")
print(f"Amount mismatches: {len(amount_mismatches)}")
print(f"Status mismatches: {len(status_mismatches)}")