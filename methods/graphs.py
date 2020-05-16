from methods.exp_tree import exp_tree
import re
from methods.max_ramification import max_ram

class Graph():

    def __init__(self, vertex, edges):
        self.vertex = vertex
        self.edges = edges
        self.check(vertex, edges)

    def check(self, vertex, edges):
        for i in vertex:
            if type(i) != str:
                raise TypeError(f'Vertex must be stringº and {i} is not')
        for j in edges:
            matchobj = re.match('.*-.*',j)
            if not matchobj:
                raise ValueError(f'Edges must be defined as vertex-vertex and {j} is not')
        for edge in edges:
            if (not edge.split('-')[0] in vertex) or (not edge.split('-')[1] in vertex):
                raise ValueError(f'Some of the vertex in {edge} are not defined')


    def expansion_tree(self, pesos=None):
        ed = self.edges
        v = self.vertex
        exp_tree(ed, v, pesos)

    def maximum_ramification(self, weights):
        ed = self.edges
        v = self.vertex
        max_ram(ed, v, weights)




