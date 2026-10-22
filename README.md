# E-commerce Customer Analytics

An end-to-end data analytics project focused on customer segmentation, purchasing behavior, retention analysis, and churn prediction using MySQL, Python, Machine Learning, and Power BI.

## 📌 Project Overview

E-commerce businesses need to understand their customers to improve retention, identify valuable customers, and make better business decisions.

This project analyzes customer and order data from the Brazilian E-Commerce Public Dataset by Olist. It combines SQL-based analytics, RFM segmentation, customer clustering, churn-model evaluation, and dashboard reporting to uncover useful business insights.

## 🎯 Business Objectives

- Analyze customer purchasing behavior and order revenue.
- Segment customers using Recency, Frequency, and Monetary (RFM) analysis.
- Identify customer retention patterns using cohort analysis.
- Explore customer groups using K-Means clustering.
- Evaluate a baseline machine learning model for churn prediction.
- Present business insights through Power BI dashboards.

## 🛠️ Tools and Technologies

- **MySQL:** Data cleaning checks, joins, aggregations, RFM analysis, and cohort retention.
- **Python:** Data processing and exploratory analysis.
- **Pandas and NumPy:** Data manipulation and numerical analysis.
- **Scikit-learn:** K-Means clustering and churn-model evaluation.
- **Matplotlib:** Data visualization.
- **Power BI:** Business overview and customer retention reporting.
- **Git and GitHub:** Version control and project documentation.

## 📂 Project Structure

```text
ecommerce-customer-analytics/
│
├── models/
│   └── customer_kmeans_model.joblib
│
├── notebooks/
│   └── customer_clustering.py
│
├── sql/
│   ├── 01_data_quality_checks.sql
│   ├── 02_order_analytics.sql
│   ├── 03_customer_summary.sql
│   ├── 04_rfm_analysis.sql
│   ├── 05_customer_segmentation.sql
│   └── 06_monthly_activity_retention.sql
│
├── outputs/
│   ├── kmeans_evaluation.csv
│   ├── customer_cluster_assignments.csv
│   └── customer_cluster_profiles.csv
│
├── requirements.txt
├── .gitignore
└── README.md
```

*Note: The structure above lists key project artifacts. File availability may vary; raw dataset files and local database credentials should not be committed to GitHub.*

## 📊 Analysis Performed

### 1. Data Quality and SQL Analytics

- Checked source-table row counts and data quality.
- Analyzed delivered orders and purchase timestamps.
- Aggregated product revenue, freight, and payment values.
- Created customer-level purchase summaries.

### 2. RFM Customer Segmentation

RFM analysis evaluates customers based on:

- **Recency:** How recently a customer purchased.
- **Frequency:** How often a customer purchased.
- **Monetary Value:** How much a customer spent.

Customers were classified into seven segments:

- Champions
- Loyal Customers
- Potential Loyalists
- Recent Customers
- At Risk
- Hibernating
- Needs Attention

The existing segmentation contains 93,358 customers.

### 3. Customer Retention Analysis

Cohort analysis groups customers by their first purchase month and tracks subsequent purchasing activity.

The analysis includes:

- Monthly active customers
- Cohort sizes
- Active customers by cohort month
- Retention percentages over time

### 4. Customer Clustering

K-Means clustering was evaluated to explore differences in customer purchasing behavior.

**Recorded evaluation result:**

- Selected number of clusters: 2
- Silhouette score: approximately 0.7118
- Cluster 0: 90,557 customers (approximately 97%)
- Cluster 1: 2,801 customers (approximately 3%)

The smaller cluster showed higher average purchase frequency and monetary value in the recorded results. The clusters are useful for exploration, but should be validated before being used for business decisions.

### 5. Churn Prediction

A baseline Logistic Regression model was evaluated using historical customer features, including recency, order count, historical revenue, and average order value.

Recorded evaluation results:

- ROC-AUC: approximately 0.6036
- Accuracy: approximately 57%
- The churn labels were highly imbalanced, with approximately 99.44% labeled as churned.

These results indicate limited predictive performance. The class imbalance and churn definition need further investigation before the model can be considered reliable for targeting customers.

## 💡 Key Findings

- The RFM analysis identifies distinct customer groups with different purchasing patterns.
- The recorded K-Means results indicate a large low-frequency group and a smaller group with higher average spending and frequency.
- Cohort analysis provides a way to monitor repeat purchasing behavior over time.
- The churn dataset is highly imbalanced, making accuracy alone an unsuitable measure of model quality.
- Further work is needed to improve churn labels, evaluate alternative models, and validate retention strategies.

## 📈 Power BI Dashboard

The project includes business overview and customer retention dashboard work.

Planned dashboard content includes:

- Revenue and order KPIs
- Customer segment distribution
- Monthly customer activity
- Cohort retention matrix
- Interactive filters and slicers

Dashboard screenshots and the Power BI `.pbix` file will be added when available.

## 🚀 Getting Started

### Prerequisites

- MySQL 8.0 or compatible version
- Python 3
- Git
- Power BI Desktop for dashboard exploration

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/akshayasamala2608-code/ecommerce-customer-analytics.git
   cd ecommerce-customer-analytics
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python -m venv venv
   ```

   On Windows PowerShell:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Download the Olist dataset from its original source and place the CSV files in the local `data/raw/` directory. The raw files are not included in this repository.

5. Create the MySQL database and import the source tables.

6. Review the SQL files in the `sql/` folder. Execute the data-quality checks first. Review table-creation scripts carefully and adapt them to your database before running them.

## 🔮 Future Improvements

- Improve churn labeling and handle class imbalance.
- Compare additional classification models and evaluation metrics.
- Validate customer clusters and refine segment definitions.
- Add dashboard screenshots and the final Power BI report.
- Automate the analytics workflow and document reproducible results.

## 👩‍💻 Author

**Akshaya Samala**  
B.Tech, Computer Science and Engineering – Data Science

Interested in Data Analytics, SQL, Python, Machine Learning, and business intelligence.

[GitHub Profile](https://github.com/akshayasamala2608-code)
