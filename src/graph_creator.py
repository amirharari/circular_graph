import networkx as nx
import matplotlib.pyplot as plt
import nxviz as nv
from nxviz import annotate
import collections
from random import randint
import numpy as np
import pandas as pd

def rotate_graph_90_degree(g):
    values = []
    for node in g.nodes():
        values.append(g.nodes()[node]["sort"])
    values.sort()
    values = values[(-(round(len(values) / 4.6))):]
    for node in g.nodes():
        if g.nodes()[node]["sort"] in values:
            g.nodes()[node]["sort"] += -1000


def add_padding(g, padding_size, sort_value):
    for i in range(padding_size):
        node_value = i * randint(1,1000000)
        g.add_node(node_value)
        g.nodes()[node_value]["group"] = "_"
        g.nodes()[node_value]["transparent"] = 0
        g.nodes()[node_value]["sort"] = sort_value
        sort_value += 1
    return sort_value


def add_values(g, items, sort_value):
    for k1, v1 in items:
        for i1 in v1:
            g.nodes()[i1[0]]["group"] = k1
            g.nodes()[i1[0]]["transparent"] = 1
            g.nodes()[i1[0]]["sort"] = sort_value
            sort_value += 1
        sort_value = add_padding(g,
                                 5,
                                 sort_value)
    return sort_value


def create_graph(filtered_matrix, groups):
    g = nx.from_numpy_array(filtered_matrix, groups).to_directed()
    left = groups[0]
    right = groups[1]
    other = groups[2]
    sort_value = 0
    sort_value = add_padding(g,
                             30,
                             sort_value)
    sort_value = add_values(g,
                            collections.OrderedDict(sorted(left.items())).items(),
                            sort_value)
    sort_value = add_values(g,
                            other.items(),
                            sort_value)
    add_values(g,
               collections.OrderedDict(sorted(right.items(), reverse=True)).items(),
               sort_value)
    
    rotate_graph_90_degree(g)
    nx.set_edge_attributes(g, {e:np.sqrt(w) for e, w in nx.get_edge_attributes(g, 'weight').items()}, 'sqrt_weight')
    nv.circos(g,
              node_color_by="group",
              sort_by="sort", 
              node_alpha_by="transparent", 
              edge_alpha_by = "sqrt_weight",
              lw_by = "sqrt_weight")
    annotate.node_colormapping(g,
                               color_by="group",
                               legend_kwargs={"loc": "lower left", "bbox_to_anchor": (0.0, 1.0)})
    plt.show()
