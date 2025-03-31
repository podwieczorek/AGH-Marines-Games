import pygame
from constants import *

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

def draw_title_bar():
    pygame.draw.rect(win, TITLE_BAR_BG_COLOR, (0, 0, SCREEN_WIDTH, TITLE_BAR_HEIGHT))

    mouse_pos = pygame.mouse.get_pos()
    if CLOSE_BTN_RECT.collidepoint(mouse_pos):
        pygame.draw.rect(win, CLOSE_BTN_HOVER_COLOR, CLOSE_BTN_RECT)
    else:
        pygame.draw.rect(win, CLOSE_BTN_COLOR, CLOSE_BTN_RECT)

    put_text("Marine Lens", FONT, TITLE_BAR_TEXT_COLOR, 10, 5)