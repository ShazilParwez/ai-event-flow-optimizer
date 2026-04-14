import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from sklearn.cluster import KMeans


def classify_crowd(data):
    # Validation
    if data is None or data.empty:
        raise ValueError("Input data is empty")

    if "area_name" not in data.columns or "density" not in data.columns:
        raise ValueError("Missing required columns")

    # Aggregate density per area
    area_metrics = (
        data.groupby("area_name")["density"]
        .sum()
        .reset_index(name="total_density")
    )

    # 🔥 RETURN DICTIONARY INSTEAD OF LIST
    labels = {}

    for _, row in area_metrics.iterrows():
        area = row["area_name"]
        val = row["total_density"]

        if val < 60:
            labels[area] = "Low"
        elif val < 120:
            labels[area] = "Medium"
        else:
            labels[area] = "High"

    return labels

    # KMeans clustering
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    area_metrics["cluster"] = kmeans.fit_predict(
        area_metrics[["total_density"]]
    )

    # Map clusters → labels
    cluster_centers = kmeans.cluster_centers_.flatten()
    sorted_clusters = sorted(
        enumerate(cluster_centers), key=lambda x: x[1]
    )

    label_map = {
        sorted_clusters[0][0]: "Low",
        sorted_clusters[1][0]: "Medium",
        sorted_clusters[2][0]: "High",
    }

    area_metrics["level"] = area_metrics["cluster"].map(label_map)

    return area_metrics["level"].tolist()