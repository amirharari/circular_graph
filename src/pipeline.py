from src.Circular_graph import Circular_graph


"""Run as Class: Circular_graph
Enter the connectivity map of interest.
Enter the Brain Atlas of interest.
"""
conmat = "BNA_with_cerebellum.csv"
atlas = "atlas-brainnetome_count-1M_scale-length_connectome.csv"
conmat_path = "data/examples/connectivity_matrices/{}".format(atlas)
atlas_path = "data/examples/parcellation_schemes/{}".format(conmat)

bna = Circular_graph(conmat_path, atlas_path)
bna.show_graph()
