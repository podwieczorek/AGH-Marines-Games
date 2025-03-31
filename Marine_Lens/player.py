import pygame
from constants import *
from utils import *
from image_loading import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = PLAYER_SPEED
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 100

    def move(self, key, dt, joystick=None):
        #keyboard movement
        if key[pygame.K_UP] and self.y > -50:
            self.y -= self.speed
        if key[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - 200:
            self.y += self.speed
        if key[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - 300:
            self.x += self.speed
        if key[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed

        #joystick movement
        if joystick:
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)

            if abs(axis_x) > DEAD_ZONE:
                self.x += axis_x * self.speed
            if abs(axis_y) > DEAD_ZONE:
                self.y += axis_y * self.speed

            self.x = max(0, min(self.x, SCREEN_WIDTH - 300))
            self.y = max(-50, min(self.y, SCREEN_HEIGHT - 200))


    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(PLAYER_FRAMES)

    def draw(self, win):
        win.blit(PLAYER_FRAMES[self.current_frame], (self.x, self.y))

    def get_position(self):
        return self.x, self.y