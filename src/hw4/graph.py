
import math
import Queue
import sys
import random



def make(filename):
    """ build a graph """
    fin = open(filename, "r")
    linenum = 0
    verts = 0
    edges = 0
    graph = None
    no_weight = False
    for line in fin:
        # print ("line " + line)
        values = line.split("\t")
        # print ("values " + str(values))
        # strip the wack n if present
        try:
            for i in values:
                # print ("i [" + i + "]")
                i = float(str(i).strip("\n"))
        except Exception as ex:
            print "\nError parsing the file.  This is probably from using spaces instead of tabs."
            print"Exiting...\n"
            # print(ex)
            raise ex

        # if first get graph verts n edges
        if linenum == 0:
            verts = int(values[0])
            edges = int(values[1])
            graph = Graph(int(verts), int(edges))
        else: # else connect the verts
            node1 = int(values[0])
            node2 = int(values[1])

            graph.connect(node1, node2)

            if len(values) == 3:
                weight = float(values[2])
                graph.add_cost(node1, node2, weight)
            else:
                no_weight = True

        linenum += 1

    if no_weight:
        print "\nThe file you passed does not contain measures for weighted edges."
        print "Please make sure this is correct.\n"

    fin.close()
    return graph

class GraphException(Exception):
    """ make a graph ex """
    def __str__(self):
        return repr(self.message)

### not used, just messing with python overloading
class Matrix:
    """ make a matrix """
    def __init__(self, r, c):
        self.rows = r
        self.cols = c
        self.data = [[0 in range(self.cols)] in range(self.rows)]
    def __getitem__(self, key):
        print "key: " + str(key)
        return self.data[key]
    def __setitem__(self, key, value):
        print "set key: " + str(key) + " val: " + str(value)
        self.data[key] = value
    def output(self):
        for  i in range(self.rows):
            row = ""
            for j in range(self.cols):
                row += (str(self.data[i][j]) + "   ")
            print row + "\n"
    def set(self, a, b, val):
        self.data[a][b] = val
    def fill(self, value):
        for i in range(self.rows):
            for j in range(self.cols):
                self.set(i, j, value)

