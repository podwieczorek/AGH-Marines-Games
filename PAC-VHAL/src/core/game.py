import pygame
from src.core.maze import Maze
from src.units.player import Player
from src.units.enemy import Enemy
from src.units.pickup import Pickup
from src.units.player import *
from src.core.draw import Draw

class Game:
    
    COLORS = {
        0: (4, 105, 151),  # Background (blue)
        1: (37, 65, 23),   # Walls (green)
    }
    last_speed_change = 0
    game_speed = 1000  # milliseconds per frame
    
    
    def __init__(self, screen):
        self.screen = screen
        self.maze = None
        self.draw = None
    
    def setup_maze(self, rows, cols, cell_size):
        self.maze = Maze(rows, cols)
        self.draw = Draw(self.screen, cell_size, self.maze)
        
        
    def ui_loop(self):
        pass

    def game_loop(self, events):
        for player in Player.player_list:
            player.input(events)
    
        current_time = pygame.time.get_ticks()
        
        game_speed = 1000 - current_time // 200
        if game_speed < 300:
            game_speed = 300
        #print(game_speed)
    
        self.draw.draw_maze()
        for u in Unit.unit_list:
            u.check_colision()
            if current_time - u.last_frame > game_speed / u.speed:
                u.step()
                u.last_frame = current_time
            self.draw.draw_unit(u)
        last_tick = current_time

    