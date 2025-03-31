import pygame
import random
from .unit import Unit
from .projectile import Bullet
from ..core.maze import Maze


class Player(Unit):
    score = 0
    tag = 'player'
    player_list = []
    def __init__(self, maze: Maze, hp, speed, projectile_speed):
        super().__init__(maze, speed)  # Call Unit's __init__ to initialize maze, x, y, and append to list
        self.direction = (0, 0)
        self.input_stack = []
        self.last_direction = (1, 0)
        self.projectile_speed = projectile_speed
        self.x = 1
        self.y = 1
        self.hp = hp
        self.joystick = None
        self.player_list.append(self)
        self.spawn()
        
        self.map_direction = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0),
            'stop': (0, 0)
                
        }
        
    def spawn(self):
        x = random.randint(0, self.maze.cols - 1)
        y = random.randint(0, self.maze.rows - 1)
        while self.maze.grid[y][x] == 1:
            x = random.randint(0, self.maze.cols - 1)
            y = random.randint(0, self.maze.rows - 1)
        self.x = x
        self.y = y

    def step(self):
        if self.direction != (0, 0):
            self.direction = (0, 0)
            
        if len(self.input_stack) != 0:
            self.execute_key(self.input_stack[-1])
        
        new_x, new_y = self.x + self.direction[0], self.y + self.direction[1]
        if 0 <= new_x < self.maze.cols and 0 <= new_y < self.maze.rows and self.maze.grid[new_y][new_x] == 0:
            if self.direction != (0, 0):
                self.state = 'moving'
            else:
                self.state = 'idle'
            self.x, self.y = new_x, new_y
        else:
            self.direction = (0, 0)
            self.state = 'idle'

    def colides(self, other):
        match other.tag:
            case 'enemy':
                self.hp -= 1
                other.respawn()
            case 'pickup':
                Player.score += other.value
                print("score: ", self.score)
            case _:
                pass
        
    def input(self,events):        
        pass

    def execute_key(self, key):              
        match key:
            case 'up' | 'down' | 'left' | 'right':
                self.direction = self.map_direction[key]
                self.last_direction = self.direction
            case 'fire':
                self.fire(self.last_direction)
                self.state = 'firing'
            
    def is_alive(self):
        if self.hp <= 0:
            return False
        return True

    def fire(self, direction):
        Bullet(self.maze, self.x, self.y , direction, self.projectile_speed)

    def __str__(self):
        return f'Player at (coords:({self.x}, {self.y} | {self.direction}), score:{self.score})'
        
    def __repr__(self):
        return f'Player {self.player_list.index(self)}'

class Keyboard_player(Player):
    def __init__(self, maze, hp, speed, projectile_speed, key_list = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE]):
        super().__init__(maze, hp, speed, projectile_speed)
        self.joystick = False
        self.key_list = key_list

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
            'right': (1, 0),
            'stop': (0, 0)
        }
        
    def input(self,events):        
        for event in events:    
            if event.type == pygame.KEYDOWN and event.key in self.key_list:
                self.input_stack.append(self.map_key[event.key])
            if event.type == pygame.KEYUP and event.key in self.key_list and self.input_stack != []:
                self.input_stack.remove(self.map_key[event.key])

class Joystick_player(Player):
    # these are the identifiers for the PS4's accelerometers
    AXIS_X = 0
    AXIS_Y = 1

    # variables we'll store the rotations in, initialised to zero
    rot_x = 0.0
    rot_y = 0.0
    def __init__(self, maze, hp, speed, projectile_speed,  key_list = []):
        super().__init__(maze, hp, speed, projectile_speed)
        self.input_states = {i:0 for i in range(20)}
        self.button = [0, 0, 0, 0, 0]
        self.joystick = True
        self.buttons = {}
        
        self.JOYSTICK_OFFSET = 4
        self.map_key = {
            11: 'up',
            13: 'left',
            14: 'right',
            12: 'down',
            2: 'fire' 
        }

        self.map_direction = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0),
            'stop': (0, 0)
                
        }
    
    def input(self,events):     
        # self.axis[self.AXIS_X] = self.rot_x
        # self.axis[self.AXIS_Y] = self.rot_y
        axis = {
            0: 0,
            1: 0,
            2: 0,
            3: 0
        }
        for event in events:    
                # print(event.axis)
            if event.type == pygame.JOYBUTTONDOWN:
                key = event.button
                # print(key)
                if key in self.map_key:
                    self.input_stack.append(self.map_key[key])
                # else:
                #     self.input_stack.append(event.button + self.JOYSTICK_OFFSET)
            if event.type == pygame.JOYBUTTONUP:
                key = event.button
                if key in self.map_key:
                    self.input_stack.remove(self.map_key[key])
