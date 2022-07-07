from circular_graph import circular_graph
from normalizer import normalize_and_set_threshold
from data_loader import load_data

"""Run as Class: Circular_graph
Enter the connectivity map of interest.
Enter the Brain Atlas of interest.
"""
"""Run as functions"""
connectivity_matrix, groups = \
    load_data(
        "../data/examples/connectivity_matrices/atlas-brainnetome_count-1M_scale-length_connectome.csv",
        "../data/examples/parcellation_schemes/BNA_with_cerebellum.csv",
        "Lobe",
        "Label",
        "ROIname",
    )
filter_normalized_matrix = normalize_and_set_threshold(connectivity_matrix, threshold=0.5)
bna = circular_graph(filter_normalized_matrix, groups)
bna.show_graph()
