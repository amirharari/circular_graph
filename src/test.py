import networkx as nx
import matplotlib.pyplot as plt
import nxviz as nv
import data_loader
import nxviz as nz


normalized_connectivity_matrix, groups = data_loader.load_data(
    "../data/examples/connectivity_matrices/atlas-brainnetome_count-1M_scale-length_connectome.csv",
    "../data/examples/parcellation_schemes/BNA_with_cerebellum.csv",
    "Lobe",
    "Label",
    "ROIname",
)
Threshold = 0.5
filtered_matrix = normalized_connectivity_matrix
filtered_matrix[normalized_connectivity_matrix < Threshold] = 0
G = nx.from_numpy_array(filtered_matrix)
nz.CircosPlot(G)
plt.show()
