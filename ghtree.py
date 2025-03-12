import networkx as nx
import pandas as pd
from tqdm import tqdm
import numpy as np

def process_clustering_network_part(csv_path, leiden_col, target_cluster, output_ttree_path, output_gtree_path):
    clustering_df = pd.read_csv(csv_path, index_col=0)
    print("previous: ")
    print(clustering_df.head())
    G = nx.Graph()
    if leiden_col in clustering_df.columns:
        cells_in_cluster = clustering_df[clustering_df[leiden_col] == target_cluster].index.tolist()
        new_node = 0  
        print(f"New node for {leiden_col} cluster {target_cluster}: {new_node}")
        for cell in cells_in_cluster:
            if cell in G:
                neighbors = list(G.neighbors(cell))
                for neighbor in neighbors:
                    G.remove_edge(cell, neighbor)
            if G.has_edge(cell, new_node):
                G[cell][new_node]['weight'] += 1
            else:
                G.add_edge(cell, new_node, weight=1)

        for col in tqdm(clustering_df.columns):
            if col == leiden_col:
                unique_clusters = clustering_df[col].unique()
                unique_clusters = unique_clusters[unique_clusters != target_cluster] 
            else:
                unique_clusters = clustering_df[col].unique()
            
            for cluster in tqdm(unique_clusters):
                cells_in_cluster = clustering_df[clustering_df[col] == cluster].index.tolist()
                for i in range(len(cells_in_cluster)):
                    for j in range(i + 1, len(cells_in_cluster)):
                        cell1, cell2 = cells_in_cluster[i], cells_in_cluster[j]
                        if cell1 in cells_in_cluster:
                            cell1 = new_node
                        if cell2 in cells_in_cluster:
                            cell2 = new_node
                        if G.has_edge(cell1, cell2):
                            G[cell1][cell2]['weight'] += 1
                        else:
                            G.add_edge(cell1, cell2, weight=1)

    nx.write_graphml(G, output_gtree_path)
    print(f"G save to '{output_gtree_path}'")

    for u, v, data in tqdm(G.edges(data=True)):
        if 'weight' in data:
            G[u][v]['capacity'] = data['weight']
    T = nx.gomory_hu_tree(G)
    
    nx.write_graphml(T, output_ttree_path)
    print(f"Ttree save to '{output_ttree_path}'")

def process_clustering_network_all(csv_path, output_gtree_path, output_ttree_path):
    clustering_df = pd.read_csv(csv_path, index_col=0)
    print("Reading clustering data")
    print(clustering_df.head())

    G = nx.Graph()
    for col in clustering_df.columns:
        print(f"Processing column {col}")
        unique_clusters = clustering_df[col].unique()
        for cluster in tqdm(unique_clusters):
            cells_in_cluster = clustering_df[clustering_df[col] == cluster].index.tolist()
            for i in range(len(cells_in_cluster)):
                for j in range(i + 1, len(cells_in_cluster)):
                    cell1, cell2 = cells_in_cluster[i], cells_in_cluster[j]
                    if G.has_edge(cell1, cell2):
                        G[cell1][cell2]['weight'] += 1
                    else:
                        G.add_edge(cell1, cell2, weight=1)

    print("Calculating edge capacities")
    for u, v, data in tqdm(G.edges(data=True)):
        if 'weight' in data:
            G[u][v]['capacity'] = data['weight']

    print("Calculating Gomory-Hu tree")
    T = nx.gomory_hu_tree(G)

    print("Saving G")
    nx.write_graphml(G, output_gtree_path)
    print(f"Graph G saved to {output_gtree_path}")

    print("Saving T")
    nx.write_graphml(T, output_ttree_path)
    print(f"Tree T saved to {output_ttree_path}")
