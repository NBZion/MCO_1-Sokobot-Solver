from src.solver.graph import SokBotGraph
import networkx as nx
import matplotlib.pyplot as plt
import src.gui.game
import time

class State:
    def __init__(self, player_pos: tuple[int, int], boxes_pos: list[(int, int)]):
        self.player_pos = player_pos
        self.boxes_pos = boxes_pos
        self.deadspace = []

    def redefineBoxes(self, new_boxes_pos: list[(int, int)]):
        self.boxes_pos = new_boxes_pos

class Node:
    def __init__(self, state: State, g: int, h: int, p: str):
        self.state = state
        self.g = g # Cost
        self.h = h # Heuristic
        self.p = p # Path

class SokoBot:

    def __init__(self):
        self.minimum_distance_goals = {}
        self.visited_states = {} # stores visited states
        self.frontier = [] # stores frontier nodes

        self.goals_pos = []


    def solveSokobanPuzzle(self, width, height, mapData, itemsData):
        # YOU NEED TO REWRITE THE IMPLEMENTATION OF THIS METHOD TO MAKE THE BOT SMARTER
        # Default stupid behavior: Think (sleep) for 3 seconds, and then return a
        # sequence
        # that just moves left and right repeatedly.

        # Initialize SokoBot graph
        graph = SokBotGraph()

        # graph.convertDataToGraph(mapData, itemsData)

        # Draw nodes and edges
#        nx.draw(graph.graph, with_labels=True, node_color='skyblue', node_size=500)

        # Displays an interactive desktop GUI window
#        plt.title("2D Grid Graph")
#        plt.show()


    # A STAR IMPLEMENTATION
    # NOTE: State contains player position and boxes position, while node contains State, g, h, and s

    # 1. Get Initial State and Starting Node

        # Initialize intial positions and goal position BFS
        init_player_pos: tuple[int, int]
        init_boxes_pos = list((int, int))
        self.deadspace = self.load_map_deadspace(mapData, width, height)

        for row in range(len(itemsData)):
            for column in range(len(itemsData[row])): # read the itemsData and check for player and boxes
                if(itemsData[row][column] == '@'):
                    init_player_pos = {row, column}
                elif(itemsData[row][column] == '$'):
                    init_boxes_pos.append({row, column})

        for row in range(len(mapData)):
            for column in range(len(mapData[row])):
                if(mapData[row][column] == '.'):
                    self.goals_pos.append({row, column})

        for goal in self.goals_pos:
            self.minimum_distance_goals[goal] = graph.getHue_bfs(tuple(goal[0], goal[1]))

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
                        if self.deadspace[new_box_pos[0]][new_box_pos[1]]:
                            continue
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
            h += min([self.minimum_distance_goals[goal_pos][box_pos[0]][box_pos[1]] for goal_pos in self.goals_pos])
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




    def is_block_corner(self, map_data, row: int, col: int) -> bool:
        return (map_data[row - 1][col] == "#" and map_data[row][col - 1] == "#") or (map_data[row - 1][col] == "#" and map_data[row][col + 1] == "#") or (map_data[row + 1][col] == "#" and map_data[row][col - 1] == "#") or (map_data[row + 1][col] == "#" and map_data[row][col + 1] == "#")




    def load_map_deadspace (self, map_data, width, height):
        self.deadspace = [[False for _ in range (len(map_data[r]))] for r in range(len(map_data))]
        
        for row in range(len(map_data)):
            for col in range(len(map_data[row])): # read the itemsData and check for player and boxes
                if self.deadspace[row][col]:
                    continue
                if map_data[row][col] == "#":
                    self.deadspace[row][col] = True
                elif map_data[row][col] == ".":
                    self.deadspace[row][col] = False
                elif row > 0 and col > 0 and row < height - 2 and col < width - 2 and self.is_block_corner(map_data, row, col) and map_data[row][col] != ".":
                    self.deadspace[row][col] = True
        
        for row in range(len(map_data)):
            for col in range(len(map_data[row])):
                if(map_data[row][col] == "#" and map_data[row][col] == "."):
                    continue
                elif(self.deadspace[row][col]):
                    continue
                elif(row > 0 and col > 0 and col < width - 2 and row < height - 2):
                    if(map_data[row-1][col] == "#" or map_data[row+1][col] == "#"):
                        
                        right_col = col                                                                        
                        
                        while right_col < width - 1 and map_data[row][right_col + 1] != "#" and (map_data[row - 1][right_col] == "#" or map_data[row+1][right_col] == "#") and map_data[row][right_col] != ".":
                            right_col += 1
                        if not self.is_block_corner(map_data, row, right_col) or not self.deadspace[row][right_col]:
                            continue
                        
                        left_col = col

                        while left_col > 0 and map_data[row][col - 1] != "#" and (map_data[row-1][right_col] == "#" or map_data[row+1][left_col] == "#") and map_data[row][left_col] != ".":
                            left_col -= 1
                        if not self.is_block_corner(map_data, row, left_col) or not self.deadspace[row][left_col]:
                            continue

                        for current_col in range (left_col, right_col + 1):
                            self.deadspace[row][current_col] = True

                    if map_data[row][col-1] == "#" or map_data[row][col+1] == "#":
                        
                        top_row = row
                        while top_row > 0 and map_data[top_row-1][col] != "#" and (map_data[top_row][col-1] == "#" or map_data[top_row][col+1] == "#") and map_data[top_row][col] != ".":
                            top_row -= 1
                        if not self.is_block_corner(map_data, top_row, col) or not self.deadspace[top_row][col]:
                            continue
                        
                        bottom_row = row
                        while bottom_row < height - 1 and map_data[bottom_row+1][col] != "#" and (map_data[bottom_row][col-1] == "#" or map_data[bottom_row][col+1] == "#") and map_data[bottom_row][col] != ".":
                            bottom_row += 1
                        if not self.is_block_corner(map_data, bottom_row, col) or not self.deadspace[bottom_row][col]:
                            continue 

                        for current_row in range (top_row, bottom_row + 1):
                            self.deadspace[current_row][col] = True
        













# -------------------------------------------------------------------------------------------------------------------------------------------------
# NOTE:
# 1. DIAGRAM IS IN ROW-MAJOR (i.e., position is [row][column])

# 2. FOLLOW THE FOLLOWING NOTATION FOR THE STRING RETURN VALUE
    # u: execute_move(0) -> row--
    # d: execute_move(1) -> row++
    # l: execute_move(2) -> column--
    # r: self.execute_move(3) -> column++

# 3. {0, 0} is always at the top left