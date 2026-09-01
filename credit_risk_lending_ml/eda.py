import pandas as pd

df = pd.read_csv("credit_applicants.csv")

default_rate = df["default"].mean()
print(f"Default rate: {default_rate:.4f} ({default_rate*100:.2f}%)")

missing_pct = df["credit_bureau_score"].isna().mean()
print(f"Missing credit_bureau_score: {missing_pct:.4f} ({missing_pct*100:.2f}%)")

df["is_thin_file"] = df["credit_bureau_score"].isna().astype(int)
print(df["is_thin_file"].value_counts())
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("credit_applicants.csv")
df["is_thin_file"] = df["credit_bureau_score"].isna().astype(int)

# stratified split on default, 75/25
train_df, test_df = train_test_split(
    df, test_size=0.25, stratify=df["default"], random_state=42
)

# median of NON-missing credit_bureau_score, computed from TRAINING split only
train_median = train_df["credit_bureau_score"].median()
print(f"Training median bureau score: {train_median:.2f}")

# fill missing values in BOTH splits using that training-derived median
train_df["credit_bureau_score"] = train_df["credit_bureau_score"].fillna(train_median)
test_df["credit_bureau_score"] = test_df["credit_bureau_score"].fillna(train_median)

# encode employment_type (one-hot)
train_df = pd.get_dummies(train_df, columns=["employment_type"])
test_df = pd.get_dummies(test_df, columns=["employment_type"])
# align columns in case a category is missing in one split
train_df, test_df = train_df.align(test_df, join="left", axis=1, fill_value=0)

print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)
print("Any missing bureau scores left?", train_df["credit_bureau_score"].isna().sum(),
      test_df["credit_bureau_score"].isna().sum())