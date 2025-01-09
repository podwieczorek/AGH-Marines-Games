import random
import pygame
import opensimplex


def draw_square(screen, color, x, y, size):
    rect = pygame.Rect(x * size, y * size, size, size)
    pygame.draw.rect(screen, color, rect)


class Maze:
    def __init__(self, columns, rows):
        self.cols = columns
        self.rows = rows
        self.grid = [[1 for _ in range(columns)] for _ in range(rows)]
        
        
    
        
        
    def __str__(self): 
        str_grid = '\n'.join(' '.join(str(tile) for tile in row) for row in self.grid)
        for f, t in {
            '0':' ',
            '1':'@'
        }.items():
            str_grid = str_grid.replace(f, t)

        return str_grid



    def simplex_cave(self,seed=random.randrange(0,100000),complexity=4,probability=0.2):
        opensimplex.seed(seed)
        for y in range(self.rows):
            for x in range(self.cols):
                if opensimplex.noise2(x/complexity, y/complexity) > probability:
                    self.grid[y][x] = 1 
                else:
                    self.grid[y][x] = 0
                    
    def remove_not_connected_spaces(self):
        def bfs(x,y):
            visited = set()
            queue = [(x,y)]
            while queue:
                x,y = queue.pop(0)
                if (x,y) not in visited:
                    visited.add((x,y))
                    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < self.cols and 0 <= new_y < self.rows and self.grid[new_y][new_x] == 0:
                            queue.append((new_x, new_y))
                            if len(visited) > 25:
                                return visited
            return visited
        
        
        visited = set()
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] not in visited or self.grid[y][x] == 0:
                    blob = bfs(x,y)
                    visited.update(blob)
                    if len(blob) < 25:
                        for x,y in blob:
                            self.grid[y][x] = 1
        
    
        
        
        
    

    def carve(self, x=0, y=0):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        random.shuffle(directions)  # Randomize the order of traversal

        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy  # Look two cells away

            if 0 <= nx < self.cols and 0 <= ny < self.rows and self.grid[ny][nx] == 1:
                # Remove the wall between the current cell and the next cell
                self.grid[y + dy][x + dx] = 0
                self.grid[ny][nx] = 0
                # Recursively generate the maze from the next cell
                self.carve(nx, ny)
    
    
    
    
    def add_paths(self, probability):
        for y in range(self.rows-1):
            for x in range(self.cols-1):
                if self.grid[y][x] == 1:
                    neighbors = sum(self.grid[y + dy][x + dx] == 0 # count amount of neighbors
                                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]) 
                    
                    if neighbors == 2 and random.random() < probability:
                        self.grid[y][x] = 0;
            
            
            

    def draw(self):
        offset_x = (SCREEN_WIDTH / CELL_SIZE - self.cols) // 2
        offset_y = (SCREEN_HEIGHT / CELL_SIZE - self.rows) // 2
        for y in range(self.rows):
            for x in range(self.cols):
                color = COLORS[self.grid[y][x]]
                draw_square(screen, color, x + offset_x, y + offset_y, CELL_SIZE)
                rect = pygame.Rect((x + offset_x) * CELL_SIZE, (y + offset_y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    def get_valid_directions(self, x, y):
        valid_directions = [(0, 0)]
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.cols and 0 <= new_y < self.rows and self.grid[new_y][new_x] == 0:
                valid_directions.append((dx, dy))
        return valid_directions

class Unit:
    unit_list = []
    tag = 'nikt'
    def __init__(self, maze):
        self.maze = maze
        self.x = -1  # Initialize x position
        self.y = -1  # Initialize y position
        if self not in self.unit_list:
            self.unit_list.append(self)  # Append the instance to Unit.list

    def __str__(self):
        return f'Unit {self.unit_list.index(self)}'

    def __repr__(self):
        return self.__str__()   
    
    def get_valid_directions(self):
        valid_directions = [(0, 0)]
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < self.maze.cols and 0 <= new_y < self.maze.rows and self.maze.grid[new_y][new_x] == 0:
                valid_directions.append((dx, dy))
        return valid_directions
    
    def step(self):
        pass
    
    def draw(self):
        offset_x = (SCREEN_WIDTH / CELL_SIZE - maze.cols) // 2
        offset_y = (SCREEN_HEIGHT / CELL_SIZE - maze.rows) // 2
        draw_square(screen, (0, 255, 0), self.x + offset_x, self.y + offset_y, CELL_SIZE)


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

class Player(Unit):
    tag = 'gracz'
    player_list = []
    def __init__(self, maze: Maze, hp, key_list = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE]):
        super().__init__(maze)  # Call Unit's __init__ to initialize maze, x, y, and append to list
        self.direction = (0, 0)
        self.input_stack = []
        self.key_list = key_list
        self.last_direction = (1, 0)
        self.x = 1
        self.y = 1
        self.hp = hp
        self.score = 0
        
        self.map_key = {
            key_list[0]: 'up',
            key_list[1]: 'down',
            key_list[2]: 'left',
            key_list[3]: 'right',
            key_list[4]: 'fire' 
        }
        self.map_direction = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }
        self.player_list.append(self)
        
        
        
        
    def step(self):
        if len(self.input_stack) != 0:
            self.execute_key(self.map_key[self.input_stack[-1]])
        new_x, new_y = self.x + self.direction[0], self.y + self.direction[1]
        if 0 <= new_x < self.maze.cols and 0 <= new_y < self.maze.rows and self.maze.grid[new_y][new_x] == 0:
            self.x, self.y = new_x, new_y
        if self.direction != (0, 0):
            self.direction = (0, 0)
            
            
            
            
    def draw(self):
        offset_x = (SCREEN_WIDTH / CELL_SIZE - maze.cols) // 2
        offset_y = (SCREEN_HEIGHT / CELL_SIZE - maze.rows) // 2
        draw_square(screen, (255, 0, 0), self.x + offset_x, self.y + offset_y, CELL_SIZE)
        
        
    def colides(self, other):
        match other.tag:
            case 'enemy':
                self.hp -= 1
                #print("auuu")
            case 'pickup':
                self.score += other.value
                print("score: ", self.score)
            case _:
                pass
                
        
        
    def input(self,events):        
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in self.key_list:
                self.input_stack.append(event.key)
        keys = pygame.key.get_pressed()
        while len(self.input_stack)>0 and keys[self.input_stack[-1]] == False:
            self.input_stack.pop()
        



    def execute_key(self, key):              
        match key:
            case 'up' | 'down' | 'left' | 'right':
                self.direction = self.map_direction[key]
                self.last_direction = self.direction
            case 'fire':
                self.fire(self.last_direction)
                self.input_stack.pop()
            


    def fire(self, direction):
        Bullet(maze, self.x, self.y , direction)


    def __str__(self):
        return f'Player at (coords:({self.x}, {self.y} | {self.direction}), score:{self.score})'
        
    def __repr__(self):
        return f'Player {self.player_list.index(self)}'
    
    
