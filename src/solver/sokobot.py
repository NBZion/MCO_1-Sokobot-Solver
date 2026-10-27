from src.solver.graph import SokBotGraph
import networkx as nx
import matplotlib.pyplot as plt
import src.gui.game
import time

class State:
    def __init__(self, player_pos: {int, int}, boxes_pos: list[{int, int}]):
        self.player_pos = player_pos
        self.boxes_pos = boxes_pos

    def redefineBoxes(self, new_boxes_pos: list[{int, int}]):
        self.boxes_pos = new_boxes_pos

class Node:
    def __init__(self, state: State, g: int, h: int, p: str):
        self.state = state
        self.g = g # Cost
        self.h = h # Heuristic
        self.p = p # Path

class SokoBot:

    def __init__(self):
        self.minimum_distance_goals = dict()
        self.visited_states = {} # stores visited states
        self.frontier = [] # stores frontier nodes
        self.danger_zones = self.__get_danger_zones()




    def solveSokobanPuzzle(self, width, height, mapData, itemsData):
        # YOU NEED TO REWRITE THE IMPLEMENTATION OF THIS METHOD TO MAKE THE BOT SMARTER
        # Default stupid behavior: Think (sleep) for 3 seconds, and then return a
        # sequence
        # that just moves left and right repeatedly.

        # Initialize SokoBot graph
        graph = SokBotGraph()

        graph.convertDataToGraph(mapData, itemsData)

        # Draw nodes and edges
#        nx.draw(graph.graph, with_labels=True, node_color='skyblue', node_size=500)

        # Displays an interactive desktop GUI window
#        plt.title("2D Grid Graph")
#        plt.show()


    # A STAR IMPLEMENTATION
    # NOTE: State contains player position and boxes position, while node contains State, g, h, and s

    # 1. Get Initial State and Starting Node

        # Initialize intial positions
        init_player_pos: {int, int}
        init_boxes_pos: list[{int, int}]

        for row in range(len(itemsData)):
            for column in range(len(itemsData[row])): # read the itemsData and check for player and boxes
                if(itemsData[row][column] == '@'):
                    init_player_pos = {row, column}
                elif(itemsData[row][column] == '$'):
                    init_boxes_pos.append({row, column})

        # Set initial states and starting node
        initial_state = State(init_player_pos, init_boxes_pos)
        starting_node = Node(initial_state, 0, self.__get_h_of_state(initial_state.boxes_pos), '')

        self.__insertToFrontier(starting_node)

        while self.frontier:
            node = self.frontier.pop(0)
            state = node.state

            if self.__checkGoal(state): return node.s

            if state in self.visited_states: continue # Skip the state
            self.visited_states[state] = True

            for dx, dy, dp in [(1, 0, 'd'), (-1, 0, 'u'), (0, 1, 'r'), (0, -1, 'l')]:
                # TODO: Check if tile is out of bounds or an impassable object
                new_player_pos = (state.player_pos[0] + dx, state.player_pos[1] + dy)
                new_boxes_pos = state.boxes_pos

                if 0 <= new_player_pos[0] < height and 0 <= new_player_pos[1] < width and mapData[new_player_pos[0]][new_player_pos[1]] != '#':
                    if new_player_pos in new_boxes_pos:
                        new_box_pos = (new_player_pos[0] + dx, new_player_pos[1] + dy)
                        if 0 <= new_box_pos[0] < height and 0 <= new_box_pos[1] < width and mapData[new_box_pos[0]][new_box_pos[1]] != '#' and new_box_pos not in new_boxes_pos:
                            new_boxes_pos.remove(new_player_pos)
                            new_boxes_pos.append(new_box_pos)
                        else: continue
                    new_state = State(new_player_pos, new_boxes_pos)
                    new_node = Node(new_state, node.g + 1, self.__get_h_of_state(new_boxes_pos), node.s + dp)
                    self.__insertToFrontier(new_node)

        return None




    def __insertToFrontier(self, node: Node):

        # GO THROUGH STATES
        sorted_boxes_pos = sorted(node.state.boxes_pos)
        node.state.redefineBoxes(sorted_boxes_pos)

        if node.state in self.visited_states: return

        f = node.g + node.h

        # Find a node with a greater f value to place the value at
        for n in range(len(self.frontier)):
            if self.frontier[n].h + self.frontier[n].g > f:
                self.frontier.insert(n, node)
                return
        self.frontier.append(node)
        return




    def __get_h_of_state(self, boxes_pos: list[{int, int}]):
        h = 0
        for box_pos in boxes_pos:
            # add the heuristic of each box
            # h += 
            pass
        return h




    def __get_danger_zones():
        pass




    def __checkGoal(self, state: State, mapData) -> bool:
        for box in state.boxes_pos:
            if mapData[state.player_pos[0]][state.player_pos[1]] != '.':
                return False
        return True
        # TODO: Check if every box is in the goal




















# -------------------------------------------------------------------------------------------------------------------------------------------------
# NOTE:
# 1. DIAGRAM IS IN ROW-MAJOR (i.e., position is [row][column])

# 2. FOLLOW THE FOLLOWING NOTATION FOR THE STRING RETURN VALUE
    # u: execute_move(0) -> row--
    # d: execute_move(1) -> row++
    # l: execute_move(2) -> column--
    # r: self.execute_move(3) -> column++

# 3. {0, 0} is always at the top left