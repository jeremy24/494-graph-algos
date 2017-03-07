from __future__ import print_function

import sys
from graph import make
from graph import GraphException
from timer import Timer


def main():
    if len(sys.argv) == 3:
        try:
            filename = str(sys.argv[1])

            # print(sys.argv)

            timer = Timer()
            graph = make(filename)
            k = sys.argv[2]
            graph.cluster_edit(k)

        except Exception as ex:
            print ("Exception in main")
            raise ex
    else:
        print (GraphException("You must supply a valid graph file"))

main()
