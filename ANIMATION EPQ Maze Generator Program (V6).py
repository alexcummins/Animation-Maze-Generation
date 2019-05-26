# Maze generation and anaylsis program #
# Created by Alex Cummins - 2018       #

import networkx as nx
import matplotlib.pyplot as plt
import pylab
import random
import math

global GRIDSIZE_X
global GRIDSIZE_Y
global TESTINGFORCYCLES

GRIDSIZE_X = 10
GRIDSIZE_Y = 10
TESTINGFORCYCLES = False  # Was used when I was testing whether the algorithms worked
RANDOMSTART = True  # Whether the mazes start generating at a random point

pylab.ion()


def drawG(mazeGrid):  # This is not really used when animating the maze generation
    pos = dict([(n, n) for n in list(mazeGrid.nodes())])  # Makes every node have an attribute of it's own length

    nx.draw(mazeGrid, pos=pos, edges=mazeGrid.edges(), edge_color="black", width=3, node_size=30)


def getFigures(algorithm, mazeGrid, currentNode, newEdge, currentNodeList, currentIterNode):  # Displays the maze's current status
    plt.clf()
    pos = dict([(n, n) for n in list(mazeGrid.nodes())])  # Makes every node have an attribute of it's own length
    nodeColours = ['red' if (u, v) == currentNode else 'blue' if (u, v) in currentNodeList else 'lime' if (u, v) == currentIterNode else 'white' for u, v in mazeGrid.nodes()]
    edgeColours = ['red' if ((u, v) == (newEdge[0], newEdge[1]) or (v, u) == (newEdge[0], newEdge[1])) else 'white' for u, v in mazeGrid.edges()]
    # The previous two create a list that colours each node and edge white unless I wanted to highlight it in some way. Not all are used for each algorithm.
    nx.draw(mazeGrid, pos=pos, edges=mazeGrid.edges(), edge_color=edgeColours, width=25, node_size=575, node_color=nodeColours, node_shape='o')
    fig = plt.figure(1)
    fig.patch.set_facecolor('black')  # Makes background black so it looks more like a maze
    fig.canvas.set_window_title(algorithm)
    pylab.draw()
    plt.pause(0.25)  # The time delay between each update. Make smaller to generate faster (and vice versa)


def getEdges(fullGrid, mazeGrid, nodeList, currentNode, startNode):  # Gets the edges around a node that connect to a node NOT in the maze
    neighbourList = []
    for node in list(fullGrid.neighbors(currentNode)):
        if node not in nodeList:
            neighbourList.append([currentNode, node])
    return neighbourList


def iterNewNode(algorithm, fullGrid, mazeGrid, nodeList, currentNode):
    for y in range(GRIDSIZE_Y):
        for x in range(GRIDSIZE_X):  # for every node (x, y) in the grid
            getFigures(algorithm, mazeGrid, currentNode, [0, 0], [], (x, y))
            if (x, y) not in nodeList:  # if the node is not in the maze, check if a neighbour is
                for node in list(fullGrid.neighbors((x, y))):  # if a neighbour is, return the node
                    if node in nodeList:
                        return (x, y), node, False  # Returns the new currentNode & mazeNode it is connected to
    return None, None, True  # If no free nodes found in the whole grid that are next to maze


def chooseNewNode(currentNodeList, mazeAttributes):  # helper function to choose which node to pick in the Growing Tree algorithm list
    randomNum = random.randint(1, 100)
    bounds = [mazeAttributes['newest'], mazeAttributes['oldest'], mazeAttributes['middle'], mazeAttributes['random']]
    if randomNum <= bounds[0]:
        return currentNodeList[-1]  # Returns most recent node to be added to currentNodelist
    elif bounds[0] < randomNum <= bounds[0] + bounds[1]:
        return currentNodeList[0]  # Returns oldest node to be added to currentNodeList
    elif bounds[0] + bounds[1] < randomNum <= bounds[0] + bounds[1] + bounds[2]:
        return currentNodeList[int(math.floor(len(currentNodeList) / 2))]  # Returns middle node
    elif bounds[0] + bounds[1] + bounds[2] < randomNum <= bounds[0] + bounds[1] + bounds[2] + bounds[3]:
        return random.choice(currentNodeList)  # Returns random node in currentNodeList


def createMaze(algorithm, newest, oldest, middle, rand):
    fullGrid = nx.grid_2d_graph(GRIDSIZE_X, GRIDSIZE_Y)  # Graph Setup
    mazeGrid = nx.grid_2d_graph(GRIDSIZE_X, GRIDSIZE_Y)
    mazeGrid.remove_edges_from(list(mazeGrid.edges))     # Creates a grid with only nodes

    if RANDOMSTART is True:
        startNode = (random.randint(0, GRIDSIZE_X - 1), random.randint(0, GRIDSIZE_Y - 1))
    else:
        startNode = (0, 0)

    currentNode = None  # Failsafe if algorithm doesn't have these for getFigures()
    newEdge = None

