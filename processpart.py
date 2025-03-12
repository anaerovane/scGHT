import pandas as pd
import numpy as np
import networkx as nx

def process_clustering_part(graphml_path, csv_path, leiden_col, target_cluster, start_node, threshold, new_col_name, output_path):
    T = nx.read_graphml(graphml_path)
    clustering_df = pd.read_csv(csv_path, index_col=0)
    print("previous:")
    print(clustering_df.head())
    
    if leiden_col in clustering_df.columns:
        cells_in_cluster = clustering_df[clustering_df[leiden_col] == target_cluster].index.tolist()
    else:
        raise ValueError(f"column '{leiden_col}' no exists")

    leiden_cluster_node = [str(obj) for obj in cells_in_cluster]
    edge_weights = [data['weight'] for u, v, data in T.edges(data=True)]
    percentile_10 = np.percentile(edge_weights, 10)
    percentile_20 = np.percentile(edge_weights, 20)
    percentile_25 = np.percentile(edge_weights, 25)
    percentile_33 = np.percentile(edge_weights, 33)
    percentile_50 = np.percentile(edge_weights, 50)
    print("\n cankao")
    print(f"10%: {percentile_10}")
    print(f"20%: {percentile_20}")
    print(f"25%: {percentile_25}")
    print(f"33%: {percentile_33}")
    print(f"50%: {percentile_50}")

    def minimum_edge_weight_in_shortest_path(T, u, v):
        path = nx.shortest_path(T, u, v, weight="weight")
        min_weight = float('inf')
        min_edge = None
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            weight = T[u][v]["weight"]
            if weight < min_weight:
                min_weight = weight
                min_edge = (u, v)
        return min_weight, min_edge

    coun = [node for node in T.nodes() if node not in leiden_cluster_node]
    added_nodes = {start_node}

    for node in coun:
        if node == start_node:
            continue
        min_cut, _ = minimum_edge_weight_in_shortest_path(T, start_node, node)
        if min_cut < threshold:
            added_nodes.add(node)

    print("\nAdded nodes:", added_nodes)
    clustering_df[new_col_name] = clustering_df[leiden_col]

    valid_added_nodes = [int(node) for node in added_nodes if int(node) in clustering_df.index]
    clustering_df.loc[valid_added_nodes, new_col_name] = target_cluster
    print("after:")
    print(clustering_df.head())
    clustering_df.to_csv(output_path)
    print(f"\nUpdated clustering results saved to '{output_path}'")