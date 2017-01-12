

def make(filename):
    file = open(filename, "r")
    linenum = 0
    verts = 0
    edges = 0
    graph = None
    for line in file:
        values = line.split("\t")
        for i in values:
            print(values[i])
        print (str(values))
        if linenum == 0:
            verts = values[0]
            edges = values[1]
            graph = Graph(int(verts), int(edges))
        else:
            graph.connect(int(values[0]), int(values[1]))
    graph.output()
    return graph




class Graph:
    def __init__(self, vs, es):
        self.verts = vs
        self.edges = es
        self.data = [[ 0 for x in range(self.verts)] for y in range(self.verts)]

    def output(self):
        for  i in range(self.verts):
            row = ""
            for j in range (self.verts):
                row += (str(self.data[i][j]) + "  ")
            print ( row + "\n")
    def connect(self, a, b):
        self.data[a][b] = 1
        self.data[b][a] = 1

    def remove(self, a, b):
        self.data[a][b] = 0
        self.data[b][a] = 0

    def degree(self, switch):
        target = 0
        for i in range(self.verts):
            tmp = 0
            for j in range(self.verts):
                tmp += self.data[i][j]
            print ("tmp: " + str(tmp))
            if (switch == "max"):
                print("finding max")
                if (tmp > target):
                    target = tmp
            else:
                if ( tmp < target):
                    target = tmp
        return target
