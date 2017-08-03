import sys
from graph import *


def go():
	if (len(sys.argv) == 2):
		filename = str(sys.argv[1])
		graph = make(filename)

		print("Max Degree: " + str(graph.degree("max")))
		print("Min Degree: " + str(graph.degree("min")))
		print("Density: " + str(graph.density()))
		# graph.output()
	else:
		print(GraphException("You must supply a valid graph file"))


go()