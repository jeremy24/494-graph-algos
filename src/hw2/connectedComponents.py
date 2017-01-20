import sys
from graph import Graph
from graph import make
from graph import GraphException
from graph import Matrix

def go():

    if ( len(sys.argv) == 2 ):
        filename = str(sys.argv[1])
     	data = make( filename )

        visited = data.comps()



        for item in visited:
            comp = ""
            for vert in item:
                comp += str(vert) + " "
            print "\n" + comp

    else:
        print (GraphException("You must supply a valid graph file"))




go()
