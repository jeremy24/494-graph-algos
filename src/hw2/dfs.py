

from __future__ import print_function

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

        visited = graph.dfs(start)

        out = ""
        for item in visited:
            out += str(object=item) + " "
        out += "\n"
        print (out)

    else:
        print (GraphException("You must supply a valid graph file"))




go()
