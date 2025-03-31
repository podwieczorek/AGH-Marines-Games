class Unit:
    unit_list = []
    tag = 'nikt'

    def __init__(self, maze, speed):
        self.last_frame = 0
        self.direction = (0, 0) 
        self.last_direction = (0, 0)
        self.state = 'idle'
        self.speed = speed
        self.maze = maze
        self.x = -1  # Initialize x position
        self.y = -1  # Initialize y position
        if self not in self.unit_list:
            self.unit_list.append(self)  # Append the instance to Unit.list

    def __str__(self):
        return f'Unit {self.unit_list.index(self)}'

    def __repr__(self):
        return self.__str__()   
    
    def check_colision(self):
        for unit in Unit.unit_list:
            if self.does_colide(unit):
                unit.colides(self)
                self.colides(unit)
    
    def get_valid_directions(self):
        valid_directions = [(0, 0)]
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < self.maze.cols and 0 <= new_y < self.maze.rows and self.maze.grid[new_y][new_x] == 0:
                valid_directions.append((dx, dy))
        return valid_directions
    
    def step(self):
        pass

    def does_colide(self, other):
        if self != other:
            return self.x == other.x and self.y == other.y
        return False

    def colides(self, other):
        pass
    
    def get_path_to(self, start_x, start_y, target, visited):
        queue = [(start_x, start_y, [])]
        visited.add((start_x, start_y))

        while queue:
            x, y, path = queue.pop(0)
            if (x, y) == (target.x, target.y):
                return path

            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.maze.cols and 0 <= new_y < self.maze.rows and self.maze.grid[new_y][new_x] == 0 and (new_x, new_y) not in visited:
                    visited.add((new_x, new_y))
                    queue.append((new_x, new_y, path + [(dx, dy)]))

        return []

    def die(self):
        if self in self.unit_list:
            self.unit_list.remove(self)
            del self
