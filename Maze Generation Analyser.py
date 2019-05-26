import networkx as nx
import matplotlib.pyplot as plt
import random
import math

global GRIDSIZE_X
global GRIDSIZE_Y
global TESTINGFORCYCLES

GRIDSIZE_X = 32
GRIDSIZE_Y = 32
TESTINGFORCYCLES = False
RANDOMSTART = True


def drawG(mazeGrid):
    pos = dict([(n, n) for n in list(mazeGrid.nodes())])  # Makes every node have an attribute of it's own length

    nx.draw(mazeGrid, pos=pos, edges=mazeGrid.edges(), edge_color="black", width=3, node_size=30)


def getEdges(fullGrid, mazeGrid, nodeList, currentNode, startNode):
    # print('currentNode is ', currentNode)
    neighbourList = []
    if currentNode not in list(fullGrid.nodes()):
        print(currentNode, list(fullGrid.nodes()))
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
        return currentNodeList[-1]  # Returns most recent node to be added to currentNodelist
    elif bounds[0] < randomNum <= bounds[0] + bounds[1]:
        return currentNodeList[0]  # Returns oldest node to be added to currentNodeList
    elif bounds[0] + bounds[1] < randomNum <= bounds[0] + bounds[1] + bounds[2]:
        return currentNodeList[int(math.floor(len(currentNodeList) / 2))]  # Returns middle node
    elif bounds[0] + bounds[1] + bounds[2] < randomNum <= bounds[0] + bounds[1] + bounds[2] + bounds[3]:
        return random.choice(currentNodeList)  # Returns random node in currentNodeList


def createMaze(algorithm):
    fullGrid = nx.grid_2d_graph(GRIDSIZE_X, GRIDSIZE_Y)  # Graph Setup
    mazeGrid = nx.grid_2d_graph(GRIDSIZE_X, GRIDSIZE_Y)
    mazeGrid.remove_edges_from(list(mazeGrid.edges))     # Creates a grid with only nodes

    if RANDOMSTART is True:
        startNode = (random.randint(0, GRIDSIZE_X - 1), random.randint(0, GRIDSIZE_Y - 1))
    else:
        startNode = (0, 0)

#  -----------------------------------------------------------------------------------
    if algorithm == "Prim":

        currentNode = startNode
        possibleEdgeList = []
        nodeList = []
        nodeList.append(currentNode)

        while True:
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
                    newEdge = random.choice(possibleEdgeList)
                    mazeGrid.add_edge(newEdge[0], newEdge[1])
                    currentNode = newEdge[1]
                    backtrackList.append(currentNode)
                    nodeList.append(currentNode)
            else:   # backtracking
                currentNode = backtrackList[-1]
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
            possibleEdgeList = []
            for node in list(fullGrid.neighbors(currentNode)):  # Not using getEdges() because do not care if in grid
                possibleEdgeList.append([currentNode, node])
            newEdge = random.choice(possibleEdgeList)
            if newEdge[1] not in nodeList:
                mazeGrid.add_edge(newEdge[0], newEdge[1])
                nodeList.append(newEdge[1])
            currentNode = newEdge[1]
            if len(nodeList) == totalNodes:
                break
# -----------------------------------------------------------------------------------
    if algorithm == 'Hunt and Kill':
        currentNode = startNode

        nodeList = []
        nodeList.append(currentNode)
        totalNodes = GRIDSIZE_X * GRIDSIZE_Y
        completedMaze = False

        while True:
            possibleEdgeList = getEdges(fullGrid, mazeGrid, nodeList, currentNode, startNode)
            if possibleEdgeList == []:
                currentNode, mazeNode, completedMaze = iterNewNode(fullGrid, mazeGrid, nodeList, currentNode)
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
        mazeAttributes = {'newest': 0, 'oldest': 0, 'middle': 0, 'random': 100}  # MUST all add to 100
        print('new', mazeAttributes['newest'], 'old', mazeAttributes['oldest'], 'mid', mazeAttributes['middle'], 'ran', mazeAttributes['random'])
        currentNode = startNode

        visitedNodeList = []  # Historical list of all nodes that are now in the maze
        visitedNodeList.append(currentNode)
        currentNodeList = []  # The nodes whose neighbors are going to be added to the maze, eg:
        currentNodeList.append(currentNode)  # nodes who are surrounded by the maze are not a 'current node'
        totalNodes = GRIDSIZE_X * GRIDSIZE_Y

        while True:
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
        for y in range(GRIDSIZE_Y):
            for x in range(GRIDSIZE_X):  # for every node (x, y) in the grid
                chance = random.randint(0, 1)
                if chance == 0:  # Create an edge to the right
                    if (x + 1, y) in fullGrid.neighbors((x, y)):
                        mazeGrid.add_edge((x, y), (x + 1, y))
                    elif (x, y + 1) in fullGrid.neighbors((x, y)):  # Unless cannot, then create edge upwards
                        mazeGrid.add_edge((x, y), (x, y + 1))

                if chance == 1:  # Create an edge upwards
                    if (x, y + 1) in fullGrid.neighbors((x, y)):
                        mazeGrid.add_edge((x, y), (x, y + 1))
                    elif (x + 1, y) in fullGrid.neighbors((x, y)):  # Unless cannot, then create edge to the right
                        mazeGrid.add_edge((x, y), (x + 1, y))
