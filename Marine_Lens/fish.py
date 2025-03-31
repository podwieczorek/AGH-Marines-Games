import pygame
import random
from constants import *
from utils import *
from image_loading import *

class Fish:
    def __init__(self):
        self.chance = random.randint(0, 100)
        self.spawn_side = random.choice(["left", "right"])
        self.swimming_away = False
        self.animation_timer = 0
        self.animation_speed = 300
        self.current_frame = 0
        
        #small fish
        if self.chance <= 70:
            self.frames_left = SMALL_FISH_LEFT
            self.frames_right = SMALL_FISH_RIGHT
            self.width = int(56 * SCALE_X)
            self.height = int(44 * SCALE_Y)
            self.value = 10
            self.speed = random.uniform(4, 8)
            self.swim_away_speed = 40
            self.i = random.randint(0, 4)

        #big fish
        elif self.chance <= 95:
            self.frames_left = BIG_FISH_LEFT
            self.frames_right = BIG_FISH_RIGHT
            self.width = int(180 * SCALE_X)
            self.height = int(114 * SCALE_Y)
            self.value = 15
            self.speed = random.uniform(1, 4)
            self.swim_away_speed = 30
            self.i = random.randint(0, 4)
            
        #jellyfish  
        elif self.chance <= 98:
            self.frames_left = JELLYFISH_FRAMES_LEFT
            self.frames_right = JELLYFISH_FRAMES_RIGHT
            self.width = int(240 * SCALE_X)
            self.height = int(160 * SCALE_Y)
            self.value = 30
            self.speed = random.uniform(7, 10)
            self.swim_away_speed = 50
        
        #turtles
        elif self.chance > 98:
            self.frames_left = TURTLE_FRAMES_LEFT
            self.frames_right = TURTLE_FRAMES_RIGHT
            self.width = int(430 * SCALE_X)
            self.height = int(330 * SCALE_Y)
            self.value = 30
            self.speed = random.uniform(4, 8)
            self.swim_away_speed = 60

        if self.spawn_side == "right":
            self.x = SCREEN_WIDTH
            self.speed = -self.speed
            self.frames = self.frames_left
        else:
            self.x = -self.width
            self.frames = self.frames_right

        self.y = random.randint(self.height, SCREEN_HEIGHT-self.height)
        self.colour = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    
    def update(self, dt):
        self.x += self.speed

        if self.chance > 95:
            self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)


    def draw(self):
        if self.chance > 95:
            frame = self.frames[self.current_frame]
        else: 
            frame = self.frames[self.i]
        win.blit(frame, (self.x, self.y))
    
    def swim_away(self):
        self.swimming_away = True

        if self.spawn_side == "right":
            self.frames = self.frames_right
            self.speed = self.swim_away_speed
        else:
            self.frames = self.frames_left
            self.speed = -self.swim_away_speed