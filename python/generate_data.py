"""
Financial Analytics & Risk Assessment Dashboard - Data Generator
=================================================================
Generates synthetic but realistic financial datasets:
  - customers.csv   : 1,500 customers with demographics & credit info
  - transactions.csv: ~45,000 transactions over 24 months
  - loans.csv       : 2,000 loans with performance & default status
  - revenue.csv     : 24 months of revenue / expense / profit data

Outputs are written to ../data/ as both CSV and a single Excel workbook
(Financial_Data.xlsx) so they can be imported directly into Power BI.

Dependencies:  pip install pandas numpy openpyxl
Usage:         python generate_data.py
"""

import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
random.seed(42)
np.random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)
N_CUSTOMERS = 1500
N_LOANS = 2000
TXN_PER_CUSTOMER_RANGE = (15, 55)

PRODUCT_CATEGORIES = [
    "Credit Card", "Personal Loan", "Mortgage",
    "Auto Loan", "Savings Account", "Investment Fund",
    "Insurance", "Business Loan",
]

TRANSACTION_TYPES = ["Deposit", "Withdrawal", "Payment", "Transfer", "Fee", "Interest"]

REGIONS = ["North", "South", "East", "West", "Central"]
EMPLOYMENT_STATUS = ["Employed", "Self-Employed", "Unemployed", "Retired"]
LOAN_STATUSES = ["Active", "Closed", "Defaulted", "Late"]

# --------------------------------------------------------------------------- #
# 1. Customers
# --------------------------------------------------------------------------- #
def generate_customers():
    rows = []
    for i in range(1, N_CUSTOMERS + 1):
        age = np.random.normal(42, 12)
        age = max(18, min(85, int(age)))
        income = max(20000, np.random.lognormal(11.0, 0.55))
        credit_score = max(300, min(850, int(np.random.normal(685, 90))))
        debt_to_income = round(min(0.95, max(0.01, np.random.beta(2.5, 5))), 3)

        rows.append({
            "customer_id": f"CUST-{i:05d}",
            "customer_name": f"Customer_{i}",
            "age": age,
            "gender": random.choice(["M", "F"]),
            "region": random.choice(REGIONS),
            "employment_status": random.choices(
                EMPLOYMENT_STATUS, weights=[55, 20, 12, 13]
            )[0],
            "annual_income": round(income, 2),
            "credit_score": credit_score,
            "debt_to_income_ratio": debt_to_income,
            "account_open_date": START_DATE - timedelta(days=random.randint(30, 2000)),
        })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA_DIR, "customers.csv"), index=False)
    return df


# --------------------------------------------------------------------------- #
# 2. Transactions
# --------------------------------------------------------------------------- #
def generate_transactions(customers_df):
    rows = []
    txn_id = 1
    date_range_days = (END_DATE - START_DATE).days

    for _, cust in customers_df.iterrows():
        n_txn = random.randint(*TXN_PER_CUSTOMER_RANGE)
        # Higher-income customers transact larger amounts
        income_factor = cust["annual_income"] / 80000

        for _ in range(n_txn):
            txn_date = START_DATE + timedelta(
                days=random.randint(0, date_range_days),
                hours=random.randint(0, 23),
            )
            amount = abs(np.random.lognormal(3.8, 1.1)) * income_factor
            amount = round(min(amount, 50000), 2)

            rows.append({
                "transaction_id": f"TXN-{txn_id:06d}",
                "customer_id": cust["customer_id"],
                "transaction_date": txn_date.strftime("%Y-%m-%d"),
                "transaction_type": random.choices(
                    TRANSACTION_TYPES, weights=[25, 20, 25, 15, 8, 7]
                )[0],
                "amount": amount,
                "product_category": random.choice(PRODUCT_CATEGORIES),
                "region": cust["region"],
            })
            txn_id += 1

    df = pd.DataFrame(rows)
    df = df.sort_values("transaction_date").reset_index(drop=True)
    df.to_csv(os.path.join(DATA_DIR, "transactions.csv"), index=False)
    return df


