import networkx as nx
import matplotlib.pyplot as plt
import random
import math

import time
import numpy as np
import matplotlib

global GRIDSIZE_X
global GRIDSIZE_Y
global TESTINGFORCYCLES

GRIDSIZE_X = 15
GRIDSIZE_Y = 15
TESTINGFORCYCLES = False


def drawG(mazeGrid):
    pos = dict([(n, n) for n in list(mazeGrid.nodes())])  # Makes every node have an attribute of it's own length

    nx.draw(mazeGrid, pos=pos, edges=mazeGrid.edges(), edge_color="black", width=3, node_size=30)
    # DrawLikeMaze
    # nx.draw(mazeGrid, pos=pos, edges=mazeGrid.edges(), edge_color="black", width=3, node_size=30)
    return pos


def getEdges(fullGrid, mazeGrid, nodeList, currentNode, startNode):
    # print('currentNode is ', currentNode)
    neighbourList = []
    for node in list(fullGrid.neighbors(currentNode)):
        if node not in nodeList:
            neighbourList.append([currentNode, node])
    return neighbourList


def iterNewNode(fullGrid, mazeGrid, nodeList, currentNode):
    for y in range(GRIDSIZE_Y):
        for x in range(GRIDSIZE_X):  # for every node (x, y) in the grid
            if (x, y) not in nodeList:  # if the node is not in the maze, check if a neighbour is
                for node in list(fullGrid.neighbors((x, y))):  # if a neighbour is, return the node
                    if node in nodeList:
                        return (x, y), node, False  # Returns the new currentNode & mazeNode it is connected to
    return None, None, True  # If no free nodes found in the whole grid that are next to maze


def chooseNewNode(currentNodeList, mazeAttributes):
    randomNum = random.randint(1, 100)
    bounds = [mazeAttributes['newest'], mazeAttributes['oldest'], mazeAttributes['middle'], mazeAttributes['random']]
    if randomNum <= bounds[0]:
        print('Newest')
        return currentNodeList[-1]  # Returns most recent node to be added to currentNodelist
    elif bounds[0] < randomNum <= bounds[0] + bounds[1]:
        print("Oldest")
        return currentNodeList[0]  # Returns oldest node to be added to currentNodeList
    elif bounds[0] + bounds[1] < randomNum <= bounds[0] + bounds[1] + bounds[2]:
        print("Middle")
        return currentNodeList[int(math.floor(len(currentNodeList) / 2))]  # Returns middle node
    elif bounds[0] + bounds[1] + bounds[2] < randomNum <= bounds[0] + bounds[1] + bounds[2] + bounds[3]:
        print("Random")
        return random.choice(currentNodeList)  # Returns random node in currentNodeList


def createMaze(algorithm):
    fullGrid = nx.grid_2d_graph(GRIDSIZE_X, GRIDSIZE_Y)  # Graph Setup
    mazeGrid = nx.grid_2d_graph(GRIDSIZE_X, GRIDSIZE_Y)
    mazeGrid.remove_edges_from(list(mazeGrid.edges))     # Creates a grid with only nodes
    print(fullGrid)


createMaze("Binary Tree")
plt.show()
