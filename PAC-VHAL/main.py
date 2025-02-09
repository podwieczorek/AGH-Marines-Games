import pygame
from src.core.game import Game
from src.core.UI.ui import UI
from src.core.UI.button import Button
from src.core.maze import Maze
from src.units.player import Player
from src.units.enemy import Enemy
from src.units.pickup import Pickup
from src.units.player import *
from src.core.draw import Draw




pygame.init()
screen = pygame.display.set_mode((1920, 1080))
game = Game(screen)
game.setup_maze(100, 70, 15)
game.maze.simplex_cave()
game.maze.remove_not_connected_spaces()
        
clock = pygame.time.Clock()
running = True
last_speed_change = pygame.time.get_ticks()
game_speed = 1000  # milliseconds per frame

player = Keyboard_player(game.maze, 99999)
for i in range(10):
    Enemy(game.maze)
    
for i in range(10):
    Pickup(game.maze)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    game.game_loop(events)
    
    pygame.display.flip() # flip() displays the drawing
    clock.tick(60)  # limits FPS to 60
