# scGHT

We connect identical classifications across different clusters to form a graph and then generate a Gomory-Hu tree on this graph. Subsequently, we perform joint learning of clustering on the minimum cut tree, optimizing the boundaries of the clusters. This optimization process includes global boundary contraction optimization (the “all” part) and single-category boundary extension optimization (the “part” part).



## Contact

Email: 2210454@mail.nankai.edu.cn (Wuzheng Dong) , 2210455@mail.nankai.edu.cn (Yujuan Zhu)



## Installation

```bash
git clone https://github.com/anaerovane/scGHT.git
cd scGHT
conda create -n scGHT python==3.12
conda activate scGHT
pip install -r requirements.txt
```



## Usage_ALL

#### Construct Gomory-Hu tree (CPU)

```python
from ghtree import process_clustering_network_all
process_clustering_network_all(
    csv_path='clustering_results.csv',
    output_gtree_path="Gtree0312.graphml",
    output_ttree_path="Ttree0312.graphml"
)
```

#### Construct Gomory-Hu tree (GPU)

```python
from GPUghtree import process_clustering_network_all
GPUprocess_clustering_network_all(
    csv_path='clustering_results.csv',
    output_gtree_path="Gtree0312.graphml",
    output_ttree_path="Ttree0312.graphml"
)
```
#### Process Gomory-Hu tree 

```python
from processpart import process_clustering_all
process_clustering_all(
T_file="Ttree0312.graphml", 
clustering_file="clustering_results0313.csv", 
initial_clustering_method="leiden",
threshold1=1700, 
threshold2=1900,
task=1)
```

You can find the process example on **example_all.ipynb**



## Usage_PART

#### Construct Gomory-Hu tree (CPU)

```python
from ghtree import process_clustering_network_part, process_clustering_network_all
process_clustering_network_part(
    csv_path='clustering_results0313.csv',
    leiden_col='leiden',
    target_cluster=2,
    output_ttree_path="Ttree0313T.graphml",
    output_gtree_path="Gtree0313G.graphml"
)
```

#### Construct Gomory-Hu tree (GPU)

```python
from GPUghtree import process_clustering_network_part, process_clustering_network_all
GPUprocess_clustering_network_part(
    csv_path='clustering_results0313.csv',
    leiden_col='leiden',
    target_cluster=2,
    output_ttree_path="Ttree0313T.graphml",
    output_gtree_path="Gtree0313G.graphml"
)
```
#### Process Gomory-Hu tree 

```python
from processpart import process_clustering_part
process_clustering_part(
    graphml_path="Ttree0313.graphml",
    csv_path='clustering_results.csv',
    leiden_col='leiden',
    target_cluster=2,
    start_node="0",
    threshold=1800,
    new_col_name='leiden_new',
    output_path='updated_clustering_results.csv'
)
```

You can find the process example on **example_part.ipynb**



## Result Shown



## Note

We conducted the tests on both Windows CPU systems and Ubuntu 22.04LTS GPU systems (with an Nvidia Tesla M40 GPU VRAM12G)

We are still making significant modifications and optimizations to the project



