import networkx as nx
import matplotlib.pyplot as plt
import nxviz as nv
from nxviz import annotate
import collections


def rotate_graph_90_degree(g):
    values = []
    for node in g.nodes():
        values.append(g.nodes()[node]["sort"])
    values.sort()
    values = values[(-(round(len(values) / 5))):]
    for node in g.nodes():
        if g.nodes()[node]["sort"] in values:
            g.nodes()[node]["sort"] += -1000


def add_padding(g, sort_value):
    for i in range(1, 30):
        node_value = i * " "
        g.add_node(node_value)
        g.nodes()[node_value]["group"] = " "
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
    return sort_value


def create_graph(filtered_matrix, groups):
    G = nx.from_numpy_array(filtered_matrix, groups).to_directed()
    left = groups[0]
    right = groups[1]
    other = groups[2]
    sort_value = 0
    sort_value = add_padding(G, sort_value)
    sort_value = add_values(G,
                            collections.OrderedDict(sorted(left.items())).items(),
                            sort_value)
    sort_value = add_values(G,
                            other.items(),
                            sort_value)
    add_values(G,
               collections.OrderedDict(sorted(right.items(), reverse=True)).items(),
               sort_value)

    rotate_graph_90_degree(G)
    nv.circos(G,
              node_color_by="group",
              sort_by="sort",
              edge_color_by="source_node_color",
              node_alpha_by="transparent")
    annotate.node_colormapping(G,
                               color_by="group",
                               legend_kwargs={"loc": "lower left", "bbox_to_anchor": (0.0, 1.0)})
    plt.show()
