"""
Financial Analytics & Risk Assessment Dashboard - Statistical Analysis
========================================================================
Performs descriptive statistics, correlation analysis, hypothesis testing,
trend analysis, and anomaly detection on the cleaned data.
Outputs a summary report to ../analysis_summary.txt.

Dependencies:  pip install pandas numpy scipy
Usage:         python statistical_analysis.py
"""

import os
import numpy as np
import pandas as pd
from scipy import stats

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "analysis_summary.txt")

lines = []
def p(text=""):
    lines.append(text)
    print(text)


def section(title):
    p(f"\n{'=' * 70}")
    p(f"  {title}")
    p(f"{'=' * 70}")


# --------------------------------------------------------------------------- #
# Load
# --------------------------------------------------------------------------- #
customers = pd.read_csv(os.path.join(DATA_DIR, "customers_clean.csv"))
transactions = pd.read_csv(os.path.join(DATA_DIR, "transactions_clean.csv"), parse_dates=["transaction_date"])
loans = pd.read_csv(os.path.join(DATA_DIR, "loans_clean.csv"))
revenue = pd.read_csv(os.path.join(DATA_DIR, "revenue.csv"), parse_dates=["month_start"])
risk = pd.read_csv(os.path.join(DATA_DIR, "customer_risk_scores.csv"))

# --------------------------------------------------------------------------- #
# 1. Descriptive statistics
# --------------------------------------------------------------------------- #
section("1. DESCRIPTIVE STATISTICS")

p("\n-- Transaction Amounts --")
p(transactions["amount"].describe().round(2).to_string())

p("\n-- Annual Income --")
p(customers["annual_income"].describe().round(2).to_string())

p("\n-- Loan Amounts --")
p(loans["loan_amount"].describe().round(2).to_string())

p("\n-- Revenue --")
p(revenue["revenue"].describe().round(2).to_string())

# --------------------------------------------------------------------------- #
# 2. Correlation analysis
# --------------------------------------------------------------------------- #
section("2. CORRELATION ANALYSIS")

corr_cols = ["credit_score", "debt_to_income_ratio", "annual_income",
             "age", "risk_score", "total_txn_amount", "total_loan_amount"]
corr = risk[corr_cols].corr().round(3)
p("\nPearson correlation matrix:")
p(corr.to_string())

# --------------------------------------------------------------------------- #
# 3. Hypothesis testing
# --------------------------------------------------------------------------- #
section("3. HYPOTHESIS TESTING")

# Do high-risk customers have lower credit scores than low-risk?
low = risk.loc[risk["risk_band"] == "Low", "credit_score"]
high = risk.loc[risk["risk_band"].isin(["High", "Critical"]), "credit_score"]
t_stat, p_val = stats.ttest_ind(low, high, equal_var=False)
p(f"\nTwo-sample t-test: Credit score (Low vs High/Critical risk)")
p(f"  t-statistic = {t_stat:.4f}, p-value = {p_val:.2e}")
p(f"  Mean Low risk = {low.mean():.1f} | Mean High risk = {high.mean():.1f}")

# Chi-square: employment status vs risk band
ct = pd.crosstab(risk["employment_status"], risk["risk_band"])
chi2, chi_p, dof, _ = stats.chi2_contingency(ct)
p(f"\nChi-square test: Employment status vs Risk band")
p(f"  chi2 = {chi2:.2f}, dof = {dof}, p-value = {chi_p:.2e}")

# --------------------------------------------------------------------------- #
# 4. Trend analysis - monthly transaction volume
# --------------------------------------------------------------------------- #
section("4. TREND ANALYSIS")

monthly_txn = (
    transactions.groupby("year_month")
    .agg(total_amount=("amount", "sum"), txn_count=("transaction_id", "count"))
    .reset_index()
    .sort_values("year_month")
)
p("\nMonthly transaction volume (first 6 / last 6):")
p(monthly_txn.head(6).to_string(index=False))
p("  ...")
p(monthly_txn.tail(6).to_string(index=False))

# Simple linear regression on revenue
x = np.arange(len(revenue))
y = revenue["revenue"].values
slope, intercept, r_value, p_value_r, std_err = stats.linregress(x, y)
p(f"\nRevenue linear trend:")
p(f"  Slope = {slope:.2f}/month, R² = {r_value**2:.3f}, p-value = {p_value_r:.2e}")

# --------------------------------------------------------------------------- #
# 5. Anomaly detection - Z-score on transaction amounts
# --------------------------------------------------------------------------- #
section("5. ANOMALY DETECTION (Z-SCORE > 3)")

z = np.abs(stats.zscore(transactions["amount"]))
anomalies = transactions.loc[z > 3]
p(f"\nNumber of anomalous transactions (|z| > 3): {len(anomalies)}")
if len(anomalies) > 0:
    p(f"Mean anomaly amount: {anomalies['amount'].mean():.2f}")
    p(f"Max anomaly amount: {anomalies['amount'].max():.2f}")
    p("\nTop 5 anomalous transactions:")
    p(anomalies.nlargest(5, "amount")[
        ["transaction_id", "customer_id", "transaction_date", "amount", "transaction_type"]
    ].to_string(index=False))

# --------------------------------------------------------------------------- #
# 6. Loan default rate by category
# --------------------------------------------------------------------------- #
section("6. LOAN DEFAULT ANALYSIS")

total_loans = len(loans)
defaulted = (loans["status"] == "Defaulted").sum()
overall_rate = defaulted / total_loans * 100
p(f"\nOverall default rate: {overall_rate:.2f}%  ({defaulted}/{total_loans})")

by_type = (
    loans.groupby("loan_type")
    .agg(total=("loan_id", "count"), defaulted=("status", lambda s: (s == "Defaulted").sum()))
    .assign(default_rate=lambda d: (d["defaulted"] / d["total"] * 100).round(2))
    .sort_values("default_rate", ascending=False)
)
p("\nDefault rate by loan type:")
p(by_type.to_string())

# --------------------------------------------------------------------------- #
# Write report
# --------------------------------------------------------------------------- #
with open(REPORT_PATH, "w") as f:
    f.write("\n".join(lines))
print(f"\nReport written to {REPORT_PATH}")
