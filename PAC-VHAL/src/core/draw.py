import pygame
from src.core.maze import COLORS
from src.units.player import Player
import os

class Draw():
    def __init__(self, screen, size, maze):
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()
        self.size = size
        self.maze = maze
        self.font = pygame.font.Font(None, 36)
        
        self.offset = (
            (self.width - maze.cols * size) // 2,
            (self.height - maze.rows * size) // 2
        )

        self.color_map = {
            'player': (255, 0, 0),
            'enemy': (0, 123, 255),
            'pickup': (0, 255, 0),
            'bullet': (255, 255, 0),
        }
    
    def grid_to_screen(self, x, y):
        return x * self.size + self.offset[0], y * self.size + self.offset[1]
        
    def draw_raw(self, x, y, size, color, img = None):
        if img:
            img = pygame.transform.scale(img, (size, size))
            self.screen.blit(img, (x, y))
        else:
            rect = pygame.Rect(x, y, size, size)
            pygame.draw.rect(self.screen, color, rect)

    def draw_square(self, x, y, color):
        x, y = self.grid_to_screen(x, y)
        self.draw_raw(x, y, self.size, color)
        
    def draw_image(self, x, y, img):
        x, y = self.grid_to_screen(x, y)
        self.screen.blit(img, (x, y))
    
    
    def draw_unit(self, unit):
        x, y = self.grid_to_screen(unit.x, unit.y)
        self.draw_raw(x, y, self.size, self.color_map[unit.tag])
            
    def draw_maze(self):
        cols = self.maze.cols
        rows = self.maze.rows
        for y in range(rows):
            for x in range(cols):
                color = COLORS[self.maze.grid[y][x]]
                self.draw_square(x, y, color)
                
    def draw_hud(self):
        text = self.font.render(f'Score: {Player.score}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        
        for index, player in enumerate(Player.player_list):
            hp = player.hp
            text = self.font.render(f'HP: {hp}', True, (255, 255, 255))
            self.screen.blit(text, (10, 10+30*(index+1)))
    
        


