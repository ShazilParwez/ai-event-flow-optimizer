from sklearn.cluster import KMeans
import warnings


def classify_crowd(data):
    # Suppress sklearn convergence warnings for small datasets
    warnings.filterwarnings("ignore")

    # Aggregate density per semantic area
    area_metrics = (
        data.groupby("area_name")["density"].sum().to_frame(name="total_density")
    )

    # Re-introduce Machine Learning clustering (KMeans)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    area_metrics["raw_cluster"] = kmeans.fit_predict(area_metrics[["total_density"]])

    # KMeans assigns cluster labels (0, 1, 2) randomly. We must sort them by actual density
    cluster_means = (
        area_metrics.groupby("raw_cluster")["total_density"].mean().sort_values()
    )

    # Create an ordered mapping: Lowest -> 0, Middle -> 1, Highest -> 2
    remap_ordered = {
        old_label: new_label for new_label, old_label in enumerate(cluster_means.index)
    }
    area_metrics["zone_index"] = area_metrics["raw_cluster"].map(remap_ordered)

    # Map area results back to the main point data
    area_to_index = area_metrics["zone_index"].to_dict()
    data["zone_index"] = data["area_name"].map(area_to_index)

    # Explicitly override the Walkways (ambient crowd) to safely always be lowest density
    data.loc[data["area_name"] == "Walkways", "zone_index"] = 0

    # Apply the requested classification map
    zone_map = {0: "Low Density", 1: "Moderate Density", 2: "High Density / Congested"}

    data["zone_label"] = data["zone_index"].map(zone_map)

    return data