# -----------------------------------------------------------------------------------
    if TESTINGFORCYCLES is True:
        try:
            nx.find_cycle(mazeGrid)
            # There was a cycle:
            print("YES - WAS A CYCLE")
        except nx.NetworkXNoCycle:
            print("NO CYCLES")
    # drawG(mazeGrid)
    return mazeGrid


def analyseMaze(mazeGrid, percentageDict, totalNodes, REPEAT):
    fourJunction = 0  # Node has 4 connected nodes (edges)
    threeJunction = 0  # Node has 3 connected nodes (edges)
    twoCorner = 0  # Node has 2 connected nodes, which are perpendicular
    straightLineHorizontal = 0  # Node has 2 connected nodes, which are opposite x directions (so in a straight line)
    straightLineVertical = 0  # Node has 2 connected nodes, which are opposite y directions (so in a straight line)
    straightLine = 0  # Combination of both directions
    deadEnds = 0  # Node has only 1 connected node, so is a dead end

    for y in range(GRIDSIZE_Y):
            for x in range(GRIDSIZE_X):
                neighbourList = list(mazeGrid.neighbors((x, y)))  # Nodes connected to the current node
                if len(neighbourList) == 4:
                    fourJunction += 1  # connected to all 4 surrounding nodes so is a 4 way junction
                if len(neighbourList) == 3:
                    threeJunction += 1
                if len(neighbourList) == 2:
                    if (x + 1, y) in neighbourList and (x - 1, y) in neighbourList:
                        straightLineHorizontal += 1
                        straightLine += 1
                    elif (x, y + 1) in neighbourList and (x, y - 1) in neighbourList:
                        straightLineVertical += 1
                        straightLine += 1
                    else:
                        twoCorner += 1
                if len(neighbourList) == 1:
                    deadEnds += 1
                if len(neighbourList) == 0:
                    raise Exception("Node with no neighbours - Should always have at least 1 connected!")
    fourJunction = (fourJunction / totalNodes) * 100
    threeJunction = (threeJunction / totalNodes) * 100
    twoCorner = (twoCorner / totalNodes) * 100
    straightLineHorizontal = (straightLineHorizontal / totalNodes) * 100
    straightLineVertical = (straightLineVertical / totalNodes) * 100
    straightLine = (straightLine / totalNodes) * 100
    deadEnds = (deadEnds / totalNodes) * 100
    percentageDict['fourJunction'] += fourJunction / REPEAT
    percentageDict['threeJunction'] += threeJunction / REPEAT
    percentageDict['twoCorner'] += twoCorner / REPEAT
    percentageDict['straightLineHorizontal'] += straightLineHorizontal / REPEAT
    percentageDict['straightLineVertical'] += straightLineVertical / REPEAT
    percentageDict['straightLine'] += straightLine / REPEAT
    percentageDict['deadEnds'] += deadEnds / REPEAT
    # print("fourWayJunction", fourJunction)
    # print("threeWayJunction", threeJunction)
    # print("twoWayCorner", twoCorner)
    # print("straightLineHorizontal", straightLineHorizontal)
    # print("straightLineVertical", straightLineVertical)
    # print("straightLine", straightLine)
    # print("deadEnds", deadEnds)

percentageDict = {'fourJunction': 0, 'threeJunction': 0, 'twoCorner' : 0,'straightLineHorizontal' : 0, 'straightLineVertical' : 0, 'straightLine' : 0, 'deadEnds' : 0}
totalNodes = GRIDSIZE_X * GRIDSIZE_Y
REPEAT = 1000
algorithm = input("Which maze would you like to analyse? ")
for i in range(REPEAT):
    print(i)
    mazeGrid = createMaze(algorithm)
    analyseMaze(mazeGrid, percentageDict, totalNodes, REPEAT)
print(percentageDict)
stopper = input('Is the result complete?')

# plt.show()
