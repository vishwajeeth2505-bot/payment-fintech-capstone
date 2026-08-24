import sqlite3

conn = sqlite3.connect("paytm_payments.db")
cursor = conn.cursor()

print("=" * 60)
print("QUERY 1: Chargeback Impact")
print("=" * 60)
cursor.execute("""
SELECT
    COUNT(*) AS chargeback_count,
    COUNT(DISTINCT user_id) AS unique_users_affected,
    SUM(amount_inr) AS total_chargeback_amount
FROM transactions
WHERE status = 'chargeback'
""")
result = cursor.fetchone()
print(f"Chargeback transactions: {result[0]}")
print(f"Unique users affected: {result[1]}")
print(f"Total chargeback amount: ₹{result[2]}")


print("=" * 60)
print("QUERY 2: Burner Account Detection")
print("=" * 60)
cursor.execute("""
SELECT
    t.transaction_id,
    t.user_id,
    u.signup_date,
    t.transaction_time,
    t.amount_inr
FROM transactions t
INNER JOIN users u ON t.user_id = u.user_id
WHERE t.status = 'chargeback'
  AND julianday(t.transaction_time) - julianday(u.signup_date) >= 0
  AND julianday(t.transaction_time) - julianday(u.signup_date) < 30
""")
results = cursor.fetchall()
print(f"Burner account transactions found: {len(results)}")
for row in results[:5]:
    print(row)

    print("=" * 60)
print("QUERY 3: Velocity Attack Detection")
print("=" * 60)
cursor.execute("""
SELECT
    user_id,
    CAST(strftime('%s', transaction_time) / 600 AS INTEGER) AS time_bucket,
    COUNT(*) AS txn_count,
    MIN(transaction_time) AS earliest_txn
FROM transactions
GROUP BY user_id, time_bucket
HAVING COUNT(*) >= 3
ORDER BY user_id, time_bucket
""")
results = cursor.fetchall()
print(f"Velocity attack clusters found: {len(results)}")
for row in results:
    print(row)

    print("=" * 60)
print("QUERY 3: Velocity Attack Detection")
print("=" * 60)
cursor.execute("""
SELECT
    user_id,
    CAST(strftime('%s', transaction_time) / 600 AS INTEGER) AS time_bucket,
    COUNT(*) AS txn_count,
    MIN(transaction_time) AS earliest_txn
FROM transactions
GROUP BY user_id, time_bucket
HAVING COUNT(*) >= 3
ORDER BY user_id, time_bucket
""")
results = cursor.fetchall()
print(f"Velocity attack clusters found: {len(results)}")
for row in results:
    print(row)

    print("=" * 60)
print("QUERY 4: Transaction Count per Merchant (LEFT JOIN)")
print("=" * 60)
cursor.execute("""
SELECT
    m.merchant_id,
    m.merchant_name,
    m.category,
    COUNT(t.transaction_id) AS total_transactions
FROM merchants m
LEFT JOIN transactions t ON m.merchant_id = t.merchant_id
GROUP BY m.merchant_id, m.merchant_name, m.category
ORDER BY total_transactions DESC
LIMIT 10
""")
results = cursor.fetchall()
print("Top 10 merchants by transaction count:")
for row in results:
    print(row)
    print("=" * 60)
print("QUERY 5: Highest-Value Transactions (DISTINCT payment methods)")
print("=" * 60)
cursor.execute("""
SELECT DISTINCT payment_method, amount_inr, status
FROM transactions
ORDER BY amount_inr DESC
LIMIT 10
""")
results = cursor.fetchall()
print("Top 10 highest-value transactions (distinct method/amount/status combos):")
for row in results:
    print(row)

    print("=" * 60)
print("QUERY 6: Chargeback Rate by Merchant Category")
print("=" * 60)
cursor.execute("""
SELECT
    m.category,
    COUNT(t.transaction_id) AS total_txns,
    SUM(CASE WHEN t.status = 'chargeback' THEN 1 ELSE 0 END) AS chargebacks
FROM transactions t
INNER JOIN merchants m ON t.merchant_id = m.merchant_id
GROUP BY m.category
ORDER BY chargebacks DESC
""")
results = cursor.fetchall()
print("Chargebacks by category:")
for row in results:
    print(row)

conn.close()