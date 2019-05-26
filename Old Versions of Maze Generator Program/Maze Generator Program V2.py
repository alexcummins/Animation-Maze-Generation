import networkx as nx
import matplotlib.pyplot as plt
import random

global GRIDSIZE_X
global GRIDSIZE_Y

GRIDSIZE_X = 25
GRIDSIZE_Y = 25


def drawG(mazeGrid):
    pos = dict([(n, n) for n in list(mazeGrid.nodes())])  # Makes every node have an attribute of it's own length

    nx.draw(mazeGrid, pos=pos, edges=mazeGrid.edges(), edge_color="black", width=3, node_size=30)
    return pos


def getEdges(fullGrid, mazeGrid, currentNode, startNode):
    # print('currentNode is ', currentNode)
    neighbourList = []
    for node in list(fullGrid.neighbors(currentNode)):
        if checkConnectedToTree(mazeGrid, startNode, node) is False:
            neighbourList.append([currentNode, node])
    return neighbourList


def checkConnectedToTree(graph, nodeA, nodeB):
    try:
        nx.bidirectional_dijkstra(graph, nodeA, nodeB)
    except nx.NetworkXNoPath:
        return False
    else:
        return True


def removeCurrentEdges(graph, startNode, node, possibleEdgeList):
    # Removes the edge just added, as well as any that are connected to the tree.
    for i in possibleEdgeList:
        if i[1] == node or checkConnectedToTree(graph, startNode, i[1]) is True:
            possibleEdgeList.remove(i)
    return possibleEdgeList


def createMaze(algorithm):
    fullGrid = nx.grid_2d_graph(GRIDSIZE_Y, GRIDSIZE_X)  # Graph Setup
    mazeGrid = nx.grid_2d_graph(GRIDSIZE_Y, GRIDSIZE_X)
    mazeGrid.remove_edges_from(list(mazeGrid.edges))

    print(mazeGrid)
    if algorithm == "Prim":
        startNode = (0, 0)
        currentNode = startNode
        possibleEdgeList = []

        while True:
            for i in getEdges(fullGrid, mazeGrid, currentNode, startNode):
                possibleEdgeList.append(i)
            newEdge = random.choice(possibleEdgeList)
            if checkConnectedToTree(mazeGrid, startNode, newEdge[1]) is False:
                # print(checkConnectedToTree(mazeGrid, startNode, newEdge[1]))
                mazeGrid.add_edge(newEdge[0], newEdge[1])
                possibleEdgeList.remove(newEdge)
                currentNode = newEdge[1]
                possibleEdgeList = removeCurrentEdges(mazeGrid, startNode, currentNode, possibleEdgeList)
            else:
                possibleEdgeList.remove(newEdge)
            if possibleEdgeList == []:
                break

    if algorithm == "Kruskals":
        startNode = (0, 0)
        currentNode = startNode

        possibleEdgeList = list(fullGrid.edges())

        while True:
            newEdge = random.choice(possibleEdgeList)
            mazeGrid.add_edge(newEdge[0], newEdge[1])
            possibleEdgeList.remove(newEdge)
            try:
                nx.find_cycle(mazeGrid, source=newEdge[1])
                # There was a cycle:
                mazeGrid.remove_edge(newEdge[0], newEdge[1])
            except nx.NetworkXNoCycle:
                None
            if possibleEdgeList == []:
                break
    drawG(mazeGrid)


createMaze("Prim")
plt.show()
