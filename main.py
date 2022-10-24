import cluster


def main():
    this_cluster, that_cluster = cluster.find_mid_clusters(1900, 2000, "Brazil")
    print(this_cluster)
    print(that_cluster)


if __name__ == "__main__":
    main()
