from random import randint


def rotate_node_by_count(g, count):
    """
    This function gets a nx graph and rotate it by count.
    Parameters
    ----------
    g: networkx.Graph

    count: int
        by how many points the graph should be rotated
    """
    values = [g.nodes()[node]["sort"] for node in g.nodes]
    print(count)
    values.sort()
    values = values[-count:]
    for node in g.nodes():
        if g.nodes()[node]["sort"] in values:
            g.nodes()[node]["sort"] += -1000


def add_padding(g, padding_count, sort_value):
    """
    This function gets a nx graph and add empty padding values
    ----------
    g: networkx.Graph

    padding_count: int
        how many empty points should be added

    sort_value: int
        running index for sorting

    Returns
    -------
      sort_value: int
        running index for sorting
    """
    for i in range(padding_count):
        node_value = i * randint(1000, 100000000)
        g.add_node(node_value)
        g.nodes()[node_value]["group"] = "_"
        g.nodes()[node_value]["transparent"] = 0
        g.nodes()[node_value]["sort"] = sort_value
        sort_value += 1
    return sort_value


def add_values(g, items, sort_value):
    """
    This function add values to a graph
    ----------
    g: networkx.Graph

    items: dictionary<(int,str>
        dictionary from key to tuple of int and label

    sort_value: int
        running index for sorting

    rotate_nodes: Boolean
        should rotate the list labels

    Returns
    -------
      sort_value: int
        running index for sorting
    """
    for k1, v1 in items:
        for i1 in v1:
            g.nodes()[i1[0]]["group"] = k1
            g.nodes()[i1[0]]["transparent"] = 1
            g.nodes()[i1[0]]["sort"] = sort_value
            sort_value += 1
        sort_value = add_padding(g, 5, sort_value)
    return sort_value
