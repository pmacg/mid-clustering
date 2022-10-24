import cluster
import graph_builder
import pandas as pd


def main():
    # The data files should be stored in these given locations.
    country_codes_filename = "./data/COW-country-codes.csv"
    dyadic_mid_filename = "./data/dyadic_mid_4.01.csv"
    graphs_directory = "./graphs"
    graph_builder.override_data_location(country_codes_filename, dyadic_mid_filename, graphs_directory)
    
    this_cluster, that_cluster = cluster.find_mid_clusters(1900, 1950, "Indonesia")
    print(this_cluster)
    print(that_cluster)
    

if __name__ == "__main__":
    main()

