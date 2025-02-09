import pygame
from src.core.maze import COLORS
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

class Draw():
    def __init__(self, screen, size, maze):
        self.screen = screen
        self.size = size
        self.maze = maze
        self.offset = (
            (SCREEN_WIDTH - maze.cols * size) // 2,
            (SCREEN_HEIGHT - maze.rows * size) // 2
        )

        self.img_map = {
            
        }
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
        
        
    def draw_unit(self, unit):
        x, y = self.grid_to_screen(unit.x, unit.y)
        if unit.tag in self.img_map:
            self.draw_raw(x, y, self.size, None, self.img_map[unit.tag])
        elif unit.tag in self.color_map:
            self.draw_raw(x, y, self.size, self.color_map[unit.tag])
            
    def draw_maze(self):
        cols = self.maze.cols
        rows = self.maze.rows
        for y in range(rows):
            for x in range(cols):
                color = COLORS[self.maze.grid[y][x]]
                self.draw_square(x, y, color)
        


