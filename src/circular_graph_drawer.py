from tokenize import group

import data_loader
import graph_drawer


def create_graph(connectivity_matrix, atlas_path, grouping_name, calculating_field_name):
    label_and_values = data_loader.load_data(connectivity_matrix, atlas_path,
                                             grouping_name, calculating_field_name)
    graph_drawer.draw_graph(label_and_values)
