import pygame

#game window setup
pygame.init()
screen_info = pygame.display.Info()

SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

BASE_WIDTH = 1920
BASE_HEIGHT = 1080

SCALE_X = SCREEN_WIDTH / BASE_WIDTH
SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Marine Lens")


#initialize joystick
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    joystick = None


#game constants
GAME_DURATION = 60000

#player's speed
PLAYER_SPEED = 10

#joystick buttons
PHOTO_BUTTON = 3
ENTER_BUTTON = 1
ESC_BUTTON = 2
DEAD_ZONE = 0.1

#fonts
FONT = pygame.font.Font("slkscr.ttf", 40)
FONT2 = pygame.font.Font("slkscr.ttf", 60)

#files
HIGH_SCORE_FILE = "Marine_Lens/highscore.txt"

#title bar configuration
TITLE_BAR_HEIGHT = 45
TITLE_BAR_BG_COLOR = (16, 18, 43)
TITLE_BAR_TEXT_COLOR = (255, 255, 255)

#close button configuration
CLOSE_BTN_COLOR = (200, 50, 50)
CLOSE_BTN_HOVER_COLOR = (255, 75, 75)
CLOSE_BTN_RECT = pygame.Rect(SCREEN_WIDTH - 50, 0, 50, TITLE_BAR_HEIGHT)

#colours
PLAYER_COLOUR = (83, 116, 140)
CAMERA_COLOUR = [(250, 207, 65),
                (161, 161, 161), 
                (255, 255, 255)]
#ready color, cooldown color, flash colour
