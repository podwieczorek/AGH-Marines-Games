import pygame
import random
import pygame.image

pygame.init()

#game window setup
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

BASE_WIDTH = 1920
BASE_HEIGHT = 1080

SCALE_X = SCREEN_WIDTH / BASE_WIDTH
SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Marine Lens")


#fonts
FONT = pygame.font.Font("slkscr.ttf", 40)
FONT2 = pygame.font.Font("slkscr.ttf", 60)

#files
HIGH_SCORE_FILE = "highscore.txt"

#helpful functions
def scale_image(image):
    original_size = image.get_size()
    scaled_size = (int(original_size[0] * SCALE_X), int(original_size[1] * SCALE_Y))
    return pygame.transform.scale(image, scaled_size)

def put_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    win.blit(img, (x, y))

def load_high_score():
    with open(HIGH_SCORE_FILE, "r") as file:
        return int(file.read())

def save_high_score(new_high_score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(new_high_score))


#images loading
PLAYER_FRAMES = [
    scale_image(pygame.image.load("game_images/narwhal1new.png")),
    scale_image(pygame.image.load("game_images/narwhal2new.png")),
    scale_image(pygame.image.load("game_images/narwhal3new.png"))
]

INSTRUCTION_FRAMES = [
    scale_image(pygame.image.load("game_images/instructions1.png")),
    scale_image(pygame.image.load("game_images/instructions2.png"))
]

GAME_OVER_FRAMES = [
    scale_image(pygame.image.load("game_images/game_over_screen1.png")),
    scale_image(pygame.image.load("game_images/game_over_screen2.png"))
]

BACKGROUND_IMAGE = pygame.transform.scale(
    pygame.image.load("game_images/background_image_game.png").convert(),
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

GAME_MENU_FRAMES = [
    scale_image(pygame.image.load("game_images/menu1.png")),
    scale_image(pygame.image.load("game_images/menu2.png"))
]

SMALL_FISH_LEFT = [
    scale_image(pygame.image.load("game_images/pink1.png")),
    scale_image(pygame.image.load("game_images/purple1.png")),
    scale_image(pygame.image.load("game_images/blue1.png")),
    scale_image(pygame.image.load("game_images/green1.png")),
    scale_image(pygame.image.load("game_images/yellow1.png"))
]

BIG_FISH_LEFT = [
    scale_image(pygame.image.load("game_images/bigpink1.png")),
    scale_image(pygame.image.load("game_images/bigpurple1.png")),
    scale_image(pygame.image.load("game_images/bigblue1.png")),
    scale_image(pygame.image.load("game_images/biggreen1.png")),
    scale_image(pygame.image.load("game_images/bigyellow1.png"))
]

JELLYFISH_FRAMES_LEFT = [
    scale_image(pygame.image.load("game_images/jellyfish1.png")),
    scale_image(pygame.image.load("game_images/jellyfish2.png"))
]

TURTLE_FRAMES_LEFT = [
    scale_image(pygame.image.load("game_images/turtle1.png")),
    scale_image(pygame.image.load("game_images/turtle2.png")),
    scale_image(pygame.image.load("game_images/turtle3.png"))
]



SMALL_FISH_RIGHT = [pygame.transform.flip(img, True, False) for img in SMALL_FISH_LEFT]
BIG_FISH_RIGHT = [pygame.transform.flip(img, True, False) for img in BIG_FISH_LEFT]
JELLYFISH_FRAMES_RIGHT = [pygame.transform.flip(img, True, False) for img in JELLYFISH_FRAMES_LEFT]
TURTLE_FRAMES_RIGHT = [pygame.transform.flip(img, True, False) for img in TURTLE_FRAMES_LEFT]




#title bar configuration
TITLE_BAR_HEIGHT = 45
TITLE_BAR_BG_COLOR = (16, 18, 43)
TITLE_BAR_TEXT_COLOR = (255, 255, 255)

def draw_title_bar():
    pygame.draw.rect(win, TITLE_BAR_BG_COLOR, (0, 0, SCREEN_WIDTH, TITLE_BAR_HEIGHT))

    mouse_pos = pygame.mouse.get_pos()
    if CLOSE_BTN_RECT.collidepoint(mouse_pos):
        pygame.draw.rect(win, CLOSE_BTN_HOVER_COLOR, CLOSE_BTN_RECT)
    else:
        pygame.draw.rect(win, CLOSE_BTN_COLOR, CLOSE_BTN_RECT)

    put_text("Marine Lens", FONT, TITLE_BAR_TEXT_COLOR, 10, 5)

#close button configuration
CLOSE_BTN_COLOR = (200, 50, 50)
CLOSE_BTN_HOVER_COLOR = (255, 75, 75)
CLOSE_BTN_RECT = pygame.Rect(SCREEN_WIDTH - 50, 0, 50, TITLE_BAR_HEIGHT)

#colours
BG_COLOUR = (16, 18, 43)
PLAYER_COLOUR = (83, 116, 140)
CAMERA_COLOUR = [(252, 242, 91),
                (161, 161, 161), 
                (255, 255, 255)]
#ready color, cooldown color, flash colour



#first player coordinates
PLAYER_x = 860
PLAYER_y = 700
PLAYER_SPEED = 10



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

class Camera:
    def __init__(self):
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

    def update(self):
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
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 4)
    
    def take_photo(self):
        if self.photo_ready:
            self.is_flashing = True
            self.photo_ready = False
            self.colour = CAMERA_COLOUR[2]

    def fish_in_range(self, fish):
        camera_hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        fish_hitbox = pygame.Rect(fish.x, fish.y, fish.width, fish.height).inflate(5, 5)
        return camera_hitbox.colliderect(fish_hitbox)

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
    
    def update(self):
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


