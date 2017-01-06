# UniformKMeans
Python K-means implementation that produces equally sized clusters
## About
The K-Means algorithm aims to partition n data points into k clusters in such a way that minimizes the overall squared Euclidean distances between each point and its associated cluster center (within-cluster-sum-of-squares, or WCSS). However, K-Means ensures nothing about the number of points in each cluster. This equal cluster K-Means implementation guarantees clusters sized either floor(n/k) or ceil(n/k). While ensuring near-equal cluster sizes compromises on the WCSS, there are some cases where equal cluster sizes are desirable.
## Requirements
* Python 3.x
* Numpy
* Matplotlib (Optional, to run Testing.py and to plot general results)

## Usage
The constructor takes three arguments, ```points_list```, ```seeds```, and ```k```:
* ```points_list```: 2d list containing n-dimensional points

  points_list = [[Point1], [Point2], etc.]; n-dimensional point x = [X1, X2, ..., Xn]
* ```seeds```: 2d list of k n-dimensional points that serve as the initial centroids- list follows the same format as ```points_list```. The seeds can be obtained from any K-Means++ implementation. Usage instructions for the one in this repository can be found [here](https://github.com/JasonFuu/KMeansPlusPlus).
*  ```k```: Number of desired clusters

Calling ```final_clusters``` and ```final_centroids``` returns the final 2d lists of clusters and centroids, respectively. These lists follow the same format as ```points_list```.

The iteration count is hard-coded at 100. This should work well for most data sets, but I have not/do not know how to rigorously determine an appropriate value. 

## Example
Points from randomly generated data, x∈[0, 100], y∈[0, 50], n = 80, k = 4. (Centroids marked in black):
![alt text](https://github.com/JasonFuu/UniformKMeans/blob/master/Screenshots/figure_1.png)

## Notes
* Given n points and k clusters, UniformKMeans will create n%k clusters with ceil(n/k) points, and k-n%k clusters with floor(n/k) points
* As stated earlier, UniformKMeans works for any set of n-dimensional points, not just 2D
* Testing.py takes seeds from my [K-Means++ implementation](https://github.com/JasonFuu/KMeansPlusPlus). Feel free to use SciPy or any other K-Means++ implementation to get appropriate seeds.

## TODO 
Make code not look like trash; clean up methods
