import random
import pygame
import opensimplex







        

    
    
    
def init_joystick():
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

maze = Maze(80, 60)
#maze.carve()
#maze.add_paths(0.40)
#maze.simplex_cave(1,4,0.2)
maze.simplex_cave()
maze.remove_not_connected_spaces(set())
print(maze)


init_joystick()
for joystick in [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]:
    Joystick_player(maze, 3)
    
Keyboard_player(maze, 3)

print(Player.player_list)



for i in range(5):
    Enemy(maze, 10)

for i in range(10):
    Pickup(maze)

# Constants for screen dimensions and colors
TICK_INTERVAL = 100
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CELL_SIZE = 15
COLORS = {
    0: (4, 105, 151),  # Background (blue)
    1: (37, 65, 23),   # Walls (green)
}

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


clock = pygame.time.Clock()
running = True
last_speed_change = pygame.time.get_ticks()
game_speed = 1000  # milliseconds per frame

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    


    

    for player in Player.player_list:
        player.input(events)
    
    current_time = pygame.time.get_ticks()
    
    game_speed = 1000 - current_time // 200
    if game_speed < 300:
        game_speed = 300
    #print(game_speed)
  
    screen.fill(COLORS[0])
    maze.draw()
    for u in Unit.unit_list:
        u.check_colision()
        if current_time - u.last_frame > game_speed / u.speed:
            u.step()
            u.last_frame = current_time
        u.draw()
    last_tick = current_time


    
    
    pygame.display.flip() # flip() displays the drawing
    clock.tick(60)  # limits FPS to 60