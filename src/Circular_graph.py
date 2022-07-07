import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import nxviz as nv
from nxviz import annotate
import collections
from random import randint


class Circular_graph:
    """create an object of a brain atlas and connectivity matrix that can be represented as a circular graph
    with nodes as brain ROIs and width of edges representing the degree of connection between 2 ROIs"""

    def __init__(
        self,
        connectivity_matrix_path,
        atlas_path,
        grouping_name="Lobe",
        label="Label",
        roi_names="ROIname",
        hemisphere="Hemi",
        left_symbol="L",
        right_symbol="R",
        threshold=0.5,
    ) -> None:
        """
        Parameters
        ----------
        connectivity_matrix_path: string
            Path to the connectivity matrix .csv file.
            The shape of the matrix must be n X n matrix where n is the number of ROIs in  the atlas.
            Each cell in the matrix describes the connection between each pair of ROIs.
        atlas_path: string
            Path to an atlas .csv file
        grouping_name: string
            The name of variable by which we will group ROIs in the graph.
            the name of grouping variable must be the title of one of the columns.
        label: string
            Name of column in the atlas that contains the numbers (labels) of the ROIs
        roi_names: string
            Name of column in the atlas that contains the ROIs names.
            These names will be presented on the circular graph
        hemisphere: string
            name of column indicating the hemisphere in which the ROI is.
        left_symbol: string
            how "left hemisphere" is indicated in the hemisphere column.
        right_symbol: string
            how "right hemisphere" is indicated in the hemisphere column.
        threshold: float
            threshold of connectivity strength over which will appear in graph.
        """
        self.connectivity_matrix_path = connectivity_matrix_path
        self.atlas_path = atlas_path
        self.grouping_name = grouping_name
        self.label = label
        self.roi_names = roi_names
        self.hemisphere = hemisphere
        self.left_symbol = left_symbol
        self.right_symbol = right_symbol
        self.threshold = threshold
        self.connectivity_matrix = []
        self.groups = []
        self.filtered_normalize_matrix = []

    def show_graph(self):
        """
        This method will call the other methods in this class
        to produce and present the circular connectivity graph.
        Returns
        -------
        Figure of circular graph with color legend according to grouping. The degree of connectivity between
        ROIs is indicated by the the width of the edges.
        """
        self.data_loader()
        self.normalizing_and_thresholding()
        self.create_graph()

    def data_loader(self):
        """
        This function loads and returns a connectivity matrix from a .csv file.
        In addition, it groups the ROIs according to a grouping variable (such as lobes or networks) provided by the atlas.
        Default values match the brainnetome atlas (with cerebellum)

        Returns
        -------
        connectivity_matrix: np.ndarray
            n X n matrix where n is the number of ROIs in  the atlas.
            Each cell in the matrix describes the connection between each pair of ROIs.
        groups: list
            List of dictionaries for each hemisphere. Each dictionary is divided by the grouping variable.
            The keys are the groups names. The values are lists of tuples, each tuple represents an ROI in the group.
            Each tuple contains the index of an ROI in the connectivity matrix (starting from zero) and the ROI name.
            for example:  {"Frontal lobe": [(0, precentral gyrus), (1, SFG), (2, MFG), (3, IFG)}

        """

        connectivity_matrix = pd.read_csv(
            self.connectivity_matrix_path, header=None
        ).values  # load connectivity matrix
        atlas = pd.read_csv(self.atlas_path)  # load atlas

        # validate inputs
        n_rows, n_cols = connectivity_matrix.shape
        num_rois = np.max(atlas[self.label])
        if n_rows != n_cols:
            raise ValueError(
                "The number of rows and the number of columns must be same!\nNumber of rows is {n_rows}\nNUmber of columns is {n_cols}".format(
                    n_rows=n_rows, n_cols=n_cols
                )
            )

        if n_rows != num_rois:
            raise ValueError(
                "The number of rows and columns must match the number of ROIs ({num_rois})".format(
                    num_rois=num_rois
                )
            )

        if not (self.grouping_name in atlas.columns):
            raise ValueError(
                "There is no column named {grouping_name} in the provided atlas!\nPlease enter another grouping variable!".format(
                    grouping_name=self.grouping_name
                )
            )

        if not (self.label in atlas.columns):
            raise ValueError(
                "There is no column named {label} in the provided atlas!\nPlease enter the name of the labels column!".format(
                    label=self.label
                )
            )

        if not (self.roi_names in atlas.columns):
            raise ValueError(
                "There is no column named {roi_names} in the provided atlas!\nPlease enter the name of the labels column!".format(
                    roi_names=self.roi_names
                )
            )

        # grouping
        sorted_hemisperes = atlas.apply(
            lambda row: "else"
            if row[self.hemisphere] != "L" and row[self.hemisphere] != "R"
            else row[self.hemisphere],
            axis=1,
        )
        atlas_by_hemispheres = atlas
        atlas_by_hemispheres[self.hemisphere] = sorted_hemisperes

        grouped_atlas_hemisphere = atlas.groupby(self.hemisphere)
        L_group = grouped_atlas_hemisphere.get_group(self.left_symbol)
        R_group = grouped_atlas_hemisphere.get_group(self.right_symbol)
        else_group = grouped_atlas_hemisphere.get_group("else")

        self.connectivity_matrix = connectivity_matrix
        self.groups = [
            self.create_dictionary(L_group),
            self.create_dictionary(R_group),
            self.create_dictionary(else_group),
        ]

    def create_dictionary(self, grouped_by_hemisphere):
        """
        This function groups the ROIs according to a grouping variable within hemisphere.

        Parameters
        ----------
        grouped_by_hemisphere: DataFrame
            Part of the atlas that relates to specific hemisphere.
        grouping_name: string
            The name of variable by which we will group ROIs in the graph.
            The name of grouping variable must be the name of one of the columns.

        Returns
        -------
        groups: dictionary
            Dictionary of groups of ROIs, divided by the grouping variable.
            The keys are the groups names. The values are lists of tuples, each tuple represents an ROI in the group.
            Each tuple contains the index of an ROI in the connectivity matrix (starting from zero) and the ROI name.
            for example:  {"Frontal lobe": [(0, precentral gyrus), (1, SFG), (2, MFG), (3, IFG)}

        """
        grouped_atlas = grouped_by_hemisphere.groupby([self.grouping_name])
        groups_names = list(grouped_atlas.groups.keys())
        groups = {}
        for group in groups_names:
            group_df = grouped_atlas.get_group(group)
            groups[group] = list(
                zip(group_df[self.label] - 1, group_df[self.roi_names])
            )
        return groups

    def normalizing_and_thresholding(self):
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
        filtered_normalize_matrix: np.ndarray
            connecitivty matrix after thresholding and normalization
        """
        if self.threshold < 0 or self.threshold > 1:
            raise ValueError("Threshold value must be between 0-1!")

        normalized_connectivity_matrix = (
            self.connectivity_matrix - np.min(self.connectivity_matrix)
        ) / (np.max(self.connectivity_matrix) - np.min(self.connectivity_matrix))

        filtered_normalize_matrix = normalized_connectivity_matrix
        filtered_normalize_matrix[normalized_connectivity_matrix < self.threshold] = 0

        self.filtered_normalize_matrix = filtered_normalize_matrix

    def create_graph(self):
        def rotate_node_by_count(g, count):
            values = [g.nodes()[node]["sort"] for node in g.nodes]
            print(count)
            values.sort()
            values = values[-count:]
            for node in g.nodes():
                if g.nodes()[node]["sort"] in values:
                    g.nodes()[node]["sort"] += -1000

        def add_padding(g, padding_size, sort_value):
            for i in range(padding_size):
                node_value = i * randint(1000, 100000000)
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
                sort_value = add_padding(g, 5, sort_value)
            return sort_value

        g = nx.from_numpy_array(
            self.filtered_normalize_matrix, self.groups
        ).to_directed()
        nx.set_edge_attributes(
            g,
            {e: w * 3 for e, w in nx.get_edge_attributes(g, "weight").items()},
            "doubled_weight",
        )
        left = self.groups[0]
        right = self.groups[1]
        other = self.groups[2]
        sort_value = 0
        padding_size = 30
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
