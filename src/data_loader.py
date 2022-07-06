import pandas as pd
import numpy as np


def load_data(
    connectivity_matrix_path,
    atlas_path,
    grouping_name,
    label,
    roi_names,
    hemisphere="Hemi",
    left_symbol="L",
    right_symbol="R",
):
    """
    This function loads and returns a connectivity matrix from a .csv file.
    In addition, it groups the ROIs according to a grouping variable (such as lobes or networks) provided by the atlas.

    Parameters
    ----------
    connectivity_matrix: string
        Path to the connectivity matrix .csv file.
        The shape of the matrix must be n X n matrix where n is the number of ROIs in  the atlas.
        Each cell in the matrix describes the connection between each pair of ROIs.
    atlas_path: string
        Path to an atlas .csv file
    grouping_name: string
        The name of variable by which we will group ROIs in the graph.
        the name of grouping variaible must be
    label: string
        Name of column in the atlas that contains the numbers (labels) of the ROIs
    roi_names: string
        Name of column in the atlas that contains the ROIs names.
        These names will be presented on the circular graph

    Returns
    -------
    connectivity_matrix: np.ndarray
        n X n matrix where n is the number of ROIs in  the atlas.
        Each cell in the matrix describes the connection between each pair of ROIs.
    groups: list
        List of dictionaries for each hemisphere. Each dictionary is divided by the grouping variable.
        The keys are the groups names. The values are lists of tuples, each tuple represents a ROI in the group.
        Each tuple contains the index of a ROI in the connectivity matrix (starting from zero) and the ROI name.
        for example:  {"Frontal lobe": [(0, precentral gyrus), (1, SFG), (2, MFG), (3, IFG)}

    """

    connectivity_matrix = pd.read_csv(
        connectivity_matrix_path, header=None
    ).values  # load connectivity matrix
    atlas = pd.read_csv(atlas_path)  # load atlas

    # validate inputs
    n_rows, n_cols = connectivity_matrix.shape
    num_rois = np.max(atlas[label])
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

    if not (grouping_name in atlas.columns):
        raise ValueError(
            "There is no column named {grouping_name} in the provided atlas!\nPlease enter another grouping variable!".format(
                grouping_name=grouping_name
            )
        )

    if not (label in atlas.columns):
        raise ValueError(
            "There is no column named {label} in the provided atlas!\nPlease enter the name of the labels column!".format(
                label=label
            )
        )

    if not (roi_names in atlas.columns):
        raise ValueError(
            "There is no column named {roi_names} in the provided atlas!\nPlease enter the name of the labels column!".format(
                roi_names=roi_names
            )
        )

    grouped_atlas_hemisphere = atlas.replace({hemisphere: {np.nan: "missing"}}).groupby(
        hemisphere
    )
    hemisperic_names = list(grouped_atlas_hemisphere.groups.keys())
    L_group = grouped_atlas_hemisphere.get_group(left_symbol)
    R_group = grouped_atlas_hemisphere.get_group(right_symbol)
    other_group = grouped_atlas_hemisphere.get_group(hemisperic_names[2])

    return connectivity_matrix, [
        create_dictionary(L_group),
        create_dictionary(R_group),
        create_dictionary(other_group),
    ]


def create_dictionary(grouped_by_hemisphere, grouping_name=grouping_name):
    """
    This function groups the ROIs according to a grouping variable within hemisphere.

    Parameters
    ----------
    grouped_by_hemisphere: DataFrame
        Part of the matrix that related to specific hemisphere.
    grouping_name: string
        The name of variable by which we will group ROIs in the graph.
        the name of grouping variaible must be

    Returns
    -------
    groups: dictionary
        Dictionary of groups of ROIs, divided by the grouping variable.
        The keys are the groups names. The values are lists of tuples, each tuple represents a ROI in the group.
        Each tuple contains the index of a ROI in the connectivity matrix (starting from zero) and the ROI name.
        for example:  {"Frontal lobe": [(0, precentral gyrus), (1, SFG), (2, MFG), (3, IFG)}

    """

    grouped_atlas = grouped_by_hemisphere.groupby([grouping_name])
    groups_names = list(grouped_atlas.groups.keys())
    groups = {}
    for group in groups_names:
        group_df = grouped_atlas.get_group(group)
        groups[group] = list(zip(group_df[label] - 1, group_df[roi_names]))
    return groups
