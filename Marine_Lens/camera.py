import pygame
import random
from constants import *
from utils import *
from image_loading import *

class Camera:
    def __init__(self, PLAYER_x, PLAYER_y):
        self.width = int(300 * SCALE_X)
        self.height = int(200 * SCALE_Y)
        self.x = PLAYER_x + (PLAYER_FRAMES[0].get_width() - self.width) // 2
        self.y = PLAYER_y - (self.height // 4)
        self.colour = CAMERA_COLOUR[0]

        self.cooldown = 1000
        self.flash_time = 200
        self.timer = 0
        self.photo_ready = True
        self.is_flashing = False

    def update(self, dt, PLAYER_x, PLAYER_y):
        self.x = PLAYER_x + (PLAYER_FRAMES[0].get_width() - self.width) // 2
        self.y = PLAYER_y - (self.height // 4)

        if self.is_flashing:
            self.timer += dt
            if self.timer > self.flash_time:
                self.is_flashing = False
                self.colour = CAMERA_COLOUR[1]
                self.timer = 0
        elif not self.photo_ready:
            self.timer += dt
            if self.timer > self.cooldown:
                self.photo_ready = True
                self.colour = CAMERA_COLOUR[0]
                self.timer = 0

    def draw(self):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 8)
    
    def take_photo(self):
        if self.photo_ready:
            self.is_flashing = True
            self.photo_ready = False
            self.colour = CAMERA_COLOUR[2]

    def fish_in_range(self, fish):
        camera_hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        fish_hitbox = pygame.Rect(fish.x, fish.y, fish.width, fish.height).inflate(5, 5)
        return camera_hitbox.colliderect(fish_hitbox)