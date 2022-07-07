import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import nxviz as nv
from nxviz import annotate
import collections
from nv_graph_utils import rotate_node_by_count, add_padding, add_values


class circular_graph:
    """create an object of a brain atlas and connectivity matrix that can be represented as a circular graph
    with nodes as brain ROIs and width of edges representing the degree of connection between 2 ROIs"""

    def __init__(
            self,
            filtered_normalize_matrix,
            right_left_and_natural_groups) -> None:
        """
        Parameters
        ----------
        right_left_and_natural_groups: List<Dictionary<string,List<(int, string)>>
            List of dictionaries for each hemisphere. Each dictionary is divided by the grouping variable.
            The keys are the groups names. The values are lists of tuples, each tuple represents a ROI in the group.
            Each tuple contains the index of a ROI in the connectivity matrix (starting from zero) and the ROI name.
            for example:  {"Frontal lobe": [(0, precentral gyrus), (1, SFG), (2, MFG), (3, IFG)}
        filtered_matrix: np.ndarray
            connecitivty matrix after thresholding and normalization
        """
        self.rightLeftAndNaturalGroups = right_left_and_natural_groups
        self.filtered_normalize_matrix = filtered_normalize_matrix

    def show_graph(self):
        """
               This function encapsulate the logic of graph creation
        """
        g = nx.from_numpy_array(
            self.filtered_normalize_matrix, self.rightLeftAndNaturalGroups
        ).to_directed()
        nx.set_edge_attributes(
            g,
            {e: w * 3 for e, w in nx.get_edge_attributes(g, "weight").items()},
            "doubled_weight",
        )
        left = self.rightLeftAndNaturalGroups[0]
        right = self.rightLeftAndNaturalGroups[1]
        other = self.rightLeftAndNaturalGroups[2]
        sort_value = 0
        padding_size = 9
        sort_value = add_padding(g, padding_size, sort_value)
        sort_value = add_values(
            g, collections.OrderedDict(sorted(left.items())).items(), sort_value
        )
        sort_value = add_values(g, other.items(), sort_value)
        add_values(
            g,
            collections.OrderedDict(sorted(right.items(), reverse=True)).items(),
            sort_value,
        )

        rotate_node_by_count(g, round(((len(g.nodes)) / 4) - padding_size / 3))
        nx.set_edge_attributes(
            g,
            {e: np.sqrt(w) for e, w in nx.get_edge_attributes(g, "weight").items()},
            "sqrt_weight",
        )
        fig, ax = plt.subplots()
        nv.circos(
            g,
            node_color_by="group",
            sort_by="sort",
            node_alpha_by="transparent",
            edge_color_by="source_node_color",
            edge_lw_by="doubled_weight",
        )

        annotate.node_colormapping(
            g,
            color_by="group",
            legend_kwargs={"loc": "lower left", "bbox_to_anchor": (0.0, 1.0)},
        )
        plt.text(0.1, 0.5, "Left\nHemisphere", transform=fig.transFigure, fontsize=15)
        plt.text(0.8, 0.5, "Right\nHemisphere", transform=fig.transFigure, fontsize=15)
        plt.show()
