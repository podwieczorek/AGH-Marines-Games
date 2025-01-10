import pygame

pygame.init()

#screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

#fonts
PIXEL_FONT = pygame.font.Font("slkscr.ttf", 40)

#colours
WHITE = (255, 255, 255)
HIGHLIGHT = (178, 176, 235)

#menu options
options = ["Play Game 1", "Play Game 2", "Play Game 3", "Exit"]
select = 0
spacing = 50

#images
title = pygame.image.load("images/title.png")

game_images = [
    pygame.image.load("images/game1.png"),
    pygame.image.load("images/game2.png"),
    pygame.image.load("images/game3.png")
]

option_frame = pygame.image.load("images/option_frame1.png")
option_frame_highlight = pygame.image.load("images/option_frame2.png")


#setting the window
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("AGH Marines Games")


#used to display any text
def put_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    window.blit(img, (x, y))


#main loop
run = True
while run:
    window.fill((10, 4, 26))
    window.blit(title, (160, 40))

    #menu options
    total_width = sum(PIXEL_FONT.size(option)[0] for option in options) + spacing * (len(options) - 1)
    #total_width = sum(PIXEL_FONT.size(option)[0] for option in options)
    start_x = (SCREEN_WIDTH - total_width) // 2
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
            x += PIXEL_FONT.size(option)[0] + 10 + PIXEL_FONT.size("Exit")[0] #spacing between options

    #exit button
    put_text("Exit", PIXEL_FONT, colour, SCREEN_WIDTH *0.9, SCREEN_HEIGHT*0.9)


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
