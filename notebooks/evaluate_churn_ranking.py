import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    precision_score,
    recall_score
)

# Load saved test predictions
df = pd.read_csv("outputs/churn_test_predictions.csv")

# Actual label: 1 = churned, 0 = returned
actual_churn = df["actual_churn"]

# Model risk score
model_risk = df["churn_risk_probability"]

# Compare top 500 customers by predicted churn risk
top_n = min(500, len(df))

model_top = df.nlargest(
    top_n, "churn_risk_probability"
)

print("===== MODEL RANKING =====")
print("Customers ranked:", top_n)
print(
    "Churn rate in selected group:",
    round(model_top["actual_churn"].mean() * 100, 2),
    "%"
)

# Compare with a simple recency-only rule.
# Recreate the comparison using the original dataset.
features = pd.read_csv("outputs/customer_churn_dataset.csv")

test_ids = set(df["customer_unique_id"])
test_features = features[
    features["customer_unique_id"].isin(test_ids)
].copy()

# Merge actual labels from saved predictions
test_features = test_features.merge(
    df[["customer_unique_id", "actual_churn"]],
    on="customer_unique_id",
    suffixes=("", "_test")
)

# Higher recency means the customer has been
# inactive longer, so rank by recency descending.
recency_top = test_features.nlargest(
    top_n, "recency_days"
)

print("\n===== RECENCY-ONLY COMPARISON =====")
print(
    "Churn rate in selected group:",
    round(recency_top["actual_churn"].mean() * 100, 2),
    "%"
)

print("\n===== MODEL PRECISION-RECALL SUMMARY =====")
print(
    "Average precision for churn:",
    round(
        average_precision_score(
            actual_churn, model_risk
        ),
        4
    )
)
