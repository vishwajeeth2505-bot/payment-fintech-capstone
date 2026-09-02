import pandas as pd

df = pd.read_csv("credit_applicants.csv")

default_rate = df["default"].mean()
print(f"Default rate: {default_rate:.4f} ({default_rate*100:.2f}%)")

missing_pct = df["credit_bureau_score"].isna().mean()
print(f"Missing credit_bureau_score: {missing_pct:.4f} ({missing_pct*100:.2f}%)")

df["is_thin_file"] = df["credit_bureau_score"].isna().astype(int)
print(df["is_thin_file"].value_counts())
