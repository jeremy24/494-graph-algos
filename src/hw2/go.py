import sys
from graph import Graph
from graph import make
from graph import GraphException
from graph import Matrix

def go():

    if ( len(sys.argv) == 2 ):
        filename = str(sys.argv[1])
        graph = make( filename )

        # visited = graph.dfs(3, None)
        visited = graph.bfs(3, None)

        for item in visited:
            print ("visited:  " + str(item))

        # print ("Max Degree: " + str(graph.degree("max")))
        # print ("Min Degree: " + str(graph.degree("min")))
        # print ("Density: " + str(graph.density()))
        # graph.output()
    else:
        print (GraphException("You must supply a valid graph file"))




go()
