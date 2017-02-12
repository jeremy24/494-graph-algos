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

            output = list()

            output.append("Cut Vertices: " + str(graph.get_cut_verts(pretty_print=True)) + "\n\ttook " + str(timer.clock()) + "\n")

            print("verts done")

            output.append("Bridges: " + str(graph.get_cut_edges(pretty_print=True)) + "\n\ttook " + str(timer.clock()))

            for out in output:
                print(out)

        except Exception as ex:
            print ("Exception in main")
            raise ex
    else:
        print (GraphException("You must supply a valid graph file"))

main()
