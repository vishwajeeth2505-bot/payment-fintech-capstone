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
from sklearn.preprocessing import StandardScaler

numeric_cols = ["age", "monthly_income_inr", "existing_loans_count",
                 "credit_utilization_ratio", "upi_monthly_inflow_inr",
                 "bounced_payments_count", "credit_bureau_score"]

scaler = StandardScaler()
train_df[numeric_cols] = scaler.fit_transform(train_df[numeric_cols])
test_df[numeric_cols] = scaler.transform(test_df[numeric_cols])

print(train_df[numeric_cols].describe().loc[["mean", "std"]])
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

feature_cols = [c for c in train_df.columns if c not in ["applicant_id", "default"]]

X_train = train_df[feature_cols]
y_train = train_df["default"]
X_test = test_df[feature_cols]
y_test = test_df["default"]

log_reg = LogisticRegression(random_state=42, max_iter=1000)
log_reg.fit(X_train, y_train)

dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)

print("Logistic Regression trained.")
print("Decision Tree trained.")
print("Feature columns used:", feature_cols)
from sklearn.metrics import (confusion_matrix, accuracy_score, precision_score,
                              recall_score, f1_score, roc_auc_score)

def evaluate(model, name):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print(f"\n--- {name} ---")
    print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"F1:        {f1_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC:   {roc_auc_score(y_test, y_proba):.4f}")

evaluate(log_reg, "Logistic Regression")
evaluate(dt, "Decision Tree")

test_df["predicted_prob"] = log_reg.predict_proba(X_test)[:, 1]

test_df["risk_tier"] = pd.qcut(test_df["predicted_prob"], q=4,
                                 labels=["Low", "Medium-Low", "Medium-High", "High"])

pricing_table = test_df.groupby("risk_tier", observed=True).agg(
    n_applicants=("default", "count"),
    actual_default_rate=("default", "mean"),
    avg_predicted_prob=("predicted_prob", "mean"),
).reset_index()

# illustrative interest rate: higher risk tier -> higher rate
rate_map = {"Low": "8-10%", "Medium-Low": "11-14%", "Medium-High": "15-19%", "High": "20-25%"}
pricing_table["illustrative_rate"] = pricing_table["risk_tier"].map(rate_map)

print(pricing_table)

print(pricing_table[["risk_tier", "n_applicants", "actual_default_rate", "illustrative_rate"]].to_string(index=False))