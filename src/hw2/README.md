## HW 2 - Jeremy Poff ##

1.   a
2.      
            python dfs.py [graph] [start]
3.      
            python bfs.py [graph] [start]
4.      
            python connectedComponents.py [graph]
5. None, for all of the graphs bfs runs faster.  The times tend to be very close except for Random-1000.8 which is a very dense graph and leads to dfs checking the same verts it has alredy covered many times.  From this I can conclude that dfs tends to be faster for sparse graphs and bfs is better for dense graphs.   You can see my times by running
        python time.py
