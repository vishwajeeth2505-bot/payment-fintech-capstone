import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

behaviour = pd.read_csv("txn_behaviour.csv")

features = ["txn_hour", "is_new_device", "txn_amount_inr"]
X = behaviour[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

contamination_rate = 15 / 265
print(f"Contamination rate: {contamination_rate:.4f}")

iso_forest = IsolationForest(random_state=42, contamination=contamination_rate)
behaviour["anomaly_flag"] = iso_forest.fit_predict(X_scaled)
# IsolationForest returns -1 for anomaly, 1 for normal

behaviour["is_seeded_anomaly"] = behaviour["txn_id"].str.startswith("BTXNA")

flagged = behaviour[behaviour["anomaly_flag"] == -1]
caught_seeded = flagged["is_seeded_anomaly"].sum()
total_seeded = behaviour["is_seeded_anomaly"].sum()

print(f"Total flagged as anomalies: {len(flagged)}")
print(f"Seeded anomalies caught: {caught_seeded} / {total_seeded}")
print(f"Recall on seeded anomalies: {caught_seeded/total_seeded:.4f}")