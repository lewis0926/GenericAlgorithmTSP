# Project README - Solving TSP and Clustering Problems using Genetic Algorithms

## Overview

This project is an implementation of Genetic Algorithms (GA) for solving Traveling Salesman Problem (TSP). The code is written in Python within Jupyter Notebook environments and utilizes several libraries for data manipulation, visualization, and algorithmic implementations.

## Project Structure

The project is structured into multiple files and directories:

- `main.ipynb`: The primary Jupyter Notebook containing the core project code and execution flow.
- `ga_tsp.py`: A module that includes general-purpose GA functions used across different TSP variations.
- `ga_given_start_end.py`: Specific GA functions for solving TSP with given start and end cities.
- `ga_atsp.py`: GA functions tailored for solving the Asymmetric Traveling Salesman Problem (ATSP).
- `ga_sop.py`: GA functions designed for addressing the Sequential Ordering Problem (SOP).
- `clustering.ipynb`: The main Jupyter Notebook for clustering tasks, with clustering results stored in "Dataset/clustering_result.csv."

## Dependencies

The project relies on the following Python libraries:

- `numpy`: For efficient numerical operations and data manipulation.
- `matplotlib.pyplot`: Used for data visualization and plotting.
- `random`: For generating random numbers and operations.
- `time`: For timing and profiling parts of the code.

Additionally, the following libraries are utilized for clustering:

- `pandas`: For data manipulation and handling.
- `sklearn.datasets`: Used for accessing and managing datasets.
- `sklearn.cluster`: Provides clustering algorithms and functionality.

## Usage

1. Open and run `main.ipynb` in your Jupyter Notebook environment to execute the primary project code.
2. The notebook provides step-by-step instructions and explanations for various TSP problem variations and clustering tasks.
3. Customize hyperparameters, input data, and algorithm configurations to suit your specific use case.
4. Review the results, visualizations, and analysis presented within the notebook.

## Important Notes

- A basic understanding of genetic algorithms, TSP variations, clustering, and Python programming is assumed.
- Ensure that you have the required libraries installed via `pip` or `conda` before running the code.
- Adjust hyperparameters and settings as necessary for your problem and dataset.
- Clustering results are available in "Dataset/clustering_result.csv."

If you have any questions or need assistance with the project, please feel free to reach out.

Happy coding!

