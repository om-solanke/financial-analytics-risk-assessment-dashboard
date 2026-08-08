# 💰 Financial Analytics & Risk Assessment Dashboard

> **An end-to-end financial analytics project built with Python, SQL, Excel, Power BI, Power Query, and DAX.**

A comprehensive **Financial Analytics & Risk Assessment Dashboard** designed to transform raw financial data into actionable insights across **revenue, profitability, customer risk, loans, and transaction activity**.

The project combines **data generation, data cleaning, risk scoring, statistical analysis, SQL analytics, and interactive Power BI reporting** into a single end-to-end business intelligence workflow.

---

## 📊 Project Overview

Financial institutions need to monitor more than just revenue.

They need to understand:

- 💵 How revenue and profitability are changing
- 📈 Whether financial performance is improving or declining
- 🏦 Which loan categories have the highest default rates
- 👥 Which customers represent higher financial risk
- 💳 How transaction activity changes over time
- 🌎 How financial performance varies by region
- ⚠️ Where potential risk indicators exist
- 📅 How business performance changes across time

This project addresses these questions through an interactive **5-page Power BI dashboard** supported by Python-generated datasets, SQL analysis, Power Query transformations, and DAX measures.

---

# ✨ Key Features

### 💵 Revenue & Profitability
- Total revenue
- Total profit
- Profit margin
- Monthly revenue trends
- Previous-month revenue
- Revenue growth
- Cumulative revenue

### 🏦 Loan Performance
- Total loans
- Defaulted loans
- Loan default rate
- Loan performance by type
- Loan status analysis
- Regional loan analysis

### 👥 Customer Risk
- Total customers
- Average risk score
- High-risk customers
- High-risk customer percentage
- Risk-band distribution
- Customer-level risk analysis

### 💳 Transaction Analytics
- Total transaction amount
- Transaction count
- Average transaction amount
- Monthly transaction trends
- Transaction analysis by region
- Transaction analysis by category and type

### 🎛️ Interactive Analysis
- Year/Month slicer
- Region slicer
- Risk-band slicer
- Cross-filtering between visuals
- Interactive dashboard navigation

---

# 🖥️ Dashboard Pages

| # | Dashboard Page | Purpose | Key Visuals |
|---|---|---|---|
| 01 | **Executive Summary** | High-level financial overview | KPI cards, revenue trend, regional analysis |
| 02 | **Loan Performance & Default** | Monitor lending performance | Default rate, loan status, loan-type analysis |
| 03 | **Customer Risk Analysis** | Identify and analyze customer risk | Risk distribution, risk score analysis, risk table |
| 04 | **Transaction Trends** | Understand transaction activity | Monthly trends, transaction volume, regional analysis |
| 05 | **Revenue & Profitability** | Deep financial performance analysis | Revenue trends, cumulative revenue, profitability |

---

# 🧩 Project Architecture

