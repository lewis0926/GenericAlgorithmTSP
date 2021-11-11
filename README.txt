My code is implemented by Python language with Jupyter notebook. It requires numpy, matplotlib.pyplot, random and time lib.
Moreover, clustering requires pandas, sklearn.datasets and sklearn.cluster.

All the main code can be found in main.ipynb. Other .py files are the algorithms being called by the main program. General GA functions are in ga_tsp.py. Other GA functions under specific conditions can be found in differnt .py files.

Given start and end cities: ga_given_start_end.py
Asymmetric traveling salesman problem (ATSP): ga_atsp.py
Sequential ordering problem (SOP): ga_sop.py
Clustering :  (clustering.ipynb for main clustering. Clustering output is in "Dataset/clustering_result.csv")