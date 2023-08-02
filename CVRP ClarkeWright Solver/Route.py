from Vertex import Vertex
from Edge import Edge

class Route:
    def __init__(self, numb, capacity):
        self.num = numb
        self.sequence = []
        self.cost = 0
        self.maxCapacity = capacity
        self.capacity = 0
    
    def addEdges(self, edges, position, addedCost):
        for x in reversed(edges):
            self.sequence.insert(position, x)
        self.capacity += addedCost
    
    def calcCost(self):
        self.cost = 0
        for x in self.sequence:
            self.cost += x.cost

    def setNum(self, num):
        self.num = num
       