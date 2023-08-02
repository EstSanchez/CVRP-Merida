import sumolib
import random
import sys
from Points import point


#    Generate point objects, warehouse with set coordinates, then a given length array
#    of points with random x and y coords given a limit

def genRandPoints(number, warehousex, warehousey, limitx, limity, network):
    error = True
    while error == True:
        locations = []
        for x in range(number+1):
            if(x == 0):
                warehouse = point(warehousex, warehousey)
            else:
                locations.append(point(random.randrange(limitx * 1/5, limitx), random.randrange(limity * 1/5, limity)))

    #   Finds the nearest edge to the coordinates of the point, assigns this edge to the point object

        listaRev = []
        edges = network.getNeighboringEdges(warehouse.posx, warehouse.posy, r = 150)
        if len(edges) > 0:
            distancesAndEdges = sorted(edges, key=lambda x: x[1])
            closestEdge, distance = distancesAndEdges[0]
            warehouse.setEdge(closestEdge)
            listaRev.append(warehouse.edge)
        for x in locations:
            edges = network.getNeighboringEdges(x.posx, warehouse.posy, r = 2000)
            distancesAndEdges = sorted(edges, key=lambda y: y[1])
            closestEdge, distance = distancesAndEdges[0]
            x.setEdge(closestEdge)
            listaRev.append(x.edge)
        if len(listaRev) == len(set(listaRev)):
            error = False
    return warehouse, locations



#     Given an array of point objects, generate the number of non-warehouse nodes, randomly assign a 
#     cost to each node (except for the warehouse which is 0) and generate a costMatrix beetween the 
#     nodes' edges using the getFastestPath sumolib method. Returns the number of nodes, costlist and 
#     costMatrix for the edges of the new graph.

def getNetworkInfo(network, vertexList, numVeh, capacidad):

    #   assign the values to the arrays

    numNodes = len(vertexList)
    costList = []
    for x in range(numNodes):
        if x == 0:
            costList.append(0)
        else:
            costList.append(random.randrange(1, 6))
    
    costMatrix = [[0 for i in range(numNodes)] for i in range(numNodes)]
    for i in range(numNodes):
        for j in range(numNodes):
            vertexA = vertexList[i]
            vertexB = vertexList[j]
            shortEdges, costMatrix[i][j] = network.getShortestPath(vertexA.edge, vertexB.edge)
            costMatrix[i][j] = round(costMatrix[i][j], 2)
            if costMatrix[i][j] == 'inf':
                costMatrix[i][j] = 99999999

    #   print the arrays 

    sys.stdout.write("numVeh = " + str(numVeh) + "\n")
    sys.stdout.write("capacidad = " + str(capacidad) + "\n")
    sys.stdout.write("numNodos = " + str(numNodes - 1) + "\n\n")
    sys.stdout.write("costoNodos = [")
    for x in costList:
        if x == 0:
            sys.stdout.write(str(x))
        else:
            sys.stdout.write(", " + str(x))
    sys.stdout.write("] \n\n")
    sys.stdout.write("costoAristas = [")
    for i in range(numNodes):
        if i != 0:
            sys.stdout.write(", \n")
        sys.stdout.write("[")
        for j in range(numNodes):
            if j != 0:
                sys.stdout.write(", ")
            sys.stdout.write(str(costMatrix[i][j]))
        sys.stdout.write("]")
    sys.stdout.write("]")









network = sumolib.net.readNet("MeridaFinal.net.xml.gz")

#   Get the limits of the map in x and y coordinates
limits = network.getBBoxXY()
limitx = int(limits [1][0] - limits[1][0]/6)
limity = int(limits [1][1] - limits[1][1]/6)

#   Define the coordinates of the warehouse location
warehousex = int(limitx/2)
warehousey = int(limity/2)

#   Define the number of nodes (additional to the warehouse) your graph will have
numNodes = 10

#   Generate the point objects of your nodes (with coords)
warehouse, locations = genRandPoints(numNodes, warehousex, warehousey, limitx, limity, network)
vertexList = []
vertexList.append(warehouse)
vertexList = vertexList + locations

#   Arbitrary parameters for printing the data
numVeh = 3
capacidad = 12



getNetworkInfo(network, vertexList, numVeh, capacidad)
print()
print()
counter = 0
for x in vertexList:
    print(str(counter) + str(x.edge))
    counter += 1



