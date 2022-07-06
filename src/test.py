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

def normalize_threshold(connectivity_matrix, threshold = 0.5):
    """
    This function gets a connectivity matrix and normalize its values between 0 to 1. 
    After normalization, the function zero the matrix values that are lower than  the threshold

    Parameters 
    ----------
    connectivity_matrix: np.ndarray
        n X n matrix where n is the number of ROIs in  the atlas. 
        Each cell in the matrix describes the connection between each pair of ROIs.
    
    threshold: float
        A float between 0 to 1 by. Values lower than threshold are set to zero.
    
    Returns
    -------
    filtered_matrix: np.ndarray
        connecitivty matrix after thresholding and normalization
    """
    if threshold < 0 or threshold > 1:
        raise ValueError("Threshold value must be between 0-1!")

    normalized_connectivity_matrix = (connectivity_matrix - np.min(connectivity_matrix)) / (np.max(connectivity_matrix) - np.min(connectivity_matrix))
    
    filtered_matrix = normalized_connectivity_matrix
    filtered_matrix[normalized_connectivity_matrix < threshold] = 0

    return filtered_matrix
    

G = nx.from_numpy_array(filtered_matrix, groups)
nv.CircosPlot(G)
plt.show()
