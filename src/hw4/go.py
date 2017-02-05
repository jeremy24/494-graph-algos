import sys
from graph import make
from graph import GraphException
from timer import Timer

def main():
    if len(sys.argv) == 2:
        try:
            filename = str(sys.argv[1])

            timer = Timer(units="ms", prec=4)
            graph = make(filename)

            res = graph.color("max")
            # timer.delta()
            print "High to Low:", res["number"], "colors ", timer.output()

            timer.reset()
            timer.delta()
            res = graph.color("min")
            print "Low to High:", res["number"],"colors ", timer.output()

            timer.reset()
            timer.delta()
            res = graph.color("random")
            print "Random:     ", res["number"],"colors ", timer.output()
        except Exception as ex:
            print "Exception in main"
            raise ex
    else:
        print (GraphException("You must supply a valid graph file"))

main()
