"""
Methods for finding clusters in the MID datasets.
"""
import graph_builder
import scipy.sparse
import stag.graph
import stag.graphio
import stag.cluster


def load_graph(start_year, end_year):
    # Generate the graph if it hasn't been already
    graph_builder.generate_graph(start_year, end_year)

    # Now, load the graph from edgelist
    return stag.graphio.load_edgelist(
        graph_builder.edgelist_filename(start_year, end_year))


def load_vertex_dictionaries(start_year, end_year):
    # Generate the graph if it hasn't been already
    graph_builder.generate_graph(start_year, end_year)

    # Construct and return the dictionaries of country names to node ids.
    vertex_to_country = {}
    country_to_vertex = {}
    with open(graph_builder.vertex_filename(start_year, end_year), 'r') as fin:
        for i, line in enumerate(fin.readlines()):
            country = line.strip()
            vertex_to_country[i] = country
            country_to_vertex[country] = i

    return country_to_vertex, vertex_to_country


def find_mid_clusters(start_year: int, end_year: int, seed_country: str):
    """
    Use the local clustering algorithm from [MS2021] to find clusters of allies
    in the MID dataset.

    [MS2021] Macgregor, Peter, and He Sun.
    "Local algorithms for finding densely connected clusters."
    International Conference on Machine Learning. PMLR, 2021.

    :param start_year:
    :param end_year:
    :param seed_country: A string giving the country around which to find the clusters
    :return:
    """
    # Start by constructing a graph representing the interstate disputes during
    # the given time period.
    g = load_graph(start_year, end_year)

    # Now, we construct the double cover graph of g
    adj_mat = g.adjacency()
    identity = scipy.sparse.csc_matrix((g.number_of_vertices(), g.number_of_vertices()))
    double_cover_adj = scipy.sparse.bmat([[identity, adj_mat], [adj_mat, identity]])
    h = stag.graph.Graph(double_cover_adj)

    # Load dictionaries mapping between graph nodes and country names
    country_to_vertex, vertex_to_country = load_vertex_dictionaries(start_year, end_year)

    # Get the starting vertex of the algorithm
    if seed_country not in country_to_vertex:
        raise Exception("Seed country not found in dataset.")
    starting_vertex = country_to_vertex[seed_country]

    # Run the local clustering algorithm. Pass as the target volume ~half the volume
    # of the original graph
    dc_cluster = stag.cluster.local_cluster(h, starting_vertex, int(g.total_volume() / 2))

    # Should instead get the pagerank vector directly, run simplify, and then sweep set - two of which
    # can use the STAG library.
    pass