class Pickup(Unit):
    tag='pickup'
    def __init__(self, maze, value=1  ):
        super().__init__(maze)
        x = random.randint(0, maze.cols - 1)
        y = random.randint(0, maze.rows - 1)
        while maze.grid[y][x] == 1:
            x = random.randint(0, maze.cols - 1)
            y = random.randint(0, maze.rows - 1)
        self.x = x
        self.y = y
        self.value = value
        
        
    def step(self):
        for player in Player.player_list:
            if self.does_colide(player):
                player.colides(self)
                self.colides(self)
    
    
                
    def colides(self, other):
        self.__init__(maze, 1)
        
        


class Enemy(Unit):
    tag='enemy'
    def __init__(self, maze, detection_radius = 10):
        super().__init__(maze)
        x = random.randint(0, maze.cols - 1)
        y = random.randint(0, maze.rows - 1)
        while maze.grid[y][x] == 1:
            x = random.randint(0, maze.cols - 1)
            y = random.randint(0, maze.rows - 1)
            
        self.direction = (0, 0)
        self.x = x
        self.y = y
        self.radius = detection_radius
        self.path = []
        self.cooldown = 0
    
    
    def step(self):
        for player in Player.player_list:
            if self.does_colide(player):
                player.colides(self)
        self.ai()
        
    def draw_path(self):
        offset_x = (SCREEN_WIDTH / CELL_SIZE - maze.cols) // 2
        offset_y = (SCREEN_HEIGHT / CELL_SIZE - maze.rows) // 2
        path = []
        nx, ny = self.x, self.y
        for d in self.path:
            nx, ny = nx + d[0], ny + d[1]
            draw_square(screen, (25, 25, 100), nx+offset_x, ny+offset_y, CELL_SIZE)
        
            
    def ai(self):
        #print(self.cooldown)
        base_cooldown = 20  # cooldown after losing aggro
        probability = 0.95  # aggro probability
        target = self.player_in_radius()
        
        
        if self.path == []:
            self.path = self.get_patrol_path()
        if self.cooldown > 0:
            self.cooldown -= 1
        elif target != self:
            self.path = self.get_path_to(self.x, self.y, target, set())
            if random.random() > probability:
                self.cooldown = base_cooldown

                
        self.draw_path()
        if self.path != []:
            self.direction = self.path.pop(0)
        
        
        self.x += self.direction[0]
        self.y += self.direction[1]
        
    def get_patrol_path(self):
        while True:
            target = random.choice(Unit.unit_list)
            if target.tag == 'pickup':
                path = self.get_path_to(self.x, self.y, target, set())
                if len(path) > 3:
                    return path


    def player_in_radius(self):
        for player in Player.player_list:
            if (player.x - self.x) ** 2 + (player.y - self.y) ** 2 <= self.radius ** 2: 
                return player
        return self
            
    
    
    def remove_hp(self, player):
        player.hp -= 1
        self.__init__(maze)
        
    def draw(self):
        offset_x = (SCREEN_WIDTH / CELL_SIZE - maze.cols) // 2
        offset_y = (SCREEN_HEIGHT / CELL_SIZE - maze.rows) // 2
        draw_square(screen, (0, 123, 255), self.x + offset_x, self.y + offset_y, CELL_SIZE)
        
        

