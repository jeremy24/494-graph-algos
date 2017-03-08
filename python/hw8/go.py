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
            ops = graph.cluster_edit(k)

            if ops == None:
                print("No Solution")
            elif len(ops) == 0:
                print("No operations necessary")
            else:
                for line in ops:
                    print(line)

        except Exception as ex:
            print ("Exception in main")
            raise ex
    else:
        print (GraphException("You must supply a valid graph file"))

main()
