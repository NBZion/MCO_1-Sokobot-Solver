from src.solver.graph import SokBotGraph
import networkx as nx
import matplotlib.pyplot as plt
import src.gui.game
from time import perf_counter

class State:
    def __init__(self, player_pos: tuple[int, int], boxes_pos: list[(int, int)]):
        self.player_pos = player_pos
        self.boxes_pos = boxes_pos

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
        self.minimum_distance_goals = {} # stores the distance from each in the map to every goal
        self.visited_states = {} # stores visited states
        self.frontier = [] # stores frontier nodes

        self.goals_pos = [] # stores every goal's position in the map
        self.deadspace = []


    def solveSokobanPuzzle(self, width, height, mapData, itemsData):
        # Initialize SokoBot graph
        graph = SokBotGraph()
        graph.convertDataToGraph(mapData, itemsData)

    # 1. Get Initial State and Starting Node

        # Initialize intial positions and goal position BFS
        init_player_pos = []
        init_boxes_pos = []
        self.load_map_deadspace(mapData, width, height)

        # Get initial player position and every box position in the map
        start_time = perf_counter()
        for col in range(len(itemsData)):
            for row in range(len(itemsData[col])): # read the itemsData and check for player and boxes
                if(itemsData[col][row] == '@'):
                    init_player_pos = (col, row)
                elif(itemsData[col][row] == '$'):
                    init_boxes_pos.append((col, row))

        end_time = perf_counter()
        total_time = end_time - start_time
        print(f"Item Data Time: {total_time:.6f} seconds")


        # Get every goal position in the map
        start_time = perf_counter()
        for col in range(len(mapData)):
            for row in range(len(mapData[col])):
                if(mapData[col][row] == '.'):
                    self.goals_pos.append((col, row))

        end_time = perf_counter()
        total_time = end_time - start_time
        print(f"Goal Data Time: {total_time:.6f} seconds")

        # For every goal position, get the minimum distance from each position in the graph
        start_time = perf_counter()
        g = 0
        for goal in self.goals_pos:
            g += 1
            start_time_g = perf_counter()
            self.minimum_distance_goals[goal] = graph.getHue_bfs((goal[0], goal[1]))
            end_time_g = perf_counter()
            total_time = end_time_g - start_time_g
            print(g)
            print(f"nd Goal BFS Time: {total_time:.6f} seconds")
        end_time = perf_counter()
        total_time = end_time - start_time
        print(f"All Goals Data Time: {total_time:.6f} seconds")

        # Set initial states and starting node
        initial_state = State(init_player_pos, init_boxes_pos)
        starting_node = Node(initial_state, 0, self.__get_h_of_state(initial_state.boxes_pos), '')

        self.__insertToFrontier(starting_node)

    # 2. Start Exploring the Different States
        while self.frontier:
            node = self.frontier.pop(0)
            state = node.state

            if self.__checkGoal(state, mapData):
                print("Successful!")
                return node.p

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
                    new_node = Node(new_state, node.g + 1, self.__get_h_of_state(new_boxes_pos), node.p + dp)
                    print(new_state)
                    print(new_node)
                    self.__insertToFrontier(new_node)

        print("Failure")
        return None




    def __insertToFrontier(self, node: Node):

        start_time = perf_counter()
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

        end_time = perf_counter()
        total_time = end_time - start_time
        print(f"Frontier Append Time: {total_time:.6f} seconds")
        return




    def __get_h_of_state(self, boxes_pos):
        start_time = perf_counter()
        h = 0
        for box_pos in boxes_pos:
            h += min([self.minimum_distance_goals[goal_pos][box_pos] for goal_pos in self.goals_pos])
            pass

        end_time = perf_counter()
        total_time = end_time - start_time
        print(f"Heuristic of State Retrieval Time: {total_time:.6f} seconds")
        return h




    def __checkGoal(self, state: State, mapData) -> bool:
        returnValue = False
        for goal in self.goals_pos:
            print("Goal:")
            print(goal)
            for box in state.boxes_pos:
                print("Box")
                print(box)
                if box != goal:
                    returnValue = False
                    continue
                returnValue = True
                break
            if not returnValue: return returnValue

        return returnValue
                

        # TODO: Check if every box is in the goal




    def is_block_corner(self, map_data, row: int, col: int) -> bool:
        return (map_data[col-1][row] == "#" and map_data[col][row-1] == "#") or (map_data[col-1][row] == "#" and map_data[col][row+1] == "#") or (map_data[col+1][row] == "#" and map_data[col][row-1] == "#") or (map_data[col+1][row] == "#" and map_data[col][row+1] == "#")




    def load_map_deadspace (self, map_data, width, height):
        start_time = perf_counter()
        self.deadspace = [[False for _ in range (len(map_data[r]))] for r in range(len(map_data))]

        for col in range(len(map_data)):
            for row in range(len(map_data[col])): # read the itemsData and check for player and boxes
                if self.deadspace[col][row]:
                    continue
                if map_data[col][row] == "#":
                    self.deadspace[col][row] = True
                elif map_data[col][row] == ".":
                    self.deadspace[col][row] = False
                elif row > 0 and col > 0 and row < height - 2 and col < width - 2 and self.is_block_corner(map_data, row, col) and map_data[row][col] != ".":
                    self.deadspace[col][row] = True

        for col in range(len(map_data)):
            for row in range(len(map_data[col])):
                if(map_data[col][row] == "#" and map_data[col][row] == "."):
                    continue
                elif(self.deadspace[col][row]):
                    continue
                elif(row > 0 and col > 0 and col < width - 1 and row < height - 1):
                    if(map_data[col-1][row] == "#" or map_data[col+1][row] == "#"):

                        right_col = col

                        while right_col < width - 1 and map_data[right_col + 1][row] != "#" and (map_data[right_col][row-1] == "#" or map_data[right_col][row+1] == "#") and map_data[right_col][row] != ".":
                            right_col += 1
                        if not self.is_block_corner(map_data, row, right_col) or not self.deadspace[right_col][row]:
                            continue

                        left_col = col

                        while left_col > 0 and map_data[left_col - 1][row] != "#" and (map_data[left_col][row-1] == "#" or map_data[left_col][row+1] == "#") and map_data[left_col][row] != ".":
                            left_col -= 1
                        if not self.is_block_corner(map_data, row, left_col) or not self.deadspace[left_col][row]:
                            continue

                        for current_col in range (left_col, right_col + 1):
                            self.deadspace[current_col][row] = True

                    if map_data[col-1][row] == "#" or map_data[col+1][row] == "#":

                        top_row = row
                        while top_row > 0 and map_data[col][top_row-1] != "#" and (map_data[col-1][top_row] == "#" or map_data[col+1][top_row] == "#") and map_data[col][top_row] != ".":
                            top_row -= 1
                        if not self.is_block_corner(map_data, top_row, col) or not self.deadspace[col][top_row]:
                            continue

                        bottom_row = row
                        while bottom_row < height - 1 and map_data[col][bottom_row+1] != "#" and (map_data[col-1][bottom_row] == "#" or map_data[col+1][bottom_row] == "#") and map_data[col][bottom_row] != ".":
                            bottom_row += 1
                        if not self.is_block_corner(map_data, bottom_row, col) or not self.deadspace[col][bottom_row]:
                            continue

                        for current_row in range (top_row, bottom_row + 1):
                            self.deadspace[col][current_row] = True

        end_time = perf_counter()
        total_time = end_time - start_time
        print(f"Deadlock Execution Time: {total_time:.6f} seconds")













# -------------------------------------------------------------------------------------------------------------------------------------------------
# NOTE:
# 1. DIAGRAM IS IN ROW-MAJOR (i.e., position is [row][column])

# 2. FOLLOW THE FOLLOWING NOTATION FOR THE STRING RETURN VALUE
    # u: execute_move(0) -> row--
    # d: execute_move(1) -> row++
    # l: execute_move(2) -> column--
    # r: self.execute_move(3) -> column++

# 3. {0, 0} is always at the top left

# 4. State contains player position and boxes position, while node contains State, g, h, and s
