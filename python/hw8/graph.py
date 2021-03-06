from __future__ import print_function

try:
    import Queue
    import sys
    import random
except Exception as ex:
    print("Error importing a module: ", ex.message)
    raise ex


try:
    import numpy as np
except Exception as ex:
    print("The numpy package is not installed, If you attempt to call any")
    print("\tgraph methods that require numpy, they will fail and throw an exception.\n")


def make(filename, zero_index = True):
    """ build a graph """
    fin = open(filename, "r")
    linenum = 0
    graph = None
    no_weight = False


    if not zero_index:
        print("\nYou specified a graph with verts indexed at 1\n",
            "Please make sure this is connect\n\n")


    for line in fin:
        values = line.split("\t")
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
            graph = Graph(int(verts), int(edges), zero_index=zero_index)
        else:  # else connect the verts
            try:
                node1 = int(values[0])
                node2 = int(values[1])

                if zero_index:
                    graph.connect(node1, node2)
                else:
                    graph.connect(node1-1, node2-1)

                if len(values) == 3:
                    weight = float(values[2])
                    if zero_index:
                        graph.add_cost(node1, node2, weight)
                    else:
                        graph.add_cost(node1-1, node2-1, weight)

                else:
                    no_weight = True
            except Exception as ex:
                print("Error connecting verts or adding weights",
                    ex.message,"\n")
                raise ex
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
# class Matrix:
#     """ make a matrix """

#     def __init__(self, r, c):
#         self.rows = r
#         self.cols = c
#         self.data = [[0 in range(self.cols)] in range(self.rows)]

#     def __getitem__(self, key):
#         print("key: " + str(key))
#         return self.data[key]

#     def __setitem__(self, key, value):
#         print("set key: " + str(key) + " val: " + str(value))
#         self.data[key] = value

#     def output(self):
#         try:
#             for i in range(self.rows):
#                 row = ""
#                 for j in range(self.cols):
#                     row += (str(int(self.data[i][j])) + "   ")
#                 print(row + "\n")
#         except Exception as ex:
#             print("Error outputting graph:", ex.message)
#             raise GraphException(ex)
#     def set(self, a, b, val):
#         self.data[a][b] = val

#     def fill(self, value):
#         for i in range(self.rows):
#             for j in range(self.cols):
#                 self.set(i, j, value)


