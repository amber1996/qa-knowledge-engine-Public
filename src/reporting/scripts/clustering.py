import pandas as pd
from collections import defaultdict

def build_clusters(
    df,
    all_ids=None,
    min_type=("SIMILAR", "DUPLICATE"),
    cluster_prefix="CLUSTER_AUTHENTICATION_ACCESS"
):
    """
    Build requirement clusters based on similarity/duplicate matches
    """

    graph = defaultdict(set)

    for _, row in df.iterrows():
        if row["Match_Type"] in min_type:
            graph[row["ID1"]].add(row["ID2"])
            graph[row["ID2"]].add(row["ID1"])

    visited = set()
    clusters = []

    for node in graph:
        if node not in visited:
            stack = [node]
            cluster = set()

            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    cluster.add(current)
                    stack.extend(graph[current] - visited)

            clusters.append(cluster)
                
    # Add singletons (no matches)
    if all_ids:
        matched = set().union(*clusters) if clusters else set()
        for rid in set(all_ids) - matched:
            clusters.append({rid})

    # Assign readable cluster names
    named_clusters = {}
    for i, cluster in enumerate(clusters, start=1):
        cluster_name = f"{cluster_prefix}_{i:02d}"
        for rid in cluster:
            named_clusters[rid] = cluster_name

    return clusters