#fish "management"
fish_list = []
fish_spawn_timer = 0
fish_spawn_rate = 500

#other
key = pygame.key.get_pressed()

#game loop
run = True
instructions = False
menu = True
game_over = False
camera = Camera()

#score and highscore management
score = 0
high_score = load_high_score()

#time-related variables
clock = pygame.time.Clock()
GAME_DURATION = 60000

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
                instructions = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    instructions = False
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if CLOSE_BTN_RECT.collidepoint(mouse_pos):
                        run = False
                        menu = False

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
        
            win.blit(INSTRUCTION_FRAMES[instruction_frame], ((SCREEN_WIDTH - INSTRUCTION_FRAMES[instruction_frame].get_width()) // 2, (SCREEN_HEIGHT - INSTRUCTION_FRAMES[instruction_frame].get_height()) // 2))
            draw_title_bar()

            if key[pygame.K_RETURN]:
                start_time = pygame.time.get_ticks()
                instructions = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    instructions = False
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if CLOSE_BTN_RECT.collidepoint(mouse_pos):
                        run = False
                        instructions = False

            pygame.display.update()

    key = pygame.key.get_pressed()
    win.blit(BACKGROUND_IMAGE, (0, 0))
    dt = clock.tick(60)

    #timer
    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = max(0, GAME_DURATION - elapsed_time)
    remaining_seconds = remaining_time // 1000

    put_text(f"Time remaining: {remaining_seconds} s", FONT, (255, 255, 255), 20, TITLE_BAR_HEIGHT)

    if remaining_time <= 0:
        game_over = True

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
            game_over = False

            #resetting variables
            score = 0
            fish_list.clear()
            PLAYER_x = SCREEN_WIDTH // 2
            PLAYER_y = SCREEN_HEIGHT // 2

            menu = True
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

        pygame.display.update()
    
    #score counter
    put_text(f"Score: {score}", FONT, (255, 255, 255), SCREEN_WIDTH-300, TITLE_BAR_HEIGHT)

    if key[pygame.K_UP] and PLAYER_y > -50:
        PLAYER_y -= PLAYER_SPEED
    if key[pygame.K_DOWN] and PLAYER_y < SCREEN_HEIGHT - 200:
        PLAYER_y += PLAYER_SPEED
    if key[pygame.K_RIGHT] and PLAYER_x < SCREEN_WIDTH - 300:
        PLAYER_x += PLAYER_SPEED
    if key[pygame.K_LEFT] and PLAYER_x > 0:
        PLAYER_x -= PLAYER_SPEED

    #spawn fish
    fish_spawn_timer += dt
    if fish_spawn_timer >= fish_spawn_rate:
        fish_spawn_timer = 0
        fish_list.append(Fish())

    #update and draw fish
    for fish in fish_list[:]:
        fish.update()
        fish.draw()
        if fish.x < -fish.width or fish.x > SCREEN_WIDTH + fish.width:
            fish_list.remove(fish)


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
                    

    camera.update()
    camera.draw()

    #animation of player
    animation_timer += dt
    if animation_timer >= animation_speed:
        animation_timer = 0
        current_frame = (current_frame + 1) % len(PLAYER_FRAMES)
    
    win.blit(PLAYER_FRAMES[current_frame], (PLAYER_x, PLAYER_y))
    draw_title_bar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if CLOSE_BTN_RECT.collidepoint(mouse_pos):
                run = False

    
    pygame.display.update()
pygame.quit()