class Graph:
    def __init__(self, vs, es, hasWeights=False):
        self.verts = vs
        self.edges = es
        self.data = [[0 for x in range(self.verts)] for y in range(self.verts)]
        self.isWeighted = bool(hasWeights)

        #  init all weights to "infinity"
        self.weights = [[sys.maxint for x in range(self.verts)] for y in range(self.verts)]

    def __getitem__(self, key):
        return self.data[key]

    def output(self):
        for  i in range(self.verts):
            row = ""
            for j in range(self.verts):
                row += (str(self.data[i][j]) + "   ")
            print row + "\n"

    def add_cost(self, a, b, weight):
        self.weights[a][b] = float(weight)
        self.weights[b][a] = float(weight)


    def connect(self, a, b, weight=None):
        self.data[a][b] = 1
        self.data[b][a] = 1
        if weight != None:
            add_cost(a, b, weight)

    def remove(self, a, b):
        self.data[a][b] = 0
        self.data[b][a] = 0

    def density(self):
        if self.edges == 0 and self.verts == 0:
            return 0
        else:
            top = 2 * float(self.edges)
            bottom = float(self.verts) * float(self.verts - 1)
            return round((top/bottom), 5)

    def edge_cost(self, a, b):
        return self.weights[a][b]

    # run a bfs
    def bfs(self, start):
        visited = list()

        queue = Queue.Queue()
        queue.put(start)
        while not queue.empty():
            vert = queue.get()
            if vert not in visited:
                visited.append(vert)
                for index in range(0, len(self.data[vert])):
                    if self.data[vert][index] == 1:
                        queue.put(index)
        return visited

    # run a dfs
    def dfs(self, start):
        visited = list()

        stack = list()
        stack.append(start)
        while len(stack):
            vert = stack.pop()
            if vert not in visited:
                visited.append(vert)
                for index in range(0, len(self.data[vert])):
                    if self.data[vert][index] == 1:
                        stack.append(index)
        return visited

    def dij_path(self, start, end):
        if end >= self.verts:
            raise GraphException("Cannot find a vertex that is not in the graph")

        visited = list()
        dists = [sys.maxint for x in range(self.verts)]
        dists[start] = 0

        search = self.dfs(start)
        path = list()

        queue = Queue.Queue()
        queue.put(start)

        while not queue.empty():
            vert = queue.get()
            if vert not in visited:
                visited.append(vert)
                for index in range(0, len(self.data[vert])):
                    if self.data[vert][index] == 1:
                        queue.put(index)
                        if (dists[vert] + self.weights[vert][index]) < dists[index]:
                            # print("its less")
                            dists[index] = dists[vert] + self.weights[vert][index]
                        if dists[vert] == sys.maxint:
                            # print("inf, setting to", self.weights[vert][index])
                            dists[index] = self.weights[vert][index]
                            # path.append(vert)

        for i in search:
            path.append(i)
            if i == end:
                break
        return {"distance": dists[end], "path": path}

    def comps(self):
        ret = set()
        seen = set()
        while ( len(seen) != len(self.data) ):
		    for index in range(0, len(self.data[0])):
			    if index not in seen:
				    conns = frozenset(self.dfs(index))
				    seen = seen | conns ## union the sets
				    ret.add(conns)
        return ret

    def degree(self, switch):
        target = 0
        if (switch == "min"):
            target = self.verts - 1
            if ( target < 0 ):
                target = 0
        for i in range(self.verts):
            tmp = 0
            for j in range(self.verts):
                tmp += self.data[i][j]
            if (switch == "max"):
                if (tmp > target):
                    target = tmp
            elif(switch == "min"):
                if ( tmp < target):
                    target = tmp
            else:
                print (GraphException("Invalid switch passed to degree."))
        return target

    def order_verts(self, direction):
        deg_bound = 0

        degs = list()

        for i in range( self.verts ):
            deg = 0
            for j in range(self.verts):
                if self.data[i][j] == 1:
                    deg += 1
            degs.append([i,deg])

        if direction == "max":
            degs = sorted(degs, key=lambda tup: tup[1])
            degs.reverse()
        elif direction == "min":
            degs = sorted(degs, key=lambda tup: tup[1])
        elif direction == "random":
            degs = random.sample(degs, len(degs))
        else:
            raise GraphException("Invalid direction passed to order_verts: " + direction)

        # pluck out the vert numbers and drop the deg used to order
        degs = [i for [i,j] in degs]

        return degs

    def color(self, direction):
        vert_set = None

        try:
            vert_set = self.order_verts(direction=direction)
        except GraphException as ex:
            print "Cannot continue, invalid direction given"
            raise ex
        except Exception as generalEx:
            raise GraphException(generalEx)

        colors = set()
        current_color = 1
        colored = dict() ## dict[vert]: color

        colors.add(0)

        try:
            for vert in vert_set:
                valid_colors = set()
                valid_colors = valid_colors | colors # make all colors initially valid

                if vert not in colored:
                    for i in range(self.verts):
                        if self.data[vert][i] == 0:
                            continue
                        neighbor = i
                        if neighbor in colored.keys():
                            try:
                                # print "neighbor color:", colored[neighbor], "valid color:", colored[neighbor] in valid_colors
                                if colored[neighbor] in valid_colors:
                                    # remove the neighbor color from valid list
                                    valid_colors.remove(colored[neighbor])
                            except Exception as ex:
                                print "neighbor check error for", neighbor
                                raise ex
                    try:
                        if len(valid_colors) == 0:
                            colors.add(current_color)
                            colored[vert] = current_color
                            current_color += 1
                        else:
                            colored[vert] = min(valid_colors)

                    except Exception as ex:
                        print "assign error"
                        raise ex
                else:
                    print "vert", vert, "already colored"
            # print colored
            # print "took", len(colors), "different colors"
            return { "number": len(colors), "colors": colors }
        except Exception as ex:
            raise ex
