#
# All the Graph Shenanigans, Will be using NetworkX for graph implementation
# Also where Heuristics and Costs will be Managed.
import networkx as nx
from collections import deque # For Queues
from enum import Enum

class TileType(Enum):
    EMPTY = 0
    BOX = 1
    PLAYER = 2
    GOAL = 3
    WALL = 4

class SokBotGraph:
    graph = nx.Graph()
    goalsPosition = None
    currentBoxPosition = None

    def __init__(self):
        self.goalsPosition = []
        self.currentBoxPosition = []

    # Private Helper Function to Create Node
    def __createNode(self, mapData, itemsData):
        # Create Nodes
        for row in range(len(mapData)):
            for column in range(len(mapData[row])):

                position = (column, row)
                currentTileType:TileType = TileType.EMPTY

                # HUERISTIC CALCULATION HERE
                h = 0

                if(mapData[row][column] != '#' and mapData[row][column] != '.'):
                    match itemsData[row][column]:
                        case ' ':
                            currentTileType = TileType.EMPTY
                        case '@':
                            currentTileType = TileType.PLAYER
                        case '$':
                            currentTileType = TileType.BOX
                            self.currentBoxPosition.append(position)
                else: # If mapData is a wall
                        if mapData[row][column] == '#':
                            currentTileType = TileType.WALL
                        else:
                            currentTileType = TileType.GOAL
                            self.goalsPosition.append(position)

                # EXPERIMENTAL
                # Dont create State if it's a wall
                if currentTileType == TileType.WALL:
                    continue
                self.graph.add_node(position, hue=h, tileType = currentTileType)


    # Private Helper Function to Generate Edges
    def __generateEdges(self, graph:nx.Graph):
        for node in graph.nodes(data=True):
            x,y = node[0]
            cost = 1

            neighbors = [
                (x, y-1),
                (x, y+1),
                (x-1,y),
                (x+1,y)
            ]

            for neighbor in neighbors:
                if graph.has_node(neighbor):
                    # Check if Neighbor Node is BOX
                    if graph.nodes[neighbor]['tileType'] == TileType.BOX:
                        cost = 2
                    graph.add_edge((x,y), neighbor, weight=cost)


    # Prepare functions to get Hueristics for BFS
    def getHue_bfs(self, goalPosition: tuple): # Returns List of list[(position),hueristic]
        queue = deque()
        distances = {}

        distances[goalPosition] = 0
        queue.append(goalPosition)

        while queue:
            currentNode = queue.popleft()
            currentDistance = distances[currentNode]

            #  Get Neighbors
            for neighbor in self.graph.neighbors(currentNode):
                if not neighbor in distances:
                    distances[neighbor] = currentDistance + 1
                    queue.append(neighbor)

        return distances

    def getHue_man(self):
        pass

    def convertDataToGraph(self, mapData, itemsData):
        # Create Node
        self.__createNode(mapData, itemsData)

        # Generate Edges
        self.__generateEdges(self.graph)

        # DEBUG GETHUE_BFS
        # GOAL POSITIONS FOR 1 (3,4) (8,4)
        # print(self.graph.neighbors((3,4)))
        print(self.getHue_bfs((3,4)))
