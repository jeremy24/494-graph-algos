
import time
import os
from graph import Graph
from graph import make
from graph import GraphException
from graph import Matrix


def run(name):
    graph = make( name )

    ret = [0,0]

    start = time.time()
    graph.dfs(0)
    ret[1] = (time.time()-start)

    start = time.time()
    graph.bfs(0)
    ret[0] = (time.time()-start)

    return ret



def go():

    names = list()
    bfs = list()
    dfs = list()

    for name in os.listdir("./graphs"):
        names.append(name)

        name = "./graphs/" + name

        res = run(name)

        bfs.append(res[0])
        dfs.append(res[1])

    for index in range(0, len(names)):
        name = names[index]
        b = bfs[index]
        d = dfs[index]
        first = "%s" % str(object=name).ljust(30, " ")
        second = "%s" % str(object=b).rjust(18, " ")
        third = "%s" % str(object=d).ljust(20, " ")

        print "dfs: " + str(d) + "  bfs: " + str(b)

        if d > b:
            print "dfs is faster on " + first + " by " + str(abs(b-d)) + " seconds"
        else:
            print "bfs is faster on " + first + " by " + str(abs(b-d)) + " seconds"

        # print first + " took " + second + "  " + third



go()
