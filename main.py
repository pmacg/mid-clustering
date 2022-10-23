import graph_builder
import stag.graph
import stag.graphio


def load_graph(start_year, end_year):
    return stag.graphio.load_edgelist(
        graph_builder.edgelist_filename(start_year, end_year))


def main():
    graph_builder.generate_graph(1800, 1900)
    g: stag.graph.Graph = load_graph(1800, 1900)
    pass


if __name__ == "__main__":
    main()
