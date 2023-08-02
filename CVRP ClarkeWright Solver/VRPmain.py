from Vertex import Vertex
from Edge import Edge
from Route import Route
from Savings import Saving
import sys
import time

start = time.time()

def createNetwork(numNodos, costoNodos, costoAristas):
    nvertices = []
    for x in range(numNodos+1):
        nvertices.append(Vertex(x, costoNodos[x]))
    
    nedges = []
    counterA = 0
    counterB = 0
    for a in nvertices:
        for b in nvertices:
            nedges.append(Edge(a,b, costoAristas[counterA][counterB]))
            counterB += 1
        counterA += 1
        counterB = 0
    return nvertices, nedges



def findEdge(edges, A, B):
    for x in edges:
        if(x.vertexA == A and x.vertexB == B):
            edge = x
            break
    
    return edge


def initRoutes(vertices, edges, capacity):
    routes = []
    i = 0
    for x in vertices:
        if(x != vertices[0]):
            newCost = x.cost
            routes.insert(i, Route(i+1, capacity))
            routes[i].addEdges([findEdge(edges,vertices[0],x),findEdge(edges,x,vertices[0])], 0, newCost)
            i += 1
    return routes


def displayRoutes(routes):
    for x in routes:
        sys.stdout.write("Route " + str(x.num) + ": [")
        for edge in x.sequence:
            sys.stdout.write("(" + str(edge.vertexA.num) + ", " + str(edge.vertexB.num) + "),")
        sys.stdout.write("]")
        print()
    return


def computeSavings(A, B, edges, vertices, parameter):
    value = findEdge(edges, A, vertices[0]).cost + findEdge(edges, vertices[0], B).cost - (parameter*findEdge(edges, A, B).cost)
    return value


def createSavings(vertices, edges, parameter):
    savings = []
    for A in vertices:
        for B in vertices:
            if (A.num != 0 and B.num != 0 and A != B):
                value = computeSavings(A, B, edges, vertices, parameter)
                savings.append(Saving(A, B, value))
    savings.sort(key = lambda x:x.value,reverse = True)
    return savings


def checkSavingFeasibility(routes, saving, vertices):
    if (saving.value <= 0):
        return False
    A = saving.vertexA
    B = saving.vertexB
    Afound = False
    Bfound = False
    requirementA = False
    requirementB = False
    for x in routes:
        for edge in x.sequence:
            if(edge.vertexA == A and edge.vertexB == vertices[0]):
                Afound = True
            if(edge.vertexB == B and edge.vertexA == vertices[0]):
                Bfound = True
        if(Afound == True and Bfound == True):
            return False
        if(Afound == True):
            requirementA = True
            routeA = x
        if(Bfound == True):
            requirementB = True
            routeB = x
        Afound = False
        Bfound = False
    if(requirementA == True and requirementB == True) and (routeA.capacity + routeB.capacity <= routeA.maxCapacity):
        return True
    return False


def mergeRoutes(saving, edges, routes, vertices, capacidad):
    i = 0
    for x in routes:
        for edge in x.sequence:
            if(edge.vertexA == saving.vertexA and edge.vertexB == vertices[0]):
                A = i
            if(edge.vertexA == vertices[0] and edge.vertexB == saving.vertexB):
                B = i
        i += 1
    del(routes[A].sequence[len(routes[A].sequence)-1])
    del(routes[B].sequence[0])
    connector = [findEdge(edges, saving.vertexA, saving.vertexB)]
    newSequence = routes[A].sequence + connector + routes[B].sequence
    addedCost = routes[A].capacity + routes[B].capacity
    del(routes[A])
    if(A>B):
        del(routes[B])
    else:
        del(routes[B-1])
    routes.append(Route(len(routes),capacidad))
    routes[len(routes)-1].addEdges(newSequence, 0, addedCost)
    return routes

def ClarkeAndWright(vertices, edges, capacity, parameter):
    routes = []
    routes = initRoutes(vertices, edges, capacity)
    savings = createSavings(vertices, edges, parameter)
    while len(savings) > 0:
        i = 0
        if checkSavingFeasibility(routes, savings[i], vertices) == True:
            routes = mergeRoutes(savings[i], edges, routes, vertices, capacity)
        del(savings[i])
        i += 1
    for x in routes:
        x.calcCost()
    routes.sort(key = lambda x: x.cost, reverse = True)
    j = 1
    for x in routes:
        x.setNum(j)
        j += 1
    return routes

def calculateCost(routes):
    cost = 0
    for x in routes:
        for w in x.sequence:
            cost += w.cost
    return cost



numVeh = 12
capacidad = 25
numNodos = 10

costoNodos = [0, 3, 3, 3, 2, 4, 3, 4, 4, 1, 4]

costoAristas = [[50.79, 856.42, 1413.8, 363.11, 3037.11, 756.9, 2523.16, 4166.49, 4140.17, 1940.91, 2672.65],
[980.35, 103.16, 931.04, 597.12, 3718.78, 388.41, 3204.83, 4848.16, 4821.84, 1319.4, 3354.32],
[1622.33, 946.31, 93.31, 1401.41, 4002.56, 1024.51, 3721.5, 5131.94, 5320.76, 995.16, 3798.33],
[490.25, 707.55, 1357.02, 47.81, 3203.12, 608.03, 2689.17, 4332.5, 4306.18, 1758.01, 2838.66],
[3126.92, 3638.23, 3929.28, 3306.42, 126.41, 3538.71, 1114.53, 1706.26, 1848.95, 4485.78, 965.04],
[866.23, 375.34, 1024.81, 469.4, 3591.06, 92.5, 3077.11, 4720.44, 4694.12, 1425.8, 3226.6],
[2656.25, 3379.17, 3670.22, 2968.57, 860.43, 3279.65, 149.49, 2093.81, 2096.48, 4226.72, 298.98],
[4089.9, 4601.21, 4892.26, 4269.4, 1728.87, 4501.69, 2138.98, 84.5, 1181.86, 5448.76, 1989.49],
[4545.06, 5308.59, 5599.64, 4857.38, 2347.52, 5209.07, 2645.53, 1531.42, 21.03, 6156.14, 2496.04],
[2208.56, 1450.19, 1239.7, 1877.04, 4616.03, 1528.39, 4334.97, 5745.41, 5934.23, 167.57, 4411.8],
[2506.76, 3291.04, 3645.93, 2819.08, 1009.92, 3191.52, 298.98, 2243.3, 2245.97, 4202.43, 149.49]]



















vertices, edges = createNetwork(numNodos, costoNodos, costoAristas)
routes = ClarkeAndWright(vertices, edges, capacidad, 1)
print("Clarke and Wright")
displayRoutes(routes)
cost = calculateCost(routes)
print(cost)
end = time.time()
print("Time: " + str(end-start))

routes = ClarkeAndWright(vertices, edges, capacidad, 0.4)
print("Clarke and Wright (Enhanced)")
displayRoutes(routes)
cost = calculateCost(routes)
print(cost)

    
