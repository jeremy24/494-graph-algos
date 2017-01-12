import sys
from graph import Graph
from graph import make


def go():
    if ( len(sys.argv) == 2 ):
        filename = str(sys.argv[1])
        graph = make( filename )
        
        print ("Max Degree: " + str(graph.degree("max")))
        print ("Min Degree: " + str(graph.degree("min")))
        print ("Density: " + str(graph.density()))
    else:
        print ("Must supply a valid graph file")

go()