#  -----------------------------------------------------------------------------------
    if algorithm == "Prims":

        currentNode = startNode
        possibleEdgeList = []
        nodeList = []
        nodeList.append(currentNode)
        newEdge = None

        while True:
            getFigures(algorithm, mazeGrid, currentNode, newEdge, [], [])
            for i in getEdges(fullGrid, mazeGrid, nodeList, currentNode, startNode):
                possibleEdgeList.append(i)
            while possibleEdgeList != []:
                newEdge = random.choice(possibleEdgeList)
                possibleEdgeList.remove(newEdge)
                if newEdge[1] not in nodeList:
                    break

            if possibleEdgeList == []:
                break

            mazeGrid.add_edge(newEdge[0], newEdge[1])
            currentNode = newEdge[1]
            nodeList.append(currentNode)
# ------------------------------------------------------------------------------------
    if algorithm == "Kruskals":
        currentNode = None

        possibleEdgeList = list(fullGrid.edges())

        while True:
            newEdge = random.choice(possibleEdgeList)
            mazeGrid.add_edge(newEdge[0], newEdge[1])
            possibleEdgeList.remove(newEdge)
            try:
                nx.find_cycle(mazeGrid, source=newEdge[1])  # <-- This is very inefficient
                # There was a cycle:                        # and really slows down the algorithm
                mazeGrid.remove_edge(newEdge[0], newEdge[1])
            except nx.NetworkXNoCycle:
                None
                getFigures(algorithm, mazeGrid, currentNode, newEdge, [], [])
            if possibleEdgeList == []:
                break
# ------------------------------------------------------------------------------------
    if algorithm == "Recursive Backtracker":
        currentNode = startNode
        possibleEdgeList = []

        nodeList = []
        nodeList.append(currentNode)

        backtracking = False
        backtrackList = []
        backtrackList.append(currentNode)

        while True:
            if not backtracking:  # Going forward
                possibleEdgeList = getEdges(fullGrid, mazeGrid, nodeList, currentNode, startNode)
                if possibleEdgeList == []:
                    backtracking = True
                else:
                    getFigures(algorithm, mazeGrid, currentNode, newEdge, [], [])
                    newEdge = random.choice(possibleEdgeList)
                    mazeGrid.add_edge(newEdge[0], newEdge[1])
                    currentNode = newEdge[1]
                    backtrackList.append(currentNode)
                    nodeList.append(currentNode)
            else:   # backtracking
                currentNode = backtrackList[-1]
                newEdge = [0, 0]
                getFigures(algorithm, mazeGrid, currentNode, newEdge, [], [])
                backtrackList.pop(-1)  # removes last entry in backtrackList
                backtracking = False
                if currentNode == startNode:
                    break
                if backtrackList == []:
                    break
# -----------------------------------------------------------------------------------
    if algorithm == "Aldous-Broder":  # Uniform Spanning Tree
        currentNode = startNode

        nodeList = []
        nodeList.append(currentNode)
        totalNodes = GRIDSIZE_X * GRIDSIZE_Y

        while True:
            getFigures(algorithm, mazeGrid, currentNode, newEdge, [], [])
            possibleEdgeList = []
            for node in list(fullGrid.neighbors(currentNode)):  # Not using getEdges() because do not care if in grid
                possibleEdgeList.append([currentNode, node])
            newEdge = random.choice(possibleEdgeList)
            currentNode = newEdge[1]
            if newEdge[1] not in nodeList:
                mazeGrid.add_edge(newEdge[0], newEdge[1])
                nodeList.append(newEdge[1])
            else:
                newEdge = [0, 0]  # For the animation - clears the new edge
            if len(nodeList) == totalNodes:
                getFigures(algorithm, mazeGrid, currentNode, newEdge, [], [])
                break
# -----------------------------------------------------------------------------------
    if algorithm == 'Hunt and Kill':
        currentNode = startNode

        nodeList = []
        nodeList.append(currentNode)
        totalNodes = GRIDSIZE_X * GRIDSIZE_Y
        completedMaze = False

        while True:
            getFigures(algorithm, mazeGrid, currentNode, newEdge, [], [])
            possibleEdgeList = getEdges(fullGrid, mazeGrid, nodeList, currentNode, startNode)
            if possibleEdgeList == []:
                currentNode, mazeNode, completedMaze = iterNewNode(algorithm, fullGrid, mazeGrid, nodeList, currentNode)
                if completedMaze is True:  # maze is complete
                    break
                else:
                    mazeGrid.add_edge(currentNode, mazeNode)  # Connects the new starting node to the maze
                    nodeList.append(currentNode)
            else:
                newEdge = random.choice(possibleEdgeList)
                mazeGrid.add_edge(newEdge[0], newEdge[1])
                currentNode = newEdge[1]
                nodeList.append(currentNode)
