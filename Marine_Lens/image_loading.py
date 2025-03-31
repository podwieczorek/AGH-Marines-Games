import pygame
import pygame.image
from utils import scale_image
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

#images loading
PLAYER_FRAMES = [
    scale_image(pygame.image.load("Marine_Lens/game_images/narwhal1new.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/narwhal2new.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/narwhal3new.png"))
]

GAME_OVER_FRAMES = [
    scale_image(pygame.image.load("Marine_Lens/game_images/game_over_screen1.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/game_over_screen2.png"))
]

BACKGROUND_IMAGE = pygame.transform.scale(
    pygame.image.load("Marine_Lens/game_images/background_image_game.png").convert(),
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

GAME_MENU_FRAMES = [
    scale_image(pygame.image.load("Marine_Lens/game_images/menu1.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/menu2.png"))
]

SMALL_FISH_LEFT = [
    scale_image(pygame.image.load("Marine_Lens/game_images/pink1.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/purple1.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/blue1.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/green1.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/yellow1.png"))
]

BIG_FISH_LEFT = [
    scale_image(pygame.image.load("Marine_Lens/game_images/bigpink1.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/bigpurple1.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/bigblue1.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/biggreen1.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/bigyellow1.png"))
]

JELLYFISH_FRAMES_LEFT = [
    scale_image(pygame.image.load("Marine_Lens/game_images/jellyfish1.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/jellyfish2.png"))
]

TURTLE_FRAMES_LEFT = [
    scale_image(pygame.image.load("Marine_Lens/game_images/turtle1.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/turtle2.png")),
    scale_image(pygame.image.load("Marine_Lens/game_images/turtle3.png"))
]


SMALL_FISH_RIGHT = [pygame.transform.flip(img, True, False) for img in SMALL_FISH_LEFT]
BIG_FISH_RIGHT = [pygame.transform.flip(img, True, False) for img in BIG_FISH_LEFT]
JELLYFISH_FRAMES_RIGHT = [pygame.transform.flip(img, True, False) for img in JELLYFISH_FRAMES_LEFT]
TURTLE_FRAMES_RIGHT = [pygame.transform.flip(img, True, False) for img in TURTLE_FRAMES_LEFT]