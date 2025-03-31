import random
import opensimplex

COLORS = {
        0: (4, 105, 151),  # Background (blue)
        1: (37, 65, 23),   # Walls (green)
    }


class Maze:
    def __init__(self, columns, rows):
        self.cols = columns
        self.rows = rows
        self.grid = [[1 for _ in range(columns)] for _ in range(rows)]

    def __str__(self): 
        str_grid = '\n'.join(' '.join(str(tile) for tile in row) for row in self.grid)
        for f, t in {
            '0': ' ',
            '1': '@'
        }.items():
            str_grid = str_grid.replace(f, t)

        return str_grid

    def simplex_cave(self, seed=random.randrange(0, 100000), complexity=4, probability=0.2):
        opensimplex.seed(seed)
        for y in range(self.rows):
            for x in range(self.cols):
                if opensimplex.noise2(x/complexity, y/complexity) > probability:
                    self.grid[y][x] = 1 
                else:
                    self.grid[y][x] = 0

    def remove_not_connected_spaces(self, visited=set()):
        def bfs(x, y, visited):
            if (x, y) in visited:
                return set()
            visited = set()
            queue = [(x, y)]
            while queue:
                x, y = queue.pop(0)
                if (x, y) not in visited:
                    visited.add((x, y))
                    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < self.cols and 0 <= new_y < self.rows and self.grid[new_y][new_x] == 0:
                            queue.append((new_x, new_y))
            return visited

        visited = set()
        blobs = []
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] not in visited and self.grid[y][x] == 0:
                    blob = bfs(x, y, visited)
                    visited.update(blob)
                    blobs.append(blob)
                    
        blobs = sorted(blobs, key=len)
        blobs.pop()
        for blob in blobs:
            for x, y in blob:
                self.grid[y][x] = 1

    def get_valid_directions(self, x, y):
        valid_directions = [(0, 0)]
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.cols and 0 <= new_y < self.rows and self.grid[new_y][new_x] == 0:
                valid_directions.append((dx, dy))
        return valid_directions
