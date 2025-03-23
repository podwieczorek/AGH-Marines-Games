import pygame
import pygame.image
from constants import *
from utils import *
from image_loading import *
from fish import Fish
from player import Player
from camera import Camera

#animation variables
game_over_frame = 0
game_over_timer = 0
game_over_speed = 500

menu_frame = 0
menu_timer = 0
menu_speed = 500

#fish "management"
fish_list = []
fish_spawn_timer = 0
fish_spawn_rate = 500

#other
key = pygame.key.get_pressed()

#initializing player
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

#initialize camera
camera = Camera(player.x, player.y)

#game loop
run = True
menu = True
game_over = False

#score and highscore management
score = 0
high_score = load_high_score()
clock = pygame.time.Clock()

while run:

    if menu:
        while menu:
            win.blit(BACKGROUND_IMAGE, (0,0))
            key = pygame.key.get_pressed()
            dt = clock.tick(60)

            menu_timer += dt
            if menu_timer >= menu_speed:
                menu_timer = 0
                menu_frame = (menu_frame + 1) % len(GAME_MENU_FRAMES)
            
            win.blit(GAME_MENU_FRAMES[menu_frame], ((SCREEN_WIDTH - GAME_MENU_FRAMES[menu_frame].get_width()) // 2, (SCREEN_HEIGHT - GAME_MENU_FRAMES[menu_frame].get_height()) // 2))
            draw_title_bar()

            if key[pygame.K_RETURN]:
                pygame.time.delay(200)
                menu = False
                start_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if CLOSE_BTN_RECT.collidepoint(mouse_pos):
                        run = False
                        menu = False
                
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == ENTER_BUTTON:
                        pygame.time.delay(200)
                        menu = False
                        start_time = pygame.time.get_ticks()

            pygame.display.update()

    #game over screen
    while game_over:
        win.blit(BACKGROUND_IMAGE, (0, 0))
        key = pygame.key.get_pressed()
        dt = clock.tick(60)

        game_over_timer += dt
        if game_over_timer >= game_over_speed:
            game_over_timer = 0
            game_over_frame = (game_over_frame + 1) % len(GAME_OVER_FRAMES)

        win.blit(GAME_OVER_FRAMES[game_over_frame], ((SCREEN_WIDTH - GAME_OVER_FRAMES[game_over_frame].get_width()) // 2, (SCREEN_HEIGHT - GAME_OVER_FRAMES[game_over_frame].get_height()) // 2))
        draw_title_bar()

        #score and high score display
        put_text(f"Score:  {score}", FONT2, (243, 252, 154), (SCREEN_WIDTH - FONT2.render(f"Score: {score}", True, (243, 252, 154)).get_width()) // 2, SCREEN_HEIGHT//2 - 200)
        previous_high_score = high_score

        if score > previous_high_score:
            new_high_score = score
            save_high_score(new_high_score)
            put_text("New High Score!", FONT2, (255, 255, 255), (SCREEN_WIDTH - FONT2.render("New High Score!", True, (255, 255, 255)).get_width()) // 2, SCREEN_HEIGHT//2)
            put_text(f"High Score:  {new_high_score}", FONT2, (243, 252, 154), (SCREEN_WIDTH - FONT2.render(f"High Score: {new_high_score}", True, (243, 252, 154)).get_width()) // 2, SCREEN_HEIGHT//2 - 100)
        else:
            put_text(f"High Score:  {previous_high_score}", FONT2, (243, 252, 154), (SCREEN_WIDTH - FONT2.render(f"High Score: {previous_high_score}", True, (243, 252, 154)).get_width()) // 2, SCREEN_HEIGHT // 2 - 100)

        if key[pygame.K_ESCAPE]:
            run = False
            game_over = False
        
        if key[pygame.K_RETURN]:
            #resetting variables
            score = 0
            fish_list.clear()
            player.x = SCREEN_WIDTH // 2
            player.y = SCREEN_HEIGHT // 2

            menu = True
            game_over = False
            start_time = pygame.time.get_ticks()
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                game_over = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if CLOSE_BTN_RECT.collidepoint(mouse_pos):
                        run = False
                        game_over = False

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == ENTER_BUTTON:
                    game_over = False

                    #resetting variables
                    score = 0
                    fish_list.clear()
                    player.x = SCREEN_WIDTH // 2
                    player.y = SCREEN_HEIGHT // 2

                    menu = True
                    start_time = pygame.time.get_ticks()
                    break
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == ESC_BUTTON:
                    run = False
                    game_over = False

        pygame.display.update()
    
    
    key = pygame.key.get_pressed()
    win.blit(BACKGROUND_IMAGE, (0, 0))
    dt = clock.tick(60)

    #timer
    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = max(0, GAME_DURATION - elapsed_time)
    remaining_seconds = remaining_time // 1000

    if remaining_time <= 0:
        game_over = True

    put_text(f"Time remaining: {remaining_seconds} s", FONT, (255, 255, 255), 20, TITLE_BAR_HEIGHT)

    #score counter
    put_text(f"Score: {score}", FONT, (255, 255, 255), SCREEN_WIDTH-300, TITLE_BAR_HEIGHT)


    #spawn fish
    fish_spawn_timer += dt
    if fish_spawn_timer >= fish_spawn_rate:
        fish_spawn_timer = 0
        fish_list.append(Fish())

    #update and draw fish
    for fish in fish_list[:]:
        fish.update(dt)
        fish.draw()
        if fish.x < -fish.width or fish.x > SCREEN_WIDTH + fish.width:
            fish_list.remove(fish)

    #updating player and camera
    camera.update(dt, *player.get_position())
    camera.draw()
    
    draw_title_bar()

    player.move(key, dt, joystick)
    player.animate(dt)
    player.draw(win)

    #taking photos
    if key[pygame.K_SPACE]:
        if camera.photo_ready:
            camera.take_photo()  
            for fish in fish_list:
                if camera.fish_in_range(fish):
                    score += fish.value
                    fish.swim_away()
                    if fish.x < -fish.width or fish.x > SCREEN_WIDTH + fish.width:
                        fish_list.remove(fish)
                    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if CLOSE_BTN_RECT.collidepoint(mouse_pos):
                run = False     
        
        
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == PHOTO_BUTTON:  # Replace with the correct button number
                if camera.photo_ready:
                    camera.take_photo()  
                    for fish in fish_list:
                        if camera.fish_in_range(fish):
                            score += fish.value
                            fish.swim_away()
                            if fish.x < -fish.width or fish.x > SCREEN_WIDTH + fish.width:
                                fish_list.remove(fish)
        
    pygame.display.update()
pygame.quit()