```text
                    ┌─────────────────────┐
                    │   Synthetic Data    │
                    │      Generation     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Data Cleaning &   │
                    │   Risk Calculation  │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
          ┌────────────┐ ┌──────────┐ ┌─────────────┐
          │   Python   │ │   SQL    │ │    Excel    │
          │ Statistics │ │ Analysis │ │ Data Store  │
          └─────┬──────┘ └────┬─────┘ └──────┬──────┘
                │              │              │
                └──────────────┼──────────────┘
                               ▼
                    ┌─────────────────────┐
                    │    Power Query      │
                    │  Data Transformation│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Power BI      │
                    │  Data Model + DAX   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Interactive Financial│
                    │      Dashboard       │
                    └─────────────────────┘
📁 Project Structure
financial-dashboard/
│
├── 📂 data/
│   ├── customers.csv
│   ├── transactions.csv
│   ├── loans.csv
│   ├── revenue.csv
│   ├── customers_clean.csv
│   ├── transactions_clean.csv
│   ├── loans_clean.csv
│   ├── customer_risk_scores.csv
│   └── Financial_Data.xlsx
│
├── 📂 python/
│   ├── generate_data.py
│   ├── clean_and_score.py
│   └── statistical_analysis.py
│
├── 📂 sql/
│   └── schema_and_queries.sql
│
├── 📂 dashboard/
│   ├── dax_measures.dax
│   ├── power_query_transforms.m
│   └── BUILD_GUIDE.md
│
├── 📂 assets/
│   └── financial_theme.json
│
└── 📄 README.md
🚀 Quick Start
1️⃣ Clone the Repository
git clone <your-repository-url>
cd financial-dashboard
2️⃣ Install Python Dependencies
pip install pandas numpy scipy openpyxl
3️⃣ Generate the Dataset

Navigate to the Python directory:

cd python

Run the data-generation pipeline:

python generate_data.py

Then clean the generated datasets and calculate customer risk scores:

python clean_and_score.py

Run the statistical analysis:

python statistical_analysis.py

statistical_analysis.py is optional and can be used for exploratory/statistical analysis.

📦 Generated Data

The pipeline generates a synthetic financial environment containing approximately:

Dataset	Approximate Volume
👥 Customers	~1,500
💳 Transactions	~45,000
🏦 Loans	~2,000
💰 Revenue	24 months
🎯 Customer Risk Scores	Customer-level

All data is synthetically generated and contains no real customer information.

📊 Power BI Setup
1. Import the Main Dataset

Open Power BI Desktop.

Go to:

Home
→ Get Data
→ Excel Workbook

Select:

data/Financial_Data.xlsx

Import the required tables.

2. Import Customer Risk Scores

Import:

data/customer_risk_scores.csv

using:

Home
→ Get Data
→ Text/CSV
3. Create the Data Model

The primary model follows this structure:

                 Calendar
                /    |    \
               /     |     \
              ▼      ▼      ▼
        Transactions Revenue Loans
              ▲        ▲      ▲
              │        │      │
              └────────┴──────┘
                    Customers
                        │
                        ▼
              Customer Risk Scores

The exact relationships should be verified in Model View based on the available keys and date columns.

📅 Calendar Table

A dedicated Calendar table is used for time-based analysis.

Recommended fields include:

Calendar
├── Date
├── Year
├── Month
├── MonthNo
├── MonthSort
├── Quarter
└── YearMonth

The Calendar table should be marked as a Date Table using:

Table Tools
→ Mark as date table
→ Date

This enables reliable time-intelligence calculations.

🧮 DAX Measures

The dashboard uses DAX measures for business calculations.

Revenue
Total Revenue =
SUM ( Revenue[revenue] )
Total Profit =
SUM ( Revenue[profit] )
Profit Margin % =
DIVIDE ( [Total Profit], [Total Revenue], 0 )
Revenue Growth
Revenue Prev Month =
CALCULATE (
    [Total Revenue],
    DATEADD ( Calendar[Date], -1, MONTH )
)
Revenue Growth % =
DIVIDE (
    [Total Revenue] - [Revenue Prev Month],
    [Revenue Prev Month],
    0
)
Loans
Total Loans =
COUNTROWS ( Loans )
Defaulted Loans =
CALCULATE (
    COUNTROWS ( Loans ),
    Loans[status] = "Defaulted"
)
Loan Default Rate % =
DIVIDE ( [Defaulted Loans], [Total Loans], 0 )
Customer Risk
Total Customers =
DISTINCTCOUNT ( Customers[customer_id] )
Avg Risk Score =
AVERAGE ( customer_risk_scores[risk_score] )
High Risk Customers =
CALCULATE (
    [Total Customers],
    customer_risk_scores[risk_band] IN { "High", "Critical" }
)
High Risk % =
DIVIDE (
    [High Risk Customers],
    [Total Customers],
    0
)
Transactions
Total Transaction Amount =
SUM ( Transactions[amount] )
Total Transaction Count =
COUNTROWS ( Transactions )
Avg Transaction Amount =
DIVIDE (
    [Total Transaction Amount],
    [Total Transaction Count],
    0
)
Cumulative Revenue
Cumulative Revenue =
CALCULATE (
    [Total Revenue],
    FILTER (
        ALLSELECTED ( Calendar ),
        Calendar[Date] <= MAX ( Calendar[Date] )
    )
)
🎯 Customer Risk Scoring

Each customer receives a risk score from 0–100, where a higher score represents greater financial risk.

The score combines multiple financial and behavioral indicators.

Risk Factor	Weight	Risk Logic
💳 Credit Score	30%	Lower credit score → higher risk
📊 Debt-to-Income Ratio	20%	Higher DTI → higher risk
🏦 Default History	20%	More defaults/late payments → higher risk
💼 Employment	10%	Unemployment → higher risk
💰 Income Stability	15%	Lower/stable income profile → higher risk
💳 Transaction Behavior	5%	Higher anomaly/outlier behavior → higher risk
Risk Bands
Score	Risk Band
< 25	🟢 Low
25–50	🟡 Medium
50–75	🟠 High
> 75	🔴 Critical
📈 Statistical Analysis

The Python analysis layer can be used to investigate:

Correlation between financial variables
Revenue trends
Customer risk relationships
Transaction behavior
Loan performance
Statistical significance
Potential anomalies

The statistical analysis is designed to complement the Power BI dashboard rather than replace it.

🧹 Data Transformation

Power Query is used to prepare imported data before analysis.

Typical transformations include:

Data type conversion
Column renaming
Null handling
Duplicate handling
Date normalization
Text standardization
Data validation
Derived columns

Power Query scripts are available in:

dashboard/power_query_transforms.m
🗄️ SQL Analytics

The SQL layer contains:

Database schema
Table definitions
Analytical queries
Aggregations
Customer analysis
Loan analysis
Transaction analysis
Revenue analysis

Location:

sql/schema_and_queries.sql

This allows the project to demonstrate both BI reporting and SQL-based analytical thinking.

🎨 Power BI Theme

A custom financial theme is included:

assets/financial_theme.json
Color Palette
Purpose	Color
Primary	#1B4F72
Secondary Blue	#2874A6
Light Blue	#5DADE2
Positive	#27AE60
Warning	#F39C12
Negative	#E74C3C
Background	#FFFFFF

Apply the theme from:

View
→ Themes
→ Browse for themes
→ financial_theme.json
🎛️ Dashboard Interactivity

The dashboard includes interactive slicers such as:

📅 Year / Month
Calendar[YearMonth]
🌎 Region
Customers[region]
⚠️ Risk Band
customer_risk_scores[risk_band]

These slicers allow users to dynamically explore different segments of the financial data.

📌 Key Business Questions

The dashboard is designed to answer questions such as:

Revenue
How much revenue was generated?
Is revenue growing month over month?
Which periods generated the highest revenue?
How is profitability changing?
Loans
What is the overall default rate?
Which loan types have the highest default rates?
How many loans are currently defaulted?
Which regions have higher loan risk?
Customers
How many customers are high risk?
What is the average customer risk score?
Which risk bands contain the most customers?
Which customer segments require additional attention?
Transactions
How much money is being transacted?
How many transactions occur each month?
What is the average transaction value?
Which regions and categories generate the most activity?
🛠️ Technology Stack
Technology	Role
🐍 Python	Data generation, cleaning, scoring, statistics
🐼 Pandas	Data manipulation
🔢 NumPy	Numerical computation
📐 SciPy	Statistical analysis
🗄️ SQL	Data modeling and analytical queries
📗 Excel	Data storage and Power BI source
🔄 Power Query	ETL and transformation
📊 Power BI	Dashboard and visualization
🧮 DAX	Business calculations and KPIs
🎨 JSON	Power BI theme configuration
🔄 End-to-End Workflow
Generate
   ↓
Clean
   ↓
Validate
   ↓
Calculate Risk Scores
   ↓
Perform Statistical Analysis
   ↓
Store / Query with SQL
   ↓
Transform with Power Query
   ↓
Build Power BI Data Model
   ↓
Create DAX Measures
   ↓
Apply Theme
   ↓
Build Interactive Dashboard
   ↓
Generate Financial Insights
📚 Documentation

Detailed Power BI construction instructions are available in:

dashboard/BUILD_GUIDE.md

The guide covers:

Data import
Power Query transformations
Data relationships
Calendar table
Date-table configuration
DAX measures
KPI visuals
Cards
Charts
Slicers
Formatting
Dashboard layout
Theme application
⚠️ Current Scope

The current Power BI model focuses on:

Revenue
Profitability
Loan performance
Customer risk
Transaction analytics
Time-based analysis
Anomaly Detection

The original project concept included transaction anomaly/outlier measures.

However, the current Transactions dataset does not contain an is_outlier field. Therefore, the Power BI implementation does not force an anomaly measure onto the dashboard.

This keeps the dashboard aligned with the actual available source data rather than introducing unsupported calculations.

Anomaly detection can be added later using a statistical method such as IQR or Z-score analysis if required.

🎓 Portfolio Value

This project demonstrates an end-to-end analytics workflow rather than only dashboard creation.

Data Engineering
Synthetic data generation
Data cleaning
Data transformation
Data validation
Analytics
Financial KPIs
Customer risk scoring
Loan default analysis
Transaction analysis
Statistical analysis
Business Intelligence
Data modeling
DAX
Power Query
Time intelligence
Interactive dashboards
KPI design
Technical Skills
Python
SQL
Power BI
DAX
Power Query M
Excel
Statistics
🚀 Future Enhancements

Potential future improvements include:

 Add automated anomaly detection
 Add year-over-year revenue measures
 Add profit growth analysis
 Add loan loss provision metrics
 Add customer segmentation
 Add predictive loan-default modeling
 Add automated Power BI refresh
 Add drill-through customer profiles
 Add advanced tooltip pages
 Add executive-level financial alerts
 Connect the model to a live SQL database
 Deploy the dashboard through Power BI Service
📁 Data Privacy

All datasets included in this project are synthetically generated.

No real customer, banking, transaction, loan, or personally identifiable information is used.

The project is intended for:

🎓 Educational purposes
💼 Portfolio demonstration
📊 Business intelligence practice
🧪 Data analytics experimentation
👨‍💻 Project Status

Status: 🟢 Active / Portfolio Project

The core data pipeline, analytical model, DAX measures, Power BI theme, and dashboard architecture are established.

Further enhancements can be added as the project evolves.

📜 License

This project uses synthetic data and is intended for educational and portfolio purposes.

You are free to adapt the project structure, analytical methods, and dashboard concepts for learning and demonstration purposes.