import random
from .unit import Unit
from .player import Player

class Pickup(Unit):
    tag='pickup'
    def __init__(self, maze, value=1):
        super().__init__(maze, 1)
        x = random.randint(0, maze.cols - 1)
        y = random.randint(0, maze.rows - 1)
        while maze.grid[y][x] == 1:
            x = random.randint(0, maze.cols - 1)
            y = random.randint(0, maze.rows - 1)
        self.x = x
        self.y = y
        self.value = value
        
        
    def step(self):
        pass
    
    def check_colision(self):
        for player in Player.player_list:
            if self.does_colide(player):
                player.colides(self)
                self.colides(self)
                
    def colides(self, other):
        self.__init__(self.maze, 1)
        
        