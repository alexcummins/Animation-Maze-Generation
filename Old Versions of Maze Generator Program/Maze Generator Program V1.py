import networkx as nx
import matplotlib.pyplot as plt
import random

global GRIDSIZE_X
global GRIDSIZE_Y

GRIDSIZE_X = 8
GRIDSIZE_Y = 8

# SOME RANDOM LOOPS, NEED TO FIX


def drawG(g):
    pos = dict([(n, n) for n in list(g.nodes())])  # Makes every node have an attribute of it's own length
    # edgeColour = dict([e, 'b'] for e in list(g.edges()) if e['inST'] is True)
    edgeColours = ['black' if g[u][v]['inST'] == (True) else 'white' for u, v in g.edges()]
    print(edgeColours)

    nx.draw(g, pos=pos, edges=g.edges(), edge_color=edgeColours, width=10)
    return pos


def getEdges(graph, node):
    # print('currentNode is ', node)
    neighbourList = []
    # print('all neighbors', list(graph.neighbors(node)))
    for i in list(graph.neighbors(node)):
        # print('considered', i)
        # print('is not possible to add', graph[node][i]['inST'])
        if graph[node][i]['inST'] == (False) and checkConnectedToTree(graph, i) == (False):
            neighbourList.append([node, i])
    # print('all successful neighbors', neighbourList)
    return neighbourList


def checkConnectedToTree(graph, node):
    for i in list(graph.neighbors(node)):
        # print('neighbors being checked', node, i)
        if graph[node][i]['inST'] == (True):
            # print('had a connected edge')
            return True
    return False


def removeCurrentEdges(graph, node, possibleEdgeList):
    for i in possibleEdgeList:
        if i[1] == node:
            possibleEdgeList.remove(i)
    return possibleEdgeList


def createMaze(algorithm):
    g = nx.grid_2d_graph(GRIDSIZE_Y, GRIDSIZE_X)  # Graph Setup
    nx.set_edge_attributes(g, False, "inST")
    print(g)
    if algorithm == "Prim":
        # print(algorithm)
        currentNode = (0, 0)
        possibleEdgeList = []

        while True:
            for i in getEdges(g, currentNode):
                possibleEdgeList.append(i)
            # print('possibleEdgeList -', possibleEdgeList)
            newEdge = random.choice(possibleEdgeList)
            # print(newEdge[0], 'new edges', newEdge[1])
            g[newEdge[0]][newEdge[1]]['inST'] = (True)
            possibleEdgeList.remove(newEdge)
            currentNode = newEdge[1]
            possibleEdgeList = removeCurrentEdges(g, currentNode, possibleEdgeList)
            if possibleEdgeList == []:
                break
            # print(len(possibleEdgeList))
    drawG(g)


createMaze("Prim")
plt.show()
