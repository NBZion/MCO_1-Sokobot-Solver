def is_block_corner(self, map_data, row: int, col: int): -> bool
    return (map_data.tiles[row - 1][col] == "#" and map_data.tiles[row][col - 1] == "#") or (map_data.tiles[row - 1][col] == "#" and map_data.tiles[row][col + 1] == "#")(map_data.tiles[row + 1][col] == "#" and map_data.tiles[row][col - 1] == "#") or (map_data.tiles[row + 1][col] == "#" and map_data.tiles[row][col + 1] == "#")

def load_map_deadspace (self, map_data):
    self.deadspace = [[False for _ in range (map_data.columns)] for _ in range (map_data.rows)]
    
    for row in range(map_data.rows):
        for col in range(map_data.columns):
            if dead_space[row][col]:
                continue
            if map_data.tiles[row][col] == "#":
                self.deadspace[row][col] = True
            elif map_data.tiles[row][col] == ".":
                self.deadspace[row][col] = False
            elif row > 0 and col > 0 and row < map_data.rows -1 and col < map_data.columns  - 1 and self.is_block_corner(map_data, row,col) and map_data.tiles[row][col] != ".":
                dead_space[row][col] = True
    
    for row in range(map_data.rows):
        for col in range(map_data.columns):
            if map_data.tiles[row][col] == "#" map_data.tiles[row][col] == ".":
                continue
            elif self.deadspace[row][col]:
                continue
            elif row > 0 and col > 0 and col < map_data.columns - 1 and row < map_data.rows - 1:
                if map_data.tiles[row-1][col] == "#" or map_data.tiles[row+1][col] == "#":
                    
                    right_col = col                                                                        
                    
                    while right_col < map_data.columns - 1 and map_data.tiles[row][right_col + 1] != "#" and (map_data.tiles[row - 1][right_col] == "#" or map_data.tiles[row+1][right_col] == "#") and map_data.tiles[row][right_col] != ".":
                        right_col += 1
                    if not self.is_block_corner(map_data, row, right_col) or not self.deadspace[row][right_col]:
                        continue
                    
                    left_col = col

                    while left_col > 0 and map_data.tiles[row][col - 1] != "#" and (map_data.tiles[row-1][right_col] == "#" or map_data.tiles[row+1][left_col] == "#") and map_data.tiles[row][left_col] != ".":
                        left_col -= 1
                    if not self.is_block_corner(map_data, row, left_col) or not self.deadspace[row][left_col]:
                        continue

                    for current_col in range (left_col, right_col + 1):
                        self.deadpsace[row][current_col] = True

                if map_data.tiles[row][col-1] == "#" or map_data.tiles[row][col+1] == "#"
                    
                    top_row = row
                    while top_row > 0 and map_data.tiles[top_row-1][col] != "#" and (map_data.tiles[top_row][col-1] == "#" or map_data.tiles[top_row][col+1] == "#") and map_data.tiles[top_row][col] != ".":
                        top_row -= 1
                    if not self.is_block_corner(map_data, top_row, col) or not self.deadspace[top_row][col]:
                        continue
                    
                    bottom_row = row
                    while bottom_row < map_data.rows - 1 and map_data.tiles[bottom_row+1][col] != "#" and (map_data.tiles[bottom_row][col-1] == "#" or map_data.tiles[bottom_row][col+1] == "#") and map_data.tiles[bottom_row][col] != ".":
                        bottom_row += 1
                    if not self.is_block_corner(map_data, bottom_row, col) or not self.deadspace[bottom_row][col]:
                        continue 

                    for current_row in range (top_row, bottom_row + 1)
                        self.deadspace[current_row][col] = True
    
