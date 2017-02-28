from __future__ import print_function

import sys
from graph import make
from graph import GraphException
from timer import Timer


def main():
    if len(sys.argv) == 2:
        try:
            filename = str(sys.argv[1])

            # print(sys.argv)

            timer = Timer()
            graph = make(filename, zero_index=False)
            prufer = graph.prufer()

            if prufer == False:
                print("The graph is not a tree.")
            

        except Exception as ex:
            print ("Exception in main")
            raise ex
    else:
        print (GraphException("You must supply a valid graph file"))

main()
