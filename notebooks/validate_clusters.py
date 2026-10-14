import pandas as pd

# Load model evaluation results
evaluation = pd.read_csv("outputs/kmeans_evaluation.csv")

# Load customer cluster profiles
profiles = pd.read_csv("outputs/customer_cluster_profiles.csv")

print("\n===== CLUSTER EVALUATION =====")
print(evaluation.to_string(index=False))

print("\n===== CUSTOMER CLUSTER PROFILES =====")
print(profiles.to_string(index=False))

print("\n===== VALIDATION CHECKS =====")

# Check silhouette scores
best_row = evaluation.loc[
    evaluation["silhouette_score"].idxmax()
]

print(
    f"\nBest tested k: {int(best_row['k'])}"
)
print(
    f"Best silhouette score: "
    f"{best_row['silhouette_score']:.4f}"
)

# Check whether any cluster is very small
if "customer_percentage" in profiles.columns:
    print("\nSmallest cluster percentage:",
          profiles["customer_percentage"].min())

    print("Largest cluster percentage:",
          profiles["customer_percentage"].max())

print("\nValidation report generated.")
