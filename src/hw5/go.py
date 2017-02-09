from __future__ import print_function

import sys
from graph import make
from graph import GraphException
from timer import Timer


def main():
    if len(sys.argv) == 2:
        try:
            filename = str(sys.argv[1])

            timer = Timer()
            graph = make(filename)

            res = graph.color("max")
            
            print ("High to Low:", res["number"], "colors ", timer.clock())

        except Exception as ex:
            print ("Exception in main")
            raise ex
    else:
        print (GraphException("You must supply a valid graph file"))

main()
