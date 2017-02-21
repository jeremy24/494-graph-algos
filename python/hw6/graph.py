from __future__ import print_function

import Queue
import sys
import random
import numpy as np



def make(filename):
    """ build a graph """
    fin = open(filename, "r")
    linenum = 0
    graph = None
    no_weight = False
    for line in fin:
        # print ("line " + line)
        values = line.split("\t")
        # print ("values " + str(values))
        # strip the \n  if present
        try:
            i = 0
            while i < len(values):
                values[i] = float(str(values[i]).strip("\n"))
                i += 1
        except Exception as ex:
            print("\nError parsing the file.  This is probably from using spaces instead of tabs.")
            print("Exiting...\n")
            # print(ex)
            raise ex

        # if first get graph verts n edges
        if linenum == 0:
            verts = int(values[0])
            edges = int(values[1])
            graph = Graph(int(verts), int(edges))
        else:  # else connect the verts
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
        print("\nThe file you passed does not contain measures for weighted edges.")
        print("Please make sure this is correct.\n")

    fin.close()
    return graph


class GraphException(Exception):
    """ make a graph ex """

    def __str__(self):
        return repr(self.message)


# not used, just messing with python overloading
class Matrix:
    """ make a matrix """

    def __init__(self, r, c):
        self.rows = r
        self.cols = c
        self.data = [[0 in range(self.cols)] in range(self.rows)]

    def __getitem__(self, key):
        print("key: " + str(key))
        return self.data[key]

    def __setitem__(self, key, value):
        print("set key: " + str(key) + " val: " + str(value))
        self.data[key] = value

    def output(self):
        for i in range(self.rows):
            row = ""
            for j in range(self.cols):
                row += (str(int(self.data[i][j])) + "   ")
            print(row + "\n")

    def set(self, a, b, val):
        self.data[a][b] = val

    def fill(self, value):
        for i in range(self.rows):
            for j in range(self.cols):
                self.set(i, j, value)


