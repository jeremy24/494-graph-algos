
import sys
from graph import Graph
from graph import make
from graph import GraphException
from graph import Matrix

def go():

    if ( len(sys.argv) == 3 ):
        filename = str(sys.argv[1])
        start = int (sys.argv[2])

        graph = make( filename )

        visited = graph.bfs(start)

        out = ""
        for item in visited:
            out += str(object=item) + " "
        out += "\n"
        print out

        # print ("Max Degree: " + str(graph.degree("max")))
        # print ("Min Degree: " + str(graph.degree("min")))
        # print ("Density: " + str(graph.density()))
        # graph.output()
    else:
        print (GraphException("You must supply a valid graph file"))




go()
