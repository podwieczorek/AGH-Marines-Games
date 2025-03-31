import pygame
import os
from src.core.game import Game
from src.units.player import Player

root = os.path.dirname(__file__)


pygame.init()
pygame.display.set_caption("PAC-VHAL")

game = Game(root)

clock = pygame.time.Clock()
running = True
last_speed_change = pygame.time.get_ticks()

bg = pygame.image.load(os.path.join(root, 'static', 'images', 'background', 'title.png'))
bg = pygame.transform.scale(bg, (game.settings.s["screen_width"], game.settings.s["screen_height"]))

while running:
    game.screen.fill(game.COLORS[1])  # fill screen with background color
    game.screen.blit(bg, (0, 0))
    
    while game.state == -1:
        game.screen.blit(bg, (0, 0))
        game.ui.instructions(game.screen)
        pygame.display.flip()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    game.state = 1
        clock.tick(game.settings.s["framerate"])
    
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
        case _:
            pass
    
    pygame.display.flip()  # flip() displays the drawing
    clock.tick(game.settings.s["framerate"])  # limits FPS
    