class Bullet(Unit):
    tag='bullet'
    def __init__(self, maze, x, y, direction):
        super().__init__(maze)
        self.x = x
        self.y = y
        self.direction = direction
        
    def step(self):
        if self.x < 0 or self.x >= maze.cols or self.y < 0 or self.y >= maze.rows:
            Unit.unit_list.remove(self)
            
        self.x += self.direction[0]
        self.y += self.direction[1]
        
        if maze.grid[self.y][self.x] == 1:
            maze.grid[self.y][self.x] = 0
            self.colides(self)
            
        for unit in Unit.unit_list:
            if self.does_colide(unit):
                unit.colides(self)
        
        
    def colides(self, other):
        Unit.unit_list.remove(self)
        
    def draw(self):
        offset_x = (SCREEN_WIDTH / CELL_SIZE - maze.cols) // 2
        offset_y = (SCREEN_HEIGHT / CELL_SIZE - maze.rows) // 2
        draw_square(screen, (255, 255, 0), self.x + offset_x, self.y + offset_y, CELL_SIZE)
        
                
    
        
        

maze = Maze(80, 60)
#maze.carve()
#maze.add_paths(0.40)
#maze.simplex_cave(1,4,0.2)
maze.simplex_cave()
maze.remove_not_connected_spaces()
print(maze)

player = Player(maze, 3)

for i in range(5):
    Enemy(maze, 10)

for i in range(10):
    Pickup(maze)

# Constants for screen dimensions and colors
TICK_INTERVAL = 100
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CELL_SIZE = 15
COLORS = {
    0: (4, 105, 151),  # Background (blue)
    1: (37, 65, 23),   # Walls (green)
}

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


clock = pygame.time.Clock()
running = True
last_tick = pygame.time.get_ticks()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    


    

    player.input(events)
    
    current_time = pygame.time.get_ticks()
    if current_time - last_tick >= TICK_INTERVAL:
        screen.fill(COLORS[0])
        maze.draw()
        for u in Unit.unit_list:
            
            u.step()
            u.draw()
        last_tick = current_time

    #print(Unit.unit_list)
    #print(player.score)
    #print(e.bfs(e.x, e.y, player, set()))
    
    
    pygame.display.flip() # flip() displays the drawing
    clock.tick(60)  # limits FPS to 60