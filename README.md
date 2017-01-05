# UniformKMeans
Python K-means implementation that produces equally sized clusters
## About
The K-Means algorithm aims to partition n data points into k clusters in such a way that minimizes the overall squared Euclidean distances between each point and its associated cluster center (within-cluster-sum-of-squares, or WCSS). However, K-Means ensures nothing about the number of points in each cluster. This equal cluster K-Means implementation guarantees clusters sized either floor(n/k) or ceil(n/k). While ensuring near-equal cluster sizes compromises on the WCSS, there are some cases where equal cluster sizes are desirable.
## Installation

## Usage

## Example
