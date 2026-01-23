import pandas as pd
from collections import defaultdict

def build_clusters(df, min_type=("SIMILAR", "DUPLICATE")):
    """
    Construye clusters de requisitos basados en matches similares/duplicados
    
    Args:
        df: DataFrame con columnas ID1, ID2, Match_Type
        min_type: Tuple de tipos de match a considerar
    
    Returns:
        List de sets, cada uno es un cluster de requirement_ids
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

    return clusters
