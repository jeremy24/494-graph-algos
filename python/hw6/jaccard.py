from __future__ import print_function

import sys
from graph import make
from graph import GraphException
from timer import Timer


def main():
    if len(sys.argv) == 4:
        try:
            filename = str(sys.argv[1])

            # print(sys.argv)

            timer = Timer()
            graph = make(filename)
            u = int(sys.argv[2])
            v = int(sys.argv[3])



            print(graph.jaccard(u, v))


        except Exception as ex:
            print ("Exception in main")
            raise ex
    else:
        print (GraphException("You must supply a valid graph file"))

main()
