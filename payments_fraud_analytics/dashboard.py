import pandas as pd
import matplotlib.pyplot as plt

ledger = pd.read_csv("ledger.csv")
gateway = pd.read_csv("gateway_export.csv")
merchants = pd.read_csv("merchants.csv")

ledger["transaction_time"] = pd.to_datetime(ledger["transaction_time"])
ledger["date"] = ledger["transaction_time"].dt.date

total_gmv = ledger["amount_inr"].sum()
success_rate = (ledger["status"] == "captured").mean() * 100

merged_check = pd.merge(ledger, gateway, on="transaction_id", suffixes=("_l", "_g"))
matched = merged_check[
    (merged_check["amount_inr_l"] == merged_check["amount_inr_g"]) &
    (merged_check["status_l"] == merged_check["status_g"])
]
match_rate = len(matched) / len(ledger) * 100

chargeback_ratio = (ledger["status"] == "chargeback").mean() * 100

print(f"Total GMV: ₹{total_gmv:,}")
print(f"Success rate: {success_rate:.2f}%")
print(f"Reconciliation match rate: {match_rate:.2f}%")
print(f"Chargeback ratio: {chargeback_ratio:.2f}%")
ig, axes = plt.subplots(1, 4, figsize=(16, 3))

scorecards = [
    ("Total GMV", f"₹{total_gmv:,.0f}"),
    ("Success Rate", f"{success_rate:.1f}%"),
    ("Match Rate", f"{match_rate:.1f}%"),
    ("Chargeback Ratio", f"{chargeback_ratio:.2f}%"),
]

for ax, (label, value) in zip(axes, scorecards):
    ax.text(0.5, 0.6, value, fontsize=24, ha="center", weight="bold")
    ax.text(0.5, 0.3, label, fontsize=12, ha="center", color="gray")
    ax.axis("off")

plt.tight_layout()
plt.savefig("dashboard_headline.png", dpi=150)
print("Saved dashboard_headline.png")
fig, axes = plt.subplots(1, 4, figsize=(16, 3))

scorecards = [
    ("Total GMV", f"₹{total_gmv:,.0f}"),
    ("Success Rate", f"{success_rate:.1f}%"),
    ("Match Rate", f"{match_rate:.1f}%"),
    ("Chargeback Ratio", f"{chargeback_ratio:.2f}%"),
]

for ax, (label, value) in zip(axes, scorecards):
    ax.text(0.5, 0.6, value, fontsize=24, ha="center", weight="bold")
    ax.text(0.5, 0.3, label, fontsize=12, ha="center", color="gray")
    ax.axis("off")

plt.tight_layout()
plt.savefig("dashboard_headline.png", dpi=150)
print("Saved dashboard_headline.png")
daily_stats = ledger.groupby("date").agg(
    daily_gmv=("amount_inr", "sum"),
    daily_chargebacks=("status", lambda x: (x == "chargeback").sum())
).reset_index()

fig, ax1 = plt.subplots(figsize=(12, 5))

ax1.plot(daily_stats["date"], daily_stats["daily_gmv"], color="steelblue", label="Daily GMV")
ax1.set_xlabel("Date")
ax1.set_ylabel("Daily GMV (₹)", color="steelblue")
ax1.tick_params(axis="x", rotation=45)

ax2 = ax1.twinx()
ax2.bar(daily_stats["date"], daily_stats["daily_chargebacks"], color="salmon", alpha=0.4, label="Chargebacks")
ax2.set_ylabel("Daily Chargeback Count", color="salmon")

plt.title("Daily GMV and Chargeback Trend (30-day window)")
plt.tight_layout()
plt.savefig("dashboard_trends.png", dpi=150)
print("Saved dashboard_trends.png")
by_method = ledger.groupby("payment_method")["amount_inr"].sum().sort_values(ascending=False)

ledger_with_category = ledger.merge(merchants[["merchant_id", "category"]], on="merchant_id")
by_category = ledger_with_category.groupby("category")["amount_inr"].sum().sort_values(ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.bar(by_method.index, by_method.values, color="steelblue")
ax1.set_title("GMV by Payment Method")
ax1.set_ylabel("GMV (₹)")
ax1.tick_params(axis="x", rotation=30)

ax2.bar(by_category.index, by_category.values, color="darkorange")
ax2.set_title("GMV by Category")
ax2.set_ylabel("GMV (₹)")
ax2.tick_params(axis="x", rotation=30)

plt.tight_layout()
plt.savefig("dashboard_breakdown.png", dpi=150)
print("Saved dashboard_breakdown.png")
merchant_stats = ledger_with_category.groupby("merchant_id").agg(
    total_txns=("transaction_id", "count"),
    chargebacks=("status", lambda x: (x == "chargeback").sum())
).reset_index()

merchant_stats = merchant_stats.merge(merchants[["merchant_id", "merchant_name"]], on="merchant_id")
merchant_stats["chargeback_ratio_pct"] = (merchant_stats["chargebacks"] / merchant_stats["total_txns"] * 100).round(2)
merchant_stats["flag"] = merchant_stats["chargeback_ratio_pct"].apply(lambda x: "⚠️ HIGH RISK" if x > 1 else "OK")

top10 = merchant_stats.sort_values("total_txns", ascending=False).head(10)
top10 = top10[["merchant_name", "total_txns", "chargebacks", "chargeback_ratio_pct", "flag"]]

fig, ax = plt.subplots(figsize=(10, 4))
ax.axis("off")
table = ax.table(
    cellText=top10.values,
    colLabels=["Merchant", "Total Txns", "Chargebacks", "Chargeback %", "Flag"],
    cellLoc="center",
    loc="center"
)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

plt.title("Top 10 Merchants by Transaction Count", pad=20)
plt.tight_layout()
plt.savefig("dashboard_details.png", dpi=150)
print("Saved dashboard_details.png")

conn_check = None