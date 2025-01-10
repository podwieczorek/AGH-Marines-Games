import pygame
import random

pygame.init()

#screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1020

#fonts
FONT = pygame.font.Font("slkscr.ttf", 40)

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Game1")

#colours
BG_COLOUR = (16, 18, 43)
PLAYER_COLOUR = (83, 116, 140)

def put_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    win.blit(img, (x, y))


#first player coordinates
PLAYER_x = 860
PLAYER_y = 700

#dimensions of images
PLAYER_WIDTH = 300
PLAYER_HEIGHT = 300

PLAYER_SPEED = 10

#images loading
PLAYER_FRAMES = [
    pygame.transform.scale(pygame.image.load("game_images/narwhalc3.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("game_images/narwhalc2.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("game_images/narwhalc1.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
]


INSTRUCTION_FRAMES = [
    pygame.image.load("game_images/instructions1.png"),
    pygame.image.load("game_images/instructions2.png")
]

GAME_OVER_FRAMES = [
    pygame.image.load("game_images/game_over_screen1.png"),
    pygame.image.load("game_images/game_over_screen2.png")
]
BACKGROUND_IMAGE = pygame.image.load("game_images/background_image_game.png").convert()

GAME_MENU_FRAMES = [
    pygame.image.load("game_images/menu1.png"),
    pygame.image.load("game_images/menu2.png")
]

#animation variables
current_frame = 0
animation_timer = 0
animation_speed = 100

instruction_frame = 0
instruction_timer = 0
instruction_speed = 500

game_over_frame = 0
game_over_timer = 0
game_over_speed = 500

menu_frame = 0
menu_timer = 0
menu_speed = 500


class Fish:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.spawn_side = random.choice(["left", "right"])
        self.speed = random.uniform(2, 6)

        if self.spawn_side == "right":
            self.x = SCREEN_WIDTH
            self.speed = -self.speed
        else:
            self.x = -self.width

        self.y = random.randint(0, SCREEN_HEIGHT-self.height)
        self.colour = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    
    def update(self):
        self.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, (self.x, self.y, self.width, self.height))

#fish "management"
fish_list = []
fish_spawn_timer = 0
fish_spawn_rate = 1000

#other
key = pygame.key.get_pressed()

#game loop
run = True
instructions = False
menu = True
game_over = False
GAME_DURATION = 60000
start_time = pygame.time.get_ticks()

clock = pygame.time.Clock()

while run:
    pygame.mouse.set_visible(False)

    if menu:
        while menu:
            win.blit(BACKGROUND_IMAGE, (0,0))
            key = pygame.key.get_pressed()
            dt = clock.tick(60)

            menu_timer += dt
            if menu_timer >= menu_speed:
                menu_timer = 0
                menu_frame = (menu_frame + 1) % len(GAME_MENU_FRAMES)
            
            win.blit(GAME_MENU_FRAMES[menu_frame], (460, 20))

            if key[pygame.K_RETURN]:
                pygame.time.delay(200)
                menu = False
                instructions = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    instructions = False
                    run = False

            pygame.display.update()


    if instructions:
        while instructions:
            win.blit(BACKGROUND_IMAGE, (0,0))
            key = pygame.key.get_pressed()
            dt = clock.tick(60)

            instruction_timer += dt
            if instruction_timer >= instruction_speed:
                instruction_timer = 0
                instruction_frame = (instruction_frame + 1) % len(INSTRUCTION_FRAMES)
        
            win.blit(INSTRUCTION_FRAMES[instruction_frame], (460, 20))

            if key[pygame.K_RETURN]:
                instructions = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    instructions = False
                    run = False

            pygame.display.update()
    
    """
    if game_over:
        win.fill(BG_COLOUR)
        key = pygame.key.get_pressed()
        dt = clock.tick(60)
        game_over_timer += dt

        if game_over_timer >= game_over_speed:
            game_over_timer = 0
            game_over_frame = (game_over_frame + 1) % len(GAME_OVER_FRAMES)
        
        win.blit(GAME_OVER_FRAMES[game_over_frame], (460, 20))

        if key[pygame.K_ESCAPE]:
            game_over = False
            run = False
    """

    key = pygame.key.get_pressed()
    win.blit(BACKGROUND_IMAGE, (0,0))
    dt = clock.tick(60)

    #timer
    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = max(0, GAME_DURATION - elapsed_time)
    remaining_seconds = remaining_time // 1000

    if remaining_time <= 0:
        game_over = True
        run = False

    put_text(f"{remaining_seconds} s", FONT, (255, 255, 255), 20, 20)
    
    if key[pygame.K_UP] and PLAYER_y > PLAYER_SPEED:
        PLAYER_y -= PLAYER_SPEED
    if key[pygame.K_DOWN] and PLAYER_y < 1020 - PLAYER_HEIGHT:
        PLAYER_y += PLAYER_SPEED
    if key[pygame.K_RIGHT] and PLAYER_x < 1920 - PLAYER_WIDTH - PLAYER_SPEED:
        PLAYER_x += PLAYER_SPEED
    if key[pygame.K_LEFT] and PLAYER_x > PLAYER_SPEED:
        PLAYER_x -= PLAYER_SPEED

    #spawn fish
    fish_spawn_timer += dt
    if fish_spawn_timer >= fish_spawn_rate:
        fish_spawn_timer = 0
        fish_list.append(Fish())

    #update and draw fish
    for fish in fish_list[:]:
        fish.update()
        fish.draw(win)
        if fish.x < -fish.width:
            fish_list.remove(fish)

    #animation of player
    animation_timer += dt
    if animation_timer >= animation_speed:
        animation_timer = 0
        current_frame = (current_frame + 1) % len(PLAYER_FRAMES)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.blit(PLAYER_FRAMES[current_frame], (PLAYER_x, PLAYER_y))
    
    pygame.display.update()
pygame.quit()