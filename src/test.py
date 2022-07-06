import networkx as nx
import matplotlib.pyplot as plt
import nxviz as nv
import data_loader

a = data_loader.load_data(
'../data/examples/connectivity_matrices/atlas-brainnetome_count-1M_scale-length_connectome.csv',
'../data/examples/parcellation_schemes/BNA_with_cerebellum.csv',
'Lobe',
"Label",
"ROIname")
plt.show()
val = input("Enter your value: ")
