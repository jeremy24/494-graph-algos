## Hw 0 ##

### Usage ###
    > go.py graph1.txt

### Question 1 ###
1. How to find k<sub>3</sub> in a graph G of order n.

        For each vertex in vertices
            if vertex has >= 2 edges   
                for edge in vertex edges
                    if edge connected to another vertex neighbor
                        return found
        return not found


2. Efficiency

    The worst case is O(n).  This is because in the worst case you
    go through (max degree) * n checks if you have a dense graph and you check every node without keeping track of ones that have already been checked. For any dense graph with 3 or more vertices you are guaranteed to have a k<sub>3</sub> occur so as the max degree of a reasonably dense graph increases the chance of finding a k<sub>3</sub> increases.
