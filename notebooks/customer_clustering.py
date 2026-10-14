
# ============================================
# E-commerce Customer Analytics
# Phase 07: K-Means Customer Clustering
# ============================================

import os
import joblib
import numpy as np
import pandas as pd
import mysql.connector

from getpass import getpass
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# --------------------------------------------
# 1. Connect to MySQL
# --------------------------------------------

DB_PASSWORD = getpass("Enter your MySQL password: ")

connection = None

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aksh@2608",
        database="ecommerce_analytics"
    )

    print("\nMySQL connection successful!")

    # ----------------------------------------
    # 2. Load customer RFM data
    # ----------------------------------------

    query = """
        SELECT
            customer_unique_id,
            recency_days,
            frequency,
            monetary_value
        FROM customer_rfm
    """

    df = pd.read_sql(query, connection)

finally:
    if connection is not None and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")

# --------------------------------------------
# 3. Validate the data
# --------------------------------------------

print("\nOriginal dataset shape:", df.shape)

features = [
    "recency_days",
    "frequency",
    "monetary_value"
]

df = df.drop_duplicates(subset=["customer_unique_id"]).copy()

df[features] = df[features].apply(
    pd.to_numeric, errors="coerce"
)

if df[features].isnull().any().any():
    raise ValueError(
        "Missing or invalid RFM values found. "
        "Inspect the data before training."
    )

if not np.isfinite(df[features].to_numpy()).all():
    raise ValueError("Infinite values found in RFM features.")

if (df["recency_days"] < 0).any():
    raise ValueError("Negative recency values found.")

if (df["frequency"] < 1).any():
    raise ValueError("Invalid frequency values found.")

if (df["monetary_value"] < 0).any():
    raise ValueError("Negative monetary values found.")

print("Data validation successful!")
print("Unique customers:", len(df))

# --------------------------------------------
# 4. Prepare features
# --------------------------------------------

X = df[features].copy()

# Log transformation reduces the effect of
# highly skewed frequency and spending values.
# It also makes the scale of recency less skewed.
X_log = np.log1p(X)

# Scale features so they contribute on comparable
# numerical scales to the K-Means distance.
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_log)

print("\nFeatures prepared and scaled.")
print("Features used:", features)

# --------------------------------------------
# 5. Compare different cluster counts
# --------------------------------------------

os.makedirs("outputs", exist_ok=True)
os.makedirs("models", exist_ok=True)

results = []

# Test between 2 and 6 clusters.
# Silhouette is calculated on a sample for speed.
for k in range(2, 9):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X_scaled)

    score = silhouette_score(
        X_scaled,
        labels,
        sample_size=min(10000, len(X_scaled)),
        random_state=42
    )

    results.append({
        "k": k,
        "inertia": model.inertia_,
        "silhouette_score": score
    })

    print(
        f"K = {k} | "
        f"Inertia = {model.inertia_:.2f} | "
        f"Silhouette = {score:.4f}"
    )

results_df = pd.DataFrame(results)

results_df.to_csv(
    "outputs/kmeans_evaluation.csv",
    index=False
)

# Select the best silhouette score among
# the tested cluster counts.
best_k = int(
    results_df.loc[
        results_df["silhouette_score"].idxmax(), "k"
    ]
)

print("\nBest candidate cluster count:", best_k)

# --------------------------------------------
# 6. Train the final K-Means model
# --------------------------------------------

kmeans = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=10
)

df["cluster"] = kmeans.fit_predict(X_scaled)

print("\nFinal K-Means model trained!")

# --------------------------------------------
# 7. Inspect cluster profiles
# --------------------------------------------

cluster_profile = df.groupby("cluster").agg(
    customer_count=("customer_unique_id", "count"),
    avg_recency_days=("recency_days", "mean"),
    avg_frequency=("frequency", "mean"),
    avg_monetary_value=("monetary_value", "mean"),
    median_recency_days=("recency_days", "median"),
    median_frequency=("frequency", "median"),
    median_monetary_value=("monetary_value", "median")
).round(2)

cluster_profile["customer_percentage"] = (
    100 * cluster_profile["customer_count"] / len(df)
).round(2)

print("\nCustomer Cluster Profiles:")
print(cluster_profile)

# --------------------------------------------
# 8. Save customer predictions and model
# --------------------------------------------

df.to_csv(
    "outputs/customer_cluster_assignments.csv",
    index=False
)

cluster_profile.to_csv(
    "outputs/customer_cluster_profiles.csv"
)

joblib.dump(
    {
        "scaler": scaler,
        "kmeans": kmeans,
        "features": features,
        "log_transform": "numpy.log1p",
        "selected_k": best_k
    },
    "models/customer_kmeans_model.joblib"
)

print("\nFiles saved:")
print("- outputs/kmeans_evaluation.csv")
print("- outputs/customer_cluster_assignments.csv")
print("- outputs/customer_cluster_profiles.csv")
print("- models/customer_kmeans_model.joblib")

print("\nK-Means clustering completed successfully!")
