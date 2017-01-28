import sys
from graph import Graph
from graph import make
from graph import GraphException
from graph import Matrix

def go():
    if ( len(sys.argv) == 4 ):
        filename = str(sys.argv[1])
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        graph = make( filename )

        res = graph.dij_path(start, end)
        st = ""
        for i in res["path"]:
            st += str(i) + " "
        print(st)
        print( res["distance"] )
        # graph.output()
    else:
        print (GraphException("You must supply a valid graph file"))



go()
