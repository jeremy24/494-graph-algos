from graph import Graph


obj = Graph(5,5)

obj.connect(1,2)
obj.connect(1,3)
obj.output()

max_degree = obj.degree("max")
min_degree = obj.degree("min")

print ("Max: " + str(max_degree) + "\nMin: " + str(min_degree))
