# MID Dataset Clustering
This repository contains code for finding clusters in the MID conflict dataset. The clustering algorithm is based on the paper "Local Algorithms for Finding Densely Connected Clusters", which appeared in ICML'21.

See [the demo page](https://staglibrary.io/clustering-demo.html) to interactively see the output of the algorithm.

## Downloading the Dataset

* Download the Dyadic MID v4.01 dataset from [here](https://correlatesofwar.org/data-sets/mids/).
* Unzip the data in the data directory with `unzip dyadic_mid_4.01.zip`.
* Download the Country Codes file from [here](https://correlatesofwar.org/data-sets/cow-country-codes-2/) and add to the data directory.

On linux, the following sequence of commands should do the job.

```bash
cd data
wget https://correlatesofwar.org/wp-content/uploads/dyadic_mid_4.01.zip
unzip dyadic_mid_4.01.zip
wget https://correlatesofwar.org/wp-content/uploads/COW-country-codes.csv
cd ..
```

## Reference

```
@InProceedings{macgregor21a,
  title = 	 {Local Algorithms for Finding Densely Connected Clusters},
  author =       {Macgregor, Peter and Sun, He},
  booktitle = 	 {Proceedings of the 38th International Conference on Machine Learning},
  pages = 	 {7268--7278},
  year = 	 {2021},
  editor = 	 {Meila, Marina and Zhang, Tong},
  volume = 	 {139},
  series = 	 {Proceedings of Machine Learning Research},
  month = 	 {18--24 Jul},
  publisher =    {PMLR},
  pdf = 	 {http://proceedings.mlr.press/v139/macgregor21a/macgregor21a.pdf},
  url = 	 {https://proceedings.mlr.press/v139/macgregor21a.html},
  abstract = 	 {Local graph clustering is an important algorithmic technique for analysing massive graphs, and has been widely applied in many research fields of data science. While the objective of most (local) graph clustering algorithms is to find a vertex set of low conductance, there has been a sequence of recent studies that highlight the importance of the inter-connection between clusters when analysing real-world datasets. Following this line of research, in this work we study local algorithms for finding a pair of vertex sets defined with respect to their inter-connection and their relationship with the rest of the graph. The key to our analysis is a new reduction technique that relates the structure of multiple sets to a single vertex set in the reduced graph. Among many potential applications, we show that our algorithms successfully recover densely connected clusters in the Interstate Disputes Dataset and the US Migration Dataset.}
}
```
