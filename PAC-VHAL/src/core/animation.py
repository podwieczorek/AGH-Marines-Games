from src.core.spriesheet import Spritesheet
from src.core.draw import Draw
import pygame
import os

class Animator:
    def __init__(self, draw_obj:Draw, root):
        self.draw = draw_obj
        self.animations = {
            'player': {
                'idle': Spritesheet(os.path.join(root, 'static', 'images', 'units', 'pacvhal-base.png'), 4, 1, self.draw.size, 8, 8),
                'moving': Spritesheet(os.path.join(root, 'static', 'images', 'units', 'pacvhal-move.png'), 4, 1, self.draw.size, 16, 8),
            },
            'bullet': {
                'moving': Spritesheet(os.path.join(root, 'static', 'images', 'units', 'bullet-move.png'), 1, 1, self.draw.size, 16, 8),
            },
            'enemy': {
                'moving': Spritesheet(os.path.join(root, 'static', 'images', 'units', 'enemy-move.png'), 4, 1, self.draw.size, 16, 8),
            }
        }
    
    def get_angle(self, unit):
        if unit.direction == (0, 0) and unit.last_direction != (0, 0):
            direction = unit.last_direction
        else:
            direction = unit.direction
        match direction:
            case (1, 0):
                return 0
            case (0, 1):
                return 270
            case (-1, 0):
                return 180
            case (0, -1):
                return 90
            case _:
                return 0
            
    def get_animation_coords(self, unit):
        match unit.direction:
            case (1, 0):
                return (unit.x-1, unit.y)
            case (0, 1):
                return (unit.x, unit.y-1)
            case (-1, 0):
                return (unit.x, unit.y)
            case (0, -1):
                return (unit.x, unit.y)
            case _:
                return (unit.x, unit.y)
        
        
    def animate(self, unit, index):
        if unit.tag in self.animations:
            if unit.state in self.animations[unit.tag]:
                x, y = self.get_animation_coords(unit)
                new_frame = pygame.transform.rotate(self.animations[unit.tag][unit.state].get_frame(index), self.get_angle(unit))
                self.draw.draw_image(x, y, new_frame)
                
                
    def can_animate(self, unit):
        return unit.tag in self.animations and unit.state in self.animations[unit.tag]