# -----------------------------------------------------------------------------------
    if algorithm == 'Growing Tree':
        # mazeAttributes is the percentage chances of each method of choosing the next node in the list
        mazeAttributes = {'newest': newest, 'oldest': oldest, 'middle': middle, 'random': rand}  # MUST all add to 100
        currentNode = startNode

        visitedNodeList = []  # Historical list of all nodes that are now in the maze
        visitedNodeList.append(currentNode)
        currentNodeList = []  # The nodes whose neighbors are going to be added to the maze, eg:
        currentNodeList.append(currentNode)  # nodes who are surrounded by the maze are not a 'current node'
        totalNodes = GRIDSIZE_X * GRIDSIZE_Y

        while True:
            getFigures(algorithm, mazeGrid, currentNode, newEdge, currentNodeList, [])
            possibleEdgeList = getEdges(fullGrid, mazeGrid, visitedNodeList, currentNode, startNode)
            if possibleEdgeList == []:
                currentNodeList.remove(currentNode)
                if len(currentNodeList) == 0:  # If no current nodes, maze is complete
                    break
                currentNode = chooseNewNode(currentNodeList, mazeAttributes)
            else:
                newEdge = random.choice(possibleEdgeList)
                if newEdge[1] not in visitedNodeList:  # if new node not in the maze
                    mazeGrid.add_edge(newEdge[0], newEdge[1])
                    currentNodeList.append(newEdge[1])
                    visitedNodeList.append(newEdge[1])
                currentNode = chooseNewNode(currentNodeList, mazeAttributes)
# -----------------------------------------------------------------------------------
    if algorithm == 'Binary Tree':
        newEdge = []
        for y in range(GRIDSIZE_Y):
            for x in range(GRIDSIZE_X):  # for every node (x, y) in the grid
                chance = random.randint(0, 1)
                if chance == 0:  # Create an edge to the right
                    if (x + 1, y) in fullGrid.neighbors((x, y)):
                        mazeGrid.add_edge((x, y), (x + 1, y))
                        newEdge = ((x, y), (x + 1, y))
                    elif (x, y + 1) in fullGrid.neighbors((x, y)):  # Unless cannot, then create edge upwards
                        mazeGrid.add_edge((x, y), (x, y + 1))
                        newEdge = ((x, y), (x, y + 1))

                if chance == 1:  # Create an edge upwards
                    if (x, y + 1) in fullGrid.neighbors((x, y)):
                        mazeGrid.add_edge((x, y), (x, y + 1))
                        newEdge = ((x, y), (x, y + 1))
                    elif (x + 1, y) in fullGrid.neighbors((x, y)):  # Unless cannot, then create edge to the right
                        mazeGrid.add_edge((x, y), (x + 1, y))
                        newEdge = ((x, y), (x + 1, y))
                getFigures(algorithm, mazeGrid, (x, y), newEdge, [], [])
# -----------------------------------------------------------------------------------
    if TESTINGFORCYCLES is True:  # Test to see if algorithm is working correctly
        try:
            nx.find_cycle(mazeGrid)
            # There was a cycle:
            print("YES - WAS A CYCLE")
        except nx.NetworkXNoCycle:
            print("NO CYCLES")

    getFigures(algorithm, mazeGrid, [], [0, 0], [], [])  # Final display with no red


algorithm = input("""Which maze would you like to generate? Options:
Prims
Kruskals
Recursive Backtracker
Aldous-Broder
Hunt and Kill
Growing Tree
Binary Tree\n""")
forever = input("Would you like them to continue forever? (Yes) (No) ").lower()

pylab.show()

if algorithm == 'Growing Tree':  # So can choose how growing tree generates each time
    newest, oldest, middle, rand = [int(i) for i in input("Enter the percentages for Newest Oldest Middle Random. Leave a gap between each one. (eg; 30 20 15 35) ").split()]
else:
    newest, oldest, middle, rand = None, None, None, None

if forever == 'yes':
    while True:
        createMaze(algorithm, newest, oldest, middle, rand)
        plt.pause(5)
else:
    createMaze(algorithm, newest, oldest, middle, rand)

input("finished?")
