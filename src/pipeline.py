

from src.graph_creator import create_graph
from src.normalize_threshold import normalize_threshold
from src.data_loader import load_data
import networkx as nx

connectivity_matrix, groups = load_data(
    "data/examples/connectivity_matrices/atlas-brainnetome_count-1M_scale-length_connectome.csv",
    "data/examples/parcellation_schemes/BNA_with_cerebellum.csv",
    "Lobe",
    "Label",
    "ROIname",)
filtered_matrix = normalize_threshold(connectivity_matrix, threshold = 0.5)
graph = create_graph(filtered_matrix,groups)