class Graph:
    def __init__(self, vs, es, has_weights=False):
        self.verts = vs
        self.edges = es
        self.data = [[0 for x in range(self.verts)] for y in range(self.verts)]
        self.isWeighted = bool(has_weights)

        #  init all weights to "infinity"
        self.weights = [[sys.maxint for x in range(self.verts)] for y in range(self.verts)]

    def __getitem__(self, key):
        return self.data[key]

    def output(self):
        for i in range(self.verts):
            row = ""
            for j in range(self.verts):
                row += (str(self.data[i][j]) + "   ")
            print(row + "\n")

    def add_cost(self, a, b, weight):
        self.weights[a][b] = float(weight)
        self.weights[b][a] = float(weight)

    def connect(self, a, b, weight=None):
        self.data[a][b] = 1
        self.data[b][a] = 1
        if weight is not None:
            self.add_cost(a, b, weight)

    def remove(self, a, b):
        self.data[a][b] = 0
        self.data[b][a] = 0

    def density(self):
        if self.edges == 0 and self.verts == 0:
            return 0
        else:
            top = 2 * float(self.edges)
            bottom = float(self.verts) * float(self.verts - 1)
            return round((top / bottom), 5)

    def edge_cost(self, a, b):
        return self.weights[a][b]

    def __neighbors_of(self, u):
        try:
            u = int(u)
        except ValueError:
            raise GraphException("value passed to neighbors_of is not an int")
        if u > self.verts:
            raise GraphException("Vert u is larger than the size of the graph")
        else:
            try:
                ret = frozenset()
                for neighbor in range(self.verts):
                    if self.data[u][neighbor] == 1:
                        ret |= frozenset([neighbor])
                return ret
            except Exception as ex:
                raise GraphException(ex)

    def __degree_of(self, u):
        return np.sum(self.data[u])

    def jaccard(self, u, v):
        try:
            S = self.__neighbors_of(u)
            T = self.__neighbors_of(v)
        except Exception as ex:
            raise(ex)

        print("u neighbors", S)
        print("v neighbors", T)

        try:
            return float(len(S.intersection(T))) / float(len(S.union(T)))
        except Exception as ex:
            raise GraphException("Jaccard error " + str(ex.message))

    def __are_connected(self, u, v):
        return (u < self.verts and v < self.verts) and self.data[u][v] == 1

    def adj_neighbors(self, u):
        neighbors = set()
        adj_neighbors = set()
        for neighbor in range(self.verts):
            if self.__are_connected(u, neighbor):
                for their_neighbor in range(self.verts):
                    if self.__are_connected(neighbor, their_neighbor) and their_neighbor in neighbors:
                        adj_neighbors.add(frozenset([neighbor, their_neighbor]))
        return adj_neighbors

    def local_clustering(self, u):
        adj_neighbors = self.adj_neighbors(u)
        total_neighbors = 0.0
        print("adj neighbors of", u, adj_neighbors)
        for i in range(self.verts):
            if self.data[u][i] == 1:
                total_neighbors += 1
        return float(len(adj_neighbors)) / float(total_neighbors)

    def fast_p3(self):
        triplets = set()

        l = []
        l.extend(range(self.verts))
        to_check = set(l)

        front_back_pairs = set()

        isolated_verts = list()

        for vert in range(self.verts):
            if self.__degree_of(vert) == 0:
                isolated_verts.append(vert)

        front_to_check = set(l)
        back_to_check = set(l)

        for v in isolated_verts:
            front_to_check.remove(v)
            back_to_check.remove(v)

        checked = 0

        for center in range(self.verts):
            if self.__degree_of(center) < 2:
                to_check.remove(center)

        # print ("fronts", front_to_check)
        # print("centers", to_check)

        for center in to_check:
            found = 0
            for front in front_to_check:

                if front == center:
                    continue
                if self.data[front][center] == 0:
                    continue

                for back in back_to_check:
                    if back == center or back == front:
                        continue
                    if self.data[center][back] == 0:
                        continue

                    if frozenset([front, back]) in front_back_pairs:
                        continue

                    # print("checking", front, center, back)
                    checked += 1
                    if self.data[front][center] + self.data[center][back] == 2:
                        # print("\tkeeping")

                        front_back_pairs.add(frozenset([front, back]))
                        to_add = frozenset([center, frozenset([front, back])])
                        triplets.add(to_add)

        # print(triplets)
        print("checked", checked, "triplets with (E, V) = (" + str(self.edges) + ", " + str(self.verts) + ")")
        print ("found", len(triplets), "P3s")



        # for i in range(self.verts):
        #     for j in range(self.verts):
        #         if i == j or self.data[i][j] == 0:
        #             continue
        #         for k in range(self.verts):
        #             print("checking", i, j, k)
        #             print("checking", j, k, i)
        #             print("checking", k, i, j)
        #             if i == k or j == k or self.data[i][k] + self.data[j][k] == 0:
        #                 continue
        #             if j not in centers and self.data[i][j] & self.data[j][k] == 1:
        #                 print("\tkeeping")
        #                 centers.add(j)
        #                 triplets.add(str(i)+str(j)+str(k))
        #             elif k not in centers and self.data[j][k] & self.data[k][i] == 1:
        #                 print("\tkeeping")
        #                 centers.add(k)
        #                 triplets.add(str(j)+str(k)+str(i))
        #             elif i not in centers and self.data[k][i] & self.data[i][j] == 1:
        #                 print("\tkeeping")
        #                 centers.add(i)
        #                 triplets.add(str(k)+str(i)+str(j))
        # print(triplets)




    def number_of_p3(self):
        self.output()
        triplets = set()
        centers = set()
        for i in range(0, self.verts):
            for j in range(i + 1, self.verts):
                if self.data[i][j] == 0:
                    continue
                for k in range(i + 2, self.verts):
                    if self.data[i][k] + self.data[j][k] == 0:
                        continue
                    print(i,j,k)
                    if self.__are_connected(i, j) and self.__are_connected(j, k) and len({i, j, k}) == 3 and j not in centers:
                        print("\tkeeping")
                        centers.add(j)
                        triplets.add(str(i) + str(j) + str(k))
                    elif self.__are_connected(i, k) and self.__are_connected(k, j) and len({i, j, k}) == 3 and j not in centers:
                        print("\tkeeping")
                        centers.add(j)
                        triplets.add(str(i) + str(j) + str(k))
                    elif self.__are_connected(j, i) and self.__are_connected(i, k) and len({i, j, k}) == 3 and j not in centers:
                        print("\tkeeping")
                        centers.add(j)
                        triplets.add(str(i) + str(j) + str(k))
        print("triplets", triplets)
        return triplets

    def number_of_k3(self):
        matrix = np.matrix(self.data)
        k3_matrix = np.linalg.matrix_power(matrix, 3)
        # print(k3_matrix)
        trace = np.matrix.trace(k3_matrix)
        return trace / 6


    def global_clustering(self):
        self.number_of_k3()
        self.fast_p3()

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
        """ Weight is correct but path is not!! """
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
        while len(seen) != len(self.data):
            for index in range(0, len(self.data[0])):
                if index not in seen:
                    conns = frozenset(self.dfs(index))
                    seen |= conns  # union the sets
                    ret.add(conns)
        return ret

    def degree(self, switch):
        target = 0
        if switch == "min":
            target = self.verts - 1
            if target < 0:
                target = 0
        for i in range(self.verts):
            tmp = 0
            for j in range(self.verts):
                tmp += self.data[i][j]
            if switch == "max":
                if tmp > target:
                    target = tmp
            elif switch == "min":
                if tmp < target:
                    target = tmp
            else:
                print(GraphException("Invalid switch passed to degree."))
        return target

    def order_verts(self, direction):

        vert_list = list()

        for i in range(self.verts):
            deg = 0
            for j in range(self.verts):
                if self.data[i][j] == 1:
                    deg += 1
            vert_list.append([i, deg])

        if direction == "max":
            vert_list = sorted(vert_list, key=lambda tup: tup[1])
            vert_list.reverse()
        elif direction == "min":
            vert_list = sorted(vert_list, key=lambda tup: tup[1])
        elif direction == "random":
            vert_list = random.sample(vert_list, len(vert_list))
        else:
            raise GraphException("Invalid direction passed to order_verts: " + direction)

        # pluck out the vert numbers and drop the deg used to order
        vert_list = [i for [i, j] in vert_list]

        return vert_list

    def color(self, direction):
        vert_set = None

        try:
            vert_set = self.order_verts(direction=direction)
        except GraphException as ex:
            print("Cannot continue, invalid direction given")
            raise ex
        except Exception as generalEx:
            raise GraphException(generalEx)

        colors = set()
        current_color = 1
        colored = dict()  # dict[vert]: color

        colors.add(0)

        try:
            for vert in vert_set:
                valid_colors = set()
                valid_colors |= colors  # make all colors initially valid

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
                                print("neighbor check error for", neighbor)
                                raise ex
                    try:
                        if len(valid_colors) == 0:
                            colors.add(current_color)
                            colored[vert] = current_color
                            current_color += 1
                        else:
                            colored[vert] = min(valid_colors)

                    except Exception as ex:
                        print("assign error")
                        raise ex
                else:
                    print("vert", vert, "already colored")
            # print colored
            # print "took", len(colors), "different colors"
            return {"number": len(colors), "colors": colors}
        except Exception as ex:
            raise ex

    def __remove_vert(self, vert):
        try:
            i = 0
            ret = list()
            while i < self.verts:
                if self.data[i][vert] == 1:
                    ret.append({"vert": i, "weight": self.weights[i][vert]})
                self.data[i][vert] = 0
                self.data[vert][i] = 0
                i += 1
            return ret
        except Exception as ex:
            print(ex)
            raise ex

    def __reconnect_vert(self, vert, conns):
        try:
            i = 0
            while i < len(conns):
                self.connect(conns[i]["vert"], vert, weight=conns[i]["weight"])
                i += 1
        except Exception as ex:
            print("Error in reconnect_vert", ex)
            raise ex

    def is_cut_vert(self, vert):
        try:
            vert = int(x=vert)
            old_comps = self.comps()
            conns = self.__remove_vert(vert)
            new_comps = self.comps()
            self.__reconnect_vert(vert, conns)
            # print("comp len diff:", len(new_comps) - len(old_comps))
            if len(new_comps) - len(old_comps) > 1:
                return True
            return False
        except Exception as ex:
            print("error in is_cut_vert", ex)
            raise ex

    def get_cut_verts(self, pretty_print=False):
        cut_verts = set()
        try:
            i = 0
            while i < self.verts:
                if self.is_cut_vert(i):
                    cut_verts.add(i)
                i += 1
            if pretty_print:
                cut_list = sorted(list(cut_verts))
                return_string = ""
                for i in cut_list:
                    return_string += str(i) + " "
                return return_string
            return cut_verts
        except Exception as ex:
            print("Error in get_cut_verts", ex)
            raise GraphException(ex)

    def get_cut_edges(self, pretty_print=False):
        try:
            i = 0
            j = 0
            checked_edges = set()
            cut_edges = set()
            while i < self.verts:
                j = 0
                while j < self.verts:
                    if self.data[i][j] == 1:
                        temp_set = frozenset([i, j])
                        if temp_set not in checked_edges:
                            checked_edges.add(temp_set)
                            old_comps = len(self.comps())
                            self.data[j][i] = 0
                            self.data[i][j] = 0
                            new_comps = len(self.comps())
                            self.data[j][i] = 1
                            self.data[i][j] = 1
                            if new_comps - old_comps > 0:
                                cut_edges.add(frozenset([i, j]))
                    j += 1
                i += 1
            if pretty_print:
                return_string = ""
                cut_edge_list = list(cut_edges)
                cut_edge_list = sorted(map(list, cut_edge_list), key=lambda tup: tup[0])
                for k in cut_edge_list:
                    return_string += "(" + str(k[0]) + "," + str(k[1]) + ") "
                return return_string
            return cut_edges
        except Exception as ex:
            print("Error getting cut edges", ex)
            raise GraphException(ex)