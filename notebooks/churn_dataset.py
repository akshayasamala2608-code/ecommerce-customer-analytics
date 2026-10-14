import pandas as pd
import numpy as np
import mysql.connector
from getpass import getpass
from pathlib import Path

# -----------------------------------------
# 1. Set the observation and label periods
# -----------------------------------------

OBSERVATION_DATE = pd.Timestamp("2018-06-01")
PREDICTION_DAYS = 90
LABEL_END_DATE = OBSERVATION_DATE + pd.Timedelta(
    days=PREDICTION_DAYS
)

print("Observation date:", OBSERVATION_DATE.date())
print("Label window ends:", LABEL_END_DATE.date())

# -----------------------------------------
# 2. Connect to MySQL and load orders
# -----------------------------------------

password = getpass("Enter your MySQL password: ")
connection = None

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="ecommerce_analytics"
    )

    query = """
        SELECT
            o.order_id,
            c.customer_unique_id,
            o.order_purchase_timestamp,
            o.order_status,
            COALESCE(items.order_revenue, 0) AS order_revenue
        FROM orders AS o
        JOIN customers AS c
            ON o.customer_id = c.customer_id
        LEFT JOIN (
            SELECT
                order_id,
                SUM(price) AS order_revenue
            FROM order_items
            GROUP BY order_id
        ) AS items
            ON o.order_id = items.order_id
        WHERE o.order_purchase_timestamp IS NOT NULL
    """

    orders = pd.read_sql(query, connection)

finally:
    if connection is not None and connection.is_connected():
        connection.close()

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

print("\nOrders loaded:", len(orders))
print(
    "Latest order date:",
    orders["order_purchase_timestamp"].max()
)

# -----------------------------------------
# 3. Check follow-up data availability
# -----------------------------------------

latest_date = orders["order_purchase_timestamp"].max()

if pd.isna(latest_date) or latest_date < LABEL_END_DATE:
    raise ValueError(
        "Insufficient order history for the full "
        "90-day label window. Choose an earlier "
        "observation date and rerun."
    )

# Qualifying purchases exclude cancelled and
# unavailable orders. This rule defines the
# behavior we want the model to predict.
qualifying_statuses = [
    "delivered",
    "shipped",
    "invoiced",
    "approved",
    "processing"
]

qualifying_orders = orders[
    orders["order_status"].isin(qualifying_statuses)
].copy()

# -----------------------------------------
# 4. Build historical customer features
# -----------------------------------------

historical = qualifying_orders[
    qualifying_orders["order_purchase_timestamp"]
    < OBSERVATION_DATE
].copy()

# Use customers with at least one historical
# qualifying purchase.
customer_features = historical.groupby(
    "customer_unique_id"
).agg(
    last_purchase_date=("order_purchase_timestamp", "max"),
    historical_order_count=("order_id", "nunique"),
    historical_revenue=("order_revenue", "sum")
).reset_index()

customer_features["recency_days"] = (
    OBSERVATION_DATE
    - customer_features["last_purchase_date"]
).dt.days

customer_features["average_order_value"] = (
    customer_features["historical_revenue"]
    / customer_features["historical_order_count"]
)

# -----------------------------------------
# 5. Create the churn label
# -----------------------------------------

future = qualifying_orders[
    (
        qualifying_orders["order_purchase_timestamp"]
        >= OBSERVATION_DATE
    )
    &
    (
        qualifying_orders["order_purchase_timestamp"]
        < LABEL_END_DATE
    )
]

future_customer_ids = set(
    future["customer_unique_id"].unique()
)

customer_features["churn"] = (
    ~customer_features["customer_unique_id"].isin(
        future_customer_ids
    )
).astype(int)

# -----------------------------------------
# 6. Validate the resulting dataset
# -----------------------------------------

feature_columns = [
    "recency_days",
    "historical_order_count",
    "historical_revenue",
    "average_order_value"
]

if customer_features[feature_columns + ["churn"]].isnull().any().any():
    raise ValueError(
        "Missing values found. Inspect before modeling."
    )

if not np.isfinite(
    customer_features[feature_columns].to_numpy()
).all():
    raise ValueError("Infinite feature values found.")

print("\nChurn dataset shape:", customer_features.shape)

print("\nChurn label counts:")
print(customer_features["churn"].value_counts())

print("\nChurn label percentages:")
print(
    (customer_features["churn"].value_counts(normalize=True) * 100)
    .round(2)
)

print("\nFeature summary:")
print(customer_features[feature_columns].describe().round(2))

# -----------------------------------------
# 7. Save the dataset
# -----------------------------------------

Path("outputs").mkdir(exist_ok=True)

output_path = "outputs/customer_churn_dataset.csv"

customer_features.to_csv(output_path, index=False)

print("\nSaved:", output_path)
print("Churn dataset created successfully!")
