from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math

import numpy as np


def make(filename):
	file = open(filename, "r")
	linenum = 0
	graph = None
	for line in file:
		values = line.split("\t")

		try:
			for i in values:
				# print ("i " + i)
				i = int(str(i).strip("\n"))
		except Exception as ex:
			print("\nError parsing the graph file.  This is probably from having spaces instead of tabs.")
			print("Exiting...\n")
			# print(ex)
			raise ex

		# if first get graph verts n edges
		if linenum == 0:
			verts = values[0]
			graph = Graph(int(verts))
		else:  # else connect the verts
			a = int(values[0])
			b = int(values[1])
			graph.connect(a, b)
		linenum += 1
	return graph


class GraphException(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


def swap(i, j):
	tmp = i
	i = j
	j = tmp
	return i, j


class Coordinate(object):
	def __init__(self, i, j):
		if j < i:
			i, j = swap(i, j)

		self.i = i
		self.j = j


class EdgeMatrix(object):
	def __init__(self, num_verts):
		assert isinstance(num_verts, int), "Number of verts must be an int"
		assert num_verts > 0, "Number of verts must be greater than zero"

		iterable = [np.array([0 for _ in range(num_verts)], dtype=np.uint8) for _ in range(num_verts)]
		self._data = np.array(iterable, dtype=np.uint8)
		self._num_edges = 0

		self.num_verts = int(num_verts)

	@property
	def count(self):
		return self._num_edges

	@staticmethod
	def _index(i, j):
		assert isinstance(i, int), "i coordinate must be an int"
		assert isinstance(j, int), "j coordinate must be an int"
		coord = Coordinate(i, j)
		return coord.i, coord.j

	def has_edge(self, i, j):
		i, j = self._index(i, j)
		return self._data[i][j]

	def connect(self, i, j):
		i, j = self._index(i, j)
		if self.has_edge(i, j):
			return
		self._data[i][j] = 1
		self._num_edges += 1

	def remove(self, i, j):
		i, j = self._index(i, j)
		if self.has_edge(i, j):
			self._num_edges -= 1
		self._data[i][j] = 0


class Graph(object):
	def __init__(self, num_verts):
		self.num_verts = int(num_verts)
		self.edges = EdgeMatrix(num_verts)

	@property
	def num_edges(self):
		return self.edges.count

	def output(self):
		for i in range(self.num_verts):
			row = ""
			for j in range(self.num_verts):
				row += str(self.edges.has_edge(i, j)) + "   "
			print(row + "\n")

	def connect(self, a, b):
		self.edges.connect(a, b)

	def remove(self, a, b):
		self.edges.remove(a, b)

	def density(self):
		if self.num_edges == 0 == self.num_verts == 0:
			return 0.0
		else:
			top = 2.0 * float(self.num_edges)
			bottom = float(self.num_verts) * float(self.num_verts - 1)
			return round((top / bottom), 5)

	def degree(self, switch):
		target = 0
		if switch == "min":
			target = self.num_verts - 1
			if target < 0:
				target = 0
		for i in range(self.num_verts):
			tmp = 0
			for j in range(self.num_verts):
				tmp += self.edges.has_edge(i, j)
			if switch == "max":
				if tmp > target:
					target = tmp
			elif switch == "min":
				if tmp < target:
					target = tmp
			else:
				print(GraphException("Invalid switch passed to degree."))
		return target
