import sys
from graph import make
from graph import GraphException
from timer import Timer

def main():
    if len(sys.argv) == 2:
        filename = str(sys.argv[1])
        # start = int(sys.argv[2])
        # end = int(sys.argv[3])
        timer = Timer("ms")
        graph = make(filename)
        timer.delta()
        print timer.output()
        res = graph.color("max")
        print( res )
        # graph.output()
    else:
        print (GraphException("You must supply a valid graph file"))



main()
