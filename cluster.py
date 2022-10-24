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


def simplify(num_g_vertices: int, sparse_vector):
    """
    Given a sparse vector (presumably from an approximate pagerank calculation on the double cover),
    and the number of vertices in the original graph, compute the 'simplified' approximate pagerank vector.

    See [MS21] for the definition of the simplified vector.

    [MS21] Macgregor, Peter, and He Sun.
    "Local algorithms for finding densely connected clusters."
    International Conference on Machine Learning. PMLR, 2021.

    :param num_g_vertices:
    :param sparse_vector:
    :return:
    """
    # Initialise the new sparse vector
    new_vector = scipy.sparse.lil_matrix((2 * num_g_vertices, 1))

    # Iterate through the entries in the matrix
    for i in range(min(num_g_vertices, sparse_vector.shape[0] - num_g_vertices)):
        if sparse_vector[i, 0] > sparse_vector[i + num_g_vertices, 0]:
            new_vector[i, 0] = sparse_vector[i, 0] - sparse_vector[i + num_g_vertices, 0]
        elif sparse_vector[i + num_g_vertices, 0] > sparse_vector[i, 0]:
            new_vector[i + num_g_vertices, 0] = sparse_vector[i + num_g_vertices, 0] - sparse_vector[i, 0]

    return new_vector.tocsc()


def find_mid_clusters(start_year: int, end_year: int, seed_country: str, size_factor: float):
    """
    Use the local clustering algorithm from [MS21] to find clusters of allies
    in the MID dataset.

    [MS21] Macgregor, Peter, and He Sun.
    "Local algorithms for finding densely connected clusters."
    International Conference on Machine Learning. PMLR, 2021.

    :param start_year:
    :param end_year:
    :param seed_country: A string giving the country around which to find the clusters
    :param size_factor: A number from 0 to 1 indicating how 'local' the cluster should be
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

    # Run the approximate pagerank on the double cover graph
    alpha = 0.01
    epsilon = size_factor * 1. / (5 * g.total_volume()) + (1 - size_factor) * 1. / (20 * g.degree(starting_vertex))
    seed_vector = scipy.sparse.lil_matrix((h.number_of_vertices(), 1))
    seed_vector[starting_vertex, 0] = 1
    p, r = stag.cluster.approximate_pagerank(h, seed_vector.tocsc(), alpha, epsilon)

    # Compute the simplified pagerank vector
    p_simplified = simplify(g.number_of_vertices(), p)

    # Compute the sweep set in the double cover
    sweep_set = stag.cluster.sweep_set_conductance(h, p_simplified)

    # Split the returned vertices into those in the same cluster as the seed, and others.
    this_cluster = [vertex_to_country[i] for i in sweep_set if i < g.number_of_vertices()]
    that_cluster = [vertex_to_country[i - g.number_of_vertices()] for i in sweep_set if i >= g.number_of_vertices()]
    return this_cluster, that_cluster
