"""
Financial Analytics & Risk Assessment Dashboard - Data Cleaning & Risk Scoring
===============================================================================
Reads the raw CSVs produced by generate_data.py, performs cleaning,
outlier detection, and customer risk scoring, then writes cleaned outputs
and a customer_risk_scores.csv file.

Outputs:
  ../data/customers_clean.csv
  ../data/transactions_clean.csv
  ../data/loans_clean.csv
  ../data/customer_risk_scores.csv

Dependencies:  pip install pandas numpy
Usage:         python clean_and_score.py
"""

import os
import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# --------------------------------------------------------------------------- #
# 1. Load
# --------------------------------------------------------------------------- #
def load_data():
    customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"), parse_dates=["account_open_date"])
    transactions = pd.read_csv(os.path.join(DATA_DIR, "transactions.csv"), parse_dates=["transaction_date"])
    loans = pd.read_csv(os.path.join(DATA_DIR, "loans.csv"), parse_dates=["open_date"])
    return customers, transactions, loans


# --------------------------------------------------------------------------- #
# 2. Clean
# --------------------------------------------------------------------------- #
def clean_customers(df):
    df = df.drop_duplicates(subset="customer_id")
    df["annual_income"] = df["annual_income"].clip(lower=20000)
    df["credit_score"] = df["credit_score"].clip(lower=300, upper=850)
    df["debt_to_income_ratio"] = df["debt_to_income_ratio"].clip(lower=0.01, upper=0.95)
    df["employment_status"] = df["employment_status"].str.strip().str.title()
    df["region"] = df["region"].str.strip().str.title()
    return df


def clean_transactions(df):
    df = df.drop_duplicates(subset="transaction_id")
    df["amount"] = df["amount"].clip(lower=0.01)
    # IQR outlier flag (per transaction type) — compute thresholds, then map back
    thresholds = (
        df.groupby("transaction_type")["amount"]
        .apply(lambda s: s.quantile(0.75) + 1.5 * (s.quantile(0.75) - s.quantile(0.25)))
        .to_dict()
    )
    df["is_outlier"] = df.apply(
        lambda r: r["amount"] > thresholds.get(r["transaction_type"], float("inf")),
        axis=1,
    )
    df["year_month"] = df["transaction_date"].dt.to_period("M").astype(str)
    return df


def clean_loans(df):
    df = df.drop_duplicates(subset="loan_id")
    df["loan_amount"] = df["loan_amount"].clip(lower=1000)
    df["remaining_balance"] = df["remaining_balance"].clip(lower=0)
    df["status"] = df["status"].str.strip().str.title()
    return df


# --------------------------------------------------------------------------- #
# 3. Customer risk scoring  (0-100, higher = riskier)
# --------------------------------------------------------------------------- #
def compute_risk_scores(customers, transactions, loans):
    # Aggregate transaction behaviour per customer
    txn_agg = (
        transactions.groupby("customer_id")
        .agg(
            total_txn_amount=("amount", "sum"),
            txn_count=("transaction_id", "count"),
            avg_txn_amount=("amount", "mean"),
            outlier_txn_count=("is_outlier", "sum"),
        )
        .reset_index()
    )

    # Loan default summary per customer
    loan_agg = (
        loans.groupby("customer_id")
        .agg(
            total_loan_amount=("loan_amount", "sum"),
            active_loans=("status", lambda s: (s == "Active").sum()),
            defaulted_loans=("status", lambda s: (s == "Defaulted").sum()),
            late_loans=("status", lambda s: (s == "Late").sum()),
        )
        .reset_index()
    )

    df = customers.merge(txn_agg, on="customer_id", how="left")
    df = df.merge(loan_agg, on="customer_id", how="left")
    df[["total_txn_amount", "txn_count", "avg_txn_amount", "outlier_txn_count",
        "total_loan_amount", "active_loans", "defaulted_loans", "late_loans"]] = \
        df[["total_txn_amount", "txn_count", "avg_txn_amount", "outlier_txn_count",
            "total_loan_amount", "active_loans", "defaulted_loans", "late_loans"]].fillna(0)

    # --- Normalised sub-scores (each 0-1) --------------------------------- #
    # Credit score: lower score => higher risk
    credit_risk = (850 - df["credit_score"]) / 550

    # DTI: higher => higher risk
    dti_risk = df["debt_to_income_ratio"]

    # Default history
    default_risk = (df["defaulted_loans"] * 0.6 + df["late_loans"] * 0.3).clip(0, 1)

    # Outlier transaction ratio
    outlier_ratio = (df["outlier_txn_count"] / df["txn_count"].replace(0, 1)).clip(0, 1)

    # Employment risk
    emp_risk = df["employment_status"].map({
        "Employed": 0.05,
        "Self-Employed": 0.20,
        "Retired": 0.25,
        "Unemployed": 0.60,
    }).fillna(0.30)

    # Income volatility (coefficient of variation proxy via txn amount)
    income_risk = (1 - np.log1p(df["annual_income"]) / np.log1p(300000)).clip(0, 1)

    # Weighted composite score (0-100)
    weights = {
        "credit": 0.30,
        "dti": 0.20,
        "default": 0.20,
        "outlier": 0.05,
        "employment": 0.10,
        "income": 0.15,
    }
    df["risk_score"] = (
        credit_risk * weights["credit"]
        + dti_risk * weights["dti"]
        + default_risk * weights["default"]
        + outlier_ratio * weights["outlier"]
        + emp_risk * weights["employment"]
        + income_risk * weights["income"]
    ) * 100
    df["risk_score"] = df["risk_score"].round(2)

    # Risk band
    def band(s):
        if s < 25:
            return "Low"
        elif s < 50:
            return "Medium"
        elif s < 75:
            return "High"
        return "Critical"
    df["risk_band"] = df["risk_score"].apply(band)

    # Keep only the columns needed for the dashboard
    keep = [
        "customer_id", "customer_name", "age", "gender", "region",
        "employment_status", "annual_income", "credit_score",
        "debt_to_income_ratio", "total_txn_amount", "txn_count",
        "avg_txn_amount", "outlier_txn_count", "total_loan_amount",
        "active_loans", "defaulted_loans", "late_loans",
        "risk_score", "risk_band",
    ]
    return df[keep]


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    customers, transactions, loans = load_data()

    print("Cleaning data...")
    customers = clean_customers(customers)
    transactions = clean_transactions(transactions)
    loans = clean_loans(loans)

    customers.to_csv(os.path.join(DATA_DIR, "customers_clean.csv"), index=False)
    transactions.to_csv(os.path.join(DATA_DIR, "transactions_clean.csv"), index=False)
    loans.to_csv(os.path.join(DATA_DIR, "loans_clean.csv"), index=False)

    print("Computing customer risk scores...")
    risk_df = compute_risk_scores(customers, transactions, loans)
    risk_df.to_csv(os.path.join(DATA_DIR, "customer_risk_scores.csv"), index=False)

    # Summary
    print(f"\nRisk band distribution:\n{risk_df['risk_band'].value_counts()}")
    print(f"Mean risk score: {risk_df['risk_score'].mean():.2f}")
    print(f"Flagged outliers: {transactions['is_outlier'].sum()}")
    print("\nCleaning and scoring complete. Outputs in ../data/")


if __name__ == "__main__":
    main()