class Graph:
    def __init__(self, vs, es, has_weights=False, zero_index = True):
        self.verts = vs
        self.edges = es
        self.data = [[0 for x in range(self.verts)] for y in range(self.verts)]
        self.isWeighted = bool(has_weights)
        self.zero_index = zero_index
        #  init all weights to "infinity"
        self.weights = [[sys.maxint for x in range(self.verts)] for y in range(self.verts)]

    def __getitem__(self, key):
        return self.data[key]

    def output(self):
        for i in range(self.verts):
            row = ""
            for j in range(self.verts):
                if self.zero_index == False:
                    row += (str(self.data[i+1][j+1]) + "   ")
                else:
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

    def add_edge(self, u, v):
        # print("bfore",self.edges)
        if self.data[u][v] == 0:
            self.edges += 1
        self.data[u][v] = 1
        self.data[v][u] = 1
        # print("after", self.edges)

    ## left in for legacy reason
    def remove(self, a, b):
        self.remove_edge(a,b)

    def remove_edge(self, u, v):
        if self.data[u][v] == 1:
            self.edges -= 1
        self.data[u][v] = 0
        self.data[v][u] = 0

    def density(self):
        if self.edges == 0 and self.verts == 0:
            return 0
        else:
            top = 2 * float(self.edges)
            bottom = float(self.verts) * float(self.verts - 1)
            return round((top / bottom), 5)

    def edge_cost(self, a, b):
        return self.weights[a][b]

    def __neighbors_of(self, u, include = False):
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
                if include == True:
                    ret |= frozenset([u])
                return ret
            except Exception as ex:
                raise GraphException(ex)

    def __degree_of(self, u):
        # return np.sum(self.data[u])
        d = np.sum(self.data[u])
        # print("Degree of", u, d)
        return d

    def jaccard(self, u, v):
        try:
            S = self.__neighbors_of(u)
            T = self.__neighbors_of(v)
        except Exception as ex:
            raise(ex)

        # print("u neighbors", S)
        # print("v neighbors", T)

        try:
            return float(len(S.intersection(T))) / float(len(S.union(T)))
        except Exception as ex:
            raise GraphException("Jaccard error " + str(ex.message))

    def __are_connected(self, u, v):
        return (u < self.verts and v < self.verts) and self.data[u][v] == 1

    def adj_neighbors(self, u):
        neighbors = set()
        adj = set()
        for vert in range(self.verts):
            if self.data[u][vert] == 1:
                neighbors.add(vert)
        for n in neighbors:
            for nn in neighbors:
                if self.data[n][nn] == 1:
                    adj.add(frozenset([n, nn]))
        return adj

    def local_clustering(self, u):
        adj_neighbors = self.adj_neighbors(u)
        total_neighbors = self.__degree_of(u)
        total_neighbors *= (total_neighbors-1)
        total_neighbors = float(total_neighbors)
        if total_neighbors == 0.0:
            return 0.0
        return round((2.0 * float(len(adj_neighbors))) / float(total_neighbors), 5)

    def __deg_gt(self, degree):
        if type(degree) is not int:
            raise GraphException("__deg_gt degree must be an int")
        ret = list()
        for vert in range(self.verts):
            if self.__degree_of(vert) > degree:
                ret.append(vert)
        return ret

    def __deg_lt(self, degree):
        try:
            if type(degree) is not int:
                raise GraphException("__deg_lt degree must be an int")
            ret = list()
            for vert in range(self.verts):
                if self.__degree_of(vert) < degree:
                    ret.append(vert)
            return ret
        except Exception as ex:
            print("__deg_lt error: ", ex.message)
            raise GraphException(ex)

    def isolated_verts(self):
        return self.__deg_lt( 1 )

    def fast_p3(self, pretty_print=False):
        l = []
        l.extend(range(self.verts))

        triplets = set()
        to_check = set( self.__deg_gt(1) )
        checked = 0
        front_back_pairs = set()
        answers = list()

        ends_to_check = set( self.__deg_gt(0) )

        for center in to_check:
            found = 0
            front_back_pairs = front_back_pairs.intersection(set()) ## clear it to {} the empty set
            for front in ends_to_check:

                if front == center or self.data[front][center] == 0:
                    continue

                for back in ends_to_check:

                    if back == center or back == front or self.data[center][back] == 0:
                        continue
                    if frozenset([center, frozenset([front, back]) ]) in front_back_pairs:
                        continue

                    # print("checking", front, center, back)
                    checked += 1
                    if self.data[front][center] + self.data[center][back] == 2:
                        # print("\tkeeping")
                        to_add = frozenset([center, frozenset([front, back])])
                        triplets.add(to_add)
                        front_back_pairs.add(to_add)

        if not pretty_print:
            return triplets

        item = None
        o_item = None
        try:
            for answer in triplets:
                answer = set(answer)
                first = answer.pop()
                second = answer.pop()
                string = "("
                if type(first) is frozenset:
                    first = set(first)
                    string += str(first.pop()) + ", " + str(second) + ", " + str(first.pop())
                elif type(second) is frozenset:
                    second = set(second)
                    string += str(second.pop()) + ", " + str(first) + ", " + str(second.pop())
                else:
                    string += "error"
                string += ")"
                answers.append(string)
            return sorted(answers)
        except Exception as ex:
            print(ex.message)
            raise GraphException(ex)

    def number_of_k3(self):
        try:
            matrix = np.matrix(self.data)
            k3_matrix = np.linalg.matrix_power(matrix, 3)
            trace = np.matrix.trace(k3_matrix)
            return trace / 6
        except Exception as ex:
            print("Exception in numnber_of_k3", ex.message)
            raise ex

    def global_clustering(self):
        try:
            num_closed_p3 = float(3 * self.number_of_k3())
            p3_list = self.fast_p3(pretty_print=True)
            # print(p3_list)
            btm = float(len(p3_list))
            if btm == 0.0:
                return 0.0
            return num_closed_p3 / btm
        except Exception as ex:
            print(ex.message)
            raise GraphException(ex)

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

    def __has_cycle(self, v, visited, parent):
        try:
            visited[v] = True
            for i in range(self.verts):
                if self.data[v][i] == 0:
                    continue
                if visited[i] == False :
                    if (self.__has_cycle(i, visited, v)):
                        return True
                elif parent != i and parent != -1:
                    return True
            return False

        except Exception as ex:
            print("Error deciding whether graph is a tree: ", ex.message)
            raise GraphException("is_tree error: " + str(ex.message))

    def has_cycle(self):
        visited = [False for x in range(self.verts)]
        return self.__has_cycle(0, visited, -1)

    def is_tree(self):
        return len(self.comps()) == 1 and self.has_cycle() == False

    def get_leaves(self):
        try:
            leaves = list()
            for vert in range(self.verts):
                if np.sum(self.data[vert]) == 1:
                    leaves.append(vert)
            return leaves
        except Exception as ex:
            print("get_leaves error: ", ex.message)
            raise GraphException(ex)

    def __get_smallest_leaf(self):
        try:
            leaves = self.get_leaves()
            if len(leaves):
                return np.amin(self.get_leaves())
            return None
        except Exception as ex:
            print("__get_smallest_leaf error: ", ex.message)
            raise GraphException(ex)

    # def output_formatted_graph(self):
    #     """ print out a graph in our class format """
    #     ## this will take into account vert lists that start at 1 instead of 0
    #     out = list()
    #     pairs = set()

    #     for i in range(self.verts):
    #         for j in range(self.verts):
    #             if self.data[i][j] == 1:
    #                 if not self.zero_index:
    #                     pairs.add(frozenset([i+1,j+1]))
    #                 else:
    #                     pairs.add(frozenset([i+1,j+1]))
    #     for i in pairs:
    #         j = list(i)
    #         out.append(str(j.pop()) + "\t" + str(j.pop()))

    #     out.insert(0, str(self.verts) + "\t" + str(len(pairs)))

    #     for line in out:
    #         print(line)

    def output_formatted_graph(self):
        out = list()
        pairs = set()

        for i in range(self.verts):
            for j in range(self.verts):
                if i == j:
                    continue
                if self.data[i][j] == 0:
                    continue
                pair = list([i, j])
                if frozenset(pair) in pairs:
                    continue
                pairs.add(frozenset(pair))
                if i < j:
                    out.append(str(i) + "\t" + str(j))
                else:
                    out.append(str(j) + "\t" + str(i))
        print( str(self.verts) + "\t" + str(len(out)) )
        for line in out:
            print(line)


    def buildFromPrufer(self, seq):
        try:
            seq = map(lambda x: x - 1 , list(seq))
            degrees = list()
            u = None
            v = None

            for i in range(self.verts):
                degrees.append( seq.count(i) + 1 )

            for i in seq:
                for j in range(len(degrees)):
                    if j == i:
                        continue
                    if degrees[j] == 1:
                        try:
                            self.connect(i, j, weight=None)
                            degrees[i] =  degrees[i] - 1
                            degrees[j] = degrees[j] - 1
                            break
                        except Exception as ex:
                            print("Error connecting:", ex.message)
                            raise ex

            for i in range(len(degrees)):
                if degrees[i] == 1:
                    if u is None:
                        u = i
                    else:
                        v = i
            self.connect(u,v, weight=None)
            self.output_formatted_graph()

        except Exception as ex:
            print(ex.message)
            raise GraphException(ex)


    def prufer(self):
        """ compute a prufer sequence   this is a destructive call """
        try:
            removed = set()
            if self.is_tree() == False:
                return False
            i = 0
            seq = list()
            max_itors = self.verts - 2
            leaf = None
            leaf_neighbors = None
            while i < max_itors:
                leaf = self.__get_smallest_leaf()
                if leaf is None:
                    print("No more leaves left")
                    return False
                leaf_neighbors = list(self.__neighbors_of(leaf))
                if len(leaf_neighbors) > 1:
                    raise GraphException("Prufer leaf has > 1 neighbor!")
                seq.append(leaf_neighbors[0])
                # print("seq at", i, seq)
                self.__remove_vert(leaf)
                removed.add(leaf)
                i += 1
            return seq

        except Exception as ex:
            print("prufer error: ", ex.message)
            raise GraphException(ex)


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
        try:
            ret = set()
            seen = set()
            while len(seen) != len(self.data):
                for index in range(0, len(self.data[0])):
                    if index not in seen:
                        conns = frozenset(self.dfs(index))
                        seen |= conns  # union the sets
                        ret.add(conns)
            return ret
        except Exception as ex:
            print("Error in comps: ", ex.message)
            raise GraphException(ex)

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

    ## run through the first reductioun rule
    def _cluster_rule_1(self, T, k):
        if k < 1:
            return { "k": 0, "ops": [] }
        checked = set()
        before_k = k
        ops = list()
        # print("Running cluster rule 1")
        for u in range(self.verts):
            if k < 1:
                break
            for v in range(self.verts) :
                if frozenset([u,v]) in checked or u == v:
                    continue
                if k < 1:
                    break

                checked.add(frozenset([u,v]))

                v_neigh = self.__neighbors_of(v, include=True)
                u_neigh = self.__neighbors_of(u, include=True)
                c_neighbors = set(v_neigh).intersection(set(u_neigh))

                num_c = len(c_neighbors)
                num_nc = (len(v_neigh) - len(c_neighbors)) + (len(u_neigh) - len(c_neighbors))

                if num_c > k: ## addition
                    if self.data[u][v] == 0:
                        k -= 1
                        ops.append("Insert (" + str(u) + ", " + str(v) +")")
                        self.add_edge(u,v)
                    self._cluster_add_rule(T, u, v, "perm")
                elif num_nc > k: # removal
                    if self.data[u][v] == 1:
                        k -= 1
                        self.remove_edge(u, v)
                        ops.append("Remove (" + str(u) + ", " + str(v) +")")
                    self._cluster_add_rule(T, u, v, "forbid")
                elif num_c > k and num_nc > k:
                    return {"k": -1, "ops": []}
        return { "k": k, "ops": ops }
    def _cluster_rule_2(self, T, k):
        if k < 1:
            return {"ops": [], "k": 0 }
        checked = set()
        before_k = k
        ops = list()

        # print("Running cluster rule 2")
        for u in range(self.verts):
            if k < 1:
                break
            for v in range(self.verts):
                if u == v:
                    continue
                if k < 1:
                    break
                for w in range(self.verts):
                    if v == w:
                        continue
                    if k < 1:
                        break
                    if T[u][v] == "perm" and T[u][w] == "perm":
                        if self.data[v][w] == 0:
                            self.add_edge(v,w)
                            ops.append("Insert (" + str(v) + ", " + str(w) +")")
                            k -= 1
                        self._cluster_add_rule(T, v, w, "perm")
                    elif T[u][v] == "perm" and T[u][w] == "forbid":
                        if self.data[v][w] == 1:
                            self.remove_edge(v, w)
                            k -= 1
                            ops.append("Remove (" + str(v) + ", " + str(w) +")")
                            # print("\tremoving ----", v, w)
                        self._cluster_add_rule(T, v, w, "forbid")
        return { "ops": ops, "k": k }
    def _cluster_add_rule(self, T, i, j, rule):
        T[i][j] = rule
        T[j][i] = rule


    def delete_clique_comps(self):
        comp_sets = self.comps()
        n_comps = len(comp_sets)
        for comp in comp_sets:
            comp = list(comp)
            edges = set()
            for v in comp:
                for i in range(self.verts):
                    if self.data[v][i] == 1:
                        edges.add(frozenset([i,v]))
            if len(edges) == (len(comp) * (len(comp) - 1)) / 2:
                n_comps -= 1
                for edge in edges:
                    e = list(edge)
                    self.remove_edge(e[0], e[1])
        return n_comps

    def _cluster_make_clique(self, comp, k):
        # print(comp)
        start_k = k
        need_for_clique = int((len(comp) * (len(comp) - 1)) / 2)
        edges = set()
        ops = []
        for u in comp:
            for v in range(self.verts):
                if self.data[u][v] == 1:
                    edges.add(frozenset([u,v]))
        # print(edges)
        diff = abs(need_for_clique - len(edges))
        # print("diff", diff)
        if diff > (need_for_clique / 2) - len(edges):
            # print("Need to insert")
            if diff > k:
                # print("Don't have enough moves left")
                return {"k": -1, "ops": []}
            else:
                max_d = len(comp) - 1
                pair = []
                done = False
                while ( done == False ):
                    pair = []
                    for piece in comp:
                        if self.__degree_of(piece) < max_d:
                            pair.append(piece)
                    # print("have", len(pair), "with low degree ----")
                    if len(pair) > 0 and k > 0:
                        first = pair[0]
                        for item in pair:
                            if item == first:
                                continue
                            if self.data[first][item]:
                                continue
                            self.add_edge(first, item)
                            ops.append("Insert (" + str(first) + ", " + str(item) + ")")
                            k -= 1
                            break
                        for piece in comp:
                            if self.__degree_of(piece) < max_d:
                                continue
                            done = True
                    else:
                        return {"k": -1, "ops": []}
                return {"k": start_k - k, "ops": ops}


    def cluster_edit(self, k):
        self.zero_index = 1
        # print("given k =", k)
        k = int(k)
        start_k = k
        ops = list()
        rule_table = [["null" for x in range(self.verts)] for y in range(self.verts)]
        # rule_table =  [[0 in range(self.verts)] in range(self.verts)]
        rule1 = self._cluster_rule_1(rule_table, k)
        rule1_k = rule1["k"]
        ops = ops + rule1["ops"]
        if rule1_k < 0:
            print("NO SOLUTION")
            return None
        else:
            # print("Rule one used: ", k - rule1_k, "moves")
            k = rule1_k
        # print("After rule 1 have", k, "moves left")
        # self.output_formatted_graph()
        rule2 = self._cluster_rule_2(rule_table, k)
        rule2_k = -1
        # print(rule2)
        if rule2 is not None:
            rule2_k = rule2["k"]
        ops = ops + rule2["ops"]
        if rule2_k < 0:
            print("NO SOLUTION")
            return None
        else:
            # print("Rule 2 used: ", k - rule2_k, "moves")
            k = rule2_k
        # print("after rule 2 have", k, "moves left")

        # print("number of comps", len(self.comps()))

        comps_left = self.delete_clique_comps()
        # print("Have", comps_left, "non-clique connected comps left")

        if comps_left > k:
            # print("more components than moves left")
            return None
        elif comps_left == 0:
            # print("Done!")
            return ops

        for comp in self.comps():
            if len(comp) > 1:
                res = self._cluster_make_clique(comp, k)
                # print("moves used: ", res)
                if res["k"] > k:
                    return None
                elif res["k"] < 0:
                    return None
                ops += res["ops"]
                k = k - res["k"]
                self.delete_clique_comps()
        # self.output_formatted_graph()
        return ops