# --------------------------------------------------------------------------- #
# 3. Loans
# --------------------------------------------------------------------------- #
def generate_loans(customers_df):
    rows = []
    loan_types = ["Personal", "Mortgage", "Auto", "Business", "Student"]

    for i in range(1, N_LOANS + 1):
        cust = customers_df.sample(1).iloc[0]
        loan_amount = round(max(2000, np.random.lognormal(10.5, 0.8)), 2)
        interest_rate = round(np.random.uniform(3.5, 18.5), 2)
        term_months = random.choice([12, 24, 36, 48, 60, 120, 360])

        open_date = START_DATE - timedelta(days=random.randint(30, 700))
        months_elapsed = min(
            term_months,
            max(0, (END_DATE.year - open_date.year) * 12 + (END_DATE.month - open_date.month)),
        )

        # Default probability rises with DTI, falls with credit score
        base_risk = cust["debt_to_income_ratio"] * 0.4
        credit_penalty = (700 - cust["credit_score"]) / 800
        default_prob = min(0.35, max(0.02, base_risk + credit_penalty))

        if months_elapsed >= term_months:
            status = "Closed"
        elif random.random() < default_prob:
            status = "Defaulted"
        elif random.random() < default_prob * 0.5:
            status = "Late"
        else:
            status = "Active"

        monthly_payment = round(
            loan_amount * (interest_rate / 1200)
            / (1 - (1 + interest_rate / 1200) ** (-term_months)),
            2,
        )
        remaining_balance = round(
            loan_amount * (1 - months_elapsed / term_months)
            if status != "Defaulted"
            else loan_amount * 0.65,
            2,
        )

        rows.append({
            "loan_id": f"LOAN-{i:04d}",
            "customer_id": cust["customer_id"],
            "loan_type": random.choice(loan_types),
            "loan_amount": loan_amount,
            "interest_rate": interest_rate,
            "term_months": term_months,
            "monthly_payment": monthly_payment,
            "remaining_balance": max(0, remaining_balance),
            "open_date": open_date.strftime("%Y-%m-%d"),
            "status": status,
            "credit_score": cust["credit_score"],
            "annual_income": cust["annual_income"],
            "debt_to_income_ratio": cust["debt_to_income_ratio"],
        })

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA_DIR, "loans.csv"), index=False)
    return df


# --------------------------------------------------------------------------- #
# 4. Revenue (monthly P&L)
# --------------------------------------------------------------------------- #
def generate_revenue():
    rows = []
    current = START_DATE.replace(day=1)
    base_revenue = 450000

    while current <= END_DATE:
        month_num = (current.year - START_DATE.year) * 12 + current.month
        # Upward trend with seasonality (Q4 peak)
        trend = 1 + month_num * 0.015
        seasonal = 1 + 0.18 * np.sin((current.month - 1) * np.pi / 6)
        noise = np.random.normal(1, 0.06)

        revenue = base_revenue * trend * seasonal * noise
        # Expenses grow slightly slower -> improving margin over time
        expense_ratio = max(0.62, 0.75 - month_num * 0.003) + np.random.normal(0, 0.02)
        expenses = revenue * expense_ratio
        profit = revenue - expenses

        rows.append({
            "month": current.strftime("%Y-%m"),
            "month_start": current.strftime("%Y-%m-%d"),
            "revenue": round(revenue, 2),
            "operating_expenses": round(expenses, 2),
            "profit": round(profit, 2),
            "interest_income": round(revenue * np.random.uniform(0.35, 0.48), 2),
            "fee_income": round(revenue * np.random.uniform(0.15, 0.25), 2),
            "loan_loss_provision": round(revenue * np.random.uniform(0.03, 0.07), 2),
        })
        # Advance one month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA_DIR, "revenue.csv"), index=False)
    return df


# --------------------------------------------------------------------------- #
# 5. Combined Excel workbook
# --------------------------------------------------------------------------- #
def write_excel(customers, transactions, loans, revenue):
    path = os.path.join(DATA_DIR, "Financial_Data.xlsx")
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        customers.to_excel(writer, sheet_name="Customers", index=False)
        transactions.to_excel(writer, sheet_name="Transactions", index=False)
        loans.to_excel(writer, sheet_name="Loans", index=False)
        revenue.to_excel(writer, sheet_name="Revenue", index=False)
    print(f"Excel workbook written: {path}")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    print("Generating customers...")
    customers = generate_customers()
    print(f"  -> {len(customers)} customers")

    print("Generating transactions...")
    transactions = generate_transactions(customers)
    print(f"  -> {len(transactions)} transactions")

    print("Generating loans...")
    loans = generate_loans(customers)
    print(f"  -> {len(loans)} loans")

    print("Generating revenue...")
    revenue = generate_revenue()
    print(f"  -> {len(revenue)} months of P&L")

    print("Writing Excel workbook...")
    write_excel(customers, transactions, loans, revenue)

    print("\nAll data generated successfully in ../data/")


if __name__ == "__main__":
    main()
