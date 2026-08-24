import sqlite3
import pandas as pd

conn = sqlite3.connect("paytm_payments.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS transactions")
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS merchants")

cursor.execute("""
CREATE TABLE merchants (
    merchant_id INTEGER PRIMARY KEY,
    merchant_name TEXT,
    category TEXT,
    region TEXT
)
""")

cursor.execute("""
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    signup_date TEXT
)
""")

cursor.execute("""
CREATE TABLE transactions (
    transaction_id TEXT PRIMARY KEY,
    user_id INTEGER,
    merchant_id INTEGER,
    transaction_time TEXT,
    amount_inr INTEGER,
    payment_method TEXT,
    status TEXT,
    risk_score INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
)
""")

conn.commit()

merchants_df = pd.read_csv("merchants.csv")
users_df = pd.read_csv("users.csv")
ledger_df = pd.read_csv("ledger.csv")

merchants_df.to_sql("merchants", conn, if_exists="append", index=False)
users_df.to_sql("users", conn, if_exists="append", index=False)
ledger_df.to_sql("transactions", conn, if_exists="append", index=False)

conn.commit()

cursor.execute("SELECT COUNT(*) FROM merchants")
print(f"Merchants loaded: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM users")
print(f"Users loaded: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM transactions")
print(f"Transactions loaded: {cursor.fetchone()[0]}")