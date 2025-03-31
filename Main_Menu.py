import pygame
import subprocess

pygame.init()

# screen dimensions
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

BASE_WIDTH = 1920
BASE_HEIGHT = 1080

SCALE_X = SCREEN_WIDTH / BASE_WIDTH
SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT


# image scaling
def scale_image(image):
    original_size = image.get_size()
    scaled_size = (int(original_size[0] * SCALE_X), int(original_size[1] * SCALE_Y))
    return pygame.transform.scale(image, scaled_size)


# fonts
PIXEL_FONT = pygame.font.Font("slkscr.ttf", 30)
PIXEL_FONT_EXIT = pygame.font.Font("slkscr.ttf", 40)

# colours
WHITE = (255, 255, 255)
HIGHLIGHT = (178, 176, 235)

# menu options
options = ["MARINE LENS", "PAC-VHAL", "Exit"]
select = 0
spacing = 50

# images
title = scale_image(pygame.image.load("images/title.png"))

game_images = [
    scale_image(pygame.image.load("images/game1.png")),
    scale_image(pygame.image.load("images/game2.png"))
]

option_frame = scale_image(pygame.image.load("images/option_frame1.png"))
option_frame_highlight = scale_image(pygame.image.load("images/option_frame2.png"))

background_picture_frames = [
    scale_image(pygame.image.load("images/background1.png")),
    scale_image(pygame.image.load("images/background2.png"))
]


# background image animation variables
current_frame = 0
animation_timer = 0
animation_speed = 500


# setting the window
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("AGH Marines Games")


# used to display any text
def put_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    window.blit(img, (x, y))


run = True
clock = pygame.time.Clock()
while run:

    # background image animation
    dt = clock.tick(60)
    animation_timer += dt
    if animation_timer >= animation_speed:
        animation_timer = 0
        current_frame = (current_frame + 1) % len(background_picture_frames)
    window.blit(background_picture_frames[current_frame], (0, 0))

    window.blit(title, ((SCREEN_WIDTH - 1600*SCALE_X)//2, (SCREEN_HEIGHT - 960*SCALE_Y)//2))

    # menu options
    total_width = sum(PIXEL_FONT.size(option)[0] for option in options) + spacing * (len(options) - 1)
    start_x = (SCREEN_WIDTH - total_width) // 2 - 20
    x = start_x

    for i, option in enumerate(options):
        if i == select:
            colour = HIGHLIGHT
        else:
            colour = WHITE
        if option != "Exit":
            if i == select:
                window.blit(option_frame_highlight, (x-25, SCREEN_HEIGHT//2 - 20))
            else:
                window.blit(option_frame, (x-25, SCREEN_HEIGHT//2 - 20))

            put_text(option, PIXEL_FONT, colour, x, SCREEN_HEIGHT//2)
            window.blit(game_images[i], (x + 25, SCREEN_HEIGHT//2 + 45))
            x += PIXEL_FONT.size(option)[0] + 100 + PIXEL_FONT.size("Exit")[0]  #spacing between options

    put_text("Exit", PIXEL_FONT_EXIT, colour, SCREEN_WIDTH * 0.9, SCREEN_HEIGHT*0.9)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True
            if event.key == pygame.K_RIGHT:
                select = (select + 1) % len(options)
            if event.key == pygame.K_LEFT:
                select = (select - 1) % len(options)
            if event.key == pygame.K_RETURN:
                if options[select] == "Exit":
                    run = False
                elif options[select] == "MARINE LENS":
                    subprocess.run(["python3", "Marine_Lens/Marine_Lens.py"])
                elif options[select] == "PAC-VHAL":
                    subprocess.run(["python3", "PAC-VHAL/main.py"])

    pygame.display.update()

pygame.quit()
