## HW 2 - Jeremy Poff ##

1.
    a. It reaches the final return on a graph that consists of merely one vertex and no edges.  The first if is false, and there are no sets S of k = 1 ... n-1 edges in a single vertex graph, thus the final return is used.

    b. The worst case behavior is when the graph is dense and every vertex is of maximum degree.

    c. T( n <sup>λ(G)</sup> )


2.      
            python dfs.py [graph] [start]
3.      
            python bfs.py [graph] [start]
4.      
            python connectedComponents.py [graph]
5. None, for all of the graphs bfs runs faster.  The times tend to be very close except for Random-1000.8 which is a very dense graph and leads to dfs checking the same verts it has alredy covered many times.  From this I can conclude that dfs tends to be faster for sparse graphs and bfs is better for dense graphs.   You can see my times by running
        python time.py
