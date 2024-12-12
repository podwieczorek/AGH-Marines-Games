import pygame

pygame.init()

#screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

#fonts
FONT = pygame.font.SysFont("Impact", 40)
FONT1 = pygame.font.SysFont("Impact", 60)

#colours
WHITE = (255, 255, 255)
HIGHLIGHT = (100, 200, 255)
TITLE_COLOUR = (209, 211, 255)

#title text
title = "AGH Marines Games"

#menu options
options = ["Play Game 1", "Play Game 2", "Play Game 3", "Exit"]
select = 0
lengths = [len(option) for option in options]

#images
background = pygame.image.load("images/ocean.jpg")
icon = pygame.image.load("images/main_menu_icon.png")
game1 = pygame.image.load("images/game1.png")
game2 = pygame.image.load("images/game2.png")
game3 = pygame.image.load("images/game3.png")

#setting the window
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AGH Marines Games")
pygame.display.set_icon(icon)


#used to display any text
def put_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    window.blit(img, (x, y))

#rectangles
def draw_rect(colour, x, y, width, height):
    pygame.draw.rect(window, colour, (x, y, width, height), 2, 20)

def calc_total_width(text, font):
    total_width = font.size(text)[0]
    return total_width


#main loop
run = True
while run:
    window.blit(background, (0,0))

    #menu title
    start_x = (SCREEN_WIDTH - calc_total_width(title, FONT1)) // 2
    put_text(title, FONT1, TITLE_COLOUR, start_x, SCREEN_HEIGHT // 4)


    #menu options
    total_width = sum(FONT.size(option)[0] + 40 for option in options)
    start_x = (SCREEN_WIDTH - total_width) // 2
    x = start_x

    for i, option in enumerate(options):
        if i == select:
            colour = HIGHLIGHT
        else:
            colour = WHITE
        if option != "Exit":
            a = calc_total_width(option, FONT) + 60
            draw_rect(colour, x-30, SCREEN_HEIGHT//2, a, a)
            put_text(option, FONT, colour, x, SCREEN_HEIGHT//2)
            x += FONT.size(option)[0] + 40 + FONT.size("Exit")[0] #spacing between options

    #exit button
    put_text("Exit", FONT, colour, SCREEN_WIDTH *0.9, SCREEN_HEIGHT*0.9)


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True
            if event.key == pygame.K_RIGHT:
                select = (select + 1)%len(options)
            if event.key == pygame.K_LEFT:
                select = (select -1)%len(options)
            if event.key == pygame.K_RETURN:
                if options[select] == "Exit":
                    run = False
                else:
                    print(f"Selected : {options[select]}")
    
    pygame.display.update()

pygame.quit()