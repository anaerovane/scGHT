import pandas as pd
import networkx as nx
from networkx.algorithms.flow import dinitz
from tqdm import tqdm
import numpy as np

def process_clustering_all(T_file, clustering_file, initial_clustering_method, threshold1, threshold2,task=1):
    T = nx.read_graphml(T_file)
    clustering_df = pd.read_csv(clustering_file, index_col=0)

    edge_weights = [data['weight'] for u, v, data in T.edges(data=True)]
    percentile_10 = np.percentile(edge_weights, 10)
    percentile_20 = np.percentile(edge_weights, 20)
    percentile_25 = np.percentile(edge_weights, 25)
    percentile_33 = np.percentile(edge_weights, 33)
    percentile_50 = np.percentile(edge_weights, 50)
    print("cankao")
    print(f"10%: {percentile_10}")
    print(f"20%: {percentile_20}")
    print(f"25%: {percentile_25}")
    print(f"33%: {percentile_33}")
    print(f"50%: {percentile_50}")

    if task==2:
        threshold1=np.percentile(edge_weights,threshold1)
        threshold2=np.percentile(edge_weights,threshold2)
    print(threshold1,threshold2)

    initial_clusters = clustering_df[initial_clustering_method].to_dict()
    unique_clusters = clustering_df[initial_clustering_method].unique().tolist()
    cluster_to_cells = {cluster: clustering_df[clustering_df[initial_clustering_method] == cluster].index.tolist() 
                        for cluster in unique_clusters}

    optimized_clusters = initial_clusters.copy()
    changed_cells = []
    discrete_cells = []

    def minimum_edge_weight_in_shortest_path(T, u, v):
        path = nx.shortest_path(T, u, v, weight="weight")
        min_weight = float('inf')
        min_edge = None
        for u_node, v_node in zip(path, path[1:]):
            weight = T[u_node][v_node]["weight"]
            if weight < min_weight:
                min_weight = weight
                min_edge = (u_node, v_node)
        return min_weight, path

    def calculate_min_cut_between_clusters(T, cluster1_cells, cluster2_cells):
        source = "source"
        sink = "sink"
        T.add_node(source)
        T.add_node(sink)
        for cell in cluster1_cells:
            T.add_edge(source, cell, weight=float('inf'))
        for cell in cluster2_cells:
            T.add_edge(cell, sink, weight=float('inf'))
        cut_value, path = minimum_edge_weight_in_shortest_path(T, source, sink)
        T.remove_nodes_from([source, sink])
        path.remove('source')
        path.remove('sink')
        
        return (cut_value, path)
    all_processed_nodes = set()  
    
    for i, cluster1 in enumerate(unique_clusters):
        for cluster2 in unique_clusters[i + 1:]:
            cluster1_cells1 = cluster_to_cells[cluster1]
            cluster2_cells2 = cluster_to_cells[cluster2]
            cluster1_cells = [str(item) for item in cluster1_cells1]
            cluster2_cells = [str(item) for item in cluster2_cells2]
            T_copy = T.copy()
            cut_value, path = calculate_min_cut_between_clusters(T_copy, cluster1_cells, cluster2_cells)
            
            if cut_value < threshold1: 
                min_weight = float('inf')
                min_edge = None
                for u, v in zip(path, path[1:]):
                    if u in T.nodes and v in T.nodes:
                        weight = T[u][v]["weight"]
                        if weight < min_weight:
                            min_weight = weight
                            min_edge = (u, v)
                
                if min_edge is not None:
                    for node in path:
                        if node in all_processed_nodes:
                            continue 
                        max_weight = -float('inf')
                        best_cluster = None
                        for cluster in unique_clusters:
                            cluster_cells = cluster_to_cells[cluster]
                            weights = []
                            for neighbor in T.neighbors(node):
                                if neighbor in cluster_cells:
                                    weights.append(T[node][neighbor]["weight"])
                            if weights:
                                current_max = max(weights)
                                if current_max > max_weight:
                                    max_weight = current_max
                                    best_cluster = cluster

                        if max_weight > threshold2 and best_cluster is not None:
                            if node not in cluster_to_cells[best_cluster]:
                                optimized_clusters[node] = best_cluster
                                changed_cells.append((node, initial_clusters[node], best_cluster))
                                all_processed_nodes.add(node)
                        else:
                            discrete_cells.append(node)
                            all_processed_nodes.add(node)

    print("Cells with changed clusters:")
    for cell, old_cluster, new_cluster in changed_cells:
        print(f"Cell {cell} changed from Cluster {old_cluster} to Cluster {new_cluster}")
    
    print("Discrete cells:", discrete_cells)

    clustering_df['optimized_' + initial_clustering_method] = clustering_df.index.map(optimized_clusters)
    final_clustering_results = clustering_df[[initial_clustering_method, 'optimized_' + initial_clustering_method]]
    final_clustering_results.to_csv('final_clustering_results.csv', index=True)
    
    print("Final clustering results saved to 'final_clustering_results.csv'.")
    print("Summary of changes:")
    print(final_clustering_results.head())
