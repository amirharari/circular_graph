import networkx as nx
import matplotlib.pyplot as plt
import nxviz as nv
from src import data_loader
import numpy as np


connectivity_matrix, groups = data_loader.load_data(
    "data/examples/connectivity_matrices/atlas-brainnetome_count-1M_scale-length_connectome.csv",
    "data/examples/parcellation_schemes/BNA_with_cerebellum.csv",
    "Lobe",
    "Label",
    "ROIname",
)


G = nx.from_numpy_array(filtered_matrix, groups)
nv.CircosPlot(G)
plt.show()
