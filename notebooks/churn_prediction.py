# ============================================
# E-commerce Customer Analytics
# Phase 07: Baseline Churn Prediction
# ============================================

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score,
    balanced_accuracy_score
)

# --------------------------------------------
# 1. Load the churn dataset
# --------------------------------------------

df = pd.read_csv("outputs/customer_churn_dataset.csv")

print("Dataset shape:", df.shape)

# Features available before the observation date
features = [
    "recency_days",
    "historical_order_count",
    "historical_revenue",
    "average_order_value"
]

X = df[features]

# Churn = 1 means no qualifying purchase
# during the following 90 days.
y = df["churn"].astype(int)

print("\nTarget distribution:")
print(y.value_counts())
print("\nTarget percentages:")
print((y.value_counts(normalize=True) * 100).round(2))

# --------------------------------------------
# 2. Split data into training and test sets
# --------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))

# --------------------------------------------
# 3. Build a baseline model
# --------------------------------------------

model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(
        class_weight="balanced",
        max_iter=2000,
        random_state=42
    ))
])

model.fit(X_train, y_train)

print("\nBaseline model trained!")

# --------------------------------------------
# 4. Evaluate churn predictions
# --------------------------------------------

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)

# Probability for churn = 1
churn_probability = probabilities[
    :, list(model.named_steps["classifier"].classes_).index(1)
]

print("\n===== CHURN CLASSIFICATION REPORT =====")
print(classification_report(
    y_test,
    predictions,
    labels=[0, 1],
    target_names=["Returned", "Churned"],
    zero_division=0
))

print("Confusion matrix (actual rows, predicted columns):")
print(confusion_matrix(y_test, predictions, labels=[0, 1]))

print(
    "\nBalanced accuracy:",
    round(balanced_accuracy_score(y_test, predictions), 4)
)

# ROC-AUC for churn as the positive class
print(
    "ROC-AUC:",
    round(roc_auc_score(y_test, churn_probability), 4)
)

# Evaluate ability to identify the rare returner class.
return_probability = 1 - churn_probability
return_actual = 1 - y_test

print(
    "Average precision for identifying returners:",
    round(
        average_precision_score(
            return_actual,
            return_probability
        ),
        4
    )
)

# --------------------------------------------
# 5. Save test-set risk predictions
# --------------------------------------------

os.makedirs("outputs", exist_ok=True)
os.makedirs("models", exist_ok=True)

results = df.loc[X_test.index, ["customer_unique_id"]].copy()
results["actual_churn"] = y_test
results["predicted_churn"] = predictions
results["churn_risk_probability"] = churn_probability

results = results.sort_values(
    "churn_risk_probability",
    ascending=False
)

results.to_csv(
    "outputs/churn_test_predictions.csv",
    index=False
)

joblib.dump(
    model,
    "models/churn_logistic_regression.joblib"
)

print("\nSaved:")
print("- outputs/churn_test_predictions.csv")
print("- models/churn_logistic_regression.joblib")
print("\nBaseline evaluation complete!")
