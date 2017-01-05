# UniformKMeans
Python K-means implementation that produces equally sized clusters
## About
The K-Means algorithm aims to partition n data points into k clusters in such a way that minimizes the overall squared Euclidean distances between each point and its associated cluster center (within-cluster-sum-of-squares, or WCSS). However, K-Means ensures nothing about the number of points in each cluster. This equal cluster K-Means implementation guarantees clusters sized either floor(n/k) or ceil(n/k). While ensuring near-equal cluster sizes compromises on the WCSS, there are some cases where equal cluster sizes are desirable.
## Requirements
* Python 3.x
* Numpy
* Matplotlib (Optional, to run Testing.py and to plot general results)

## Usage


## Example
Seeds from randomly generated data, x∈[0, 100], y∈[0, 50], n = 80, k = 4. (Centroids marked in black):
![alt text](https://github.com/JasonFuu/UniformKMeans/blob/master/Screenshots/figure_1.png)

## Notes
Testing.py takes seeds from my [K-Means++ implementation](https://github.com/JasonFuu/KMeansPlusPlus). Feel free to use SciPy or any other K-Means++ implementation to get approporate seeds.
