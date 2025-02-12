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
screen = pygame.display.set_mode((1920, 1000))
game = Game(screen)

clock = pygame.time.Clock()
running = True
last_speed_change = pygame.time.get_ticks()
game_speed = 1000  # milliseconds per frame

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.pause_game()
            
    for player in Player.player_list:
        if not player.is_alive():
            print(f'You died, score: {Player.score}')
            game.game_running = False
            
    game.input.update(events)        
    
    
    match game.state:
        case 0:
            running = False
        case 1:
            game.ui_loop()
        case 2:
            game.game_loop()
            game.hud()
        case _:
            pass
    
    pygame.display.flip() # flip() displays the drawing
    clock.tick(60)  # limits FPS to 60
    