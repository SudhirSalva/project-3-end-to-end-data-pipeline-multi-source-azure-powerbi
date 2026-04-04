import pyodbc
import random
from datetime import datetime, timedelta
import uuid
import os

# 🔐 SECURE CONNECTION (uses environment variables)
conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server={os.getenv('DB_SERVER')};"
    f"Database={os.getenv('DB_NAME')};"
    f"Uid={os.getenv('DB_USER')};"
    f"Pwd={os.getenv('DB_PASSWORD')};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# 🇮🇳 STATES + UTs
states = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi", "Jammu & Kashmir", "Ladakh", "Chandigarh",
    "Puducherry", "Andaman & Nicobar", "Lakshadweep"
]

transaction_types = ["UPI", "CARD", "NETBANKING", "WALLET", "IMPS", "NEFT", "RTGS"]

merchant_categories = [
    "Groceries", "Electronics", "Travel", "Dining", "Healthcare",
    "Entertainment", "Fuel", "Education", "Shopping", "Utilities",
    "Subscriptions", "Insurance", "Investment"
]

banks = [
    "SBI", "HDFC", "ICICI", "Axis", "Kotak", "PNB",
    "Bank of Baroda", "Canara Bank", "IndusInd",
    "IDFC First Bank", "Yes Bank"
]

devices = ["Android", "iOS", "Web"]
networks = ["4G", "5G", "WiFi", "3G"]
age_groups = ["18-25", "26-35", "36-50", "50+"]
statuses = ["Success", "Failed", "Pending"]


def generate_row():
    now = datetime.now()

    random_time = now - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

    amount = round(random.uniform(10.0, 50000.0), 2)

    fraud_flag = 1 if (amount > 20000 and random.random() < 0.3) else random.choice([0, 0, 0, 1])

    return (
        str(uuid.uuid4()),
        random_time.strftime("%Y-%m-%d %H:%M:%S"),
        random.choice(transaction_types),
        random.choice(merchant_categories),
        amount,
        random.choice(statuses),
        random.choice(age_groups),
        random.choice(age_groups),
        random.choice(states),
        random.choice(banks),
        random.choice(banks),
        random.choice(devices),
        random.choice(networks),
        fraud_flag,
        random_time.hour,
        random_time.strftime("%A"),
        "Yes" if random_time.weekday() >= 5 else "No"
    )


def run_batch_upload():
    total_rows = 5000
    batch_size = 250

    try:
        print("🔌 Connecting securely...")
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        sql = """INSERT INTO Transactions (
                    transaction_id, timestamp, transaction_type, merchant_category,
                    amount_inr, transaction_status, sender_age_group, receiver_age_group,
                    sender_state, sender_bank, receiver_bank, device_type,
                    network_type, fraud_flag, hour_of_day, day_of_week, is_weekend
                 ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

        print("🚀 Uploading data...\n")

        for current_count in range(batch_size, total_rows + batch_size, batch_size):
            batch_data = [generate_row() for _ in range(batch_size)]
            cursor.executemany(sql, batch_data)
            conn.commit()
            print(f"✅ {current_count} rows inserted...")

        print("\n🎉 SUCCESS!")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("⚠️ Check environment variables & firewall settings.")


if __name__ == "__main__":
    run_batch_upload()