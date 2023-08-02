from Vertex import Vertex
from math import sqrt

class Edge:
    def __init__(self, beginning, end, cost):
        self.vertexA = beginning
        self.vertexB = end
        self.cost = cost